import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


jump_s = pygame.mixer.Sound("data/jumps.wav")
death_s = pygame.mixer.Sound("data/deaths.wav")
star_s = pygame.mixer.Sound("data/stars.wav")
boost_s = pygame.mixer.Sound("data/boosts.wav")
break_s = pygame.mixer.Sound("data/breaks.wav")
click_s = pygame.mixer.Sound("data/click.wav")
new_game_s = pygame.mixer.Sound("data/new_game.wav")
select_s = pygame.mixer.Sound('data/select.wav')
win_s = pygame.mixer.Sound('data/win.wav')
sounds = [jump_s, death_s, star_s, boost_s, break_s]

star_display_list = [pygame.transform.scale(load_image('stars0.png'), (300, 100)),
                     pygame.transform.scale(load_image('stars1.png'), (300, 100)),
                     pygame.transform.scale(load_image('stars2.png'), (300, 100)),
                     pygame.transform.scale(load_image('stars3.png'), (300, 100))]

star_display_list_small = [pygame.transform.scale(load_image('stars0.png'), (120, 40)),
                           pygame.transform.scale(load_image('stars1.png'), (120, 40)),
                           pygame.transform.scale(load_image('stars2.png'), (120, 40)),
                           pygame.transform.scale(load_image('stars3.png'), (120, 40))]

star_display_list_big = [pygame.transform.scale(load_image('stars0.png'), (600, 200)),
                         pygame.transform.scale(load_image('stars1.png'), (600, 200)),
                         pygame.transform.scale(load_image('stars2.png'), (600, 200)),
                         pygame.transform.scale(load_image('stars3.png'), (600, 200))]

pause_im = pygame.transform.scale(load_image('pause.png'), (100, 100))

block_im = load_image('block.png')
boost_im = load_image('boost.png')
break_im = load_image('break.png')
spikes_im = load_image('spikes.png')
star_im = load_image('star.png')
grfl_im = load_image('greenflag.png')
rfl_im = load_image('redflag.png')
bg = [pygame.transform.scale(load_image('skybg.jpg'), (1072, 600)),
      pygame.transform.scale(load_image('skybg_night.jpg'), (1200, 600)),
      pygame.transform.scale(load_image('bg_stars.jpg'), (1067, 600)),
      pygame.transform.scale(load_image('bg_grass1.jpg'), (1200, 600))]

menu_ball_im = {}
image0 = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
menu_ball_im['menu'] = pygame.Surface((30, 30), pygame.SRCALPHA, 32)
pygame.draw.circle(menu_ball_im['menu'], pygame.Color("white"), (15, 15), 15)
menu_ball_im['sett'] = pygame.transform.scale(load_image('ball_sett.png'), (30, 30))
menu_ball_im['player sett ball'] = pygame.transform.scale(load_image('ball_player_sett.png'), (30, 30))

cursor_im = pygame.transform.scale(load_image('mouse.png'), (20, 20))

cont_butt_im = load_image('cont_butt.png')
menu_butt_im = load_image('menu_butt.png')
retry_butt_im = load_image('retry_butt.png')

reset_butt_im = pygame.transform.scale(load_image('reset_butt.png'), (450, 75))
sound_butt_im = (load_image('s_off_butt.png'), load_image('s_on_butt.png'))
music_butt_im = (pygame.transform.scale(load_image('m_off_butt.png'), (450, 75)),
                 pygame.transform.scale(load_image('m_on_butt.png'), (450, 75)))
sound_butt_im_sett = (pygame.transform.scale(load_image('s_off_butt.png'), (450, 75)),
                      pygame.transform.scale(load_image('s_on_butt.png'), (450, 75)))

end_level_im = load_image('end_level.png')
confirm_im = load_image('confirm.png')
quit_im = pygame.transform.scale(load_image('quit.png'), (640, 440))

images = [block_im, boost_im, break_im, spikes_im, star_im, grfl_im, rfl_im]
level_images = [pygame.transform.scale(load_image(f'levels/level{i}.png'), (150, 100)) for i in range(1, 17)]

ball_im = [pygame.Surface((100, 100), pygame.SRCALPHA, 32),
           pygame.Surface((100, 100), pygame.SRCALPHA, 32),
           pygame.Surface((100, 100), pygame.SRCALPHA, 32),
           pygame.Surface((100, 100), pygame.SRCALPHA, 32),
           pygame.Surface((100, 100), pygame.SRCALPHA, 32),
           load_image('ball_skins/angry.png'),
           load_image('ball_skins/dead.png'),
           load_image('ball_skins/happy.png'),
           load_image('ball_skins/jumpball.png'),
           load_image('ball_skins/premiumball.png')]

final_im = load_image('final.png')

pygame.draw.circle(ball_im[0], pygame.Color("white"), (50, 50), 50)
pygame.draw.circle(ball_im[1], pygame.Color((255, 50, 50)), (50, 50), 50)
pygame.draw.circle(ball_im[2], pygame.Color((100, 255, 100)), (50, 50), 50)
pygame.draw.circle(ball_im[3], pygame.Color((200, 175, 255)), (50, 50), 50)
pygame.draw.circle(ball_im[4], pygame.Color("black"), (50, 50), 50)

star_count_im = pygame.Surface((175, 75), pygame.SRCALPHA, 32)
pygame.draw.rect(star_count_im, (0, 0, 0, 150), (0, 0, 175, 75), 0)
star_count_im.blit(pygame.transform.scale(star_im, (75, 75)), (0, 0))

ball_on_im = pygame.transform.scale(load_image('ball_on.png'), (126, 75))
ball_off_im = pygame.transform.scale(load_image('ball_off.png'), (78, 75))
bg_on_im = pygame.transform.scale(load_image('bg_on.png'), (126, 75))
bg_off_im = pygame.transform.scale(load_image('bg_off.png'), (78, 75))

skin_ims = ([(load_image(f'ball_skins/0_0.png'),)] +
            [(load_image(f'ball_skins/{i}_0.png'), load_image(f'ball_skins/{i}_1.png')) for i in range(1, 10)])

costs = {0: 0,
         1: 3,
         2: 9,
         3: 15,
         4: 21,
         5: 24,
         6: 27,
         7: 30,
         8: 33,
         9: 36}

bg_ims = [pygame.Surface((200, 120), pygame.SRCALPHA, 32),
          pygame.Surface((200, 120), pygame.SRCALPHA, 32),
          pygame.Surface((200, 120), pygame.SRCALPHA, 32),
          pygame.Surface((200, 120), pygame.SRCALPHA, 32)]

bg_ims[0].blit(pygame.transform.scale(load_image('skybg.jpg'), (200, 120)), (0, 0))
bg_ims[1].blit(pygame.transform.scale(load_image('skybg_night.jpg'), (240, 120)), (0, 0))
bg_ims[2].blit(pygame.transform.scale(load_image('bg_stars.jpg'), (200, 120)), (0, 0))
bg_ims[3].blit(pygame.transform.scale(load_image('bg_grass.jpg'), (240, 120)), (0, 0))

for i in range(4):
    pygame.draw.rect(bg_ims[i], (132, 83, 79, 150), (0, 0, 200, 120), 4)

