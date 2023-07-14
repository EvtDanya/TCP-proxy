from modules.args import parse_args
from modules.print import *

import sys
import socket
import threading
import os
import logging
import datetime

def start_log() -> None:
    '''
    Start logging and report errors to log file
    '''
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        
    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"logs/proxy-errors_{datetime.datetime.now().strftime('%d%m%Y')}.log",
        filemode='a',
        encoding='utf-8'
    )

def hexdump(src, length=16) -> None:
    '''
    Print a hex dump (or text) of bytes
    '''
    result = []
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len (src), length):
        s = src[i:i + length]
        hex = b' '.join([b'%0*X' % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b'%04X %-*s %s' % (i, length * (digits + 1), hex, text))
        
    print_color('[>] Dump', 'yellow')
    print(b'\n'.join(result))
    
def receive_from(connection) -> bytes:
    '''
    Receive data from connection
    '''
    buffer=b''
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        print_color(f'[!] {e}', 'red')
        logging.error(f'[!] {e}')
        pass
    
    return buffer

def request_handler(buffer) -> bytes:
    return buffer

def response_handler(buffer) -> bytes:
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first) -> None:
    '''
    Main logic for proxy-server
    '''
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        
    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print_color(f'[i] Sending {len(remote_buffer)} bytes to localhost', 'green')
        client_socket.send(remote_buffer)
        
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print_color(f'[i] Received {len(local_buffer)} bytes from localhost', 'green')
            hexdump(local_buffer)
            
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print_color('[i] Sent to remote', 'green')
        
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print_color(f'[i] Received {len(remote_buffer)} bytes from remote', 'green')
            hexdump(remote_buffer)
            
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print_color('[i] Sent to localhost', 'green') 
        
        if not len(remote_buffer) or not len(local_buffer):
            client_socket.close()
            remote_socket.close()
            print_color('[*] No more data. Closing connections...', 'yellow')
            break

def server_loop(local_host, local_port,
                remote_host, remote_port, receive_first) -> None:
    '''
    Configuring and managing connections
    '''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print_color(f'[!] Problem on bind: {e}', 'red')
        logging.error(f'[!] {e}')
        
        print_color(f'[!] Failed to listen {local_host}:{local_port}', 'red')
        print_color(f'[i] Check for correct permissions or check for other listening sockets', 'yellow')
        
        sys.exit(0)
    
    print_color(f'[*] Listening on {local_host}:{local_port}', 'green') 
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        print_color(f'[i] Received incoming connections from {addr[0]}:{addr[1]}')
        
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first)
        )
        proxy_thread.start()
        
def main() -> None:
    print_logo()
    start_log()
    
    args = parse_args()    
    
    server_loop(args.lh, args.lp, args.rh, args.rp, args.r)
    
if __name__ == '__main__':
    main()
    