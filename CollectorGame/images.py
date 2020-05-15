'''
images.py -- images submodule
=============================
This is module, where all image resources are loaded for future use.
'''

from pygame import image as im  # type: ignore
from typing import List
import CollectorGame.utils as ut

DIR = r'CollectorGame/images/'


# game sprites
BACK_IMG: ut.Image = im.load(DIR+r'back.png')
MAN_IMG: List[ut.Image] = [im.load(DIR+r'man'+str(x)+r'.png')
                           for x in range(2)]
LMAN_IMG: List[ut.Image] = [im.load(DIR+r'lman'+str(x)+r'.png')
                            for x in range(2)]
FMAN_IMG: List[ut.Image] = [im.load(DIR+r'fman'+str(x)+r'.png')
                            for x in range(2)]
DEATH_IMG: ut.Image = im.load(DIR+r'death.png')
MONEY_IMG: List[ut.Image] = [im.load(DIR+r'money'+str(x)+r'.png')
                             for x in range(6)]
WALL_IMG: ut.Image = im.load(DIR+r'wall.png')
SWALL_IMG: ut.Image = im.load(DIR+r'swall.png')
SPIKE_IMG: ut.Image = im.load(DIR+r'spikes.png')
DSPIKE_IMG: ut.Image = im.load(DIR+r'dspikes.png')
ENEMY_IMG: List[ut.Image] = [im.load(DIR+r'enemy'+str(x)+r'.png')
                             for x in range(4)]
BOMB_IMG: ut.Image = im.load(DIR+r'bomb.png')
BBOMB_IMG: List[ut.Image] = [im.load(DIR+r'bbomb'+str(x)+r'.png')
                             for x in range(3)]
BOOM_IMG: List[ut.Image] = [im.load(DIR+r'explosion'+str(x)+r'.png')
                            for x in range(7)]
FBONUS_IMG: List[ut.Image] = [im.load(DIR+r'fbonus'+str(x)+r'.png')
                              for x in range(4)]
IBONUS_IMG: List[ut.Image] = [im.load(DIR+r'ibonus'+str(x)+r'.png')
                              for x in range(4)]
LBONUS_IMG: List[ut.Image] = [im.load(DIR+r'lbonus'+str(x)+r'.png')
                              for x in range(4)]
CBONUS_IMG: List[ut.Image] = [im.load(DIR+r'cbonus'+str(x)+r'.png')
                              for x in range(4)]

# gui images
CURSOR_IMG: ut.Image = im.load(DIR+r'cursor.png')
BUTT_TMP_IMG: ut.Image = im.load(DIR+r'button_template.png')
BUTT_TMP_PRESSED_IMG: ut.Image = im.load(DIR+r'button_template_pressed.png')
BUTT_ACC_IMG: ut.Image = im.load(DIR+r'button_accept.png')
BUTT_CLS_IMG: ut.Image = im.load(DIR+r'button_close.png')
BUTT_BCK_IMG: ut.Image = im.load(DIR+r'button_back.png')
SPLASH_IMG: ut.Image = im.load(DIR+r'splash.png')
