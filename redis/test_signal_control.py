# Overview
# test_track.py is a stand alone script that implements the tests defined in the readme file for the code. This tests the control script is working properly with the example config file

import redis
import sys
from time import sleep

r = redis.Redis()

r.rpush("signals",'"33,B,16",false,amber');
#8
sleep(5)
r.rpush("signals",'"33,B,16",false,red');
#64
echo("32,B,16 should be amber!");
