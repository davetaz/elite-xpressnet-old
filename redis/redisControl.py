# Overview
# test_track.py is a stand alone script that implements the tests defined in the readme file for the code. This tests the control script is working properly with the example config file

import redis
import sys
from time import sleep
from subprocess import call

r = redis.Redis()
r.rpush("trains",sys.argv[1]+","+sys.argv[2]+","+sys.argv[3])
