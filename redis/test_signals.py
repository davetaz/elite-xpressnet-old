# Overview
# test_track.py is a stand alone script that implements the tests defined in the readme file for the code. This tests the control script is working properly with the example config file

import redis
import sys
from time import sleep

r = redis.Redis()

r.rpush("signal_action",'"32,B,1",green');
#8
r.rpush("signal_action",'"32,B,16",red');
#64
r.rpush("signal_action",'"32,B,16",twoamber');
#32
