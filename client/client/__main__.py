#!/bin/env python
import typing
import aioserial
import aiohttp
from aiohttp import web
from escpos.escpos import Escpos
import asyncio
import cv2
import io
import os
from client.sse import aiosselient,Event
from aiohttp import web
from aiohttp_sse import sse_response
from json import dumps as json_dumps
import sys
base_url = "http://127.0.0.1:8000/"
DUMMY_PRINTER=0b10
DUMMY_CAMERA=0b01
dummy_mode=0
events=asyncio.Queue()
devices={}
class AioPrinter(Escpos):
    """Dummy printer.

    This class is used for saving commands to a variable, for use in situations where
    there is no need to send commands to an actual printer. This includes
    generating print jobs for later use, or testing output.

    inheritance:

    .. inheritance-diagram:: escpos.printer.Dummy
        :parts: 1

    """
    @staticmethod
    def is_usable() -> bool:
        """Indicate whether this printer class is usable.

        Will return True if dependencies are available.
        Will return False if not.
        """
        return True



    def __init__(self,serial:aioserial.AioSerial,*args, **kwargs) -> None:
        """Init with empty output list."""
        self.serial=serial
        Escpos.__init__(self, *args, **kwargs)
        self.tasks: List[typing.Awaitable] = []

    def _raw(self, msg: bytes) -> None:
        """Print any command sent in raw format.

        :param msg: arbitrary code to be printed
        """
        self.tasks.append(self.serial.write_async(msg))

    async def run_tasks(self) -> None:
        """Run all tasks in the buffer.

        This method will run all tasks in the buffer, in the order they were added.
        """
        await asyncio.gather(*self.tasks)
        self.clear()
    def clear(self) -> None:
        """Clear the buffer of the printer.

        This method can be called if you send the contents to a physical printer
        and want to use the Dummy printer for new output.
        """
        del self.tasks[:]

    def close(self) -> None:


def code2function(code_str: str):
        pass
    # Create a dictionary to capture the local namespace
    local_namespace = {}
    
    # Execute the code string within the local namespace
    exec(code_str, globals(), local_namespace)
    
    # The function should now be in the local namespace, so we retrieve it
    # Assuming the code string defines a function named 'func'
    if 'initrc' in local_namespace:
        return local_namespace['initrc']
    else:
        raise ValueError("The code string does not define a function named 'func'.")


def capture_image() -> bytes:
    ret, frame = camera.read()

    if not ret:
        raise Exception("Failed to capture image")
    ret, buffer = cv2.imencode(".png", frame)
    if not ret:
        raise Exception("Failed to encode image")
    return buffer.tobytes()
async def print_text(text, printer: AioPrinter):
    printer.block_text(text,font="0")
    await printer.run_tasks()
async def run_inference(image_bytes: bytes,):
    res=""
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('file',
                       io.BytesIO(image_bytes),
                       filename="captured.png",
                       content_type='image/png')
        async with session.post(os.path.join(base_url,"run"), data=data) as response:
            if response.status != 200:
                print(await response.text())
                raise Exception(f"error")
            taskid = (await response.json())
        sseclient=aiosselient(os.path.join(base_url,"stream",taskid))
        async for i in sseclient:
            event=(i.event,i.data)
            await events.put(event)
        return event[1]
        #return resp_json
# def initrc():
#     mcu_serial=aioserial.AioSerial(port='/dev/ttyACM1',baudrate=9600)#
#     printer_serial=aioserial.AioSerial(port='/dev/ttyACM0',baudrate=9600)#
#     printer=AioPrinter(printer_serial)
#     printer.magic.encoding="GBK"
#     printer.magic.encoder=type("a",(),{"encode":lambda  text,encoding:text.encode(encoding)})# This make Chinese work
#     printer.magic.disabled=True
#     printer.profile.profile_data["fonts"]['0']['columns']=30
#     return locals()
async def eventsource(request: web.Request) -> web.StreamResponse:
    async with sse_response(request) as resp:
        #await resp.send("1")
        while resp.is_connected():
            event_type,data=await events.get()
            await resp.send(json_dumps({"event":event_type,"data":data}))
            #await resp.send(data,event=event_type)
    return resp
async def test_sse(request: web.Request):
    async with sse_response(request) as resp:
        for i in range(5):
            await resp.send(json_dumps({"event":"progress","data":i}))
            await asyncio.sleep(0.1)
        for i in range(5):
            await resp.send(json_dumps({"event":"result","data":i}))
            await asyncio.sleep(0.1)
        await resp.send(json_dumps({"event":"done","data":i}))
        await asyncio.Future()
    return resp
async def test(_):
    print(1)
    asyncio.create_task(run_inference(cv2.imencode(".png", cv2.imread("a.png"))[1]))
    return web.Response(text="ok")
async def run(_):
    if dummy_mode & DUMMY_CAMERA:
        image=cv2.imencode(".png", cv2.imread("a.png"))[1]
    else:
        image=capture_image()
    text=await run_inference(image)
    if dummy_mode & DUMMY_PRINTER:
        await print_text(text,printer)
        await events.put(("print_finish",""))
app = web.Application()
app.router.add_route("GET","/test",test)
app.router.add_route("GET","/event", eventsource)
app.router.add_route("GET","/run",run)
app.router.add_route("GET","/test_sse",test_sse)
#app.add_routes([web.static('/ui', "static")])
app.add_routes([web.static('/ui', os.path.dirname(os.path.abspath(__file__))+"/static")])
# async def runapp(): await web._run_app(app)
# web.run_app(app)
# async def main():
#     import sys
#     #open initrc.py from args and prase it
#     code=open(sys.argv[1], "r").read()
#     initrc=code2function(code)
#     globals().update(initrc())
#     while 1:
#         mcu_command=await mcu_serial.readline_async()
#         print(mcu_command)
#         match mcu_command:
#             case b'start\n':
#                 image=capture_image()
#                 text=await run_inference(image) 
#                 await print_text(text,printer)
#                 await mcu_serial.write_async(b'ok\n')

def main(): #if __name__ == "__main__":
    code=open(sys.argv[1], "r").read()
    initrc=code2function(code)
    globals().update(initrc())
    web.run_app(app)

if __name__=="__main__": main()
