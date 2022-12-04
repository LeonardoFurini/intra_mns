# echo-server.py
import socket
from ..constans import Operations

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


# https://realpython.com/python-sockets/
# SOCK_STREAM = TCP
# AF_INET = família de endereços da Internet para IPv4
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # Associando o socket a uma interface especifica
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
