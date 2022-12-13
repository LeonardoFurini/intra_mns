#!/usr/bin/env python3

import sys
import socket
import selectors
import types
import json
from dataclasses import dataclass
from typing import Optional
from utils.constants import Operations

# Apelido para a implementação mais eficiente disponível na plataforma atual: essa deve ser a escolha padrão para a maioria dos usuários.
sel = selectors.DefaultSelector()


online_users = []

@dataclass
class ServerClient():
    name: str
    ip: str
    port: int
    sock: None

def on_user_msg(name: str):
    return f"O usuário {name} está online!"

def create_request(operation: Operations, users: list[tuple[str, str]] = None, payload: str = None) -> dict:
    return json.dumps({
        "operation": Operations.list_user.value, 
        "users": users, 
        "payload": payload
    })
    
def notify_all_users(message: str):
    for client in online_users:
        soc = client.sock.fileobj
        req = create_request(operation=Operations.create_user, users=client.name, payload=message)
        soc.send(bytes(req, 'utf-8'))


def string_to_dict(pld: str) -> dict:
    return json.loads(pld)

def accept_wrapper(sock):
    """ Obter o novo objeto de soquete e registrá-lo com o seletor.
    
    Caso o evento não tenha dados internos, significa que pode ser 
    um evento de conexão ou desconexão.
    """
    conn, addr = sock.accept()  
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    
    """Em seguida, você cria um objeto para armazenar os dados que deseja incluir
    junto com o soquete usando um arquivo SimpleNamespace. Como você deseja saber
     quando a conexão do cliente está pronta para leitura e gravação, ambos os
     eventos são definidos com o operador OR bit a bit :"""
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    # Cliente está pronto para leitura e gravação
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    # Registre um objeto de arquivo para seleção, monitorando-o para eventos de E/S.
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
                online_users.append(ServerClient(name=parsed_payload['payload'], ip=data.addr[0], port=data.addr[1], sock=key))
                print("Cadastrado com sucesso!!")
                #req = create_request(operation=Operations.create_user, payload=on_user_msg(parsed_payload['payload']))
                # Devo notificar todos os usuários que esta pessoa esta online
                notify_all_users(on_user_msg(parsed_payload['payload']))
            data.outb = ''
            #data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
# Abre o socket
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connections = Connections(ip=host, port=port)
 # Associando o socket a uma interface específica
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)

# Registre um objeto de arquivo para seleção, monitorando-o para eventos de E/S.
# No caso estou passando para monitorar eventos de Leitura
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        # A chamada será bloqueada até que um objeto de arquivo monitorado fique pronto.
        events = sel.select(timeout=None)
        # key       | é a ocorrência de SelectorKey correspondente a um objeto de arquivo pronto.
        # Events    | é uma máscara de bits de eventos prontos neste objeto de arquivo.
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
