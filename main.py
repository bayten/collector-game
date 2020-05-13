#!/usr/bin/env python3
import pygame
import images
import random
import utils as ut
import objects as objs


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

    def __init__(self, player=objs.Player(), map=[], enemies=[],
                 tempies=[], win_mode=ut.GameWinCondition.COLLECT_ALL):
        '''New game with active objects'''
        GameMode.__init__(self)
        self.player = player
        self.map = map
        self.enemies = enemies
        self.tempies = tempies
        self.win_mode = win_mode

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
        for map_object in self.map:
            map_object.action()
        for enemy in self.enemies:
            enemy.action()
        for temp_effect in self.tempies:
            temp_effect.action()
        self.player.action()

    def Logic(self):
        '''Game logic

        - Calculate objects' impact
        '''
        self.player.logic(self.player, self.map, self.enemies, self.tempies)

        for map_object in self.map:
            map_object.logic(self.player, self.map, self.enemies, self.tempies)

        for tmp_effect in self.tempies:
            tmp_effect.logic(self.player, self.map, self.enemies, self.tempies)
        for enemy in self.enemies:
            enemy.logic(self.player, self.map, self.enemies, self.tempies)

        self.Destroy()

    def Draw(self, surface):
        '''Draw game field

        - Draw all the objects on the top of game field

        '''
        GameMode.Draw(self, surface)
        for map_object in self.map:
            map_object.draw(surface)
        for enemy in self.enemies:
            enemy.draw(surface)
        for tmp_effect in self.tempies:
            tmp_effect.draw(surface)

        self.player.draw(surface)

    def Destroy(self):
        for idx, tmp_effect in enumerate(self.tempies):
            if tmp_effect.duration <= 0:
                tmp_effect.destroy()
                del self.tempies[idx]

        for idx, map_object in enumerate(self.map):
            if map_object.is_dead:
                map_object.destroy()
                del self.map[idx]

        for idx, enemy in enumerate(self.enemies):
            if enemy.is_dead:
                enemy.destroy()
                del self.enemies[idx]

    def GameStateCheck(self):
        '''Check for win-lose condition + spash screen'''
        if self.player.is_dead:
            # self.LoserSplashScreen()
            print("HA-HA! LOSER!")
            return True

        elif self.win_mode == ut.GameWinCondition.COLLECT_ALL:
            if self.player.gold[0] >= self.player.gold[1]:
                # self.VictorySplashScreen()
                print("CONGRATULATIONS!")
                return True
        elif self.win_mode == ut.GameWinCondition.KILL_ALL:
            if len(self.enemies) == 0:
                # self.VictorySplashScreen()
                print("CONGRATULATIONS!")
                return True

        elif self.win_mode == ut.GameWinCondition.GET_GOAL:
            if self.player.gold[0] > 0:
                # self.VictorySplashScreen()
                print("CONGRATULATIONS!")
                return True
        return False

    def Init(self):
        '''What to do when entering this mode'''
        super().Init()
        for x in range(10):
            rand_pos = (random.randint(1, 19), random.randint(1, 19))
            self.map.append(objs.Spikes(rand_pos, False))

        for x in range(10):
            rand_pos = (random.randint(1, 19), random.randint(1, 19))
            self.map.append(objs.Gold(rand_pos))

        for x in range(5):
            rand_pos = (random.randint(1, 19), random.randint(1, 19))
            rand_speed = (random.randint(-1, 1), random.randint(-1, 1))
            self.enemies.append(objs.Enemy(rand_pos, rand_speed))

        self.player.gold = (0, 10)


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
        game_state = CurrGame.GameStateCheck()
        pygame.display.flip()
        if game_state is True:
            break
    NewUniverse.Finish()
    pygame.quit()


if __name__ == '__main__':
    __main__()
