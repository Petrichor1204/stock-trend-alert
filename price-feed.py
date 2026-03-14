import asyncio
import websockets
import json

THRESHOLDS = {
    "BTC-USD": 70000,
    "ETH-USD": 5000,
}
async def connect():
    url = "wss://advanced-trade-ws.coinbase.com"

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

                        # print(f"{product}: ${price}")

                        if product in THRESHOLDS:
                            if price >= THRESHOLDS[product]:
                                print(f"ALERT: {product} hit ${price}!")
asyncio.run(connect())