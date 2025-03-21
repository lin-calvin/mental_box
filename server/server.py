
import asyncio
import base64
import datetime
import io
import json
import os
import sys
import traceback
from functools import partial
import typing
from aiostream.stream import map as amap
from aiostream import async_
from uuid import uuid4

import gradio
import litellm
import peewee
import PIL.Image
import playhouse.db_url
import strawberry
from fastapi import FastAPI, File, HTTPException, UploadFile
from sse_starlette.sse import EventSourceResponse
from strawberry.fastapi import GraphQLRouter

import const
import models
from models import ConfigTable, Record, Tag, UnTaggedRecord


pending_task:dict[str,typing.Awaitable]={}
def make_llm(**kwargs):
    assert "message" not in kwargs
    return partial(litellm.acompletion, **kwargs)

async def stream(llm, *args, tracker=None, **kwargs):
    print(kwargs)
    chunks = []
    async for i in await llm(*args, stream=True, **kwargs):
        chunks.append(i)
        if tracker:
            tracker(i.choices[0].delta.content or "")
    return litellm.stream_chunk_builder(chunks, messages=kwargs.get("messages"))
def get_config(key):
    return ConfigTable.get_or_create(key=key, defaults= const.CONFIG_DEFAULTS[key])[0].value

def do_condig(code_str: str):
    # Create a dictionary to capture the local namespace
    local_namespace = {}
    # Execute the code string within the local namespace
    exec(code_str, globals(), local_namespace)

    # The function should now be in the local namespace, so we retrieve it
    # Assuming the code string defines a function named 'func'

    return globals().update(local_namespace)

# vlm = make_llm(
#     base_url="https://api.siliconflow.cn/v1/",
#     model="openai/Pro/Qwen/Qwen2-VL-7B-Instruct",
#     api_key="sk-whfsgciephkpcjrbmijijiqealycbbycxkwbkwgkyptofbah",
# )
# llm =  make_llm(
#     base_url="https://api.siliconflow.cn/v1/",
#     model="openai/Pro/Qwen/Qwen2-VL-7B-Instruct",
#     api_key="sk-whfsgciephkpcjrbmijijiqealycbbycxkwbkwgkyptofbah",
# )
# tagging_llm =llm
# emo_llm = llm

# db = playhouse.db_url.connect("sqlite:///db.sqlite")
do_condig(open(os.environ["CONFIG_PATH"]).read())
models.bind_db(db)
# get images from gradio interface, ocr them via vlm and pass to emollm

async def tagging_record(record: Record):
    # Build the session text with query and output
    text = f"Q: {record.query}\nA:\n{record.output}"
    tag_str = g(await tagging_llm(messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "You are a helpful assistant. "
                        "Return a valid JSON object with a field 'tags' containing an array of tags. "
                        "Example: {\"tags\": [\"taga\", \"tagb\"]}"
                    )
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        f"Extract tags from the following psychological counseling session text and return them in JSON format: {text}"
                    )
                }
            ]
        }
    ]))
    print(tag_str)
    tags = json.loads(tag_str)['tags']
    tag_instances = [Tag.create(name=tag) for tag in tags]
    record.tags.add(tag_instances)

def image_to_dataurl(data, type="png"):
    # 对PNG字节进行base64编码
    encoded_png = base64.b64encode(data).decode('utf-8')
    # 创建data URL
    data_url = f"data:image/{type};base64,{encoded_png}"
    return data_url

def get_result(response: litellm.ModelResponse):
    return response.choices[0].message.content

g = get_result

async def interface_fn(image):
    if not image:
        raise Exception("No image provided")
    image.thumbnail((1080, 1080))
    image.save(image := io.BytesIO(), format="PNG")
    image_data = image_to_dataurl(image.getvalue())
    print(2)
    message = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "输出图片中的文字，不要输出其他内容。"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"{image_data}"},
                }
            ],
        }
    ]
    ocr_result=""
    async for i in await vlm(messages=message,stream=True):
        print(3)
        data=i.choices[0].delta.content or ""
        ocr_result+=data
        yield ('ocr',data)
    
    

    print("OCR_RESULT:" + ocr_result)
    # now, pass the ocr result to the emotion model
    prompt=get_config("mental_prompt")
    message = [
        {"role": "system", "content": [{"type": "text", "text": prompt}]},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": ocr_result},
            ],
        }
    ]
    print("EMO_MESSAGE:" + str(message))
    # trace it
    result=""
    async for  i in await emo_llm(messages=message,stream=True):
        data=i.choices[0].delta.content or ""
        result+=data
        yield ('final',data)

    record = Record.create(query=ocr_result, output=result)
    asyncio.create_task(tagging_record( record))
    yield ('result',result)
    # if not streaming:
    #     return response

async def gradio_fn(image):
    print(1)
    priv=""
    async for i in interface_fn(image):
        yield i[1]
        print(i[1])
        if priv!=i[0]:
            yield "#########"
        priv=i[0]
    

interface = gradio.Interface(
    fn=gradio_fn, inputs=[gradio.Image(type="pil")], outputs="text"
)


# FastAPI application and endpoint
app = FastAPI()
# graphql endpoint via strawberry
@strawberry.type
class RecordType:
    id: int
    created_at: datetime.datetime
    query: str
    output: str
    tags: typing.Optional[typing.List[str]] = None
@strawberry.type
class TagStats:
    tag: str
    count: int
@strawberry.type
class ConfigType:
    key: str
    value: str
    name: str
    description: str
@strawberry.type
class Query:
    @strawberry.field
    def call_count(self) -> int:
        return Record.select().count()

    @strawberry.field
    def records(self) -> typing.List[RecordType]:
        records = []
        for record in Record.select():
            tags=[]
            data=record.__data__|{}
            for i in record.tags:
                tags.append(i.__data__['name'])
            data['tags']=tags
            records.append(RecordType(**data))
        return records
    @strawberry.field
    def tags_stats(self) -> typing.List[TagStats]:
        tags = {}
        for record in Record.select():
            for tag in record.tags:
                tags[tag.name] = tags.get(tag.name, 0) + 1
        print([TagStats(tag=tag, count=count) for tag, count in tags.items()])
        return [TagStats(tag=tag, count=count) for tag, count in tags.items()]
    @strawberry.field
    def config(self,key:typing.Optional[str]=None) -> typing.Optional[list[ConfigType]]:
        print(key)
        if not key:
            return [ConfigType(key=i.key,value=i.value,name=i.name,description=i.description) for i in ConfigTable.select()]
        item=ConfigTable.get_or_none(key=key)
        if item!=None:
            print(item)
            return [ConfigType(key=item.key,value=item.value,name=item.name,description=item.description)]
        return None
@strawberry.type
class Mutation:
    @strawberry.mutation
    def set_config(self, key: str, value: typing.Optional[str]=None) -> int:
        print(key, value)
        item,create=ConfigTable.get_or_create(key=key, defaults={"value": value,"name":key,"description":""})
        if value==None:
            item.delete_instance()
        if not create:
            item.value=value
            item.save()
        return 1


app.include_router(GraphQLRouter(strawberry.Schema(Query,Mutation)), prefix="/graphql")
def tags_stats() -> typing.List[dict[str,int]]:
    tags = {}
    for record in Record.select():
        for tag in record.tags:
            tags[tag.name] = tags.get(tag.name, 0) + 1
    #print([TagStats(tag=tag, count=count) for tag, count in tags.items()])
    return tags# [TagStats(tag=tag, count=count) for tag, count in tags.items()]
tags_stats()
@app.get("/stream/{id}")
async def stream(id):
    try:
        task=pending_task[id]
        del pending_task[id]
        return EventSourceResponse(task)   
    except KeyError:
        return HTTPException(404)
@app.post("/run")
async def upload_image(file: UploadFile = File(...),stream: bool = True):
    try:
        contents = await file.read()
        image = PIL.Image.open(io.BytesIO(contents))
        resp=interface_fn(image)
        if stream:
        
            async def streamer():
                async for i in resp:
                    yield {"event":i[0],"data":i[1]}
            pending_task[id:=str(111    )]=streamer()
            return id  
        else:
            async for i in resp:
                if i[0]=='result':
                    return {"result": i[1]}
        #result = await interface_fn(image)
        #return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": traceback.format_exc()})

app = gradio.mount_gradio_app(app, interface, path="/gradio")

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1")
    