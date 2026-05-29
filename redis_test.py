import redis

r = redis.Redis(
    host = "localhost",
    port = 6379,
    decode_responses = True
)

r.set("name", "Harish")

value = r.get("name")

print(value)

