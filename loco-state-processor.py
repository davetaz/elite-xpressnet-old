import redis

r = redis.Redis()

def process_bits(bits):
    if (bits[0] == 's/d'):
	f = open('../www/data/locos.json','w')
	f.write(bits[3]);

while True:
    val = r.blpop('loco')
    print val
    value = val[1]
    bits = value.split(',')
    process_bits(bits);
