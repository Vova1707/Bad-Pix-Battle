import pygame
import numpy as np
from player import Player
from client import Client
import sqlite3

import pygame_widgets
from pygame_widgets.button import ButtonArray, Button
from pygame_widgets.textbox import TextBox


HOST, PORT = "localhost", 12200
pygame.init()
WINDOW_HEIGHT, WINDOW_WEIGHT = 1000, 1000


class Main_Window:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WEIGHT))
        self.RUN = True
        pygame.display.set_caption('Bad Pix Battle')
        self.clock = pygame.time.Clock()

        self.connection = sqlite3.connect('databases/users.db')
        self.cursor = self.connection.cursor()
        self.user = None
        self.create_table()

        self.view_logo()
        self.listen_all()

    def create_table(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                login TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL)
            '''
        )
        self.connection.commit()

    def update_name_users(self, new_name, id):
        self.cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_name, id))
        self.connection.commit()

    def add_user(self, username, login, password):
        print(login, password)
        try:
            self.cursor.execute("INSERT INTO users (username, login, password) VALUES (?, ?, ?)",
                                (username, login, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def find_user(self, login, password):
        query = "SELECT * FROM users WHERE login = ? AND password = ?"
        self.cursor.execute(query, (login, password))
        user = self.cursor.fetchone()
        if user:
            return user
        else:
            return False

    def listen_all(self):
        self.active_surface = 'registration'
        self.options_window_widget = np.array([])
        self.update_window = True
        while self.RUN:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.RUN = False
                    quit()
                if self.active_surface == 'menu':
                    self.menu()
                elif self.active_surface == 'game':
                    self.game_online(event)
                elif self.active_surface == 'registration':
                    self.registration()
            pygame_widgets.update(events)
            pygame.display.update()
            self.clock.tick(60)

    def game_online(self, event):
        if self.update_window:
            button = Button(
                self.screen,
                700,
                0,
                300,
                150,
                text='Выйти',
                fontSize=50,
                borderColour=(0, 0, 0),
                inactiveColour=(200, 50, 0),
                hoverColour=(150, 0, 0),
                pressedColour=(0, 200, 20),
                radius=0,
                onClick=lambda: self.restart_surface('menu', False))
            self.options_window_widget = np.append(self.options_window_widget, [button])
            self.client = Client((HOST, PORT))
            self.update_window = False


        if event.type == pygame.KEYDOWN:
            if event.key == ord('a'):
                self.client.move("left")
                print('a')
            if event.key == ord('d'):
                self.client.move("right")
            if event.key == ord('w'):
                self.client.move("up")
            if event.key == ord('s'):
                self.client.move("down")
        self.screen.fill((255, 255, 255))
        for i in self.client.players:
            player = Player((i["x"], i["y"]))
            self.screen.blit(player.image, player.rect)



    def menu(self):
        if self.update_window:
            buttonArray = ButtonArray(
                self.screen,
                50,
                350,
                500,
                600,
                (1, 4),
                border=10,
                texts=('игра по сети', 'игра оффлайн', 'что-то', 'выйти'),
                colour=(0, 0, 0),
                inactiveColours = [(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)],
                hoverColours = [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)],
                pressedColours = [(0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0)],
                onClicks=(
                lambda: self.restart_surface('game'), lambda: print('2'), lambda: print('3'), lambda: self.restart_surface('registration')))
            button = Button(
                self.screen,
                450,
                150,
                100,
                100,
                text='  Сохранить',
                fontSize=10,
                colour=(255, 255, 255),
                borderThickness=5,
                borderColour=(0, 0, 0),
                inactiveColour=(200, 50, 0),
                hoverColour=(150, 0, 0),
                pressedColour=(0, 200, 20),
                radius=10,
                onClick=lambda: print(textbox.text)
            )

            textbox = TextBox(self.screen, 50, 150, 400, 100, fontSize=50,
                              borderColour=(0, 0, 0), textColour=(0, 0, 0), radius=10, borderThickness=5)


            self.options_window_widget = np.append(self.options_window_widget, [buttonArray, textbox, button])
            self.update_window = False
        self.screen.fill((200, 100, 50))
        img = pygame.image.load("Images/Main_menu/Главная надпись.png").convert()
        self.screen.blit(img, (300, 0))

    def restart_surface(self, name, game_run=True):
        if not game_run:
            self.run_game = False
            self.client.sock.close()
        del self.options_window_widget
        self.options_window_widget = np.array([])
        self.active_surface = name
        self.update_window = True



    def view_logo(self):
        """
        Показ логотипа на 2 секунды
        """
        logo = pygame.image.load('ааав.jpeg')
        self.screen.fill((255, 255, 255))
        self.screen.blit(logo, (0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)


    def registration(self):
        if self.update_window:
            login = TextBox(self.screen, 300, 150, 400, 80, fontSize=50,
                            borderColour=(0, 0, 0), textColour=(0, 0, 0), radius=10, borderThickness=5)
            password = TextBox(self.screen, 300, 250, 400, 80, fontSize=50,
                               borderColour=(0, 0, 0), textColour=(0, 0, 0), radius=10, borderThickness=5)
            button_login = Button(
                self.screen,
                350,
                350,
                300,
                80,
                text='Зарегистрироваться',
                fontSize=10,
                colour=(255, 255, 255),
                borderThickness=5,
                borderColour=(0, 0, 0),
                inactiveColour=(200, 50, 0),
                hoverColour=(150, 0, 0),
                pressedColour=(0, 200, 20),
                radius=10,
                onClick=lambda: self.log_in(''.join(login.text), ''.join(password.text))
            )
            button_logoup = Button(
                self.screen,
                350,
                450,
                300,
                80,
                text='Войти',
                fontSize=10,
                colour=(255, 255, 255),
                borderThickness=5,
                borderColour=(0, 0, 0),
                inactiveColour=(200, 50, 0),
                hoverColour=(150, 0, 0),
                pressedColour=(0, 200, 20),
                radius=10,
                onClick=lambda: self.log_up(''.join(login.text), ''.join(password.text))
            )
            self.options_window_widget = np.append(self.options_window_widget, [login, password, button_login, button_logoup])
            self.update_window = False
        self.screen.fill((200, 100, 50))


    def log_in(self, login, passoword):
        if len(login) > 8 and len(passoword) > 8:
            if self.add_user("Новый пользователь", login, passoword):
                self.user = self.find_user(login, passoword)
                self.restart_surface('menu')

    def log_up(self, login, passoword):
        if len(login) > 8 and len(passoword) > 8:
            self.user = self.find_user(login, passoword)
            if self.user:
                self.restart_surface('menu')




if __name__ == "__main__":
    Main_Window().__init__()
