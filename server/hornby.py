import serial
import struct
import time

FORWARD = 0
REVERSE = 1
OFF = 0
ON = 1

debug = 0

ser = None

def connection_open(device, baud):
    global ser
    try:
        ser = serial.Serial(device, baud)
    except Exception as e:
        print(e)
        raise RuntimeError('Unable to open connection with Hornby Elite Controller')

def connection_close():
    global ser
    if not ser:
        raise RuntimeError('Connection cannot be closed because it has not been opened')
    try:
        ser.close()
    except Exception as e:
        print(e)
        raise RuntimeError('Unable to close connection with Hornby Elite Controller')

def set_debug(arg):
    global debug
    debug = arg

def parity(message):
    lrc = 0
    for b in message:
        lrc ^= b
    message.append(lrc)

def send(message):
    ok = False
    trys = 1
    while not ok and trys < 5:
        ser.write(message)
        if debug:
            print('trys = %d send:' % trys, end=' ')
            for byte in message:
                print(hex(byte), end=' ')
            print('receive: ', end=' ')
        time.sleep(.1)
        if debug:
            print()
        while ser.in_waiting > 0:
            enq = ser.read()
            if debug:
                print(enq.hex(), end=' ')
            if enq == b'\x05':
                ok = True
        if debug:
            print()
        trys += 1

class Train:
    def __init__(self, address):
        self.address = address
        self.group = [0, 0, 0]

    def throttle(self, speed, direction):
        message = bytearray(b'\xE4\x00\x00\x00\x00')
        message[1] = 0x13
        struct.pack_into(">H", message, 2, self.address)
        message[4] = speed
        if direction == FORWARD:
            message[4] |= 0x80
        elif direction == REVERSE:
            message[4] &= 0x7F
        parity(message)
        send(message)

    def function(self, num, switch):
        function_table = [
            [0, 0x20, 0x10, 0xEF],
            [0, 0x20, 0x01, 0xFE],
            [0, 0x20, 0x02, 0xFD],
            [0, 0x20, 0x04, 0xFB],
            [0, 0x20, 0x08, 0xF7],
            [1, 0x21, 0x01, 0xFE],
            [1, 0x21, 0x02, 0xFD],
            [1, 0x21, 0x04, 0xFB],
            [1, 0x21, 0x08, 0xF7],
            [2, 0x22, 0x01, 0xFE],
            [2, 0x22, 0x02, 0xFD],
            [2, 0x22, 0x04, 0xFB],
            [2, 0x22, 0x08, 0xF7],
        ]
        if num >= len(function_table):
            raise RuntimeError('Invalid function')
        message = bytearray(b'\xE4\x00\x00\x00\x00')
        message[1] = function_table[num][1]
        if switch == ON:
            self.group[function_table[num][0]] |= function_table[num][2]
        elif switch == OFF:
            self.group[function_table[num][0]] &= function_table[num][3]
        else:
            raise RuntimeError('Invalid switch on function')
        message[4] = self.group[function_table[num][0]]
        struct.pack_into(">H", message, 2, self.address)
        parity(message)
        send(message)

class Accessory:
    def __init__(self, address, offset):
        self.address = address
        self.offset = offset

    def activate(self):
        message = bytearray(b'\x52\x00\x00')
        message[1] = self.address
        message[2] = self.offset
        message[2] |= 0x80
        message[2] |= 0x01
        parity(message)
        send(message)

    def deactivate(self):
        message = bytearray(b'\x52\x00\x00')
        message[1] = self.address
        message[2] = self.offset
        message[2] |= 0x80
        message[2] &= 0xFE
        parity(message)
        send(message)
