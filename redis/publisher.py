import redis
import time

r = redis.Redis()

i = 0
while True:
    r.rpush('queue', 'Message %d' % i)
    i += 1
    time.sleep(1)
