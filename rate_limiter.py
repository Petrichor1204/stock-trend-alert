import redis

client = redis.Redis(host="localhost", port=6379, db=0)

def is_rate_limited(product, cooldown_seconds=300):
    # building a unique key for the alert
    key = f"alert:{product}"

    if client.get(key):
        print(f"Rate limited: {product} - skipping alert")

        return True
    
    client.setex(key, cooldown_seconds, "alerted")
    return False
