# echo-client.py

import socket
import json
from dataclasses import dataclass
from ..constans import Operations


@dataclass
class serverConnection:
    server_host: str = "127.0.0.1"
    server_port: int = 65432

    def send_message(self, message: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_host, self.server_port))
            s.sendall(str.encode(message))
            data = s.recv(1024)
            print(f"Received: {data!r}")
        pass

    def request_online_users(self):
        request = json.dumps(
            {"operation": Operations.list_user.value, "users": None, "payload": None}
        )
        print(f"Request: {request}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_host, self.server_port))
            s.sendall(str.encode(request))
            data = s.recv(1024)
            print(f"Received: {data!r}")

    def read_message(self):
        pass

    def list_online_user() -> list:
        pass


def input_params():
    pass


while True:
    print(f"Operação:\n\t(1) - Listar usuários diponíveis\n\t(2) - Enviar mensagem")
    action = input()
    if int(action) in [member.value for member in Operations]:
        con = serverConnection()
        if int(action) == Operations.list_user.value:
            print(f"Solicitando usuários disponíveis...")
            con.request_online_users()
        elif action == Operations.send_message:
            user_input = input()
            con.send_message(user_input)
