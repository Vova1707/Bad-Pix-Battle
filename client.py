import socket
import json
from threading import Thread

class Client:

    def __init__(self, addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr)
        self.players = []
        Thread(target=self.get_players).start()

    def get_players(self):
        while True:
            self.sock.sendall(bytes(json.dumps({"request": "get_all"}), 'UTF-8'))
            received = json.loads(self.sock.recv(1024).decode('UTF-8'))
            self.players = received["response"]

    def move(self, side):
        self.sock.sendall(bytes(json.dumps({"request": "move", "move": side}), 'UTF-8'))