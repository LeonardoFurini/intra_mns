#!/usr/bin/env python3
from pathlib import Path
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QGuiApplication

# =================
import socket
import selectors
import types
import names
import json
from utils.constants import Operations
from conn_parser import ConnParser
import threading

status = False

class Ponte(QObject):
    @Slot(str, result=list)
    def fetch_image(self, pokemon_id):
        pass

    @Slot(str, result=list)
    def connect_to_server(nome, server, port):
        name_user = names.get_first_name()
        start_connections(server, int(port), nome)
        main_loop()
        pass

# Captura do teclado sem bloqueio
class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return

def my_callback(inp):
    txt_to_send = input('Digite a mensagem:')
    sock = key.fileobj
    req = ConnParser.create_request(operation=Operations.send_message, users=[inp], payload=txt_to_send, origin=name_user)
    sock.send(str.encode(req))

#start the Keyboard thread
kthread = KeyboardThread(my_callback)
#=========================================================================

sel = selectors.DefaultSelector()


def start_connections(host, port, name):
    server_addr = (host, port)
    print(f"Starting connection to {server_addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    request = ConnParser.create_request(operation=Operations.create_user, payload=name)
    data = types.SimpleNamespace(
        connid=1,
        msg_total=len(request),
        recv_total=0,
        messages=str.encode(request),
        outb=b"",
    )
    sel.register(sock, events, data=data)

online_user_name = []

def service_connection(key, mask):
    global online_user_name
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            rec = json.loads(recv_data.decode("utf-8"))
            
            if rec['operation'] == Operations.list_user.value:
                # Iremos mostrar todos os usuários online
                online_user_name = rec['users']
                print("Os usários online são:")
                for i in rec['users']:
                    print(f"\t- {i}")
            elif rec['operation'] == Operations.send_message.value:
                print(f"{rec['origin']}: {rec['payload']}")
            elif rec['operation'] == Operations.create_user.value:
                print("Comando ainda não cadastrado")
            elif rec['operation'] == Operations.new_user.value:
                print(f"O usuário {rec['users'][0]} está online!")
                online_user_name.append(rec['users'][0])

            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print(f"Closing connection {data.connid}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            # Captura os bytes a serem enviados e limpa o data.message
            data.outb = data.messages
            data.messages = bytes([])
        if data.outb:
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


#if len(sys.argv) != 4:
#    print(f"Usage: {sys.argv[0]} <host> <port> <num_connections>")
#    sys.exit(1)

def main_loop():
    try:
        while True:
            events = sel.select(timeout=1)
            if events:
                for key, mask in events:
                    service_connection(key, mask)
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()


app = QGuiApplication()

engine = QQmlApplicationEngine()
engine.load("gui\client_qml.qml")

ponte = Ponte()
context = engine.rootContext()
context.setContextProperty("ponte", ponte)

app.exec()

