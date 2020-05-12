from pygame import image

BACK_IMG = image.load(r'images/back.png')
MAN_IMG = [image.load(r'images/man'+str(x)+r'.png') for x in range(2)]
FMAN_IMG = [image.load(r'images/fman'+str(x)+r'.png') for x in range(2)]
DEATH_IMG = image.load(r'images/death.png')
MONEY_IMG = [image.load(r'images/money'+str(x)+r'.png') for x in range(6)]
WALL_IMG = image.load(r'images/wall.png')
SWALL_IMG = image.load(r'images/swall.png')
SPIKE_IMG = image.load(r'images/spikes.png')
DSPIKE_IMG = image.load(r'images/dspikes.png')
ENEMY_IMG = [image.load(r'images/enemy'+str(x)+r'.png') for x in range(3)]
BOMB_IMG = image.load(r'images/bomb.png')
BONUS_IMG = image.load(r'images/bonus.png')
BBOMB_IMG = [image.load(r'images/bbomb'+str(x)+r'.png') for x in range(3)]
