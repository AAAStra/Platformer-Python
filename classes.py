import pygame
import json
pygame.init()

with open ("levels/level1.json", "r") as file:
    world_data = json.load(file)

sound_jump = pygame.mixer.Sound("music/jump.wav")
sound_jump.set_volume(0.1)

game_over = [0]

class Car:
    def __init__(self):
        self.image = pygame.image.load("car1.png")
        self.image = pygame.transform.scale(self.image, (80, 50))
        self.rect = self.image.get_rect()

    def update(self, display):
        display.blit(self.image, self.rect)

tile_size = 30

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("tile0.jpg")
        self.image = pygame.transform.scale(img,
                                            (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
lava_group = pygame.sprite.Group()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("diamond3.png")
        self.image = pygame.transform.scale(img,(tile_size, tile_size ))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
coin_group = pygame.sprite.Group()

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("exit_door.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

exit_group = pygame.sprite.Group()
class World:
    def __init__(self, data):
        dirt_img = pygame.image.load("tile10.png")
        grass_img = pygame.image.load("tile7.png")
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1 or tile == 2:
                    images = {1: dirt_img, 2: grass_img}
                    img = pygame.transform.scale(images[tile],
                                                 (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count *tile_size
                    tile =(img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 3:
                    lava = Lava(col_count * tile_size,
                                row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                elif tile == 5:
                    exit = Exit(col_count * tile_size,
                                row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                elif tile == 6:
                    coin = Coin(col_count * tile_size + (tile_size //2),
                                row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                col_count += 1
            row_count += 1

    def draw(self, display):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])

class Player:
    def __init__(self):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.direction = 0
        for num in range(1, 3):
            img_right = pygame.image.load(f"player{num}.png")
            img_right = pygame.transform.scale(img_right, (35, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()

        self.image = pygame.image.load("player1.png")
        self.image = pygame.transform.scale(self.image, (40, 75))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 600 - 130
        self.gravity = 0
        self.jumped = False
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, display, world):
        global game_over
        x = 0
        y = 0
        walk_speed = 10
        if game_over[0] == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.gravity = -15
                self.jumped = True
                sound_jump.play()
            if key[pygame.K_a]:
                x -= 5
                self.direction = -1
                self.counter += 1
            if key[pygame.K_d]:
                x += 5
                self.direction = 1
                self.counter += 1
            if self.counter > walk_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                else:
                    self.image = self.images_left[self.index]
            self.gravity += 1
            if self.gravity > 10:
                self.gravity = 10
            y += self.gravity
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + x, self.rect.y,
                                       self.width, self.height):
                    x = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + y,
                                       self.width, self.height):
                    if self.gravity < 0:
                        y = tile[1].bottom - self.rect.top
                        self.gravity = 0
                    elif self.gravity >= 0:
                        y = tile[1].top - self.rect.bottom
                        self.gravity = 0
                        self.jumped = False
            if self.rect.bottom >= 590:
                self.rect.bottom = 590
                self.jumped = False
            if self.rect.right > 590:
                self.rect.right = 590
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over[0] = -1
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over[0] = 1

            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            self.rect.x += x
            self.rect.y += y
        elif game_over[0] == -1:
            self.image = pygame.image.load("angel.png")
            self.image = pygame.transform.scale(self.image, (70, 60))
            self.rect.y -= 5
            print("Game over:(")
        display.blit(self.image, self.rect)
class Button:
    def __init__(self, location, root):
        self.image = pygame.image.load(root)
        self.image = pygame.transform.scale(self.image, (120, 60))
        self.rect = self.image.get_rect(center = location )
    def draw(self, display):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        display.blit(self.image, self.rect)
        return action