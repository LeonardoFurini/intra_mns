#!/usr/bin/env python3

import sys
import socket
import selectors
import types
import json
from dataclasses import dataclass
from typing import Optional
from utils.constants import Operations

sel = selectors.DefaultSelector()

@dataclass
class ServerClient():
    name: str
    ip: str
    port: int


@dataclass
class Connections():
    ip: str
    port: str
    client: Optional[list[ServerClient]] = None

    def send_list_user():
        pass

def create_request(operation: Operations, users: list[tuple[str, str]], payload: str = None) -> dict:
    return json.dumps({
        "operation": Operations.list_user.value, 
        "users": users, 
        "payload": None
    })
    

def string_to_dict(pld: str) -> dict:
    return json.loads(pld)

def accept_wrapper(sock):
    """ Obter o novo objeto de soquete e registrá-lo com o seletor"""
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    # Cliente está pronto para leitura e gravação
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        # Ao receber uma mensagem
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            parsed_payload = string_to_dict((data.outb).decode("utf-8"))
            
            if parsed_payload['operation'] == Operations.list_user.value:
                clients = []
                for i in range(len(events)):
                    clients.append(events[i][0].data.addr)
                req = create_request(operation=Operations.list_user, users=clients)
                sent = sock.send(bytes(req, 'utf-8'))  # Should be ready to write
            elif parsed_payload['operation'] == Operations.send_message.value:
                print("Enviar mensagem para usuários específicos!")
                pass
            elif parsed_payload['operation'] == Operations.create_user.value:
                print("Cadastrar novo usuário!")
                if connections.client:
                    connections.client += ServerClient(name=parsed_payload['payload'], ip=data.addr[0], port=data.addr[1])
                else:
                    connections.client = ServerClient(name=parsed_payload['payload'], ip=data.addr[0], port=data.addr[1])

            #data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = Connections(ip=host, port=port)
 # Associando o socket a uma interface específica
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                # É um soquete de escuta e precisa aceitar a conexão
                accept_wrapper(key.fileobj)
            else:
                # É um soquete de cliente que já foi aceito e precisa fazer a manutenção dele
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
