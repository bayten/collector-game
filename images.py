'''
images.py -- images submodule
=============================
This is module, where all image resources are loaded for future use.
'''

from pygame import image as im  # type: ignore
from typing import List
import utils as ut

# game sprites
BACK_IMG: ut.Image = im.load(r'images/back.png')
MAN_IMG: List[ut.Image] = [im.load(r'images/man'+str(x)+r'.png')
                           for x in range(2)]
LMAN_IMG: List[ut.Image] = [im.load(r'images/lman'+str(x)+r'.png')
                            for x in range(2)]
FMAN_IMG: List[ut.Image] = [im.load(r'images/fman'+str(x)+r'.png')
                            for x in range(2)]
DEATH_IMG: ut.Image = im.load(r'images/death.png')
MONEY_IMG: List[ut.Image] = [im.load(r'images/money'+str(x)+r'.png')
                             for x in range(6)]
WALL_IMG: ut.Image = im.load(r'images/wall.png')
SWALL_IMG: ut.Image = im.load(r'images/swall.png')
SPIKE_IMG: ut.Image = im.load(r'images/spikes.png')
DSPIKE_IMG: ut.Image = im.load(r'images/dspikes.png')
ENEMY_IMG: List[ut.Image] = [im.load(r'images/enemy'+str(x)+r'.png')
                             for x in range(4)]
BOMB_IMG: ut.Image = im.load(r'images/bomb.png')
BBOMB_IMG: List[ut.Image] = [im.load(r'images/bbomb'+str(x)+r'.png')
                             for x in range(3)]
BOOM_IMG: List[ut.Image] = [im.load(r'images/explosion'+str(x)+r'.png')
                            for x in range(7)]
FBONUS_IMG: List[ut.Image] = [im.load(r'images/fbonus'+str(x)+r'.png')
                              for x in range(4)]
IBONUS_IMG: List[ut.Image] = [im.load(r'images/ibonus'+str(x)+r'.png')
                              for x in range(4)]
LBONUS_IMG: List[ut.Image] = [im.load(r'images/lbonus'+str(x)+r'.png')
                              for x in range(4)]
CBONUS_IMG: List[ut.Image] = [im.load(r'images/cbonus'+str(x)+r'.png')
                              for x in range(4)]

# gui images
CURSOR_IMG: ut.Image = im.load(r'images/cursor.png')
BUTT_TMP_IMG: ut.Image = im.load(r'images/button_template.png')
BUTT_TMP_PRESSED_IMG: ut.Image = im.load(r'images/button_template_pressed.png')
BUTT_ACC_IMG: ut.Image = im.load(r'images/button_accept.png')
BUTT_CLS_IMG: ut.Image = im.load(r'images/button_close.png')
BUTT_BCK_IMG: ut.Image = im.load(r'images/button_back.png')
SPLASH_IMG: ut.Image = im.load(r'images/splash.png')
