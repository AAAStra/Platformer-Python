import pygame
pygame.init()

WIDTH = 600
HEIGHT = 600

clock = pygame.time.Clock()

display = pygame.display.set_mode((WIDTH, HEIGHT))

class Hero:
    def __init__(self):
        self.image = pygame.image.load("player1.png")
        self.rect = self.image.get_rect()
        self.direction = 1
        self.lives = 3
        self.level = 1
    def update(self):
        self.rect.x += self.direction
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.direction *= -1
        display.blit(self.image, self.rect)

    def hello(self):
        print("Hello, Player!")
    def hi(self):
        print("Hi?")

hero = Hero()
run = True
while run:
    clock.tick(60)
    display.fill("white")
    hero.update()
    pygame.display.update()
pygame.quit()


class Car:
    def __init__(self, company, type, year):
        self.company = company
        self.type = type
        self.year = year

    def display_info(self):
        print(f"car info:{self.company}{self.type}{self.year}")
car_one = Car("Skoda", "Ooctavia", "2014")
car_two = Car ("Lada", "Granta", "2011")
print (car_one.company)
print (car_two.company)
