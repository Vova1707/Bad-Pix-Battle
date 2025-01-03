import pygame
import numpy as np
import random

import pygame

# группы спрайтов
all_sprites = pygame.sprite.Group()


base_cells = pygame.sprite.Group()
players = pygame.sprite.Group()
breaking_block = pygame.sprite.Group()
other_object = pygame.sprite.Group()
shell = pygame.sprite.Group()
breaking_shell = pygame.sprite.Group()


# Общие параметры
dict_cells_group = {
                    'камень': 0,
                    'дерево': 4,
                    '1': 3,
                    '2': 3,
                    '3': 3,
                    '4': 3
                    }

dict_shell_group = {'стрела': (50, 20),
                    'шар': (100, 30)}

obj_for_kart = {1: [{'img': 'торговая_лавка.png', 'pos': (300, 390), 'size': (400, 250)}], 2: []}



class Board:
    def __init__(self, player, kart):
        self.board_kart = np.array([list(map(int, list(i.replace('\n', '')))) for i in open(
            f'Kart/kart_{kart}.txt').readlines()])
        self.cell_size = 40
        self.set_view()
        self.main_player = player
        self.pos_cell_x = False
        self.pos_cell_y = False


    def set_view(self):
        self.game_screen = pygame.Surface((6400, 860))
        self.game_screen.fill((255, 255, 255))
        self.desk = []
        for i in range(len(self.board_kart)):
            self.desk.append([])
            for j in range(len(self.board_kart[i])):
                if self.board_kart[i][j] == 1:
                    color = 'камень'
                else:
                    color = False
                self.desk[-1].append(Block((40 * j, 40 * i), color))

    def get_cell(self, mouse_pos):
        player = self.main_player
        y, x = self.celling(mouse_pos)
        if y > 0 and x > 0 and y < 1000 and x < 6400 and abs(player.rect.x - x) < 200 and abs(player.rect.y - y) < 200:
            y = y // 40
            x = x // 40
            rect_s = pygame.Rect(x * 40, y * 40, 40, 40)
            if not player.rect.colliderect(rect_s):
                self.pos_cell_x = x
                self.pos_cell_y = y
                return (y, x)
            else:
                return False
        else:
            return False


    def celling(self, mouse_pos):
        i = self.main_player.rect.x - 400 if self.main_player.rect.x - 400 > 0 else 0
        i = 4800 if i > 4800 else i
        x = mouse_pos[0] + i
        y = mouse_pos[1] - 160
        return (y, x)


    def click(self, mouse_pos, func=None):
        cell = self.get_cell(mouse_pos)
        if cell:
            i, j = cell
            if func == 'add':
                if self.board_kart[i][j] == 0 and len(self.main_player.player['block']) > 0:
                    block = self.main_player.next_block()
                    self.desk[i][j].create_block(block, dict_cells_group[block])
                    self.board_kart[i][j] = -dict_cells_group[block]
            elif func == 'delete':
                if self.board_kart[i][j] not in [0, 1]:
                    self.desk[i][j].break_block(1)
                    self.board_kart[i][j] += 1




class Block(pygame.sprite.Sprite):
    def __init__(self, pos, image=False):
        super().__init__(all_sprites)
        pygame.sprite.Sprite.__init__(self)

        self.param = {
            'forse': 0,
            'image': image,
            'pos': pos,
        }

        if image:
            self.update_cell()
            self.add(base_cells)
        else:
            self.image = pygame.Surface((40, 40))
            pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 40, 40))

        self.rect = pygame.Rect(pos[0], pos[1], 40, 40)

    def create_block(self, img, forse):
        self.param['image'] = img
        self.add(base_cells)
        self.param['forse'] = forse
        self.update_cell()

    def break_block(self, score):
        self.param['forse'] -= score
        print(self.param['forse'])
        if self.param['forse'] <= 0:
            base_cells.remove(self)
            self.create_breaking_block()
            self.image = pygame.Surface((40, 40))
            self.param['image'] = None
            self.param['forse'] = 0
            pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 40, 40))
        else:
            self.update_cell()

    def update_cell(self):
        img = self.param['image'] + '/' + str(self.param['forse'])
        self.image = pygame.transform.scale(pygame.image.load(f'Images/Blocks/{img}.jpg'), (40, 40))

    def create_breaking_block(self):
        Breaking_Block(self.param['pos'], self.param['image'])



class Breaking_Block(pygame.sprite.Sprite):
    def __init__(self, pos, image=False):
        super().__init__(all_sprites)
        pygame.sprite.Sprite.__init__(self)
        self.add(breaking_block)
        self.param = {
            'image': image
        }
        img = self.param['image'] + '/' + '0'
        self.image = pygame.transform.scale(pygame.image.load(f'Images/Blocks/{img}.jpg'), (30, 30))
        self.rect = pygame.Rect(pos[0], pos[1], 40, 40)

    def update(self):
        self.move(0, 10)

    def move(self, x, y):
        rect_x = self.rect.move(x, 0)
        rect_y = self.rect.move(0, y)
        check_x = list(filter(lambda cell: rect_x.colliderect(cell.rect), base_cells))
        check_y = list(filter(lambda cell: rect_y.colliderect(cell.rect), base_cells))
        if rect_x.x < 0 or check_x or rect_x.x > 6350:
            x = 0
        if check_y or rect_y.y < 0:
            y = 0
        self.rect = self.rect.move(x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self, id):

        # группы
        super().__init__(all_sprites)
        pygame.sprite.Sprite.__init__(self)
        self.add(players)

        pos = (id * 500, 200)
        self.player = {
            # Движение
             'id': id,
             'left': False,
             'right': False,
             'up': False,
             'cadr': 0,
            # параметры
            'score': 0,
            'heart': 100,
            'block': ['дерево'] * 20,
            'shells': ['шар'] * 20,
            'inventory': []
        }
        self.image = pygame.transform.scale(pygame.image.load(f"Images/Players/player_1/player_1_0_0.png"), (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.polog = 0

    def next_block(self):
        if self.player['block']:
            block = self.player['block'][0]
            self.player['block'] = self.player['block'][1::]
            return block
        else:
            return False

    def add_block(self, block):
        self.player['block'] = self.player['block'] + [block]


    def update(self):
        for i in breaking_block:
            if i.rect.colliderect(self.rect):
                self.add_block(i.param['image'])
                breaking_block.remove(i)
                i.kill()

        if self.player['left']:
            self.move(-10, 0)
            self.player['cadr'] = (self.player['cadr'] + 1) % 4 if (self.player['cadr'] + 1) % 4 else 1
        elif self.player['right']:
            self.move(10, 0)
            self.player['cadr'] = (self.player['cadr'] + 1) % 4 if (self.player['cadr'] + 1) % 4 else 1

        rect_x = self.rect.move(0, 10)
        if self.player['up'] and list(filter(lambda cell: rect_x.colliderect(cell.rect), base_cells)):
            self.move(0, -100)
        one = self.player['id']
        two = 2 if self.player['right'] else 1 if self.player['left'] else 0
        three = 0 if not two else self.player['cadr']
        self.image = pygame.transform.scale(pygame.image.load(f"Images/Players/player_{one}/player_{one}_{two}_{three}.png"), (50, 100))
        self.move(0, 10)


    def moving_player(self, napravlenie, znachenie):
        self.player[napravlenie] = znachenie

    def move(self, x, y):
        rect_x = self.rect.move(x, 0)
        rect_y = self.rect.move(0, y)
        check_x = list(filter(lambda cell: rect_x.colliderect(cell.rect), base_cells))
        check_y = list(filter(lambda cell: rect_y.colliderect(cell.rect), base_cells))
        if rect_x.x < 0 or check_x or rect_x.x > 6350:
            x = 0
        if check_y or rect_y.y > 700 or rect_y.y < 0:
            y = 0
        self.rect = self.rect.move(x, y)


    def shoot(self, pos):
        shell = self.next_shell()
        if shell:
            k = (self.rect.y - pos[0]) / (self.rect.x - pos[1])
            b = pos[0] - k * pos[1]
            if pos[1] < self.rect.x:
                napravlenie =  -1
            else:
                napravlenie = 1

            Shell(self.rect.x, self.rect.y, k, b, napravlenie, shell, dict_shell_group[shell][0], dict_shell_group[shell][1])


    def next_shell(self):
        if self.player['shells']:
            block = self.player['shells'][0]
            self.player['block'] = self.player['block'][1::]
            return block
        else:
            return False



class Shell(pygame.sprite.Sprite):
    def __init__(self, x, y, k, b, napr, shell, v, hp_delete):
        super().__init__(all_sprites)
        pygame.sprite.Sprite.__init__(self)
        self.add(players)


        self.image = pygame.transform.scale(pygame.image.load(f"Images/Shell/{shell}.jpg"), (50, 50))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.napr = napr
        self.k = k
        self.b = b

        self.v = v
        self.hp = hp_delete

    def update(self):
        self.rect.x = self.rect.x + self.v * self.napr
        self.rect.y = self.rect.x * self.k + self.b



class Object(pygame.sprite.Sprite):
    def __init__(self, img, pos, size, is_breaking=False):
        self.param = {'image': img,
                      'pos': pos,}
        super().__init__(all_sprites)
        pygame.sprite.Sprite.__init__(self)
        self.add(other_object)

        self.image = pygame.transform.scale(pygame.image.load(f"Images/Object/{img}"), size)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]




class Menu_Game_Offline:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((50, 200), (300, 150), '1', 0, lambda: self.parent.restart_surface('level_1'))
        self.parent.create_button((450, 200), (300, 150), '2', 0, lambda: self.parent.restart_surface('level_1'))
        self.parent.create_button((850, 200), (300, 150), '3', 0, lambda: self.parent.restart_surface('level_1'))
        self.parent.create_button((1250, 200), (300, 150), '4', 0, lambda: self.parent.restart_surface('level_1'))
        self.parent.create_button((50, 400), (300, 150), '5', 0, lambda: self.parent.restart_surface('level_1'))
        self.parent.create_button((725, 800), (150, 75), 'Выйти', 0, lambda: self.parent.restart_surface('menu'))

    def listen(self):
            self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game_Menu.jpg"), (1600, 1000)), (0, 0))
            self.parent.create_text(f'Уровни', 60, (600, 50), (0, 0, 0), (200, 100, 50))

    def listen_event(self, event):
        pass


class Game_Offline:
    def __init__(self, parent, kart):
        self.parent = parent
        self.screen = parent.screen
        self.kart = kart
        self.comands = {
            pygame.KEYDOWN:
                {(pygame.K_f, 10): lambda: self.main_player.shoot(self.pos),
                 (pygame.K_RIGHT, pygame.K_d): lambda: self.main_player.moving_player('right', True),
                 (pygame.K_LEFT, pygame.K_a): lambda: self.main_player.moving_player('left', True),
                 (pygame.K_UP, pygame.K_s): lambda: self.main_player.moving_player('up', True),
                 },
            pygame.KEYUP:
                {(pygame.K_RIGHT, pygame.K_d): lambda: self.main_player.moving_player('right', False),
                 (pygame.K_LEFT, pygame.K_a): lambda: self.main_player.moving_player('left', False),
                 (pygame.K_UP, pygame.K_s): lambda: self.main_player.moving_player('up', False),
                 },
        }

    def create_widgets(self):
        self.main_player = Player(1)
        self.board = Board(self.main_player, self.kart)
        self.parent.create_button((1300, 0), (300, 150), 'Выйти', 0, self.close_game)
        self.game_screen = self.board.game_screen
        self.create_other_obj()

    def create_other_obj(self):
        for i in obj_for_kart[self.kart]:
            Object(i['img'], i['pos'], i['size'])



    def listen_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.board.get_cell(event.pos)
            self.pos = self.board.celling(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.board.click(event.pos, 'add' if event.button == 1 else 'delete' if event.button == 3 else False)
            self.game_screen = self.board.game_screen
        if event.type in self.comands.keys():
            key = list(filter(lambda d: event.key in d, self.comands[event.type].keys()))
            if key:
                self.comands[event.type][key[0]]()

    def listen(self):
        #self.screen.fill((255, 255, 255))
        self.parent.create_text(f'''Жизни: {self.main_player.player['heart']}''', 40, (50, 50), (0, 0, 0),
                                (200, 100, 50))
        self.parent.create_text(f'''Блоков: {len(self.main_player.player['block'])}''', 40, (50, 100), (0, 0, 0), (200, 100, 50))


        all_sprites.update()

        self.board.game_screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game.jpg"), (6400, 1000)), (0, 0))
        other_object.draw(self.board.game_screen)
        base_cells.draw(self.board.game_screen)
        breaking_block.draw(self.board.game_screen)
        players.draw(self.board.game_screen)



        if self.board.pos_cell_x and self.board.pos_cell_y and abs(self.main_player.rect.x - self.board.pos_cell_x * 40) < 200 and abs(self.main_player.rect.y - self.board.pos_cell_y * 40) < 200:
            pygame.draw.rect(self.board.game_screen, (255, 255, 255), pygame.Rect(self.board.pos_cell_x * 40, self.board.pos_cell_y * 40, 4, 40))
            pygame.draw.rect(self.board.game_screen, (255, 255, 255), pygame.Rect(self.board.pos_cell_x * 40, self.board.pos_cell_y * 40, 40, 4))
            pygame.draw.rect(self.board.game_screen, (255, 255, 255),
                             pygame.Rect((self.board.pos_cell_x + 1) * 40, self.board.pos_cell_y * 40, 4, 40))
            pygame.draw.rect(self.board.game_screen, (255, 255, 255),
                             pygame.Rect(self.board.pos_cell_x * 40, (self.board.pos_cell_y + 1) * 40, 44, 4))

        else:
            self.board.pos_cell_x = 0
            self.board.pos_cell_y = 0


        pos_x = -self.main_player.rect.x + 400 if self.main_player.rect.x > 400 else 0
        pos_x = -4800 if pos_x < -4800 else pos_x
        self.screen.blit(self.board.game_screen, (pos_x, 160))


    def close_game(self):
        for i in all_sprites: i.kill()
        self.parent.restart_surface('menu')