# Overview
# test_track.py is a stand alone script that implements the tests defined in the readme file for the code. This tests the control script is working properly with the example config file

import redis
import sys
from time import sleep

r = redis.Redis()

r.rpush("turnout_action",'"34,B,1",L');
#1
r.rpush("turnout_action",'"34,B,4",R');
#8
r.rpush("turnout_action",'"34,B,1",R');
#2
