from pygame import image

# game sprites
BACK_IMG = image.load(r'images/back.png')
MAN_IMG = [image.load(r'images/man'+str(x)+r'.png') for x in range(2)]
LMAN_IMG = [image.load(r'images/lman'+str(x)+r'.png') for x in range(2)]
FMAN_IMG = [image.load(r'images/fman'+str(x)+r'.png') for x in range(2)]
DEATH_IMG = image.load(r'images/death.png')
MONEY_IMG = [image.load(r'images/money'+str(x)+r'.png') for x in range(6)]
WALL_IMG = image.load(r'images/wall.png')
SWALL_IMG = image.load(r'images/swall.png')
SPIKE_IMG = image.load(r'images/spikes.png')
DSPIKE_IMG = image.load(r'images/dspikes.png')
ENEMY_IMG = [image.load(r'images/enemy'+str(x)+r'.png') for x in range(4)]
BOMB_IMG = image.load(r'images/bomb.png')
BBOMB_IMG = [image.load(r'images/bbomb'+str(x)+r'.png') for x in range(3)]
BOOM_IMG = [image.load(r'images/explosion'+str(x)+r'.png') for x in range(7)]
FBONUS_IMG = [image.load(r'images/fbonus'+str(x)+r'.png') for x in range(4)]
IBONUS_IMG = [image.load(r'images/ibonus'+str(x)+r'.png') for x in range(4)]
LBONUS_IMG = [image.load(r'images/lbonus'+str(x)+r'.png') for x in range(4)]
CBONUS_IMG = [image.load(r'images/cbonus'+str(x)+r'.png') for x in range(4)]

# gui images
CURSOR_IMG = image.load(r'images/cursor.png')
BUTT_TMP_IMG = image.load(r'images/button_template.png')
BUTT_TMP_PRESSED_IMG = image.load(r'images/button_template_pressed.png')
BUTT_ACC_IMG = image.load(r'images/button_accept.png')
BUTT_CLS_IMG = image.load(r'images/button_close.png')
BUTT_BCK_IMG = image.load(r'images/button_back.png')
SPLASH_IMG = image.load(r'images/splash.png')
