import socket
from threading import Thread
import json

from game_ofline import Board, Player, Object, check_delete, players
from game_ofline import all_sprites, groups

HOST, PORT = 'localhost', 12222
MAX_PLAYERS = 4
obj_for_kart = {1: {'object': [{'img': 'генератор.jpg', 'pos': (1200, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_block'},
                               {'img': 'портал.png', 'pos': (3000, 440), 'size': (200, 250), 'funct': 'portal'}],
                    'enemy': [],
                    'task': {}}}


class Server:

    def __init__(self, addr, max_conn):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr)
        self.sock.listen(max_conn)

        self.board = Board(False, 1)
        self.id_players = []
        self.create_other_obj()
        self.listen()

    def create_other_obj(self):
        for i in obj_for_kart[1]['object']:
            Object(i['img'], i['pos'], i['size'], i['funct'])

    def listen(self):
        while True:
            try:
                if not 1 >= MAX_PLAYERS:
                    conn, addr = self.sock.accept()
                    Thread(target=self.handle_client,
                           args=(conn,)).start()
            except:
                print('sss')


    def handle_client(self, conn):
        id = list(filter(lambda f: f not in self.id_players, range(1, 5)))[0]
        self.main_player = Player(id)
        self.pos = (0, 0)
        while True:
            try:
                data = json.loads(data.decode('utf-8'))
                if data['request'] == 'get_all':
                    self.get_all(conn)
                if data["request"] == 'move':
                    self.main_player.moving_player(data['napravlenie'], data['znachenie'])
                elif data["request"] == 'shoot':
                    self.main_player.shoot(data['pos'])
                elif data["request"] == 'mousedown':
                    self.board.click(data['pos'], data['znachenie'], self.main_player)
                elif data["request"] == 'update_index':
                    self.main_player.update_inventory_index(data["index"])
                elif data["request"] == 'get_cell':
                    self.board.get_cell(data["pos"], self.main_player)
                    self.pos = self.board.celling(data["pos"], self.main_player)
                elif data["request"] == 'click':
                    self.board.click(data['pos'], data['funct'], self.main_player)
                elif data["request"] == 'shoot':
                    self.main_player.shoot(data['pos'])
                elif data["request"] == 'choice_inventory':
                    self.main_player.choice_inventory()

            except Exception as e:
                print(e.__class__.__name__)
            data = conn.recv(1024)
            if not data:
                pass

    def get_all(self, conn):
        for i in all_sprites: i.update()
        for i in all_sprites[::-1]: check_delete(i)
        for group in groups:
            for obj in group[::-1]:
                check_delete(obj)
        score = 0
        drawing = {}

        for group in groups:
            for obj in group:
                drawing[score] = {'size': (obj.rect.w, obj.rect.h), 'pos': (obj.rect.x, obj.rect.y),
                                  'img': obj.img_path}
                score += 1
        drawing['pos_player'] = self.main_player.rect.x
        drawing['player'] = self.main_player.player
        drawing['pos_cell_x'] = self.board.pos_cell_x
        drawing['pos_cell_y'] = self.board.pos_cell_y
        drawing['pos'] = self.pos
        conn.sendall(bytes(json.dumps(drawing), 'UTF-8'))

    def close(self):
        all_sprites.remove(self.main_player)
        players.remove(self.main_player)



if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)