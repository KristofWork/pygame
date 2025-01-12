import pygame
import sys

from random import randint

# Инициализация pygame
pygame.init()

# Создание констант(переменных)
WIDTH = 500
HEIGHT = 500
FPS = 60
BACKGROUND_COLOR = (10, 15, 40)
START_BACKGROUND_COLOR = (40, 15, 10)
START_FONT_COLOR = (147, 97, 87)

player_color = (20, 20, 20)
# Создаем экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Создаем таймер
clock = pygame.time.Clock()


class Sprite:
    def __init__(self, x, y, w, h, img_path):
        self.rect = pygame.Rect(x, y, w, h)
        self.img_orig = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img_orig, (w, h))
        self.direction = None

    def draw(self):
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


player = Sprite(0, 300, 100, 100, r"assets\img\player.png")
pickup = Sprite(200, 200, 30, 30, r"assets\img\pickup.png")
exit_door = Sprite(0, 0, 30, 30, r"assets\img\exit_door.png")

font_en = pygame.font.SysFont("Niagara Engraved", 100)
font_ru = pygame.font.SysFont("Arial", 30)

start_text1 = font_en.render("Agar.io", True, (START_FONT_COLOR))
start_text2 = font_en.render("Start", True, (START_FONT_COLOR))

start_button = pygame.Rect(
    0, 0, start_text2.get_width() + 100, start_text2.get_height() + 10
)


start_button.centerx = WIDTH / 2
start_button.centery = 350 + start_text2.get_height() / 2

game_state = "start"

# Начало игрового цикла
while True:
    if game_state == "start":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "game"
        screen.fill(START_BACKGROUND_COLOR)
        screen.blit(start_text1, (WIDTH / 2 - start_text1.get_width() / 2, 150))

        pygame.draw.rect(screen, (20, 20, 20), start_button)
        screen.blit(start_text2, (WIDTH / 2 - start_text2.get_width() / 2, 350))

    if game_state == "end":
        pass
    if game_state == "game":
        # Заливка экрана
        screen.fill(BACKGROUND_COLOR)
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_color = (255, 0, 0)
                elif event.key == pygame.K_2:
                    player_color = (0, 255, 0)
                elif event.key == pygame.K_3:
                    player_color = (0, 0, 255)
                elif event.key == pygame.K_4:
                    player_color = (20, 20, 20)

                elif event.key == pygame.K_LEFT:
                    player.direction = "left"
                elif event.key == pygame.K_RIGHT:
                    player.direction = "right"
                elif event.key == pygame.K_UP:
                    player.direction = "up"
                elif event.key == pygame.K_DOWN:
                    player.direction = "down"
            elif event.type == pygame.KEYUP:
                if event.key in (
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                    pygame.K_UP,
                    pygame.K_DOWN,
                ):
                    player.direction = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_door.rect.collidepoint(event.pos):
                    sys.exit()

        player.move()
        player.collide_grow(pickup)

        player.draw()
        pickup.draw()
        exit_door.draw()

    # Обновление экрана
    pygame.display.update()
    # Лочим FPS
    clock.tick(FPS)
