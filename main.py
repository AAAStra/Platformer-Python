import json

import pygame

from classes import Player, Car, lava_group, Button, game_over, World, exit_group, coin_group

pygame.init()

WIDTH = 600
HEIGHT = 600

clock = pygame.time.Clock()
fps = 60

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

background = pygame.image.load ("bg12.png")

sound_game_over = pygame.mixer.Sound("music/game_over.wav")
sound_game_over.set_volume(0.1)
sound_coin = pygame.mixer.Sound("music/coin.wav")
sound_coin.set_volume(0.1)

image = pygame.image.load("player1.png")
rect = image.get_rect()

player = Player()
car = Car()

level = 1
max_level = 5

score = 0

def draw_text(text, color, size, x, y):
    font = pygame.font.SysFont("Arial", size)
    img = font.render(text, True, color)
    display.blit(img, (x, y))

def reset_level():
    player.rect.x = 100
    player.rect.y = HEIGHT - 130
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()
    with open(f"levels/level{level}.json", "r") as file:
        world_data = json.load(file)
    world = World(world_data)
    return world

restart = Button((WIDTH // 2, HEIGHT // 2), "restart_btn.png")
start = Button((WIDTH // 2 , HEIGHT // 2), "start_btn.png")
exit = Button((WIDTH // 2 , HEIGHT // 2 - 100), "exit_btn.png")


run = True
main_menu = True
while run:
    display.blit(background, rect)
    if main_menu:
        if start.draw(display):
            main_menu = False
            level = 1
            score = 0
            world = reset_level()
    else:
        world.draw(display)
        lava_group.draw(display)
        player.update(display, world)

        draw_text(str(score), "#db6960", 30, 40, 40)

        if pygame.sprite.spritecollide(player, coin_group, True):
            score += 1
            sound_coin.play()
            print(score)

        lava_group.update()
        exit_group.draw(display)
        exit_group.update()
        coin_group.draw(display)
        coin_group.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if game_over[0] == -1:
        sound_game_over.play()
        restart.draw(display)
        if exit.draw(display):
            run = False
        if restart.draw(display):
            player = Player()
            # world = World(world_data)
            world = reset_level()
            game_over[0] = 0

    elif game_over[0] == 1:
        game_over[0] = 0
        if level < max_level:
            level += 1
            world = reset_level()
        else:
            print("win!")
            main_menu = True

    clock.tick(fps)
    pygame.display.update()
pygame.quit()