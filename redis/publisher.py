import redis
import sys

r = redis.Redis()

queue = sys.argv[1]
message = sys.argv[2]

r.rpush(queue, message)
