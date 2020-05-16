"""
tests.py -- module with unit-tests
==================================
This is module, which contains unit-tests for all classes and functions.
"""
from CollectorGame import utils as ut
from CollectorGame import images

from CollectorGame import objects as objs
from CollectorGame import gui
from CollectorGame import modes


# tests for CollectorGame/objects.py
def test_objects_BasicObject() -> None:
    """Unit-test for BasicObject class"""
    img = images.BOOM_IMG
    img2 = [images.BACK_IMG]

    pos = (5, 5)
    pos2 = (2, 2)

    speed = (5, 5)
    speed2 = (2, 2)

    logic_params_stub = (objs.Player(), [], [], [])

    # Test 0: incorrect initial values
    test = objs.BasicObject(img, (-1, -1))
    assert 0 <= test.pos[0] < ut.BSIZE[0]
    assert 0 <= test.pos[1] < ut.BSIZE[1]

    test = objs.BasicObject(img, ut.BSIZE)
    assert 0 <= test.pos[0] < ut.BSIZE[0]
    assert 0 <= test.pos[1] < ut.BSIZE[1]

    test = objs.BasicObject(img, pos, ut.BSIZE)
    assert abs(test.speed[0]) < ut.BSIZE[0]
    assert abs(test.speed[1]) < ut.BSIZE[1]

    test = objs.BasicObject([], pos, ut.BSIZE)
    assert len(test.img) > 0

    # Test 1: correct values of 'init' variables
    test = objs.BasicObject(img, pos, speed)
    assert test.pos == test.init_pos
    assert test.speed == test.init_speed

    # Test 2: 'init' variables are properly copied
    test = objs.BasicObject(img, pos, speed)
    test.pos = pos2
    test.speed = pos2
    assert test.pos is not test.init_pos
    assert test.pos != test.init_pos
    assert test.speed is not test.init_speed
    assert test.speed != test.init_speed

    # Test 3: proper work of copy() method
    test = objs.BasicObject(img, pos, speed)
    test2 = test.copy()

    assert test.pos == test2.pos
    assert test.speed == test2.speed
    assert test.init_pos == test2.init_pos
    assert test.init_speed == test2.init_speed
    assert test.is_dead == test2.is_dead
    assert len(test.img) == len(test2.img)
    for img_idx in range(len(test.img)):
        # There is some strange behaviour with pygame.Surface comparison
        # assert test.img[img_idx] == test2.img[img_idx]
        assert test.img[img_idx] is not test2.img[img_idx]

    test.pos = pos2
    test.speed = speed2
    test.is_dead = True
    test.img[0] = img2[0]

    assert test.pos != test2.pos
    assert test.speed != test2.speed
    assert test.is_dead != test2.is_dead
    assert test.img[0] != test2.img[0]

    # Test 4: proper work of reset() method
    test = objs.BasicObject(img, pos, speed)
    test.pos = pos2
    test.speed = speed2
    test.is_dead = True
    test.reset()

    assert test.pos == pos
    assert test.speed == speed
    assert test.is_dead is False

    # Test 5: proper work of logic() method
    test = objs.BasicObject(img, ut.BSIZE, ut.BSIZE)
    test.logic(*logic_params_stub)

    assert 0 <= test.pos[0] < ut.BSIZE[0]
    assert 0 <= test.pos[1] < ut.BSIZE[1]
    assert abs(test.speed[0]) < ut.BSIZE[0]
    assert abs(test.speed[1]) < ut.BSIZE[1]

    test = objs.BasicObject(img, (-1, -1), (-1, -1))
    test.logic(*logic_params_stub)

    assert 0 <= test.pos[0] < ut.BSIZE[0]
    assert 0 <= test.pos[1] < ut.BSIZE[1]
    assert abs(test.speed[0]) < ut.BSIZE[0]
    assert abs(test.speed[1]) < ut.BSIZE[1]


def test_objects_Player() -> None:
    """Unit-test for Player class"""
    pos = (5, 5)
    pos2 = (2, 2)
    speed2 = (2, 2)
    bombs_max = 3
    gold_max = 10

    # Test 0: incorrect initial values
    test = objs.Player(pos, (-1, bombs_max), (-1, gold_max))
    assert 0 <= test.bombs[0] <= bombs_max
    assert 0 <= test.gold[0] <= gold_max

    test = objs.Player(pos, (bombs_max+1, bombs_max), (gold_max+1, gold_max))
    assert 0 <= test.bombs[0] <= bombs_max
    assert 0 <= test.gold[0] <= gold_max

    # Test 1: correct values of 'init' variables
    test = objs.Player(pos, (bombs_max, bombs_max), (0, gold_max))
    assert test.bombs == test.init_bombs
    assert test.gold == test.init_gold

    # Test 2: 'init' variables are properly copied
    test = objs.Player(pos, (bombs_max, bombs_max), (0, gold_max))
    test.bombs = test.bombs[0] - 1, test.bombs[1] - 1
    test.gold = test.gold[0] + 1, test.gold[1] - 1

    assert test.bombs is not test.init_bombs
    assert test.bombs != test.init_bombs
    assert test.gold is not test.init_gold
    assert test.gold != test.init_gold

    # Test 3: proper work of reset() method
    test = objs.Player(pos, (bombs_max, bombs_max), (0, gold_max))
    test.pos = pos2
    test.speed = speed2
    test.is_dead = True
    test.sight = (1, 0)
    test.bombs = test.bombs[0] - 1, test.bombs[1] - 1
    test.gold = test.gold[0] + 1, test.gold[1] - 1
    test.set_bomb = True
    test.duration += 1
    test.reset()

    assert test.pos == pos
    assert test.speed == (0, 0)
    assert test.is_dead is False
    assert test.sight == (0, 0)
    assert test.bombs == (bombs_max, bombs_max)
    assert test.gold == (0, gold_max)
    assert test.set_bomb is False
    assert test.duration == 5


# tests for CollectorGame/gui.py
def test_gui_GuiObject() -> None:
    """Unit-test for GuiObject class"""
    pos = (200, 200)
    size = (100, 100)
    wsize = (ut.BSIZE[0] * ut.TILE, ut.BSIZE[1] * ut.TILE)

    cpos_x = pos[0], pos[0]+int(size[0]/2), pos[0]+size[0]
    cpos_y = pos[1], pos[1]+int(size[1]/2), pos[1]+size[1]

    # Test 0: incorrect initial values
    test = gui.GuiObject((-1, -1), (-1, -1))
    assert 0 <= test.pos[0] < wsize[0]
    assert 0 <= test.pos[1] < wsize[1]
    assert test.size[0] > 0
    assert test.size[1] > 0

    test = gui.GuiObject(ut.BSIZE, (0, 0))
    assert 0 <= test.pos[0] < wsize[0]
    assert 0 <= test.pos[1] < wsize[1]
    assert test.size[0] > 0
    assert test.size[1] > 0

    # Test 1: proper work of includes() method
    test = gui.GuiObject(pos, size)
    for ix in range(3):
        for iy in range(3):
            assert test.includes((cpos_x[ix], cpos_y[iy])) is True

    for ix in range(3):
        for iy in range(3):
            if ix == iy and iy == 1:
                continue
            assert test.includes((cpos_x[ix]+ix-1, cpos_y[iy]+iy-1)) is False

    # Test 2: proper work of can_focus() method
    test = gui.GuiObject(pos, size)

    for ix in range(3):
        for iy in range(3):
            assert test.can_focus((cpos_x[ix], cpos_y[iy])) is True

    for ix in range(3):
        for iy in range(3):
            if ix == iy and iy == 1:
                continue
            assert test.can_focus((cpos_x[ix]+ix-1, cpos_y[iy]+iy-1)) is False


def test_gui_Button() -> None:
    """Unit-test for Button class"""
    pos = 200, 200
    size = 100, 100
    cpos_x = pos[0], pos[0] + int(size[0] / 2), pos[0] + size[0]
    cpos_y = pos[1], pos[1] + int(size[1] / 2), pos[1] + size[1]
    wsize = (ut.BSIZE[0] * ut.TILE, ut.BSIZE[1] * ut.TILE)

    img = images.BUTT_TMP_IMG
    img2 = images.SPLASH_IMG
    img3 = images.BACK_IMG

    tname = 'test_trigger'
    text = ('test', ut.GAME_FONT)
    triggers1 = [('test_trigger', 0, 2)]
    triggers2 = [('test_trig', 0, 4), ('test_trigger', 4, 3), ('t', 3, 4)]

    # Test 0: incorrect initial values
    test = gui.Button((-1, -1), (-1, -1), tname, img)
    assert 0 <= test.pos[0] < wsize[0]
    assert 0 <= test.pos[1] < wsize[1]
    assert test.size[0] > 0
    assert test.size[1] > 0
    assert test.text is None

    test = gui.Button(wsize, (0, 0), tname, img, None, text)
    assert 0 <= test.pos[0] < wsize[0]
    assert 0 <= test.pos[1] < wsize[1]
    assert test.size[0] > 0
    assert test.size[1] > 0
    assert test.text is not None

    test = gui.Button(pos, size, tname, img2)
    assert test.image.get_size()[0] == size[0]
    assert test.image.get_size()[1] == size[1]

    test = gui.Button(pos, size, tname, img3)
    assert test.image.get_size()[0] == size[0]
    assert test.image.get_size()[1] == size[1]

    # Test 1: proper work of init_pdown() method

    for ix in range(3):
        for iy in range(3):
            test = gui.Button(pos, size, tname, img)
            test.init_pdown((cpos_x[ix], cpos_y[iy]))
            assert test.is_pressed is True

            test = gui.Button(pos, size, tname, img, None, text)
            test.init_pdown((cpos_x[ix], cpos_y[iy]))
            assert test.is_pressed is True
            assert test.text.is_pressed is True

    for ix in range(3):
        for iy in range(3):
            if ix == iy and iy == 1:
                continue

            test = gui.Button(pos, size, tname, img)
            test.init_pdown((cpos_x[ix]+ix-1, cpos_y[iy]+iy-1))
            assert test.is_pressed is False

            test = gui.Button(pos, size, tname, img, None, text)
            test.init_pdown((cpos_x[ix]+ix-1, cpos_y[iy]+iy-1))
            assert test.is_pressed is False
            assert test.text.is_pressed is False

    # Test 2: proper work of init_pup() method
    test = gui.Button(pos, size, tname, img)
    test.init_pdown((cpos_x[1], cpos_y[1]))
    test.init_pup((cpos_x[1], cpos_y[1]))
    assert test.is_pressed is False

    test = gui.Button(pos, size, tname, img)
    test.init_pdown((cpos_x[1], cpos_y[1]))
    test.init_pup((cpos_x[1], cpos_y[1]), [])

    test = gui.Button(pos, size, tname, img)
    test.init_pdown((cpos_x[1], cpos_y[1]))
    test.init_pup((cpos_x[1], cpos_y[1]), triggers1)
    assert triggers1[0][1] == 1

    test = gui.Button(pos, size, tname, img)
    test.init_pdown((cpos_x[1], cpos_y[1]))
    test.init_pup((cpos_x[1], cpos_y[1]), triggers2)
    assert triggers2[1][1] == 2

    triggers1 = [('test_trigger', 0, 2)]
    triggers2 = [('test_trig', 0, 4), ('test_trigger', 4, 3), ('t', 3, 4)]

    test = gui.Button(pos, size, tname, img, None, text)
    test.init_pdown((cpos_x[1], cpos_y[1]))
    test.init_pup((cpos_x[1], cpos_y[1]))
    assert test.is_pressed is False
    assert test.text.is_pressed is False

    test = gui.Button(pos, size, tname, img, None, text)
    test.init_pdown((cpos_x[1], cpos_y[1]))
    test.init_pup((cpos_x[1], cpos_y[1]), [])

    test = gui.Button(pos, size, tname, img, None, text)
    test.init_pdown((cpos_x[1], cpos_y[1]))
    test.init_pup((cpos_x[1], cpos_y[1]), triggers1)
    assert triggers1[0][1] == 1

    test = gui.Button(pos, size, tname, img, None, text)
    test.init_pdown((cpos_x[1], cpos_y[1]))
    test.init_pup((cpos_x[1], cpos_y[1]), triggers2)
    assert triggers2[1][1] == 2


def test_gui_MenuMode() -> None:
    """Unit-test for MenuMode class"""
    img = images.SPLASH_IMG
    pos = (0, 0)
    wsize = (ut.BSIZE[0] * ut.TILE, ut.BSIZE[1] * ut.TILE)

    b_pos1 = (pos[0], pos[1])
    b_pos2 = (pos[0]+50, pos[1]+50)
    b_size = (100, 100)
    b_img = images.BUTT_TMP_IMG

    test_gui = [gui.Button(b_pos1, b_size, 'trigger_1', b_img),
                gui.Button(b_pos2, b_size, 'trigger_2', b_img)]
    trigs = [('trigger1', 0, 2), ('trigger2', 0, 2)]

    # Test 0: incorrect initial values
    test = gui.MenuMode(img, (-1, -1))
    assert 0 <= test.menu_pos[0] < wsize[0]
    assert 0 <= test.menu_pos[1] < wsize[1]
    assert test.focused is None
    assert test.gui is None
    assert test.triggers is None

    test = gui.MenuMode(img, wsize)
    assert 0 <= test.menu_pos[0] < wsize[0]
    assert 0 <= test.menu_pos[1] < wsize[1]
    assert test.focused is None
    assert test.gui is None
    assert test.triggers is None

    # Test 1: proper work of init() method
    # pygame.display.init()
    # test = gui.MenuMode(img, pos, test_gui, trigs)
    # test.init(dummy_screen)
    # assert pygame.mouse.get_visible() is False  # only from pygame 2.0.0
    # pygame.mouse.set_visible(True)

    # Test 2: proper work of update_focus() method
    test = gui.MenuMode(img, pos, test_gui, trigs)
    test.update_focus((25, 25))
    assert test.focused == 0
    test.update_focus((50, 50))
    assert test.focused == 0
    test.update_focus((75, 75))
    assert test.focused == 0
    test.update_focus((125, 125))
    assert test.focused == 1
    test.update_focus((100, 100))
    assert test.focused == 1
    test.update_focus((75, 75))
    assert test.focused == 1
    test.update_focus((0, 150))
    assert test.focused is None
    test.update_focus((75, 75))
    assert test.focused == 0

    # Test 3: proper work of events() method

    # Test 4: proper work of leave() method
    # test = gui.MenuMode()
    # test.init()
    # test.leave()
    # assert pygame.mouse.get_visible() is True


# tests for CollectorGame/modes.py
def test_modes_GameMode() -> None:
    """Unit-test for GameMode class"""
    # Test 0: proper work of __init__ method
    test = modes.GameMode()
    assert test.back_img is None

    # Test 1: proper work of init() method
    test = modes.GameMode()
    test.init()
    size = (ut.BSIZE[0]*ut.TILE, ut.BSIZE[1]*ut.TILE)
    assert test.back_img.get_size() == size


def test_modes_Universe() -> None:
    """Unit-test for Universe class"""
    pass


def test_modes_CollectorGame():
    """Unit-test for CollectorGame class"""
    pass


# ultimate test function
def do_ultimate_check() -> None:
    """Check every single test possible"""
    # test objects.py
    test_objects_BasicObject()
    test_objects_Player()

    # test gui.py
    test_gui_GuiObject()
    test_gui_Button()
    test_gui_MenuMode()

    # test modes.py
    test_modes_GameMode()
    # test_modes_Universe()
    # test_modes_CollectorGame()
