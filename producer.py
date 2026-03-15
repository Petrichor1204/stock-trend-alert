import aio_pika
import json

async def publish_alert(product, price, threshold):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("alerts")

        alert = {
            "product": product,
            "price": price,
            "threshold": threshold,
        }

        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(alert).encode()),
            routing_key = "alerts"
        )

        print(f"Published alert: {alert}")

