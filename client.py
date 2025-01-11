import socket
import json
from threading import Thread

class Client:

    def __init__(self, addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr)
        Thread(target=self.get_all).start()
        self.drawing = {'pos_player': 0}
        self.pos_cell_x = 0
        self.pos_cell_y = 0
        self.pos =(0, 0)
        self.player = {
            # Движение
            'id': 0,
            'left': False,
            'right': False,
            'up': False,
            'run': False,
            'speed': 1000,
            'cadr': 0,
            # параметры
            'score': 0,
            'heart': 100,
            'block': ['дерево'] * 20,
            'shells': ['шар'] * 5,
            'inventory': [],
            'inventory_index': 0,
            'win': False,
            'task': {}
        }

    def get_all(self):
        while True:
            self.sock.sendall(bytes(json.dumps({"request": "get_all"}), 'UTF-8'))
            anser = json.loads(self.sock.recv(10 ** 8).decode('UTF-8'))
            self.drawing = anser
            self.player = anser['player']
            self.pos_cell_x = anser['pos_cell_x']
            self.pos_cell_y = anser['pos_cell_y']
            self.pos = anser['pos']
        self.sock.close()

    def move_player(self, napravlenie, znachenie):
        self.sock.sendall(bytes(json.dumps({'request': 'move', "napravlenie": napravlenie, 'znachenie': znachenie}), 'UTF-8'))

    def shoot(self, pos):
        self.sock.sendall(bytes(json.dumps({'request': 'shoot', "pos": pos}), 'UTF-8'))

    def get_pos(self, pos):
        self.sock.sendall(bytes(json.dumps({'request': 'block', "pos": pos}), 'UTF-8'))


    def update_index(self, index):
        self.sock.sendall(bytes(json.dumps({'request': 'update_index', "index": index}), 'UTF-8'))


    def get_cell(self, pos):
        self.sock.sendall(bytes(json.dumps({'request': 'get_cell', "pos": pos}), 'UTF-8'))

    def click(self, pos, funct):
        self.sock.sendall(bytes(json.dumps({'request': 'click', "pos": pos, 'funct': funct}), 'UTF-8'))

    def close(self):
        self.sock.sendall(bytes(json.dumps({'request': 'close'}), 'UTF-8'))

    def choice_inventory(self):
        self.sock.sendall(bytes(json.dumps({'request': 'choice_inventory'}), 'UTF-8'))
