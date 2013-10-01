import redis
import time
import sys

r = redis.Redis()

while 1:
	message = r.lpop(sys.argv[1])
	if (message):
		print "Message: " + message
