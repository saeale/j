import pygame
import os
import sys

pygame.init()


def game(screen, level, images, sound_mode, scores, spr, skin_mode, bg_mode):
    # предварительная загрузка ресурсов
    from resources import jump_s, death_s, star_s, boost_s, break_s, click_s, win_s
    from resources import star_display_list, star_display_list_big, level_images, star_display_list_small
    from resources import (pause_im, bg, cont_butt_im, sound_butt_im, menu_butt_im, cursor_im, end_level_im,
                           retry_butt_im, ball_im)
    from maps import maps

    # функция для spritecollideany пересечения по маске
    def collidemask(t1: pygame.sprite.Sprite, t2: pygame.sprite.Sprite):
        return bool(pygame.sprite.collide_mask(t1, t2))
    # ------------------------------------------------------------------------------------------------------------------
    # ПРЕДВАРИТЕЛЬНЫЕ НАСТРОЙКИ

    # настройка аудио
    sounds = [jump_s, death_s, star_s, boost_s, break_s, click_s, win_s]
    for sound in sounds:
        sound.set_volume(sound_mode)
    star_s.set_volume(0.5 * sound_mode)

    # подготовка групп
    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    boost_borders = pygame.sprite.Group()
    break_borders = pygame.sprite.Group()
    killed = []
    vertical_borders = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    front_layer = pygame.sprite.Group()
    pause_buttons = pygame.sprite.Group()
    cursor_group = pygame.sprite.Group()
    win_window = pygame.sprite.Group()
    win = False

    # stars_display понадобится в классах ниже
    stars_display = pygame.sprite.Sprite(front_layer)
    stars_display.image = pygame.transform.scale(star_display_list[0], (300, 100))
    stars_display.rect = pygame.Rect(0, 0, 300, 100)

    # ------------------------------------------------------------------------------------------------------------------
    # класс, соединяющий спрайты объектов в "таблицу"
    class Board:
        def __init__(self, map1, left, top, cell_size, images):
            self.width = len(map1[0])
            self.height = len(map1)
            self.left = left
            self.top = top
            self.cell_size = cell_size
            self.start = 0, 0
            self.finish = 0, 0
            self.stars = []
            self.bg = bg[bg_mode].copy()

            # подготовка изображений
            self.block_im, self.boost_im, self.break_im, self.spikes_im, self.star_im, self.grfl_im, self.rfl_im = (
                map(lambda x: pygame.transform.scale(x, (cell_size, cell_size)), images))
            self.ball_im = pygame.transform.scale(ball_im[skin_mode], (cell_size // 2, cell_size // 2))

            # инициализация всех игровых спрайтов
            for j in range(-1, self.width + 1):
                Block(-1, j, self, trnsp=True)
            for i in range(self.height):
                Block(i, -1, self, trnsp=True)
                for j in range(self.width):
                    if map1[i][j] == '#':
                        Block(i, j, self)
                    elif map1[i][j] == '-':
                        Spikes(i, j, self)
                    elif map1[i][j] == '*':
                        self.stars.append(Star(i, j, self))
                    elif map1[i][j] == 'S':
                        self.start = i, j
                        GreenFlag(i, j, self)
                    elif map1[i][j] == 'F':
                        self.finish = i, j
                        self.red_fl = RedFlag(i, j, self)
                    elif map1[i][j] == '^':
                        Boost(i, j, self)
                    elif map1[i][j] == '+':
                        Break(i, j, self)
                Block(i, self.width, self, trnsp=True)
            for j in range(-1, self.width + 1):
                Spikes(self.height, j, self, trnsp=True)
            self.ball = Ball(*self.start, self)
            self.win = False
            self.stars_count = 0

        def respawn(self):  # начинает игру заново
            for spr in self.stars:
                spr.collected = False
                spr.image = self.star_im
            self.stars_count = 0
            stars_display.image = star_display_list[0]
            self.ball.rect = pygame.Rect(self.left + self.ball.start_x * self.cell_size,
                                         self.top + self.ball.start_y * self.cell_size, 2 * self.ball.radius,
                                         2 * self.ball.radius)
            self.ball.x = self.ball.start_x
            self.ball.y = self.ball.start_y
            self.ball.vx = 0
            self.ball.vy = 0
            for spr in killed:
                spr.restore()

    class Block(pygame.sprite.Sprite):  # обычный блок
        def __init__(self, x, y, board: Board, trnsp=False):
            super().__init__()
            self.x = y
            self.y = x

            self.rect = pygame.Rect(board.left + y * board.cell_size, board.top + x * board.cell_size,
                                    board.cell_size, board.cell_size)

            if not trnsp:
                board.bg.blit(board.block_im, (board.left + y * board.cell_size, board.top + x * board.cell_size))

            # настройка границ
            self.vert1 = pygame.sprite.Sprite(vertical_borders)
            self.vert1.rect = pygame.Rect(self.rect.left, self.rect.top + self.rect.height * 0.1, 1,
                                          self.rect.height * 0.8)
            self.vert2 = pygame.sprite.Sprite(vertical_borders)
            self.vert2.rect = pygame.Rect(self.rect.right - 1, self.rect.top + self.rect.height * 0.1, 1,
                                          self.rect.height * 0.8)
            self.hor1 = pygame.sprite.Sprite(horizontal_borders)
            self.hor1.rect = pygame.Rect(self.rect.left + self.rect.width * 0.1, self.rect.top, self.rect.width * 0.8,
                                         1)
            self.hor2 = pygame.sprite.Sprite(horizontal_borders)
            self.hor2.rect = pygame.Rect(self.rect.left + self.rect.width * 0.1, self.rect.bottom - 1,
                                         self.rect.width * 0.8, 1)

    class Boost(pygame.sprite.Sprite):  # блок с усилением прыжка
        def __init__(self, x, y, board: Board):
            super().__init__(all_sprites)
            self.x = y
            self.y = x

            self.rect = pygame.Rect(board.left + y * board.cell_size, board.top + x * board.cell_size,
                                    board.cell_size, board.cell_size)

            board.bg.blit(board.boost_im, (board.left + y * board.cell_size, board.top + x * board.cell_size))

            self.image = board.boost_im
            self.mask = pygame.mask.from_surface(self.image)

            # настройка границ
            self.vert1 = pygame.sprite.Sprite(vertical_borders)
            self.vert1.rect = pygame.Rect(self.rect.left, self.rect.top + self.rect.height * 0.1, 1,
                                          self.rect.height * 0.8)
            self.vert2 = pygame.sprite.Sprite(vertical_borders)
            self.vert2.rect = pygame.Rect(self.rect.right - 1, self.rect.top + self.rect.height * 0.1, 1,
                                          self.rect.height * 0.8)
            self.hor1 = pygame.sprite.Sprite(boost_borders)
            self.hor1.rect = pygame.Rect(self.rect.left + self.rect.width * 0.1, self.rect.top, self.rect.width * 0.8,
                                         1)
            self.hor2 = pygame.sprite.Sprite(horizontal_borders)
            self.hor2.rect = pygame.Rect(self.rect.left + self.rect.width * 0.1, self.rect.bottom - 1,
                                         self.rect.width * 0.8, 1)

    class Break(pygame.sprite.Sprite):  # ломающийся блок
        def __init__(self, x, y, board: Board):
            super().__init__(all_sprites)
            self.x = y
            self.y = x

            self.rect = pygame.Rect(board.left + y * board.cell_size, board.top + x * board.cell_size,
                                    board.cell_size, board.cell_size)

            self.image = board.break_im
            self.mask = pygame.mask.from_surface(self.image)

            # настройка границ
            self.vert1 = pygame.sprite.Sprite(vertical_borders)
            self.vert1.rect = pygame.Rect(self.rect.left, self.rect.top + self.rect.height * 0.1, 1,
                                          self.rect.height * 0.8)
            self.vert2 = pygame.sprite.Sprite(vertical_borders)
            self.vert2.rect = pygame.Rect(self.rect.right - 1, self.rect.top + self.rect.height * 0.1, 1,
                                          self.rect.height * 0.8)
            self.hor1 = pygame.sprite.Sprite(break_borders)
            self.hor1.rect = pygame.Rect(self.rect.left + self.rect.width * 0.1, self.rect.top, self.rect.width * 0.8,
                                         1)
            self.hor1.parent = self
            self.hor2 = pygame.sprite.Sprite(horizontal_borders)
            self.hor2.rect = pygame.Rect(self.rect.left + self.rect.width * 0.1, self.rect.bottom - 1,
                                         self.rect.width * 0.8, 1)

        def breaks(self):
            self.kill()
            self.hor1.kill()
            self.hor2.kill()
            self.vert1.kill()
            self.vert2.kill()

        def restore(self):
            self.add(all_sprites)
            self.hor1.add(break_borders)
            self.hor2.add(horizontal_borders)
            self.vert1.add(vertical_borders)
            self.vert2.add(vertical_borders)

    class Ball(pygame.sprite.Sprite):  # мячик
        def __init__(self, x, y, board: Board):
            super().__init__(all_sprites)
            self.board = board
            self.radius = board.cell_size // 4
            self.image = board.ball_im
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = pygame.Rect(board.left + (y + 0.25) * board.cell_size, board.top + (x - 0.75) * board.cell_size,
                                    2 * self.radius, 2 * self.radius)
            self.start_x = y + 0.25
            self.start_y = x - 0.75
            self.x = y + 0.25
            self.y = x - 0.75
            self.vx = 0
            self.vy = 0
            self.left = False
            self.right = False

        def update(self):
            # настройка физики
            self.x += self.vx
            self.y += self.vy
            self.rect = pygame.Rect(board.left + self.x * self.board.cell_size,
                                    board.top + self.y * self.board.cell_size, 2 * self.radius, 2 * self.radius)
            if self.vy <= 0.20:
                self.vy += 0.003
            if self.right:
                if self.vx < 0.04:
                    self.vx += 0.004
            elif self.left:
                if self.vx > -0.04:
                    self.vx -= 0.004
            else:
                self.vx = 0

            # взаимодействия с другими спрайтами
            if pygame.sprite.spritecollideany(self, break_borders):
                for spr in break_borders:
                    if pygame.sprite.collide_rect(self, spr):
                        spr.parent.breaks()
                        killed.append(spr.parent)
                self.vy = -0.090
                break_s.play()
            if pygame.sprite.spritecollideany(self, boost_borders):
                self.vy = -0.140
                boost_s.play()
            elif pygame.sprite.spritecollideany(self, horizontal_borders):
                spr = pygame.sprite.spritecollideany(self, horizontal_borders)
                if spr.rect.top > self.rect.top + self.radius:
                    self.vy = -0.090
                    jump_s.play()
                else:
                    self.vy = 0.090
            elif pygame.sprite.spritecollideany(self, vertical_borders):
                spr = pygame.sprite.spritecollideany(self, vertical_borders)
                if spr.rect.left > self.rect.left + self.radius:
                    self.vx = -0.05
                else:
                    self.vx = 0.05
            if pygame.sprite.collide_mask(self, self.board.red_fl):
                self.board.win = True
            if pygame.sprite.spritecollideany(self, spikes, collidemask):
                self.board.respawn()
                death_s.play()
            if pygame.sprite.spritecollideany(self, stars, collidemask):
                spr = pygame.sprite.spritecollideany(self, stars, collidemask)
                star_s.play()
                spr.kill()
                killed.append(spr)
                self.board.stars_count += 1
                stars_display.image = star_display_list[self.board.stars_count]

    class Spikes(pygame.sprite.Sprite):  # шипы
        def __init__(self, x, y, board: Board, trnsp=False):
            super().__init__()
            self.add(spikes)
            self.x = y
            self.y = x
            self.rect = pygame.Rect(board.left + y * board.cell_size, board.top + x * board.cell_size, board.cell_size,
                                    board.cell_size)

            if not trnsp:
                board.bg.blit(board.spikes_im, (board.left + y * board.cell_size, board.top + x * board.cell_size))

            self.image = board.spikes_im
            self.mask = pygame.mask.from_surface(self.image)

    class Star(pygame.sprite.Sprite):  # звезда
        def __init__(self, x, y, board: Board):
            super().__init__(all_sprites)
            self.add(stars)
            self.x = y
            self.y = x

            self.rect = pygame.Rect(board.left + y * board.cell_size, board.top + x * board.cell_size,
                                    board.cell_size, board.cell_size)
            self.image = board.star_im
            self.mask = pygame.mask.from_surface(self.image)

        def restore(self):
            self.add(all_sprites)
            self.add(stars)

    class GreenFlag(pygame.sprite.Sprite):  # старт
        def __init__(self, x, y, board: Board):
            super().__init__()
            self.board = board
            self.rect = pygame.Rect(board.left + y * board.cell_size, board.top + x * board.cell_size,
                                    board.cell_size, board.cell_size)
            self.image = board.grfl_im

            board.bg.blit(board.grfl_im, (board.left + y * board.cell_size, board.top + x * board.cell_size))

    class RedFlag(pygame.sprite.Sprite):  # финиш
        def __init__(self, x, y, board: Board):
            super().__init__()
            self.board = board
            self.rect = pygame.Rect(board.left + y * board.cell_size, board.top + x * board.cell_size,
                                    board.cell_size, board.cell_size)
            self.image = board.rfl_im

            board.bg.blit(board.rfl_im, (board.left + y * board.cell_size, board.top + x * board.cell_size))

    # ------------------------------------------------------------------------------------------------------------------
    # инициализация и настройка игрового поля
    map1 = maps[level - 1]
    width = len(map1[0])
    height = len(map1)
    # расчёт cell_size и инициализация Board
    if height * 2 > width:
        cell_size = 500 / height
        board = Board(map1, (1000 - width * cell_size) / 2, 100, cell_size, images)
    else:
        cell_size = 1000 / width
        board = Board(map1, 0, (500 - height * cell_size) / 2 + 100, cell_size, images)

    # ------------------------------------------------------------------------------------------------------------------
    # НАСТРОЙКА СПРАЙТОВ

    # настройка полупрозрачных окон
    im = pygame.Surface((1000, 100), pygame.SRCALPHA)
    pygame.draw.rect(im, (0, 0, 0, 150), (0, 0, 1000, 100), 0)
    im2 = pygame.Surface((1000, 600), pygame.SRCALPHA)
    pygame.draw.rect(im2, (0, 0, 0, 150), (0, 0, 1000, 600), 0)

    # настройка спрайтов переднего плана + курсор
    pause_button = pygame.sprite.Sprite(front_layer)
    pause_button.image = pause_im
    pause_button.rect = pygame.Rect(900, 0, 100, 100)

    font = pygame.font.Font(None, 75)
    text_sprite = pygame.sprite.Sprite(front_layer)
    text_sprite.image = font.render(f"Уровень {level}", True, (255, 255, 255))
    text_sprite.rect = pygame.Rect(500, 30, 100, 50)

    cursor = pygame.sprite.Sprite(cursor_group)
    cursor.image = cursor_im
    cursor.rect = cursor.image.get_rect()
    if pygame.mouse.get_focused():
        cursor.rect.topleft = pygame.mouse.get_pos()

    retry_butt = pygame.sprite.Sprite(pause_buttons)
    retry_butt.image = retry_butt_im
    retry_butt.rect = pygame.Rect(200, 240, 600, 100)

    sound_butt = pygame.sprite.Sprite(pause_buttons)
    sound_butt.image = sound_butt_im[sound_mode]
    sound_butt.rect = pygame.Rect(200, 355, 600, 100)

    menu_butt = pygame.sprite.Sprite(pause_buttons)
    menu_butt.image = menu_butt_im
    menu_butt.rect = pygame.Rect(200, 470, 600, 100)

    win_screen = pygame.sprite.Sprite(win_window)
    win_screen.image = end_level_im.copy()
    win_screen.rect = pygame.Rect(180, 80, 640, 440)
    win_screen.rect_menu = pygame.Rect(224, 380, 164, 92)
    win_screen.rect_retry = pygame.Rect(416, 380, 164, 92)
    win_screen.rect_next = pygame.Rect(608, 380, 164, 92)
    # ------------------------------------------------------------------------------------------------------------------
    # ИГРОВОЙ ЦИКЛ
    running = True
    pause = False
    clock = pygame.time.Clock()
    clock.tick(120)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1, sound_mode  # выход => -1
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.topleft = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                click_s.play()
                if win:
                    if win_screen.rect_menu.collidepoint(x, y):  # выход в меню с победой
                        return 1, sound_mode
                    if win_screen.rect_retry.collidepoint(x, y):  # заново с сохранением результата
                        return 2, sound_mode
                    if win_screen.rect_next.collidepoint(x, y):
                        return 3, sound_mode  # следующий уровень с сохранением резльтата
                else:
                    if pause:
                        if sound_butt.rect.collidepoint(x, y):
                            sound_mode = 1 - sound_mode
                            sound_butt.image = sound_butt_im[sound_mode]
                            for sound in sounds:
                                sound.set_volume(sound_mode)
                            star_s.set_volume(0.5 * sound_mode)
                        if menu_butt.rect.collidepoint(x, y):
                            return 0, sound_mode  # выход без победы
                        if retry_butt.rect.collidepoint(x, y):
                            pause = False
                            pause_button.image = pause_im
                            pause_button.rect = pygame.Rect(900, 0, 100, 100)
                            board.respawn()
                    if pause_button.rect.collidepoint(x, y):
                        pause = not pause
                        if pause:
                            pause_button.image = cont_butt_im
                            pause_button.rect = pygame.Rect(200, 125, 600, 100)
                        else:
                            pause_button.image = pause_im
                            pause_button.rect = pygame.Rect(900, 0, 100, 100)
            if event.type == pygame.KEYDOWN:
                if not pause and event.key == pygame.K_r:
                    board.respawn()
                if event.key == pygame.K_ESCAPE:
                    pause = not pause
                    if pause:
                        pause_button.image = cont_butt_im
                        pause_button.rect = pygame.Rect(200, 125, 600, 100)
                    else:
                        pause_button.image = pause_im
                        pause_button.rect = pygame.Rect(900, 0, 100, 100)
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    board.ball.left = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    board.ball.right = True
            if event.type == pygame.KEYUP:
                keys_state = pygame.key.get_pressed()
                if not keys_state[pygame.K_a] and not keys_state[pygame.K_LEFT]:
                    board.ball.left = False
                if not keys_state[pygame.K_d] and not keys_state[pygame.K_RIGHT]:
                    board.ball.right = False

        # проверка на выигрыш
        if not win and board.win:
            win = True
            win_screen.image.blit(star_display_list_big[board.stars_count], (20, 80))
            win_s.play()

            # сохранение результата
            if board.stars_count > scores[level - 1]:
                scores[level - 1] = board.stars_count
                spr.image = level_images[level - 1].copy()
                spr.image.blit(star_display_list_small[board.stars_count], (15, 55))

        # отрисовка
        screen.blit(board.bg, (0, 0))
        all_sprites.draw(screen)

        if win:
            win_window.draw(screen)
        else:
            # обновление или заливка
            if pause:
                screen.blit(im2, (0, 0))
                pause_buttons.draw(screen)
            else:
                screen.blit(im, (0, 0))
                all_sprites.update()

            # передний фон
            front_layer.draw(screen)

        # курсор
        if pygame.mouse.get_focused():
            cursor_group.draw(screen)

        pygame.display.flip()
        clock.tick(120)
