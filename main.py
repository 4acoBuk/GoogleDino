import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))


class Dino(pygame.sprite.Sprite):
    image_jump = load_image("Dino.png", -1)
    image1 = load_image("Dino1.png", -1)
    image2 = load_image("Dino2.png", -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = self.image_jump
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 300 - self.rect.y
        self.jump_counter = 30
        self.jump = False
        self.shag = 1

    def update(self, keys):
        if keys[pygame.K_SPACE] and not self.jump:
            self.image = self.image_jump
            self.jump = True
            self.jump_counter = 30
        if self.jump:
            self.rect.y -= (self.jump_counter + 1) // 3
            self.jump_counter -= 1
            if self.jump_counter == -31:
                self.jump = False
        elif self.shag == 1:
            self.shag = -1
            self.image = self.image1
        elif self.shag == -1:
            self.shag = 1
            self.image = self.image2


class Barrier(pygame.sprite.Sprite):
    image = load_image("Pt.png", -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = 1900
        self.rect.y = 300 - self.rect.y
        self.v = 4

    def update(self, keys):
        self.rect.x -= self.v
        if self.rect.x < -100:
            self.rect.x = 1900

all_sprites = pygame.sprite.Group()
Dino(all_sprites)
Barrier(all_sprites)

running = True

fps = 120
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    all_sprites.update(pygame.key.get_pressed())
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(fps)

pygame.quit()