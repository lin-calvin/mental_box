import traceback
from functools import partial
import base64
import io
import PIL.Image
import litellm
import gradio

from fastapi import FastAPI,File,UploadFile,HTTPException
import peewee
import strawberry
api_key = "19003893b371a8faeb6f09bbba97e037.4gjxGFg7x5o8KqpU"


def make_llm(**kwargs):
    assert "message" not in kwargs
    return partial(litellm.completion, **kwargs)

def stream(llm, *args, tracker=None, **kwargs):
    print(kwargs)
    chunks=[]
    for i in (resp := llm(*args, stream=True,**kwargs)):
        chunks.append(i)
        if tracker:
            tracker(i.choices[0].delta.content or "")
    return litellm.stream_chunk_builder(chunks,messages=kwargs.get("messages"))

vlm = make_llm(
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    model="openai/glm-4v",
    api_key=api_key,
)


emo_llm = make_llm(
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    model="openai/glm-4v",
    api_key=api_key,
)
# get images from gradio interface, ocr them via vlm and pass to emollm


def image_to_dataurl(data,type="png"):
    # 对PNG字节进行base64编码
    encoded_png = base64.b64encode(data).decode('utf-8')
    # 创建data URL
    data_url = f"data:image/{type};base64,{encoded_png}"
    return data_url
def get_result(response: litellm.ModelResponse):
    return response.choices[0].message.content
g=get_result
def interface_fn(image):
    image.thumbnail((1080, 1080))
    image.save(image := io.BytesIO(), format="PNG")
    image_data = image_to_dataurl(image.getvalue())
    message = [
        {
            "role": "user",
            "content": [
                {"type":"text","text":"输出图片中的文字，不要输出其他内容。"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"{image_data}"},
                }
            ],
        }
    ]
    ocr_result = g(vlm(messages=message))
    print(ocr_result)
    # now, pass the ocr result to the emotion model
    message = [
        {"role":"system","content":[{"type":"text","text":"请你扮演为一名专业心理咨询师，根据以下文本内容，帮助用户解决心理问题。"}]},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": ocr_result},
            ],
        }
    ]
    response = g(stream(emo_llm,tracker=print,messages=message))
    return response
interface = gradio.Interface(
    fn=interface_fn, inputs=[gradio.Image(type="pil")], outputs="text"
)


# FastAPI application and endpoint
app = FastAPI()
#graphql endpoint via strawberry
@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, world!"

@app.post("/run")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = PIL.Image.open(io.BytesIO(contents))
        result = interface_fn(image)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error":traceback.format_exc()})
app = gradio.mount_gradio_app(app, interface, path="/gradio")


