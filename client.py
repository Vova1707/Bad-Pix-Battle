import socket
import pygame

"""Создание окна игры"""
pygame.init()
running = True
WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Название окна игры')

'''подключение к серверу'''
# Создание соккета(порта) клиента
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# main_socket - главный порт(соккет) сервера сюда приёмы подключений, AF_INET - тип адреса, socket.SOCK_STREAM - тип адресов (4 цыфры), используется TCP протокол, который лучше UDP
sock.setsockopt(socket.IPPROTO_IP, socket.TCP_NODELAY, 1)

# Алгоритм нейгла - упаковка данных в пакетыи редко отправляет, это чтобы такого не было
sock.connect(('localhost', 10000))
#подключение к серверу по его порту 1 значение - IP сервера
# Этот соккет не блокирующий тк зависит от ответа сервера"""


while running:
    '''Обработка событий'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    # обработка закрытия окна
    if pygame.mouse.get_focused():
        mouse_pos = pygame.mouse.get_pos()
        print(mouse_pos)
    '''Команды сервера'''
    sock.send('Идти вправо'.encode())
    # отправляем команды на сервер
    data = sock.recv(1024)
    # Как сервер что-то пришлёт только потом код будет идти дальше
    data = data.decode()
    # Новое состояние игрового поля
    print(data)
pygame.quit()

class Client:
    def __init__(self):
        pass
    # организовать клиент в виде класса