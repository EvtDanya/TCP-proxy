from modules.print import print_color, hexdump

import logging
import socket
import sys
import threading

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