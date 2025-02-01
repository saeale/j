import pygame
from game2 import game
from resources import (star_display_list_small, images, level_images, menu_ball_im, click_s, select_s,
                       new_game_s, cursor_im, sound_butt_im_sett, music_butt_im, reset_butt_im, confirm_im, quit_im,
                       final_im, star_count_im, ball_on_im, ball_off_im, bg_on_im, bg_off_im, skin_ims, bg_ims, costs)
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def sounds_update():
    for sound in sounds:
        sound.set_volume(sound_mode)
    sound_butt.image = sound_butt_im_sett[sound_mode]


def save():
    with open('data/scores.txt', 'w') as f:
        f.write('\n'.join(map(str, scores)))


def final_screen(from_game):
    if from_game and music_mode:
        pygame.mixer.music.play(-1)
    pygame.mixer.music.fadeout(4000)
    running = True
    for _ in range(480):
        clock.tick(120)
        screen.blit(bg, (0, 0))
        screen.blit(final_im, (0, 0))
        if pygame.mouse.get_focused():
            cursor_group.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.topleft = event.pos
        if not running:
            break


pygame.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption('jump')

# настройка музыки
pygame.mixer.init()
pygame.mixer.music.load('data/bg_music.mp3')
pygame.mixer.music.play(-1)
sound_mode = 1
music_mode = 1

# настройка аудио
sounds = [click_s, new_game_s, select_s]

# инициализация групп
menu_sprites = pygame.sprite.Group()
logo_sprites = pygame.sprite.Group()
level_sprites = pygame.sprite.Group()
sett_sprites = pygame.sprite.Group()
confirm_group = pygame.sprite.Group()
quit_group = pygame.sprite.Group()
back_button_group = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()
player_sett_ball = pygame.sprite.Group()
player_sett_bg = pygame.sprite.Group()

# настройка экрана и переменных
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
running = True
mode = 'menu'
skin_mode = 0
bg_mode = 0
with open('data/scores.txt', 'r') as f:
    scores = list(map(int, f.readlines()))


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(logo_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


logo = AnimatedSprite(load_image('logo_spreadsheet.png'), 6, 3, 255, 100)
horizontal_borders = pygame.sprite.Group()
spr = pygame.sprite.Sprite()
spr.rect = pygame.Rect(logo.rect.left, logo.rect.top, 100, 1)
spr.add(horizontal_borders)


class MenuBall(pygame.sprite.Sprite):  # мячик
    def __init__(self):
        super().__init__(logo_sprites)
        self.radius = 15
        self.image = menu_ball_im['menu']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(325, 40, 30, 30)
        self.vx = 0
        self.vy = 0

    def update(self):
        # настройка физики
        self.rect = self.rect.move(self.vx * 50, self.vy * 50)
        self.vy += 0.003

        # взаимодействия с другими спрайтами
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            spr = pygame.sprite.spritecollideany(self, horizontal_borders)
            if spr.rect.top > self.rect.top + self.radius:
                self.vy = -0.099
            else:
                self.vy = 0.099


bg = pygame.transform.scale(load_image('bg.jpg'), (1200, 600))
ball = MenuBall()

cursor = pygame.sprite.Sprite(cursor_group)
cursor.image = cursor_im
cursor.rect = cursor.image.get_rect()

# главное окно + кнопка меню
play_button = pygame.sprite.Sprite(menu_sprites)
play_button.rect = pygame.Rect(375, 275, 250, 250)
play_button.image = pygame.transform.scale(load_image('play.png'), (250, 250))

sett_button = pygame.sprite.Sprite(menu_sprites)
sett_button.rect = pygame.Rect(675, 300, 200, 200)
sett_button.image = pygame.transform.scale(load_image('settings.png'), (200, 200))

player_sett_button = pygame.sprite.Sprite(menu_sprites)
player_sett_button.rect = pygame.Rect(125, 300, 200, 200)
player_sett_button.image = pygame.transform.scale(load_image('player.png'), (200, 200))

back_button = pygame.sprite.Sprite(back_button_group)
back_button.rect = pygame.Rect(20, 10, 100, 52)
back_button.image = pygame.transform.scale(load_image('menu_button.png'), (100, 52))

quit_button = pygame.sprite.Sprite(menu_sprites)
quit_button.rect = pygame.Rect(920, 520, 60, 60)
quit_button.image = load_image('quit_button.png')

quit_screen = pygame.sprite.Sprite(quit_group)
quit_screen.image = quit_im
quit_screen.rect = pygame.Rect(180, 80, 640, 440)
quit_screen.yes_rect = pygame.Rect(268, 380, 204, 92)
quit_screen.no_rect = pygame.Rect(528, 380, 204, 92)
quit_screen_active = False

# окно настроек
music_butt = pygame.sprite.Sprite(sett_sprites)
music_butt.image = music_butt_im[music_mode]
music_butt.rect = pygame.Rect(275, 275, 450, 75)

sound_butt = pygame.sprite.Sprite(sett_sprites)
sound_butt.image = sound_butt_im_sett[sound_mode]
sound_butt.rect = pygame.Rect(275, 375, 450, 75)

reset_butt = pygame.sprite.Sprite(sett_sprites)
reset_butt.image = reset_butt_im
reset_butt.rect = pygame.Rect(275, 475, 450, 75)

confirm_screen = pygame.sprite.Sprite(confirm_group)
confirm_screen.image = confirm_im
confirm_screen.rect = pygame.Rect(180, 80, 640, 440)
confirm_screen.yes_rect = pygame.Rect(268, 380, 204, 92)
confirm_screen.no_rect = pygame.Rect(528, 380, 204, 92)
confirm_screen_active = False

# окно персонализации
star_count = pygame.sprite.Sprite(player_sett_ball)
star_count.add(player_sett_bg)
star_count.image = star_count_im
star_count.rect = pygame.Rect(825, 0, 300, 100)

font = pygame.font.Font(None, 75)
text_star = pygame.sprite.Sprite(player_sett_ball)
text_star.add(player_sett_bg)
text_star.rect = pygame.Rect(920, 17, 100, 50)

pl_ball = pygame.sprite.Sprite(player_sett_ball)
pl_ball.add(player_sett_bg)
pl_ball.image = ball_on_im
pl_ball.rect = pygame.Rect(0, 260, 78, 75)

pl_bg = pygame.sprite.Sprite(player_sett_ball)
pl_bg.add(player_sett_bg)
pl_bg.image = bg_off_im
pl_bg.rect = pygame.Rect(0, 350, 78, 75)

skins = []
star_sum = sum(scores)
for i in range(10):
    spr = pygame.sprite.Sprite(player_sett_ball)
    spr.rect = pygame.Rect(200 + (i % 5) * 125, 300 + (i // 5) * 125, 100, 100)
    spr.mode = i
    spr.cost = costs[i]
    if star_sum < costs[i]:
        spr.image = skin_ims[i][1]
        spr.availible = False
    else:
        spr.image = skin_ims[i][0]
        spr.availible = True
    skins.append(spr)

select_ball_spr = pygame.sprite.Sprite(player_sett_ball)
select_ball_spr.rect = pygame.Rect(200, 300, 100, 100)
select_ball_spr.image = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
pygame.draw.rect(select_ball_spr.image, (255, 255, 255), (0, 0, 100, 100), 5)

bgs = []
for i in range(4):
    spr = pygame.sprite.Sprite(player_sett_bg)
    spr.rect = pygame.Rect(250 + (i % 2) * 300, 300 + (i // 2) * 150, 200, 120)
    spr.image = bg_ims[i]
    spr.mode = i
    bgs.append(spr)

select_bg_spr = pygame.sprite.Sprite(player_sett_bg)
select_bg_spr.rect = pygame.Rect(250, 300, 200, 120)
select_bg_spr.image = pygame.Surface((200, 120), pygame.SRCALPHA, 32)
pygame.draw.rect(select_bg_spr.image, (255, 255, 255), (0, 0, 200, 120), 5)

# окно уровней
level_sprites_list = [None] * 16
for i in range(4):
    for j in range(4):
        spr = pygame.sprite.Sprite(level_sprites)
        spr.rect = pygame.Rect(100 + i * 1300/6, 100 + j * 350/3, 150, 100)
        spr.level = j * 4 + i + 1
        level_sprites_list[j * 4 + i] = spr
        spr.image = level_images[j * 4 + i].copy()
        spr.image.blit(star_display_list_small[scores[spr.level - 1]], (15, 55))


clock = pygame.time.Clock()
clock.tick(120)
ticks = 0
jumping = False
while running:
    screen.blit(bg, (0, 0))

    # logo
    if mode != 'levels':
        logo_sprites.draw(screen)
        if not jumping:
            ticks += 1
            if ticks == 1200:
                ticks = 0
                jumping = True
        if jumping:
            ticks += 1
            if ticks % 12 == 0:
                logo.update()
            if ticks == 12 * 18:
                jumping = False
        ball.update()

    # menu (меню или кнопка)
    if mode == 'menu':
        menu_sprites.draw(screen)
        if quit_screen_active:
            quit_group.draw(screen)
    else:
        back_button_group.draw(screen)

    # levels
    if mode == 'levels':
        level_sprites.draw(screen)

    # sett
    if mode == 'sett':
        sett_sprites.draw(screen)

    # player sett ball
    if mode == 'player sett ball':
        player_sett_ball.draw(screen)

    # player sett bg
    if mode == 'player sett bg':
        player_sett_bg.draw(screen)

    # экран подтверждения сброса
    if confirm_screen_active:
        confirm_group.draw(screen)

    # cursor
    if pygame.mouse.get_focused():
        cursor_group.draw(screen)

    pygame.display.flip()
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            cursor.rect.topleft = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if confirm_screen_active:
                    confirm_screen_active = False
                elif quit_screen_active:
                    quit_screen_active = False
                elif mode != 'menu':
                    mode = 'menu'
                    ball.image = menu_ball_im[mode]
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_s.play()
            x, y = event.pos

            # menu, back_button
            if mode == 'menu':
                if quit_screen_active:
                    if quit_screen.no_rect.collidepoint(x, y):
                        quit_screen_active = False
                        continue
                    if quit_screen.yes_rect.collidepoint(x, y):
                        running = False
                        continue
                elif quit_button.rect.collidepoint(x, y):
                    quit_screen_active = True
                    continue
                elif play_button.rect.collidepoint(x, y):
                    mode = 'levels'
                    continue
                elif sett_button.rect.collidepoint(x, y):
                    mode = 'sett'
                    ball.image = menu_ball_im[mode]
                    continue
                elif player_sett_button.rect.collidepoint(x, y):
                    mode = 'player sett ball'
                    star_sum = sum(scores)
                    text_star.image = font.render(str(star_sum), True, (255, 255, 255))
                    ball.image = menu_ball_im[mode]
                    pl_ball.image = ball_on_im
                    pl_bg.image = bg_off_im
                    for i in range(10):
                        if star_sum < costs[i]:
                            skins[i].image = skin_ims[i][1]
                            skins[i].availible = False
                        else:
                            skins[i].image = skin_ims[i][0]
                            skins[i].availible = True
                    continue
            elif not confirm_screen_active:
                if back_button.rect.collidepoint(x, y):
                    mode = 'menu'
                    ball.image = menu_ball_im[mode]
                    continue

            # levels
            if mode == 'levels':
                for spr in level_sprites:
                    if spr.rect.collidepoint(x, y):

                        pygame.mixer.music.stop()
                        new_game_s.play()
                        curr_level = spr.level
                        res = game(screen, curr_level, images, sound_mode, scores, spr, skin_mode, bg_mode)

                        while res[0] == 2 or res[0] == 3:  # заново или следующий уровень с сохранением результата

                            # изменение звука
                            sound_mode = res[1]
                            sounds_update()

                            if res[0] == 2:  # заново
                                res = game(screen, curr_level, images, sound_mode, scores,
                                           level_sprites_list[curr_level - 1], skin_mode, bg_mode)

                            if res[0] == 3:  # следующий уровень (после 16 1)
                                curr_level = curr_level % 16 + 1
                                res = game(screen, curr_level, images,sound_mode, scores,
                                           level_sprites_list[curr_level - 1], skin_mode, bg_mode)

                        if res[0] == -1:  # выход из игры
                            running = False
                            save()

                            final_screen(True)

                            pygame.quit()
                            sys.exit()

                        elif res[0] == 1:  # меню
                            sound_mode = res[1]
                            sounds_update()
                            if music_mode == 1:
                                pygame.mixer.music.play()

                        elif res[0] == 0:  # меню
                            sound_mode = res[1]
                            sounds_update()
                            if music_mode == 1:
                                pygame.mixer.music.play()
                        break
                if pygame.mouse.get_focused():
                    cursor.rect.topleft = pygame.mouse.get_pos()

            # sett
            if confirm_screen_active:
                if confirm_screen.no_rect.collidepoint(x, y):
                    confirm_screen_active = False
                if confirm_screen.yes_rect.collidepoint(x, y):
                    scores = [0] * 16
                    skin_mode = 0
                    select_ball_spr.rect = pygame.Rect(200, 300, 100, 100)
                    for spr in level_sprites:
                        spr.image = level_images[spr.level - 1]
                        spr.image.blit(star_display_list_small[0], (15, 55))
                    confirm_screen_active = False
            elif mode == 'sett':
                if music_butt.rect.collidepoint(x, y):
                    music_mode = 1 - music_mode
                    music_butt.image = music_butt_im[music_mode]
                    if music_mode == 0:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play()
                if sound_butt.rect.collidepoint(x, y):
                    sound_mode = 1 - sound_mode
                    sounds_update()
                if reset_butt.rect.collidepoint(x, y):
                    confirm_screen_active = True

            if mode == 'player sett ball':
                if pl_bg.rect.collidepoint(x, y):
                    mode = 'player sett bg'
                    pl_ball.image = ball_off_im
                    pl_bg.image = bg_on_im
                for spr in skins:
                    if spr.rect.collidepoint(x, y) and spr.availible:
                        select_s.play()
                        skin_mode = spr.mode
                        select_ball_spr.rect = pygame.Rect(200 + (spr.mode % 5) * 125, 300 + (spr.mode // 5) * 125, 100, 100)
            elif mode == 'player sett bg':
                if pl_ball.rect.collidepoint(x, y):
                    mode = 'player sett ball'
                    pl_ball.image = ball_on_im
                    pl_bg.image = bg_off_im
                for spr in bgs:
                    if spr.rect.collidepoint(x, y):
                        select_s.play()
                        bg_mode = spr.mode
                        select_bg_spr.rect = pygame.Rect(250 + (spr.mode % 2) * 300, 300 + (spr.mode // 2) * 150, 200, 120)

save()

final_screen(False)

pygame.quit()
