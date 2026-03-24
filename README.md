# Stock Alert System

A real-time crypto price alert system that streams live prices from Coinbase and publishes alerts via RabbitMQ when configurable thresholds are crossed.

## How It Works

```
Coinbase WebSocket  →  price-feed.py  →  RabbitMQ (alerts queue)  →  consumer.py
```

- **[price-feed.py](price-feed.py)** — connects to the Coinbase Advanced Trade WebSocket, monitors BTC-USD and ETH-USD, and publishes an alert whenever a price hits or exceeds its threshold
- **[producer.py](producer.py)** — helper module that handles publishing alert messages to the RabbitMQ queue
- **[consumer.py](consumer.py)** — listens on the RabbitMQ queue and prints incoming alerts

### Default Thresholds

| Asset   | Alert Price |
|---------|-------------|
| BTC-USD | $100,000    |
| ETH-USD | $5,000      |

## Prerequisites

- Python 3.8+
- RabbitMQ running locally on the default port (5672) with default credentials (`guest`/`guest`)

### Install RabbitMQ

**macOS (Homebrew):**
```bash
brew install rabbitmq
brew services start rabbitmq
```

**Docker:**
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

## Setup

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install aio-pika websockets
```

## Running

Open two terminal windows (both with the venv activated).

**Terminal 1 — start the consumer** (receives and prints alerts):
```bash
python consumer.py
```

**Terminal 2 — start the price feed** (connects to Coinbase and monitors prices):
```bash
python price-feed.py
```

You'll see live prices printed as they stream in. When BTC-USD hits $100,000 or ETH-USD hits $5,000, an alert is published to RabbitMQ and printed by the consumer.

## Customizing Thresholds

Edit the `THRESHOLDS` dict at the top of [price-feed.py](price-feed.py):

```python
THRESHOLDS = {
    "BTC-USD": 100000,
    "ETH-USD": 5000,
}
```

You can also add any product ID supported by the Coinbase Advanced Trade WebSocket (e.g. `"SOL-USD": 300`). Make sure to add it to the `product_ids` list in the subscribe message as well.
