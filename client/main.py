#!/bin/env python
import typing
import aioserial
import aiohttp
from escpos.printer import Escpos
import asyncio
import cv2
import io



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

        pass


def capture_image() -> bytes:
    cap = cv2.VideoCapture("/dev/video2")
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise Exception("Failed to capture image")
    ret, buffer = cv2.imencode(".png", frame)
    if not ret:
        raise Exception("Failed to encode image")
    return buffer.tobytes()
async def print_text(text, printer: AioPrinter):
    printer.block_text(text,font="0")
    print(printer.tasks)
    await printer.run_tasks()
async def run_inference(image_bytes: bytes,):
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('file',
                       io.BytesIO(image_bytes),
                       filename="captured.png",
                       content_type='image/png')
        async with session.post(url, data=data) as response:
            if response.status != 200:
                raise Exception(f"error")
            resp_json = (await response.json())['result']
            return resp_json
def initrc():
    mcu_serial=aioserial.AioSerial(port='/dev/ttyACM1',baudrate=9600)#
    printer_serial=aioserial.AioSerial(port='/dev/ttyACM0',baudrate=9600)#
    printer=AioPrinter(printer_serial)
    printer.magic.encoding="GBK"
    printer.magic.encoder=type("a",(),{"encode":lambda  text,encoding:text.encode(encoding)})# This make Chinese work
    printer.magic.disabled=True
    printer.profile.profile_data["fonts"]['0']['columns']=30
    return locals()
async def main():
    globals().update(initrc())
    while 1:
        mcu_command=await mcu_serial.readline_async()
        print(mcu_command)
        match mcu_command:
            case b'start\n':
                image=capture_image()
                text=await run_inference(image)
                await print_text(text,printer)
                await mcu_serial.write_async(b'ok\n')
if __name__ == "__main__":
    url = "http://127.0.0.1:8000/run"
    asyncio.run(main())
