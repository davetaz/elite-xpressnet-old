import redis
import time
import sys

r = redis.Redis()

message = r.lpop(sys.argv[1])
if (message):
	print "Message: " + message
