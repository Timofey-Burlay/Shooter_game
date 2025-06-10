import pygame
from pygame import sprite
from random import randint
from time import time as timer
import sys

clock = pygame.time.Clock()
FPS = 60

pygame.init()

window = pygame.display.set_mode((700, 500))
# , pygame.RESIZABLE

background = pygame.transform.scale(pygame.image.load("galaxy.jpg"), (700, 500))

pygame.display.set_caption("Шутер")


pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)
fire_sound = pygame.mixer.Sound("fire.ogg")


# hp_timer = pygame.USEREVENT + 1
# pygame.time.set_timer(hp_timer, 3000)


global_check_st = False
check_rekord = 0
check_patron = 5
check_bullet = 0
check_number = 0
check_propusk = 0
hp_hearts = 3
bullets = []


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, sixe_x, size_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (sixe_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 10:
            self.rect.x -= self.speed

        if keys[pygame.K_d] and self.rect.x < 600:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        global check_propusk
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            check_propusk += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()






player_rocket = Player("rocket.png", 250, 360, 80, 130, 8)
bullet_image = "bullet.png"
restart_image = pygame.image.load('restart_image.png')
start_image = pygame.image.load('play_image.png')

# sprites_list_win = sprite.groupcollide(Inoplanets, bullets, True, True)

# sprites_list_lose = sprite.spritecollide(player_rocket, Inoplanets, False)

number = pygame.font.SysFont('Comic Sans MS', 30)
propusk = pygame.font.SysFont('Comic Sans MS', 30)
timer_t = pygame.font.SysFont('Comic Sans MS', 30)
number_two = pygame.font.SysFont('Comic Sans MS', 30)
propusk_two = pygame.font.SysFont('Comic Sans MS', 30)
win_t = pygame.font.SysFont('Comic Sans MS', 80)
lose_t = pygame.font.SysFont('Comic Sans MS', 80)
rekord_t = pygame.font.SysFont('Comic Sans MS', 30)
reload_t = pygame.font.SysFont('Comic Sans MS', 30)

game = True


Inoplanets = pygame.sprite.Group()

# Inoplanet.kill
for i in range(1 ,4):

    Inoplanet = Enemy("ufo.png", randint(0, 620), -40, 80, 50, randint(1, 5))
    Inoplanets.add(Inoplanet)


bullets = pygame.sprite.Group()

game_screen = None
game_win = False
game_lose = False
game_restart = False
timer_check = False

rel_time = False


num_fire = 5


while game:


    num_sch = f"Счёт: {check_number}"
    propusk_f = f"Жизней: {hp_hearts}"
    timer_f = f"Патрон: {num_fire}"
    rekord_f = f"Патрон: {num_fire}"

    number_text = number.render(str(num_sch), False, (255, 255, 255))
    propusk_text = propusk.render(str(propusk_f), False, (255, 255, 255))
    timer_text = timer_t.render(str(timer_f), False, (255, 255, 255))
    win_text = win_t.render("ПОБЕДА", False, (50, 255, 0))
    lose_text = lose_t.render("ПОРАЖЕНИЕ", False, (255, 50, 0))
    number_text_two = number_two.render(str(num_sch), False, (255, 255, 255))
    propusk_text_two = propusk_two.render(str(propusk_f), False, (255, 255, 255))
    rekord_text = rekord_t.render(str(rekord_f), False, (255, 255, 255))

    if game_screen == None and game_win == False and game_lose == False:
        window.blit(background, (0, 0))
        start_rect = start_image.get_rect(topleft=(30, 10))
        window.blit(start_image, (30, 10))

        mouse = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            game_screen = True

    if game_screen == True and game_win == False and game_lose == False:

        window.blit(background, (0, 0))
        window.blit(number_text, (30, 30))
        window.blit(propusk_text, (30, 70))
        window.blit(timer_text, (30, 100))


        player_rocket.move()
        player_rocket.reset()


        Inoplanets.update()
        bullets.update()


        Inoplanets.draw(window)
        bullets.draw(window)


        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload_text = reload_t.render("Wait reload...", False, (255, 255, 255))
                window.blit(reload_text, (260, 460))
            else:
                num_fire = 5
                rel_time = False


    if game_win == True and game_screen == None and game_lose == False:
        window.blit(background, (0, 0))
        window.blit(win_text, (150, 180))
        window.blit(number_text_two, (150, 280))
        window.blit(propusk_text_two, (150, 320))
        window.blit(rekord_text, (150, 360))
        restart_rect = restart_image.get_rect(topleft=(170, 400))
        window.blit(restart_image, (170, 400))
        

        mouse = pygame.mouse.get_pos()
        if restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            check_number = 0
            hp_hearts = 3
            check_propusk = 0
            game_screen = None
            game_win = False

    if game_lose == True and game_win == False and game_screen == None:
        window.blit(background, (0, 0))
        window.blit(lose_text, (150, 180))
        window.blit(number_text_two, (150, 280))
        window.blit(propusk_text_two, (150, 320))
        window.blit(rekord_text, (150, 360))
        restart_rect = restart_image.get_rect(topleft=(170, 400))
        window.blit(restart_image, (170, 400))

        mouse = pygame.mouse.get_pos()
        if restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            check_number = 0
            hp_hearts = 3
            global_check_st = True
            check_propusk = 0
            game_win = False
            game_screen = True
            game_lose = False
            global_check_st = False




    hits = pygame.sprite.groupcollide(Inoplanets, bullets, True, True)

    for hit in hits:
        check_number += 1
        Inoplanet = Enemy("ufo.png", randint(0, 620), -40, 80, 50, randint(1, 5))
        Inoplanets.add(Inoplanet)


    if global_check_st == False:
        hits_lists = sprite.spritecollide(player_rocket, Inoplanets, True)

        for hits_list in hits_lists:
            hp_hearts -= 1
            Inoplanet = Enemy("ufo.png", randint(0, 620), -40, 80, 50, randint(1, 5))
            Inoplanets.add(Inoplanet)


    if hp_hearts <= 0:
        game_win = False
        game_screen = None
        game_lose = True


    if check_number == 20:
        game_win = True
        game_screen = None
        game_lose = False




    pygame.display.update()
    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        
        if game_screen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    if num_fire > 0 and rel_time == False: 
                        num_fire = num_fire - 1
                        player_rocket.fire()
                        fire_sound.play()
                        pygame.mixer.music.set_volume(0.2)

                    if num_fire <= 0 and rel_time == False:
                        last_time = timer()
                        rel_time = True

        # if event.type == hp_timer:
        #     global_check_st = False


    clock.tick(FPS)