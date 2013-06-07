# Processes the redis queue and outputs streaming data to the data file.
#
# Data Format (JSON)
# ===========
#
# [
# {"id":3,"direction":"f","speed":50},
# {"id":5,"direction":"r","speed":50},
# {"id":12,"direction":"f","speed":0}
# ]
#

import redis
import json

r = redis.Redis()

locos = []
for i in range(0,129):
	locos.append(i)

def process_bits(bits):
    global locos
    if (bits[0] == 's/d'):
 	#  0     1        2       3   
	# s/d,loco_id,direction,speed
	index = int(bits[1])
	locos[index] = {'direction': bits[2], 'speed': bits[3]}

def output_data():
    global locos
    f = open('www/data/locos.json','w')
    f.write("[\n")
    started = 0;
    for i in range(0,129):
	loco = locos[i]
	try:
	   line = ('{"id":' + str(i) + ',"direction":"' + loco['direction'] + '","speed":' + loco['speed'] + '}')
	   if started > 0:
		f.write(',\n\t' + line)
	   else: 
		f.write('\t' + line)
		started = 1
	except:
	   next
    f.write('\n]')
    f.close()

while True:
    val = r.blpop('loco')
#   DEBUG
#   print val
    value = val[1]
    bits = value.split(',')
    process_bits(bits);
    output_data()

