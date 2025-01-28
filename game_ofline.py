import numpy as np
import datetime
import pygame

# группы спрайтов(небольшие прототипы для начала игры)
all_sprites = []
base_cells = []
players = []
breaking_block = []
other_object = []
shells = []
breaking_shells = []
groups = [other_object, base_cells, breaking_block, players, shells, breaking_shells]


# группы
# Нет обсидиана и игровых блоков
dict_cells_group = {
                    'камень': 0,
                    'дерево': 4,
                    '1': 3,
                    '2': 3,
                    '3': 3,
                    '4': 3
                    }
# Нет снежка
dict_shell_group = {'шар': (30, 30),
                    'снежок': (25, 25)}

j = {'block': 5}
# Объекты карты
obj_for_kart = {1: {'object': [{'img': 'генератор.jpg', 'pos': (1200, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_block'},
                               {'img': 'портал.png', 'pos': (3000, 440), 'size': (200, 250), 'funct': 'portal'},
                               {'img': '1.png', 'pos': (600, 550), 'size': (40, 80), 'funct': 'medal'}],
                    'enemy': [],
                    'task': {'block': 3}},

                2: {'object': [{'img': 'генератор.jpg', 'pos': (200, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_block'},
                               {'img': 'генератор.jpg', 'pos': (400, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_shell'},
                               {'img': 'портал.png', 'pos': (3000, 440),
                                'size': (200, 250), 'funct': 'portal'},
                               {'img': '2.png', 'pos': (2200, 550),
                                'size': (40, 80), 'funct': 'medal'}],
                    'enemy': [{'pos': (2000, 520), 'atak': False}],
                    'task': {'block': 5, 'shell': 1, 'enemy': 1}},

                3: {'object': [{'img': 'генератор.jpg', 'pos': (300, 620),
                                'size': (100, 100), 'funct': 'generate_breaking_shell'},
                               {'img': 'генератор.jpg', 'pos': (600, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_block'},
                               {'img': 'генератор.jpg', 'pos': (2400, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_shell'},
                               {'img': 'торговая_лавка.png', 'pos': (2500, 390), 'size': (400, 250),
                                'funct': 'generate_inventory'},
                               {'img': 'генератор.jpg', 'pos': (4200, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_block'},
                               {'img': 'портал.png', 'pos': (5000, 440), 'size': (200, 250), 'funct': 'portal'},
                               {'img': '3.png', 'pos': (2200, 550), 'size': (40, 80), 'funct': 'medal'}],
                    'enemy': [{'pos': (600, 500), 'atak': False}, {'pos': (2800, 520), 'atak': True}],
                    'task': {'shell': 3, 'enemy': 2, 'gold_apple': 1}},


                4: {'object': [{'img': 'генератор.jpg', 'pos': (700, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_block'},
                               {'img': 'генератор.jpg', 'pos': (4000, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_shell'},
                               {'img': 'генератор.jpg', 'pos': (2730, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_block'},
                               {'img': 'торговая_лавка.png', 'pos': (2300, 390), 'size': (400, 250),
                                'funct': 'generate_inventory'},
                               {'img': 'генератор.jpg', 'pos': (4300, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_block'},
                               {'img': 'портал.png', 'pos': (5300, 440), 'size': (200, 250), 'funct': 'portal'},
                               {'img': '4.png', 'pos': (2900, 550), 'size': (40, 80), 'funct': 'medal'}],
                    'enemy': [{'pos': (2200, 500), 'atak': True}, {'pos': (4200, 500), 'atak': True}],
                    'task': {'enemy': 2, 'gold_apple': 2, 'shell': 3, 'block': 10}},

                5: {'object': [{'img': 'генератор.jpg', 'pos': (700, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_block'},
                               {'img': 'торговая_лавка.png', 'pos': (200, 390), 'size': (400, 250),
                                'funct': 'generate_inventory'},
                               {'img': 'генератор.jpg', 'pos': (2000, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_shell'},
                               {'img': 'генератор.jpg', 'pos': (2700, 620), 'size': (100, 100),
                                'funct': 'generate_breaking_block'},
                               {'img': 'портал.png', 'pos': (6000, 440), 'size': (200, 250), 'funct': 'portal'},
                               {'img': '5.png', 'pos': (2900, 550), 'size': (40, 80), 'funct': 'medal'}],
                    'enemy': [{'pos': (800, 500), 'atak': True}, {'pos': (2500, 500), 'atak': True},
                              {'pos': (4000, 500), 'atak': True}],
                'task': {'enemy': 3, 'gold_apple': 2, 'shell': 5, 'block': 10}}}


class Board:
    def __init__(self, player=False, kart=False):
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

    def get_cell(self, mouse_pos, player=False):
        if not player:
            player = self.main_player
        y, x = self.celling(mouse_pos, player)
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

    def celling(self, mouse_pos, player=False):
        if not player:
            player = self.main_player
        i = player.rect.x - 400 if player.rect.x - 400 > 0 else 0
        i = 4800 if i > 4800 else i
        x = mouse_pos[0] + i
        y = mouse_pos[1] - 160
        return (y, x)

    def click(self, mouse_pos, func=None, player=False):
        if not player:
            player = self.main_player
        cell = self.get_cell(mouse_pos, player)
        if cell:
            i, j = cell
            if func == 'add':
                if self.board_kart[i][j] == 0 and len(player.player['block']) > 0:
                    # звук добавления блока
                    hit = pygame.mixer.Sound('music/add_block.mp3')
                    hit.play()
                    block = player.next_block()
                    self.desk[i][j].create_block(block, dict_cells_group[block])
                    self.board_kart[i][j] = -dict_cells_group[block]
            elif func == 'delete':
                if self.board_kart[i][j] not in [0, 1]:
                    self.desk[i][j].break_block(1)
                    self.board_kart[i][j] += 1


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, image=False):
        pygame.sprite.Sprite.__init__(self)

        all_sprites.append(self)
        self.group = base_cells
        self.die = False

        self.param = {
            'forse': 0,
            'image': image,
            'pos': pos,
        }

        if image:
            self.update_cell()
            create(self)
        else:
            self.image = pygame.Surface((40, 40))
            pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 40, 40))

        self.rect = pygame.Rect(pos[0], pos[1], 40, 40)

    def create_block(self, img, forse=False):
        self.param['image'] = img
        create(self)
        self.param['forse'] = forse
        self.update_cell()

    def break_block(self, score):
        if self.param['image'] != 'камень':
            self.param['forse'] -= score
            # звук разбития блока
            hit = pygame.mixer.Sound('music/delete_block.mp3')
            hit.set_volume(0.5)
            hit.play()
            if self.param['forse'] <= 0:
                self.die = True
                self.create_breaking_block()
                self.image = pygame.Surface((40, 40))
                self.param['image'] = None
                self.img_path = False
                self.param['forse'] = 0
                pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 40, 40))
            else:
                self.update_cell()

    def update_cell(self):
        img = self.param['image'] + '/' + str(self.param['forse'])
        self.img_path = f'Images/Blocks/{img}.jpg'
        self.image = pygame.transform.scale(pygame.image.load(f'Images/Blocks/{img}.jpg'), (40, 40))

    def create_breaking_block(self):
        Breaking_Block(self.param['pos'], self.param['image'])


class Breaking_Block(pygame.sprite.Sprite):
    def __init__(self, pos, image=False):
        pygame.sprite.Sprite.__init__(self)
        self.group = breaking_block
        all_sprites.append(self)
        self.die = False
        create(self)

        self.param = {
            'image': image
        }
        img = self.param['image'] + '/' + '0'
        self.img_path = f'Images/Blocks/{img}.jpg'
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, player, atak):
        pygame.sprite.Sprite.__init__(self)
        all_sprites.append(self)
        self.group = players
        self.die = False
        create(self)

        self.player = {
            'heart': 100,
            'main_player': player,
            'atak': atak,
            'lose': False
        }
        self.img_path = f"Images/Players/player_2/player_2_0_0.png"
        self.image = pygame.transform.scale(pygame.image.load(f"Images/Players/player_2/player_2_0_0.png"),
                                            (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.time = datetime.datetime.now().time()

    def update(self):
        if not self.die:
            self.move(0, 10)
            for shell in filter(lambda f: f.rect.colliderect(self.rect) and f.player != self, shells):
                shell.die = True
                shell.kill()
                self.player['heart'] -= shell.hp
            if self.player['atak']:
                if abs(self.rect.x - self.player['main_player'].rect.x) <= 500 and abs(
                        self.rect.y - self.player['main_player'].rect.y) <= 200:
                    if datetime.datetime.now().time().second - self.time.second >= 1:
                        self.shoot((self.player['main_player'].rect.y, self.player['main_player'].rect.x))
                        self.time = datetime.datetime.now().time()
            self.check_kill()

    def check_kill(self):
        if self.rect.y > 900:
            self.player['heart'] = 0
        if self.player['heart'] <= 0:
            self.die = True
            # звук смерти врага
            hit = pygame.mixer.Sound('music/die_enemy.mp3')
            hit.play()
            player = list(filter(lambda player: isinstance(player, Player), players))[0]
            player.player['score'] += 1
            player.update_task('enemy')

    def shoot(self, pos):
        shell = 'шар'
        if shell:
            n = (self.rect.x - pos[1])
            if n != 0:
                k = (self.rect.y - pos[0]) / n
                b = pos[0] - k * pos[1]
                if pos[1] < self.rect.x:
                    napravlenie = -1
                else:
                    napravlenie = 1
                # звук выстрела
                hit = pygame.mixer.Sound('music/shoot.mp3')
                hit.play()
                Shell(self, k, b, napravlenie, shell, dict_shell_group[shell][0], dict_shell_group[shell][1])

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
        pygame.sprite.Sprite.__init__(self)
        all_sprites.append(self)
        self.group = players
        self.die = False
        create(self)

        pos = (300, 520)
        self.player = {
             'id': id,
             'left': False,
             'right': False,
             'up': False,
             'run': False,
             'speed': 1000,
             'cadr': 0,
             'score': 0,
             'heart': 100,
             'block': ['дерево'] * 20,
             'shells': ['шар'] * 5,
             'inventory': [],
             'inventory_index': 0,
             'win': False,
             'task': {},
             'medal': False
        }
        self.img_path = "Images/Players/player_2/player_2_0_0.png"
        self.image = pygame.transform.scale(pygame.image.load(f"Images/Players/player_1/player_1_0_0.png"),
                                            (50, 100))
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

    def add_obj(self, group, obj):
        self.player[group] = self.player[group] + [obj]
        # звук добавления предмета в инвентарь
        hit = pygame.mixer.Sound('music/add_breaking.wav')
        hit.play()

    def update_task(self, key):
        if key in self.player['task'].keys():
            self.player['task'][key] = max(0, self.player['task'][key] - 1)

    def choice_inventory(self):
        index = self.player['inventory_index']
        # звук поедания яблока
        hit = pygame.mixer.Sound('music/eat_apple.wav')
        hit.play()
        inventory = self.player['inventory']
        if index < len(inventory):
            if inventory[index] == 'Золотое_Яблоко.png':
                self.player['heart'] = min(100, self.player['heart'] + 20)
                del self.player['inventory'][index]
                self.player['inventory'].insert(index, False)

    def update(self):
        for break_block in filter(lambda f: f.rect.colliderect(self.rect), breaking_block):
            self.add_obj('block', break_block.param['image'])
            self.update_task('block')
            break_block.die = True

        for shell in filter(lambda f: f.rect.colliderect(self.rect) and f.player != self, shells):
            shell.die = True
            self.player['heart'] -= shell.hp

        for break_shell in filter(lambda f: f.rect.colliderect(self.rect), breaking_shells):
            self.add_obj('shells', break_shell.param['image'])
            self.update_task('shell')
            break_shell.die = True

        v = 0
        if self.player['run']:
            v = 10 if self.player['speed'] else v
            self.player['speed'] = max(0, self.player['speed'] - 50)
        else:
            self.player['speed'] = min(1000, self.player['speed'] + 20)

        if self.player['left']:
            self.move(-(10 + v), 0)
            self.player['cadr'] = (self.player['cadr'] + 1) % 4 if (self.player['cadr'] + 1) % 4 else 1
        elif self.player['right']:
            self.move(10 + v, 0)
            self.player['cadr'] = (self.player['cadr'] + 1) % 4 if (self.player['cadr'] + 1) % 4 else 1

        rect_x = self.rect.move(0, 10)
        if self.player['up'] and list(filter(lambda cell: rect_x.colliderect(cell.rect), base_cells)):
            self.move(0, -100)
        one = self.player['id']
        two = 2 if self.player['right'] else 1 if self.player['left'] else 0
        three = 0 if not two else self.player['cadr']
        self.img_path = f"Images/Players/player_{one}/player_{one}_{two}_{three}.png"
        self.image = pygame.transform.scale(pygame.image.load(f"Images/Players/player_{one}/" +
                                                              f"player_{one}_{two}_{three}.png"), (50, 100))
        self.move(0, 10)
        self.check_kill()

    def check_kill(self):
        if self.rect.y > 900:
            self.player['heart'] = 0
        if self.player['heart'] <= 0:
            self.die = True

    def moving_player(self, napravlenie, znachenie):
        self.player[napravlenie] = znachenie

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

    def update_inventory_index(self, score):
        self.player['inventory_index'] += score
        self.player['inventory_index'] = 0 if self.player['inventory_index'] > 3 else 3 if (
                self.player['inventory_index'] < 0) else self.player['inventory_index']

    def shoot(self, pos):
        shell = self.next_shell()
        if shell:
            k = (self.rect.y - pos[0]) / (self.rect.x - pos[1])
            b = pos[0] - k * pos[1]
            if pos[1] < self.rect.x:
                napravlenie = -1
            else:
                napravlenie = 1
            # звук выстрела
            hit = pygame.mixer.Sound('music/shoot.mp3')
            hit.play()
            Shell(self, k, b, napravlenie, shell, dict_shell_group[shell][0], dict_shell_group[shell][1])

    def next_shell(self):
        if self.player['shells']:
            block = self.player['shells'][0]
            self.player['shells'] = self.player['shells'][1::]
            return block
        else:
            return False


class Shell(pygame.sprite.Sprite):
    def __init__(self, player, k, b, napr, shell, v, hp_delete):
        pygame.sprite.Sprite.__init__(self)
        all_sprites.append(self)
        self.group = shells
        self.die = False
        create(self)
        self.img_path = f"Images/Shell/{shell}.jpg"
        self.image = pygame.transform.scale(pygame.image.load(f"Images/Shell/{shell}.jpg"), (30, 30))
        self.rect = self.image.get_rect()

        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.napr = napr
        self.k = k
        self.b = b

        self.v = v
        self.hp = hp_delete

        self.player = player

    def update(self):
        if not self.die:
            self.rect.x = self.rect.x + self.v * self.napr
            self.rect.y = self.rect.x * self.k + self.b
            check = list(filter(lambda cell: self.rect.colliderect(cell.rect), base_cells))
            if check:
                check[0].break_block(self.hp // 20)
                self.die = True


class Breaking_Shell(pygame.sprite.Sprite):
    def __init__(self, pos, image=False):
        pygame.sprite.Sprite.__init__(self)
        all_sprites.append(self)
        self.group = breaking_shells
        self.die = False
        create(self)
        self.param = {
            'image': image
        }
        img = self.param['image']
        self.image = pygame.transform.scale(pygame.image.load(f'Images/Shell/{img}.jpg'), (30, 30))
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


class Object(pygame.sprite.Sprite):
    def __init__(self, img, pos, size, funct, is_breaking=False):
        self.param = {'image': img,
                      'pos': pos}
        pygame.sprite.Sprite.__init__(self)
        all_sprites.append(self)
        self.group = other_object
        self.die = False
        create(self)
        self.img_path = f"Images/Object/{img}"
        self.image = pygame.transform.scale(pygame.image.load(f"Images/Object/{img}"), size)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.start = 0
        self.funct_for_object = {'generate_breaking_block': lambda: self.generate_breaking_block(),
                                 'generate_breaking_shell': lambda: self.generate_breaking_shell(),
                                 'inventory': lambda: self.inventoty(),
                                 'generate_inventory': lambda: self.generate_inventory(),
                                 'portal': lambda: self.portal(),
                                 'medal': lambda: self.medal()}
        self.funct = funct

    def generate_breaking_block(self):
        if self.start == 0:
            self.time = datetime.datetime.now().time()
            self.start = 1
        else:
            if datetime.datetime.now().time().second - self.time.second >= 3:
                # звук подбора
                hit = pygame.mixer.Sound('music/add_breaking.wav')
                hit.play()
                Breaking_Block((self.rect.x + self.rect.w // 2, self.rect.y - 50), 'дерево')
                self.time = datetime.datetime.now().time()

    def generate_breaking_shell(self):
        if self.start == 0:
            self.time = datetime.datetime.now().time()
            self.start = 1
        else:
            if datetime.datetime.now().time().second - self.time.second >= 3:
                # звук подбора
                hit = pygame.mixer.Sound('music/add_breaking.wav')
                hit.play()
                Breaking_Shell((self.rect.x + self.rect.w // 2, self.rect.y - 50), 'шар')
                self.time = datetime.datetime.now().time()

    def generate_inventory(self):
        if self.start == 0:
            self.time = datetime.datetime.now().time()
            self.start = 1
        else:
            if datetime.datetime.now().time().second - self.time.second >= 10:
                Object('Золотое_Яблоко.png', (self.rect.x + self.rect.w // 2, self.rect.y - 20), (30, 30),
                       'inventory')
                self.time = datetime.datetime.now().time()

    def inventoty(self):
        self.move(0, 10)

        player = list(filter(lambda player: self.rect.colliderect(player.rect) and isinstance(player, Player), players))
        if player and not self.start:
            if len(player[0].player['inventory']) < 4:
                player[0].player['inventory'].append(self.param['image'])
                player[0].update_task('gold_apple')
                self.die = True
                self.start = 1
            elif False in player[0].player['inventory']:
                player[0].player['inventory'].insert(player[0].player['inventory'].index(False), self.param['image'])
                del player[0].player['inventory'][player[0].player['inventory'].index(False)]
                player[0].update_task('gold_apple')
                self.die = True
                self.start = 1

    def portal(self):
        player = list(filter(lambda player:
                             self.rect.colliderect(player.rect) and isinstance(player, Player)
                             and player.rect.x - self.rect.x > 50, players))
        if player:
            if not list(filter(lambda task: task, player[0].player['task'].values())): player[0].player['win'] = True

    def medal(self):
        player = list(filter(lambda player: self.rect.colliderect(player.rect) and isinstance(player, Player), players))
        if player:
            if not self.die:
                # звук медали
                hit = pygame.mixer.Sound('music/add_medal.mp3')
                hit.play()
                player[0].player['medal'] = self.img_path
            self.die = True

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

    def update(self):
        self.funct_for_object[self.funct]()


def create(obj):
    if obj not in obj.group:
        obj.group.append(obj)


def check_delete(obj):
    if obj.die and obj in obj.group:
        del obj.group[obj.group.index(obj)]


class Game_Offline:
    def __init__(self, parent, kart):
        self.parent = parent
        self.screen = parent.screen
        self.kart = kart

        self.medaling = False

        self.comands = {
            pygame.KEYDOWN:
                {(pygame.K_f,): lambda: self.main_player.shoot(self.pos),
                 (pygame.K_e,): lambda: self.main_player.choice_inventory(),
                 (pygame.K_d,): lambda: self.main_player.moving_player('right', True),
                 (pygame.K_s,): lambda: self.main_player.moving_player('run', True),
                 (pygame.K_a,): lambda: self.main_player.moving_player('left', True),
                 (pygame.K_w,): lambda: self.main_player.moving_player('up', True),
                 (pygame.K_RIGHT,): lambda: self.main_player.update_inventory_index(1),
                 (pygame.K_LEFT,): lambda: self.main_player.update_inventory_index(-1),

                 },
            pygame.KEYUP:
                {(pygame.K_d,): lambda: self.main_player.moving_player('right', False),
                 (pygame.K_a,): lambda: self.main_player.moving_player('left', False),
                 (pygame.K_w,): lambda: self.main_player.moving_player('up', False),
                 (pygame.K_s,): lambda: self.main_player.moving_player('run', False),
                 },
        }
        self.passed = False

    def create_widgets(self):
        self.main_player = Player(1)
        self.board = Board(self.main_player, self.kart)
        self.parent.create_button((1400, 0), (200, 80), 'Выйти', 0, lambda: self.close_game('game_offline'))
        self.game_screen = self.board.game_screen
        self.create_other_obj()

    def create_other_obj(self):
        for i in obj_for_kart[self.kart]['object']:
            Object(i['img'], i['pos'], i['size'], i['funct'])

        for i in obj_for_kart[self.kart]['enemy']:
            Enemy(i['pos'], self.main_player, i['atak'])
        self.main_player.player['task'] = obj_for_kart[self.kart]['task'].copy()

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
        self.parent.screen.fill((196, 196, 196))
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/шкала.png"), (450, 120)),
                                (650, 0))

        pygame.draw.rect(self.parent.screen, (255, 0, 0), (210, 30, 400 *
                                                           (self.main_player.player['heart'] / 100) // 1, 40))
        pygame.draw.rect(self.parent.screen, (0, 0, 0), (210, 30, 400, 40), 5)

        if self.main_player.player['medal']:
            self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"{self.main_player.player['medal']}"),
                                                           (70, 120)),
                                    (1300, 0))
        pygame.draw.rect(self.parent.screen, (255, 255, 0),
                         (210, 70, 400 * (self.main_player.player['speed'] / 1000) // 1, 15))
        pygame.draw.rect(self.parent.screen, (0, 0, 0), (210, 70, 400, 15), 5)

        for i in range(len(self.main_player.player['inventory'])):
            if self.main_player.player['inventory'][i]:
                self.parent.screen.blit(pygame.transform.scale(
                    pygame.image.load(f"Images/Object/{self.main_player.player['inventory'][i]}"),
                    (70, 70)), (690 + i * 105, 25))

        pygame.draw.polygon(self.parent.screen, (0, 0, 0),
                            [(700 + 105 * self.main_player.player['inventory_index'], 140),
                             (725 + 105 * self.main_player.player['inventory_index'], 110),
                             (750 + 105 * self.main_player.player['inventory_index'], 140)])

        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/heart.png"), (80, 80)),
                                (170, 10))
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Blocks/дерево/0.jpg"), (50, 50)),
                                (200, 105))
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Shell/шар.jpg"), (50, 50)),
                                (350, 105))
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/алмаз.png"), (50, 50)),
                                (500, 105))
        self.parent.create_text(f''':{len(self.main_player.player['block'])}''', 40, (250, 100), (0, 0, 0),
                                (200, 100, 50))
        self.parent.create_text(f''': {len(self.main_player.player['shells'])}''', 40, (400, 100), (0, 0, 0),
                                (200, 100, 50))
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/steve.png"),
                                                       (150, 150)),
                                (10, 10))
        self.parent.create_text(f''': {self.main_player.player['score']}''', 40, (550, 100), (0, 0, 0),
                                (200, 100, 50))

        self.board.game_screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game.jpg"),
                                                           (6400, 1000)), (0, 0))

        score = 0
        for i in all_sprites[::-1]:
            check_delete(i)
        for group in groups:
            for obj in group[::-1]:
                check_delete(obj)
                score += 1

        pos_x = -self.main_player.rect.x + 400 if self.main_player.rect.x > 400 else 0
        pos_x = -4800 if pos_x < -4800 else pos_x
        for i in filter(lambda obj: obj.rect.right >= -pos_x and obj.rect.left <= -pos_x + 1600, all_sprites):
            i.update()
        for group in groups:
            for obj in filter(lambda obj: obj.rect.right >= -pos_x and obj.rect.left <= -pos_x + 1600, group):
                self.board.game_screen.blit(obj.image, obj.rect)

        if self.main_player.player['heart'] <= 0:
            # звук поражения
            hit = pygame.mixer.Sound('music/die_player.mp3')
            hit.play()
            self.close_game('game_lose_offline')
        if self.main_player.player['win']:
            # звук победы

            hit = pygame.mixer.Sound('music/next_level.mp3')
            hit.play()
            self.close_game('game_win_offline')

        if (self.board.pos_cell_x and self.board.pos_cell_y and
                abs(self.main_player.rect.x - self.board.pos_cell_x * 40) < 200 and
                abs(self.main_player.rect.y - self.board.pos_cell_y * 40) < 200):
            pygame.draw.rect(self.board.game_screen, (255, 255, 255),
                             pygame.Rect(self.board.pos_cell_x * 40, self.board.pos_cell_y * 40, 4, 40))
            pygame.draw.rect(self.board.game_screen, (255, 255, 255),
                             pygame.Rect(self.board.pos_cell_x * 40, self.board.pos_cell_y * 40, 40, 4))
            pygame.draw.rect(self.board.game_screen, (255, 255, 255),
                             pygame.Rect((self.board.pos_cell_x + 1) * 40, self.board.pos_cell_y * 40, 4, 40))
            pygame.draw.rect(self.board.game_screen, (255, 255, 255),
                             pygame.Rect(self.board.pos_cell_x * 40, (self.board.pos_cell_y + 1) * 40, 44, 4))

        else:
            self.board.pos_cell_x = 0
            self.board.pos_cell_y = 0

        pos_x = -self.main_player.rect.x + 400 if self.main_player.rect.x > 400 else 0
        pos_x = -4800 if pos_x < -4800 else pos_x

        f = pygame.font.Font('Font/DotGothic16-Regular.ttf', 40)
        text = f.render('Задачи', 1, (0, 0, 0))
        pygame.draw.rect(self.board.game_screen, (196, 196, 196), (-pos_x, 0, 260, 80 + 80 *
                                                                   len(obj_for_kart[self.kart]['task'].keys())))
        self.board.game_screen.blit(text, (-pos_x, 0))

        for task in obj_for_kart[self.kart]['task'].keys():
            if self.main_player.player['task'][task] == 0:
                color = (0, 255, 0)
            else:
                color = (0, 0, 0)
            f = pygame.font.Font('Font/DotGothic16-Regular.ttf', 40)
            text = f.render(f'{obj_for_kart[self.kart]['task'][task] - self.main_player.player['task'][task]}/'
                            f'{obj_for_kart[self.kart]['task'][task]}', 1, color)

            self.board.game_screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Task/{task}.png"),
                                                               (50, 50)),
                                        (-pos_x + 60, 80 + 80 *
                                         list(obj_for_kart[self.kart]['task'].keys()).index(task)))

            self.board.game_screen.blit(text,
                                        (-pos_x + 120,
                                         75 + 80 * list(obj_for_kart[self.kart]['task'].keys()).index(task)))
        self.screen.blit(self.board.game_screen, (pos_x, 160))

    def close_game(self, name):
        if name == 'game_win_offline':
            if not self.passed:
                self.parent.rating_user('levels')
                self.passed = False
            if not self.medaling and self.main_player.player['medal']:
                self.medaling = True
                self.parent.rating_user(f'm{self.kart}')
            self.parent.rating_user('almaz', self.main_player.player['score'])
        for group in groups:
            group.clear()
        all_sprites.clear()
        self.parent.restart_surface(name)


class Menu_Game_Offline:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((50, 200), (300, 150), '1', 0, lambda: self.parent.restart_surface('level_1'))
        self.parent.create_button((450, 200), (300, 150), '2', 0, lambda: self.parent.restart_surface('level_2'))
        self.parent.create_button((850, 200), (300, 150), '3', 0, lambda: self.parent.restart_surface('level_3'))
        self.parent.create_button((1250, 200), (300, 150), '4', 0, lambda: self.parent.restart_surface('level_4'))
        self.parent.create_button((50, 400), (300, 150), '5', 0, lambda: self.parent.restart_surface('level_5'))
        self.parent.create_button((50, 25), (175, 75), 'Выйти', 0, lambda: self.parent.restart_surface('menu'))

    def listen(self):
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game_Menu.jpg"),
                                                       (1600, 1000)), (0, 0))
        self.parent.create_text(f'Уровни', 60, (600, 50), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Это тренировочные игры. Победы не идут в рейтинг', 30, (55, 900), (255, 0, 0),
                                (200, 100, 50))

    def listen_event(self, event):
        pass


class Game_Lose_Offline:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((650, 400),
                                  (300, 150), 'Выход', 0, lambda: self.parent.restart_surface('game_offline'))
        self.screen_now = pygame.Surface((1600, 1000))
        self.screen_now.blit(self.parent.screen, (0, 0))
        red = pygame.Surface((1600, 1000))
        red.fill((255, 0, 0))
        red.set_alpha(200)
        self.screen_now.blit(red, (0, 0))

    def listen(self):
        self.parent.screen.blit(self.screen_now, (0, 0))
        self.parent.create_text(f'Вы проиграли', 60, (500, 300), (0, 0, 0), (200, 100, 50))

    def listen_event(self, event):
        pass


class Game_Win_Offline:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((650, 400),
                                  (300, 150), 'Выход', 0, lambda: self.parent.restart_surface('game_offline'))

    def listen(self):
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game_Menu.jpg"),
                                                       (1600, 1000)), (0, 0))
        self.parent.create_text(f'Вы выиграли', 60, (500, 300), (0, 0, 0), (200, 100, 50))

    def listen_event(self, event):
        pass