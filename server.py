import socket
from threading import Thread
import json

HOST, PORT = 'localhost', 12000  # Адрес сервера
MAX_PLAYERS = 2  # Максимальное кол-во подключений


class Server:

    def __init__(self, addr, max_conn):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr)
        self.players = []

        self.sock.listen(max_conn)
        self.listen()  # вызываем цикл, который отслеживает подключения к серверу

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
        self.player = {
            "id": len(self.players) + 1,
            "x": 400,
            "y": 300
        }
        self.players.append(self.player)
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("Disconnect")
                    break
                data = json.loads(data.decode('utf-8'))
                if data["request"] == "get_all":
                    conn.sendall(bytes(json.dumps({"response": self.players}), 'UTF-8'))

                if data["request"] == "move":
                    if data["move"] == "left":
                        self.player["x"] -= 10
                    if data["move"] == "right":
                        self.player["x"] += 10
                    if data["move"] == "up":
                        self.player["y"] -= 10
                    if data["move"] == "down":
                        self.player["y"] += 10
            except Exception as e:
                print(e)
                break
        self.players.remove(self.player)


if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)