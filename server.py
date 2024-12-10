import socket
import time

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# main_socket - главный порт(соккет) сервера сюда приёмы подключений, AF_INET - тип адреса, socket.SOCK_STREAM - тип адресов (4 цыфры), используется TCP протокол, который лучше UDP
main_socket.setsockopt(socket.IPPROTO_IP, socket.TCP_NODELAY, 1)
# Алгоритм нейгла - упаковка данных в пакетыи редко отправляет, это чтобы такого не было
main_socket.bind(('localhost', 10000))
# Связка с портом компьютера первые 1024 зарезервированны
main_socket.setblocking(0)
# Не нужно ждать сообщение от прота компьютера
main_socket.listen(5)
print('Создался новый соккет')
# Количество человек для подключения к главному порту
player_sockets = []
# список сокетов игроков
while True:
    try:
        new_socket, addr = main_socket.accept()
        #есть ли желающие войти в игру, new_socket = новый соккет игрока, addr = адрес игрока, направление игрока на сервер
        print('Подключился', addr)
        new_socket.setblocking(0)
        player_sockets.append(new_socket)
    except:
        print('Нет тех кто хочет играть')
        # если нет подключений
        pass
    # считываем команды игроков
    for sock in player_sockets:
        try:
            data_sock = sock.recv(1024)
            # прочитать данные соккета что в него пришло
            data = data_sock.decode()
            print('Получил', data)
        except:
            # если ничего не пришло
            pass
    # обработка данных
    # обработка состояний
    for sock in player_sockets:
        try:
            sock.send('Новое состояние игры'.encode())
            # Отправляем закодированные данные
        except:
            player_sockets.remove(sock)
            #если игрок отвалился
            sock.close()
            print('Отключился игрок')
    time.sleep(1)

class Server:
    def __init__(self):
        pass
    # организовать сервер в виде класса
