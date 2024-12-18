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
            "is_moving": 0,
            "jump": 5
        }
        self.id_players.append(id)
        self.players.append(self.player)
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("Disconnect")
                    break
                data = json.loads(data.decode('utf-8'))
                sgp = {"get_all": lambda: self.get_all(conn),
                       "move": lambda: self.move(data['move']),
                       }
                sgp[data["request"]]()

            except Exception as e:
                print(e)
                break
        del self.id_players[self.id_players.index(id)]
        print(self.id_players)
        self.players.remove(self.player)

    def get_all(self, conn):
        conn.sendall(bytes(json.dumps({"response": self.players}), 'UTF-8'))

    def move(self, moving):
        print(moving)
        self.player['is_moving'] = self.player['is_moving'] % 4 + 1 if self.player['is_moving'] % 4 == 0 else \
        self.player['is_moving'] % 4
        moved = {"left": lambda: self.moving("x", -10),
                 'right': lambda: self.moving("x", 10),
                 'up': lambda: self.moving("y", -10),
                 'down': lambda: self.moving("y", 10),
                 }
        moved[moving]()

    def moving(self, coord, value):
        self.player[coord] += value


if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)