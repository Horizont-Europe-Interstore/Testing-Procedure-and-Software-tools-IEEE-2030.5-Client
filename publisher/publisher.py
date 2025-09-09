import asyncio
import os
import signal
from nats.aio.client import Client as NATS

FILE_PATH = "../IEEE-2030.5-Client-New/output.txt"
nc = NATS()

async def send_to_nats(msg):
    await nc.publish("response.client", msg.encode())

async def watch_file():
    last_content = ""
    while True:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r") as f:
                content = f.read().strip()

            if content and content != last_content:
                print("File changed, sending contents to Instance A")
                await send_to_nats(content)
                last_content = content

        await asyncio.sleep(1) 

async def cleanup_and_exit():
    """Clear file and close NATS before exiting."""
    print("Cleaning up...")
    if os.path.exists(FILE_PATH):
        open(FILE_PATH, "w").close() 
    await nc.drain()
    await nc.close()
    print("Exited cleanly")
    os._exit(0)

async def main():
    await nc.connect("nats://18.232.7.53:4222")

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.ensure_future(cleanup_and_exit()))

    print("Watching file for changes...")
    await watch_file()

if __name__ == "__main__":
    asyncio.run(main())




# async def main():
#     nc = NATS()
#     await nc.connect("nats://18.232.7.53:4222")
#
#     await nc.publish("response.client", b"Hello from Instance B!")
#
#     # async def handler(msg):
#     #     print(f"Received on [{msg.subject}]: {msg.data.decode()}")
#     # await nc.subscribe("ieee.client.response", cb=handler)
#     # print("Listening...")
#
#     while True:
#         await asyncio.sleep(1)
#
# asyncio.run(main())
