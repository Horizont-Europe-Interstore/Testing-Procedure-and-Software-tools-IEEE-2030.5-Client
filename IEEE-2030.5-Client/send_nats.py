import asyncio
import os
import sys
from nats.aio.client import Client as NATS

async def main():
    if len(sys.argv) < 3:
        print("Usage: python3 send_nats.py <subject> <message>")
        return

    subject = sys.argv[1]
    message = sys.argv[2]

    nats_url = os.environ.get("NATS_URL", "nats://nats-server:4222")

    nc = NATS()
    await nc.connect(servers=[nats_url])

    await nc.publish(subject, message.encode())
    await nc.flush()
    await nc.close()

if __name__ == "__main__":
    asyncio.run(main())
