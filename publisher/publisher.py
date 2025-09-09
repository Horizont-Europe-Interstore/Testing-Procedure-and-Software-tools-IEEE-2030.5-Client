import asyncio
from nats.aio.client import Client as NATS

async def main():
    nc = NATS()
    await nc.connect("nats://18.232.7.53:4222")

    await nc.publish("response.client", b"Hello from Instance B!")

    # async def handler(msg):
    #     print(f"Received on [{msg.subject}]: {msg.data.decode()}")
    # await nc.subscribe("ieee.client.response", cb=handler)
    # print("Listening...")

    while True:
        await asyncio.sleep(1)

asyncio.run(main())
