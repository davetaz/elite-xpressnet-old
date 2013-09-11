import redis
import time

r = redis.Redis()

message = r.lpop('sensors')
if (message):
	print "Message: " + message
