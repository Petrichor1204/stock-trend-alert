import asyncio
import websockets
import json
import aio_pika
from producer import publish_alert

THRESHOLDS = {
    "BTC-USD": 100000,
    "ETH-USD": 5000,
}
async def publish_alert(channel, product, price, threshold):
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

async def connect():
    url = "wss://advanced-trade-ws.coinbase.com"
     
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()

    await channel.declare_queue("alerts")

    async with websockets.connect(url) as ws:
        subscribe = {
            "type": "subscribe",
            "product_ids": ["BTC-USD", "ETH-USD"],
            "channel": "ticker"
        }
        await ws.send(json.dumps(subscribe))
        print("Subsribed. Waiting for prices...")
        
        async for message in ws:
            data = json.loads(message)
            if data.get("channel") == "ticker":
                for event in data.get("events", []):
                    for ticker in event.get("tickers", []):
                        product = ticker.get("product_id")
                        price = float(ticker.get("price"))

                        print(f"{product}: ${price}")

                        if product in THRESHOLDS:
                            if price >= THRESHOLDS[product]:
                                await publish_alert(channel, product, price, THRESHOLDS[product])
asyncio.run(connect())