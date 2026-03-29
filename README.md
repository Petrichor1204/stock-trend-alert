# Real-Time Stock/Crypto Alert System

A distributed backend system that streams live cryptocurrency prices via WebSocket, 
routes threshold breach events through a message queue, and enforces rate limiting 
to prevent notification flooding.

## Architecture

WebSocket Feed → price_feed.py → RabbitMQ → consumer.py → Redis Rate Limiter → Alert

## Tech Stack

- Python (asyncio)
- WebSockets (Coinbase Advanced Trade API)
- RabbitMQ (message queue)
- Redis (rate limiting)
- Docker + Docker Compose

## How To Run

1. Start RabbitMQ and Redis:
   docker-compose up -d

2. Start the consumer in one terminal:
   python consumer.py

3. Start the price feed in another terminal:
   python price_feed.py

## Configure Alerts

Edit config.json to set your own thresholds:
{
    "alerts": [
        { "product": "BTC-USD", "threshold": 100000 },
        { "product": "ETH-USD", "threshold": 5000 }
    ]
}

## Project Structure

price_feed.py     — WebSocket connection, price streaming, threshold checking
producer.py       — publishes alert events to RabbitMQ
consumer.py       — reads from queue, enforces rate limiting, delivers alerts
rate_limiter.py   — Redis backed rate limiter with TTL
config.json       — user defined alert thresholds
docker-compose.yml — spins up RabbitMQ and Redis with one command