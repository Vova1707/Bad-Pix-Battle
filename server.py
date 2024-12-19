import socket
from threading import Thread
import json

HOST, PORT = 'localhost', 12220  # Адрес сервера
MAX_PLAYERS = 4  # Максимальное кол-во подключений


SERVER_ROOM_WIDTH = 4000
SERVER_ROOM_HEIGHT = 1000


class Server:

    def __init__(self, addr, max_conn):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr)
        self.players = []
        self.id_players = []
        self.sock.listen(max_conn)
        self.listen()

    def listen(self):
        while True:
            try:
                if not len(self.players) >= MAX_PLAYERS:
                    conn, addr = self.sock.accept()
                    print("New connection", addr)
                    Thread(target=self.handle_client,
                           args=(conn,)).start()
            except:
                pass

    def handle_client(self, conn):
        id = list(filter(lambda f: f not in self.id_players, range(1, 5)))[0]
        self.player = {
            "id": id,
            "x": 400,
            "y": 300,
            "is_moving": 1,
            'left_right': 1,
        }
        self.running = False
        self.id_players.append(id)
        self.players.append(self.player)
        self.h = 0
        self.xxx = 0

        self.x = self.player["x"]
        self.y = self.player["y"]
        self.mov = False
        self.time = 0

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("Disconnect")
                    break
                data = json.loads(data.decode('utf-8'))
                if data["request"] == 'move':
                    print(1)
                sgp = {"get_all": lambda: self.get_all(conn),
                       "move": lambda: self.move(data['move']),
                       'stop': self.stop,
                       }
                sgp[data["request"]]()

            except Exception as e:
                print(e)
                break
        del self.id_players[self.id_players.index(id)]
        self.players.remove(self.player)

    def get_all(self, conn):
        conn.sendall(bytes(json.dumps({"response": self.players}), 'UTF-8'))

    def stop(self):
        self.player['is_moving'] = 0
        self.player["left_right"] = 0

    def move(self, moving):
        moved = {"left": lambda: self.moving("x", -10, 1),
                 'right': lambda: self.moving("x", 10, 2),
                 'up': lambda: self.moving("y", -10, 1),
                 'down': lambda: self.moving("y", 10, 2),
                 }
        moved[moving]()

    def moving(self, coord, value, l_r=False):
        if self.player['is_moving'] == 0:
            self.player['is_moving'] += 1

        if l_r:
            self.player["left_right"] = l_r
        if self.xxx > 2:
            if self.player['is_moving'] >= 3:
                self.player['is_moving'] = 1
            else:
                self.player['is_moving'] += 1
                self.xxx = 0
        else:
            self.xxx += 1
        self.player[coord] += value


if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)