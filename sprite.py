import pygame
from random import randint

WIDTH = 500
HEIGHT = 500


class Sprite:
    def __init__(self, x, y, w, h, img_path):
        self.rect = pygame.Rect(x, y, w, h)
        self.img_orig = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img_orig, (w, h))
        self.direction = None

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def move(self):
        if self.direction == "left":
            self.rect.x -= 10
        elif self.direction == "right":
            self.rect.x += 10
        elif self.direction == "up":
            self.rect.y -= 10
        elif self.direction == "down":
            self.rect.y += 10

    def collide_grow(self, other_sprite):
        global game_state
        if self.rect.colliderect(other_sprite.rect):
            self.rect.width += 15
            self.rect.height += 15
            if self.rect.width >= 400:
                game_state = "end"
            other_sprite.rect.x = randint(0, WIDTH - other_sprite.rect.width)
            other_sprite.rect.y = randint(0, HEIGHT - other_sprite.rect.height)
            self.img = pygame.transform.scale(
                self.img_orig, (self.rect.width, self.rect.height)
            )
