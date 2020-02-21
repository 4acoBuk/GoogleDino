import pygame
import os
import time
import random


def draw():
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (240, 219, 125), (0, 336, width, 500))
    pygame.draw.rect(screen, (117, 187, 253), (0, 0, width, 336))
    pygame.draw.line(screen, (83, 83, 83), (0, 336), (width, 336))
    maps.draw(screen)
    draw_record(draw_score())
    dino.draw(screen)
    barriers.draw(screen)
    effects.draw(screen)
    buttons.draw(screen)
    pygame.display.flip()


def draw_score():
    font = pygame.font.Font(None, 30)
    text = font.render(str(score // 4),
                       1, (83, 83, 83))
    text_x = width - text.get_width() - 20
    text_y = 250
    screen.blit(text, (text_x, text_y))
    return text.get_width()


def draw_record(w):
    font = pygame.font.Font(None, 30)
    text = font.render('HI: ' + str(record),
                       1, (83, 83, 83))
    text_x = width - text.get_width() - w - 50
    text_y = 250
    screen.blit(text, (text_x, text_y))


def update():
    maps.update()
    dino.update(keys)
    barriers.update(keys)
    effects.update()


def pause():
    Pause.change_image()
    draw()
    font = pygame.font.Font(None, 30)
    text1 = font.render("Игра стоит на паузе", 1, (83, 83, 83))
    text_x1 = width // 2 - text1.get_width() // 2
    text_y1 = height // 2 - text1.get_height() * 3 // 2 - 10
    screen.blit(text1, (text_x1, text_y1))
    pygame.display.flip()
    time.sleep(1)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if Quit.is_pressed(event):
                    return False
                if Pause.is_pressed(event):
                    Pause.change_image()
                    return True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            Pause.change_image()
            return True


pygame.init()

width, height = 800, 600
size = width, height
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill((255, 255, 255))


def game_over():
    font = pygame.font.Font(None, 30)
    text1 = font.render("Игра окончена, если вы хотите начать заново, то", 1, (83, 83, 83))
    text2 = font.render("нажмите SPACE или стрелку вверх, иначе ESC", 1, (83, 83, 83))
    text_x1 = width // 2 - text1.get_width() // 2
    text_y1 = height // 2 - text1.get_height() * 3 // 2 - 10
    screen.blit(text1, (text_x1, text_y1))
    text_x2 = width // 2 - text1.get_width() // 2
    text_y2 = height // 2 - text1.get_height() // 2 - 10
    screen.blit(text2, (text_x2, text_y2))
    pygame.display.flip()
    time.sleep(1)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if Quit.is_pressed(event):
                    return False
        Keys = pygame.key.get_pressed()
        if Keys[pygame.K_ESCAPE]:
            return False
        elif Keys[pygame.K_SPACE] or Keys[pygame.K_UP]:
            return True


def load_image(name, colorkey=None, point=(0, 0)):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at(point)
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Dino(pygame.sprite.Sprite):
    image_jump = load_image("Dino.png", -1)
    image1 = load_image("Dino1.png", -1)
    image2 = load_image("Dino2.png", -1)
    image_shift1 = load_image("Dino_shift.png", -1)
    image_shift2 = load_image("Dino_shift2.png", -1)
    image_died = load_image("Dino_died.png", -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = self.image_jump
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 340 - self.rect.h
        self.jump_counter = 30
        self.jump = False
        self.shag = 0
        self.shift = False
        self.v_down = 10
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, keys):
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not self.jump:
            self.image = self.image_jump
            self.jump = True
            self.jump_counter = 30
        if self.jump:
            self.image = self.image_jump
            if self.rect.y <= 343 - self.rect[3]:
                if self.shift:
                    if self.jump_counter > 0:
                        self.jump_counter = -self.jump_counter
                    self.rect.y -= (8 * self.jump_counter + 4) // 9
                else:
                    self.rect.y -= (4 * self.jump_counter + 4) // 9
            if self.rect.y > 343 - self.rect[3]:
                self.rect.y = 343 - self.rect[3]
            self.jump_counter -= 2
            if self.jump_counter == -32:
                self.jump = False
        elif self.shag <= 8:
            self.image = self.image1
        elif self.shag > 8:
            self.image = self.image2
        self.shift = False
        if keys[pygame.K_DOWN]:
            self.shift = True
            if self.shag <= 8:
                self.image = self.image_shift1
            else:
                self.image = self.image_shift2
            self.y = self.rect.y + self.rect[3]
            self.rect = self.image.get_rect()
            self.rect.x = 200
            self.rect.y = self.y - self.rect[3]
        if self.shag == 16:
            self.shag = 0
        self.shag += 1

    def is_collide(self):
        for element in barriers:
            if pygame.sprite.collide_mask(self, element):
                self.image = self.image_died
                return True
        return False


class QUIT(pygame.sprite.Sprite):
    image = load_image("QUIT.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = width - self.rect[2]
        self.rect.y = 0

    def is_pressed(self, args):
        if self.rect.collidepoint(args.pos):
            return True


class PAUSE(pygame.sprite.Sprite):
    image1 = load_image("PAUSE.png")
    image2 = load_image("START.png")

    def __init__(self, group):
        super().__init__(group)
        self.im = 1
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.x = width - self.rect.w * 2 - 4
        self.rect.y = 0

    def is_pressed(self, args):
        if self.rect.collidepoint(args.pos):
            return True

    def change_image(self):
        if self.im == 1:
            self.image = self.image2
            self.im = 2
        else:
            self.image = self.image1
            self.im = 1


class Pterodakl(pygame.sprite.Sprite):
    image1 = load_image("Pt1.png", -1)
    image2 = load_image("Pt2.png", -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = self.image2
        self.rect = self.image.get_rect()
        self.rect.x = 1900
        self.rect.y = 300 - self.rect.y
        self.v = 4
        self.mask = pygame.mask.from_surface(self.image)
        self.shag = 0

    def update(self, keys):
        self.rect.x -= self.v
        if self.rect.x < -100:
            self.rect.x = 1900
        if self.shag <= 16:
            if self.image == self.image2:
                self.rect.y += 6
            self.image = self.image1
        elif self.shag > 16:
            if self.image == self.image1:
                self.rect.y -= 6
            self.image = self.image2
        if self.shag == 32:
            self.shag = 0
        self.shag += 1


class Cactus(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.images = [load_image('Cactus_n_1.png', -1), load_image('Cactus_n_2.png', -1),
                       load_image('Cactus_n_3.png', -1)]
        self.image1 = random.choice(self.images)
        self.image2 = self.image1
        self.image = self.image1
        self.rect = self.image.get_rect()
        xs = set()
        xs.add(width)
        for element in barriers:
            xs.add(element.get_x())
        mx = max(xs)
        self.rect.x = mx + random.randrange(100, 400)
        self.rect.y = 340 - self.rect.h
        self.v = 4
        self.mask = pygame.mask.from_surface(self.image)
        self.shag = 0

    def update(self, keys):
        self.rect.x -= self.v
        if self.rect.x < -100:
            number_of_image = random.randrange(len(self.images))
            self.image1 = self.images[number_of_image]
            if number_of_image != 7:
                self.image2 = self.image1
            else:
                self.image2 = self.images[-1]
            self.rect = self.image.get_rect()
            self.rect.x -= self.v
            xs = set()
            for element in barriers:
                xs.add(element.get_x())
            mx = max(xs)
            if mx < width:
                mx = width
            self.rect.x = mx + random.randrange(50, 100) * self.v
            self.rect.y = 340 - self.rect.h
            self.mask = pygame.mask.from_surface(self.image)
        if self.shag == 16:
            x = self.rect.x
            self.image = self.image2
            self.rect = self.image.get_rect()
            self.rect.y = 340 - self.rect.h
            self.rect.x = x
            self.mask = pygame.mask.from_surface(self.image)
        if self.shag == 32:
            x = self.rect.x
            self.shag = 0
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.y = 340 - self.rect.h
            self.rect.x = x
            self.mask = pygame.mask.from_surface(self.image)
        self.shag += 1

    def get_x(self):
        return self.rect.x + self.rect[2]

    def add_image(self, n):
        if n == 1:
            self.images.append(load_image('Cactus_v_1.png', -1))
            self.images.append(load_image('Cactus_v_2.png', -1))
        elif n == 2:
            self.images.append(load_image('Cactus_v_3.png', -1))
        elif n == 3:
            self.images.append(load_image('Cactus_v_4.png', -1))
        elif n == 4:
            self.images.append(load_image("Pt1.png", -1))
            self.images.append(load_image("Pt2.png", -1))


class Cloud(pygame.sprite.Sprite):
    image = load_image('Cloud.png', -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = self.image
        self.rect = self.image.get_rect()
        xs = set()
        for element in effects:
            xs.add(element.get_x())
        mx = max(xs)
        self.rect.x = mx + random.randrange(100, 200)
        self.rect.y = random.randrange(200)
        self.v = 1

    def update(self):
        self.rect.x -= self.v
        if self.rect.x < -100:
            xs = set()
            for element in effects:
                xs.add(element.get_x())
            mx = max(xs)
            if mx < width:
                mx = width
            self.rect.x = mx + random.randrange(100, 200)
            self.rect.y = random.randrange(200)

    def get_x(self):
        return self.rect.x + self.rect[2]


class Map(pygame.sprite.Sprite):
    image = load_image('map.png', -1)

    def __init__(self, group, number):
        super().__init__(group)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.w * number
        self.rect.y = 333
        self.v = 4

    def update(self):
        self.rect.x -= self.v
        if self.rect.x < -self.rect.w:
            self.rect.x = self.rect.w


maps = pygame.sprite.Group()
effects = pygame.sprite.Group()
buttons = pygame.sprite.Group()
Quit = QUIT(buttons)
Pause = PAUSE(buttons)
dino = pygame.sprite.Group()
barriers = pygame.sprite.Group()
dinosavr = Dino(dino)
for _ in range(5):
    Cactus(barriers)
for _ in range(5):
    Cloud(effects)
Map(maps, 0)
Map(maps, 1)

fps = 60
clock = pygame.time.Clock()

with open('data/record.txt', 'r') as a:
    record = int(a.read())
score = 0

game = True
gameover = True

while game:
    pause_timer = 0
    running = True
    while running:
        pause_timer += 1
        keys = pygame.key.get_pressed()
        score += 1
        if score // 4 > record:
            record = score // 4
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game = False
                gameover = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if Quit.is_pressed(event):
                    running = False
                    game = False
                    gameover = False
                elif Pause.is_pressed(event):
                     answer = pause()
                     if not answer:
                         running = False
                         game = False
                         gameover = False
        if keys[pygame.K_p] and pause_timer > fps:
            pause_timer = 0
            answer = pause()
            if not answer:
                running = False
                game = False
                gameover = False
        if score == 500:
            for element in barriers:
                element.add_image(1)
        elif score == 700:
            for element in barriers:
                element.add_image(2)
        elif score == 1000:
            for element in barriers:
                element.add_image(3)
        elif score == 1600:
            for element in barriers:
                element.add_image(4)
        fps = score // 50 + 60
        update()
        if dinosavr.is_collide():
            running = False
            game = False
        clock.tick(fps)
        draw()
    if score // 4 >= record:
        with open('data/record.txt', 'w') as m:
            m.write('{}'.format(score // 4))
    if gameover:
        answer = game_over()
        if answer:
            game = True
    dino = pygame.sprite.Group()
    barriers = pygame.sprite.Group()
    effects = pygame.sprite.Group()
    dinosavr = Dino(dino)
    for _ in range(5):
        Cactus(barriers)
    for _ in range(5):
        Cloud(effects)
    quit_buttons = pygame.sprite.Group()
    Quit = QUIT(quit_buttons)
    with open('data/record.txt', 'r') as a:
        record = int(a.read())
    score = 0
pygame.quit()

