#!/usr/bin/env python3
import pygame
import images
import random
import utils as ut
import objects as objs
# TODO: base object, player, gold, wall, bomb


def Init(sz, tile):
    '''Turn PyGame on'''
    global screen, screenrect
    pygame.init()
    screen = pygame.display.set_mode((sz[0] * tile, sz[1] * tile))
    screenrect = screen.get_rect()


class GameMode:
    '''Basic game mode'''
    def __init__(self):
        '''Set game mode up

        - Initialize field'''
        pass

    def Events(self, event):
        '''Event parser'''
        pass

    def Draw(self, screen):
        '''Draw game field'''
        screen.blit(self.back_img, (0, 0))

    def Logic(self, screen):
        '''Game logic: what to calculate'''
        pass

    def Leave(self):
        '''What to do when leaving this mode'''
        pass

    def Init(self):
        '''What to do when entering this mode'''
        wx = ut.BSIZE[0]*ut.TILE
        wy = ut.BSIZE[1]*ut.TILE
        self.back_img = pygame.Surface((wx, wy))
        for tx in range(ut.BSIZE[0]):
            for ty in range(ut.BSIZE[1]):
                self.back_img.blit(images.BACK_IMG, (tx*ut.TILE, ty*ut.TILE))


class Universe:
    '''Game universe'''

    def __init__(self, msec, tickevent=pygame.USEREVENT):
        '''Run an universe with msec tick'''
        self.msec = msec
        self.tickevent = tickevent

    def Start(self):
        '''Start running'''
        pygame.time.set_timer(self.tickevent, self.msec)

    def Finish(self):
        '''Shut down an universe'''
        pygame.time.set_timer(self.tickevent, 0)


class CollectorGame(GameMode):
    '''Game mode with active objects'''

    def __init__(self, player=objs.Player(), map=[], danger_objs=[],
                 bonus_objs=[], win_mode=ut.GameWinCondition.COLLECT_ALL):
        '''New game with active objects'''
        GameMode.__init__(self)
        self.player = player
        self.map = map
        self.danger_objs = danger_objs
        self.bonus_objs = bonus_objs
        self.win_mode = win_mode

    def load_level(self, file_name):
        '''Here we load level from filename'''
        pass

    def Events(self, event):
        '''Event parser:

        - Perform object action after every tick'''
        vx, vy = self.player.speed

        if event.type is pygame.KEYDOWN and event.key == pygame.K_LEFT:
            vx = -1
        elif event.type is pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            vx = 1

        if event.type is pygame.KEYDOWN and event.key == pygame.K_UP:
            vy = -1
        elif event.type is pygame.KEYDOWN and event.key == pygame.K_DOWN:
            vy = 1

        if event.type is pygame.KEYUP and event.key == pygame.K_LEFT:
            vx = 0
        if event.type is pygame.KEYUP and event.key == pygame.K_RIGHT:
            vx = 0

        if event.type is pygame.KEYUP and event.key == pygame.K_UP:
            vy = 0
        if event.type is pygame.KEYUP and event.key == pygame.K_DOWN:
            vy = 0

        self.player.speed = (vx, vy)
        GameMode.Events(self, event)

    def Action(self):
        for m_obj in self.map:
            m_obj.action()
        for d_obj in self.danger_objs:
            d_obj.action()
        for b_obj in self.bonus_objs:
            b_obj.action()
        self.player.action()

    def Logic(self):
        '''Game logic

        - Calculate objects' impact
        '''
        # GameMode.Logic(self, surface)

        for m_obj in self.map:
            m_obj.logic(self.player, self.map, self.danger_objs,
                        self.bonus_objs)

        self.player.logic(self.player, self.map,
                          self.danger_objs, self.bonus_objs)
        for d_obj in self.danger_objs:
            d_obj.logic(self.player, self.map,
                        self.danger_objs, self.bonus_objs)
        # Destroy()

    def Draw(self, surface):
        '''Draw game field

        - Draw all the objects on the top of game field

        '''
        GameMode.Draw(self, surface)
        for m_obj in self.map:
            m_obj.draw(surface)
        for c_obj in self.bonus_objs:
            c_obj.draw(surface)
        for d_obj in self.danger_objs:
            d_obj.draw(surface)
        self.player.draw(surface)

    def Destroy(self):
        for b_obj in self.bonus_objs:
            pass

    def Init(self):
        '''What to do when entering this mode'''
        super().Init()
        for x in range(10):
            rand_pos = (random.randint(1, 19), random.randint(1, 19))
            self.map.append(objs.Wall(rand_pos))


def __main__():
    '''Main game code'''
    # global Game

    Init(ut.BSIZE, ut.TILE)
    NewUniverse = Universe(int(1000./ut.FPS))
    NewUniverse.Start()

    CurrGame = CollectorGame()
    CurrGame.Init()
    game_trigger = True
    while game_trigger:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            game_trigger = False
        CurrGame.Events(event)
        CurrGame.Action()
        CurrGame.Logic()
        CurrGame.Draw(screen)
        pygame.display.flip()
    NewUniverse.Finish()
    pygame.quit()


if __name__ == '__main__':
    __main__()
