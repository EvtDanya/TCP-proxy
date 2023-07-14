from modules.args import parse_args
from modules.print import *
import sys
import socket
import threading

HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len (src), length):
        s = src[i:i + length]
        hex = b' '.join([b'%0*X' % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b'%04X %-*s %s' % (i, length * (digits + 1), hex, text))

    print(b'\n'.join(result))
    
def receive_from(connection):
    buffer=b''
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    
    return buffer
          
if __name__ == '__main__':
    # args = parse_args()
    print_logo()