import asyncio
import main
from main import run_inference,runapp
from cv2 import imread,imencode
main.base_url = "http://127.0.0.1:8000/"
image=imread("a.png")
asyncio.new_event_loop()


async def main(asyncio.gather(runapp(),run_inference(imencode(".png", image)[1])))


@asyncio.run
async def main():
    asyncio.create_task(runapp())
    await 