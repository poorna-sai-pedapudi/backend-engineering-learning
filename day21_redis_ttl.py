import redis
import time

r = redis.Redis(
    host = "localhost",
    port = 6379,
    decode_responses = True
)

r.set("backend_learning", "Harish")

r.expire("backend_learning", 30)

ttl = r.ttl("backend_learning")
print(ttl)

exists = r.exists("backend_learning")
print(exists)


for i in range(5):
    print(r.ttl("backend_learning"))
    time.sleep(5)
