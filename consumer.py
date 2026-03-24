import asyncio
import aio_pika
import json
from rate_limiter import is_rate_limited
async def consume():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("alerts")

        print("Waiting for alerts...")

        async with queue.iterator() as messages:
            async for message in messages:
                async with message.process():
                    alert = json.loads(message.body.decode()) 
                    product = alert["product"]

                    if not is_rate_limited(product):
                        print(f"🚨 ALERT RECEIVED: {alert['product']} hit ${alert['price']}!")

asyncio.run(consume())