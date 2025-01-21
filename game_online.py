import pygame
from client import Client


HOST, PORT = "localhost", 12220  # Для сервера в дальнельшей перспективе будет развитие до настоящего сервера
# Начальные группы спрайтов
all_sprites = []
base_cells = []
players = []
breaking_block = []
other_object = []
shells = []
breaking_shells = []
groups = [other_object, base_cells, breaking_block, players, shells, breaking_shells]


class Game:
    def __init__(self, parent, kart):
        self.parent = parent
        self.screen = parent.screen
        self.kart = kart
        self.comands = {
            pygame.KEYDOWN:
                {(pygame.K_f,): lambda: self.client.shoot(self.client.drawing['pos']) if self.client.drawing else 1,
                 (pygame.K_e,): lambda: self.client.choice_inventory(),
                 (pygame.K_d,): lambda: self.client.move_player('right', True),
                 (pygame.K_s,): lambda: self.client.move_player('run', True),
                 (pygame.K_a,): lambda: self.client.move_player('left', True),
                 (pygame.K_w,): lambda: self.client.move_player('up', True),
                 (pygame.K_RIGHT,): lambda: self.client.update_index(1),
                 (pygame.K_LEFT,): lambda: self.client.update_index(-1),

                 },
            pygame.KEYUP:
                {(pygame.K_d,): lambda: self.client.move_player('right', False),
                 (pygame.K_a,): lambda: self.client.move_player('left', False),
                 (pygame.K_w,): lambda: self.client.move_player('up', False),
                 (pygame.K_s,): lambda: self.client.move_player('run', False),
                 },

        }

    def create_widgets(self):
        self.client = Client((HOST, PORT))
        self.parent.create_button((1400, 0), (200, 80), 'Выйти', 0, lambda: self.close_game('game_online'))

    def listen_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.client.get_cell(event.pos)
            self.pos = self.client.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.client.click((event.pos[0], event.pos[1]), 'add' if event.button == 1 else
            'delete' if event.button == 3 else False)
        if event.type in self.comands.keys():
            key = list(filter(lambda d: event.key in d, self.comands[event.type].keys()))
            if key:
                self.comands[event.type][key[0]]()
        pass

    def listen(self):
        self.parent.screen.fill((196, 196, 196))
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game.jpg"), (6400, 1000)),
                                    (0, 160))
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/шкала.png"), (450, 120)),
                                (650, 0))

        pygame.draw.rect(self.parent.screen, (255, 0, 0),
                         (210, 30, 400 * (self.client.player['heart'] / 100) // 1, 40))
        pygame.draw.rect(self.parent.screen, (0, 0, 0), (210, 30, 400, 40), 5)

        pygame.draw.rect(self.parent.screen, (255, 255, 0),
                         (210, 70, 400 * (self.client.player['speed'] / 1000) // 1, 15))
        pygame.draw.rect(self.parent.screen, (0, 0, 0), (210, 70, 400, 15), 5)

        for i in range(len(self.client.player['inventory'])):
            if self.client.player['inventory'][i]:
                self.parent.screen.blit(pygame.transform.scale(
                    pygame.image.load(f"Images/Object/{self.client.player['inventory'][i]}"), (70, 70)),
                                        (690 + i * 105, 25))

        pygame.draw.polygon(self.parent.screen, (0, 0, 0),
                            [(700 + 105 * self.client.player['inventory_index'], 140),
                             (725 + 105 * self.client.player['inventory_index'], 110),
                             (750 + 105 * self.client.player['inventory_index'], 140)])

        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/heart.png"), (80, 80)),
                                (170, 10))
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Blocks/дерево/0.jpg"), (50, 50)),
                                (200, 105))
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Shell/шар.jpg"), (50, 50)),
                                (350, 105))
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/алмаз.png"), (50, 50)),
                                (500, 105))
        self.parent.create_text(f''':{len(self.client.player['block'])}''', 40, (250, 100), (0, 0, 0),
                                (200, 100, 50))
        self.parent.create_text(f''': {len(self.client.player['shells'])}''', 40, (400, 100), (0, 0, 0),
                                (200, 100, 50))
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/steve.png"), (150, 150)),
                                (10, 10))
        self.parent.create_text(f''': {self.client.player['score']}''', 40, (550, 100), (0, 0, 0),
                                (200, 100, 50))

        self.pos_cell_x = self.client.pos_cell_x
        self.pos_cell_y = self.client.pos_cell_y


        pos_x = -self.client.drawing['pos_player'] + 400 if self.client.drawing['pos_player'] > 400 else 0
        pos_x = -4800 if pos_x < -4800 else pos_x
        self.pos_x = pos_x
        for i in range(len(self.client.drawing)):
            if str(i) in self.client.drawing.keys():
                if self.client.drawing[str(i)]['img']:
                    try:
                        self.parent.screen.blit(
                            pygame.transform.scale(pygame.image.load(self.client.drawing[str(i)]['img']),
                                                   self.client.drawing[str(i)]['size']),
                            (self.client.drawing[str(i)]['pos'][0] + pos_x, self.client.drawing[str(i)]['pos'][1] +
                             160))
                    except:
                        pass
        if self.client.player['heart'] <= 0:
            self.close_game('game_lose_online')
        if self.client.player['win']:
            self.close_game('game_win_online')

    def close_game(self, name):
        for group in groups:
            group.clear()
        all_sprites.clear()
        self.parent.restart_surface(name)


class Menu_Game_Online:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((600, 450), (400, 100), 'Зайти в игру', 0, lambda:
        self.parent.restart_surface('game_online'))
        self.parent.create_textbox((500, 300), (600, 100))
        self.parent.create_button((50, 25), (175, 75), 'Выйти', 0, lambda: self.parent.restart_surface('menu'))

    def listen(self):
            self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game_Menu.jpg"),
                                                           (1600, 1000)), (0, 0))
            self.parent.create_text(f'Онлайн Режим', 60, (450, 50), (0, 0, 0), (200, 100, 50))
            self.parent.create_text(f'Пароль комнаты', 40, (530, 200), (0, 0, 0), (200, 100, 50))

    def listen_event(self, event):
        pass

class Game_Lose_Online:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((650, 400), (300, 150), 'Выход', 0,
                                  lambda: self.parent.restart_surface('game_online_menu'))

    def listen(self):
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game_Menu.jpg"),
                                                       (1600, 1000)),
                                (0, 0))
        self.parent.create_text(f'Вы проиграли', 60, (500, 300), (0, 0, 0), (200, 100, 50))

    def listen_event(self, event):
        pass


class Game_Win_Online:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((650, 400), (300, 150), 'Выход', 0,
                                  lambda: self.parent.restart_surface('game_online_menu'))

    def listen(self):
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game_Menu.jpg"),
                                                       (1600, 1000)),
                                (0, 0))
        self.parent.create_text(f'Вы выиграли', 60, (500, 300), (0, 0, 0), (200, 100, 50))

    def listen_event(self, event):
        pass
