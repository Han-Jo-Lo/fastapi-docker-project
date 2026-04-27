import redis
import json

redis_client=redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True
)

MAX_MESSAGES=10

def save_memory(user_id:str,messages:list):
    redis_client.set(user_id,json.dumps(messages[-MAX_MESSAGES:]))

def load_memory(user_id:str):
    data=redis_client.get(user_id)
    if data:
        return json.loads(data)
    return []

