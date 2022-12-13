# echo-client.py

import socket
import json
from dataclasses import dataclass
from utils.constants import Operations
from conn_parser import ConnParser
import names


@dataclass
class serverConnection:
    server_host: str = "127.0.0.1"
    server_port: int = 65432
    conn = None

    def connect_server(self, name: str):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.server_host, self.server_port))
        try:
            request = ConnParser.create_request(operation=Operations.create_user, payload=name)
            self.conn.sendall(str.encode(request))
            data = self.conn.recv(1024)
            print(data)
        except:
            print("Não foi possível criar uma conexão!")

    def send_message(self, message: str):
        self.conn.sendall(str.encode(message))
        data = self.conn.recv(1024)
        print(f"Received: {data!r}")
        pass

    def request_online_users(self):
        request = ConnParser.create_request(operation=Operations.list_user)
        print(f"Request: {request}")
        self.conn.sendall(str.encode(request))
        data = self.conn.recv(1024)
        return data

    def read_message(self):
        return self.conn.recv(1024)

    def list_online_user(self, name: str) -> list:
        request = ConnParser.create_request(operation=Operations.create_user)
        self.conn.sendall(str.encode(request))
        return self.read_message()


# TODO: Colocar em um arquivo comum
def create_request(operation: Operations, users: list[tuple[str, str]] = None, payload: str = None) -> dict:
    return json.dumps({
        "operation": Operations.list_user.value, 
        "users": users, 
        "payload": payload
    })

if __name__ == "__main__":
    print(f"Digite seu usuário:")
    #name_user = input()
    name_user = names.get_first_name()
    print(name_user)
    print(f"Conectando ao servidor...")
    try:
        con = serverConnection()
        con.connect_server(name_user)
        #print(con.read_message())
    except:
        print(f"Falha ao conectar no servidor")
    
    while True:        
        print(f"Escolha um usuário:\n")
        destiny = input()
        print(f"Mensagem:\n")
        message = input()

        req = create_request(operation=Operations.send_message, users=destiny, payload=message)
        con.send_message(req)
        #if int(action) in [member.value for member in Operations]:
        #    con = serverConnection()
        #    if int(action) == Operations.list_user.value:
        #        #print(f"Solicitando usuários disponíveis...")
        #        #resp = con.request_online_users()
        #        #user_list = ConnParser.decode_payload(bytes(resp, 'utf-8'))
        #        pass
        #    elif action == Operations.send_message:
