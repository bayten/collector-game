#!/usr/bin/env python3
import pygame
import images
import random
import utils as ut
import objects as objs
import gui


class GameMode:
    '''Basic game mode'''
    def __init__(self):
        '''Set game mode up

        - Initialize field'''
        pass

    def Events(self, event, screen):
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

    def __init__(self, sz, tile):
        '''Run an universe with msec tick'''
        pygame.init()
        self.screen = pygame.display.set_mode((sz[0] * tile, sz[1] * tile))
        self.screenrect = self.screen.get_rect()
        self.game_clock = pygame.time.Clock()
        self.time_delay = int(1000./ut.FPS)
        self.game_mode = None

    def ProcessGame(self, game_mode):
        self.game_mode = game_mode
        self.Start()
        self.MainLoop()
        self.Finish()

    def Start(self):
        '''Start running'''
        self.game_mode.Init()

    def MainLoop(self):
        game_trigger = True
        while game_trigger:
            events = pygame.event.get()
            game_trigger = self.game_mode.Events(events, self.screen)
            self.game_mode.Action()
            self.game_mode.Logic()
            self.game_mode.Draw(self.screen)
            game_state = self.game_mode.GameStateCheck(self.screen)
            pygame.display.flip()
            if game_state is True:
                break
            self.game_clock.tick(self.time_delay)
        self.game_mode.Leave()

    def Finish(self):
        '''Shut down an universe'''
        pygame.quit()


class CollectorGame(GameMode):
    '''Game mode with active objects'''

    def __init__(self, player=objs.Player((0, 0), (3, 3), (0, 10)), map=[],
                 enemies=[], tempies=[],
                 win_mode=ut.GameWinCondition.COLLECT_ALL):
        '''New game with active objects'''
        GameMode.__init__(self)
        self.player = player
        self.map = map
        self.init_map = [map_object.copy() for map_object in self.map]
        self.enemies = enemies
        self.init_enemies = [enemy.copy() for enemy in self.enemies]
        self.tempies = tempies
        self.win_mode = win_mode

    def Events(self, events, screen):
        '''Event parser:

        - Perform object action after every tick'''
        vx, vy = self.player.speed
        sight = self.player.sight

        for event in events:
            if event.type is pygame.QUIT:
                dialog = gui.CloseDialog()
                if dialog.MainLoop(screen):
                    return False

            if event.type is pygame.KEYDOWN and event.key == pygame.K_LEFT:
                vx = -1
                sight = (-1, 0)
            elif event.type is pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                vx = 1
                sight = (1, 0)
            if event.type is pygame.KEYDOWN and event.key == pygame.K_UP:
                vy = -1
                sight = (0, -1)
            elif event.type is pygame.KEYDOWN and event.key == pygame.K_DOWN:
                vy = 1
                sight = (0, 1)

            if event.type is pygame.KEYUP and event.key == pygame.K_LEFT:
                vx = 0
            if event.type is pygame.KEYUP and event.key == pygame.K_RIGHT:
                vx = 0
            if event.type is pygame.KEYUP and event.key == pygame.K_UP:
                vy = 0
            if event.type is pygame.KEYUP and event.key == pygame.K_DOWN:
                vy = 0

            if event.type is pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.set_bomb = True
            if event.type is pygame.KEYDOWN and event.key == pygame.K_3:
                self.player.duration = 3
            if event.type is pygame.KEYDOWN and event.key == pygame.K_4:
                self.player.duration = 4
            if event.type is pygame.KEYDOWN and event.key == pygame.K_5:
                self.player.duration = 5
            if event.type is pygame.KEYDOWN and event.key == pygame.K_6:
                self.player.duration = 6
            if event.type is pygame.KEYDOWN and event.key == pygame.K_7:
                self.player.duration = 7

        self.player.speed = vx, vy
        self.player.sight = sight
        GameMode.Events(self, events, screen)
        return True

    def Action(self):
        for map_object in self.map:
            map_object.action(self.map, self.tempies)
        for enemy in self.enemies:
            enemy.action(self.map, self.tempies)
        for temp_effect in self.tempies:
            temp_effect.action(self.map, self.tempies)
        self.player.action(self.map, self.tempies)

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
            if tmp_effect.is_dead:
                tmp_effect.destroy(self.map, self.tempies)
                del self.tempies[idx]

        for idx, map_object in enumerate(self.map):
            if map_object.is_dead:
                map_object.destroy(self.map, self.tempies)
                del self.map[idx]

        for idx, enemy in enumerate(self.enemies):
            if enemy.is_dead:
                enemy.destroy(self.map, self.tempies)
                del self.enemies[idx]

    def Reset(self):
        self.player.reset()
        self.map = [map_object.copy() for map_object in self.init_map]
        self.enemies = [enemy.copy() for enemy in self.init_enemies]
        self.tempies = []

    def GameStateCheck(self, screen):
        '''Check for win-lose condition + spash screen'''
        if self.player.is_dead:
            title = 'Поражение'
            text1 = 'Вы проиграли'
            advice_id = random.randint(0, len(ut.UselessAdvices)-1)
            advice = 'СОВЕТ:' + ut.UselessAdvices[advice_id]
            splash = gui.SplashScreen(title, text1, advice)
            if splash.MainLoop(screen):
                self.Reset()
                return False
            return True

        elif self.win_mode == ut.GameWinCondition.COLLECT_ALL:
            if self.player.gold[0] >= self.player.gold[1]:
                title = 'Победа'
                text1 = 'Вы собрали всё золото!'
                congrats_id = random.randint(0, len(ut.UselessCongrats) - 1)
                congrats = ut.UselessCongrats[congrats_id]
                splash = gui.SplashScreen(title, text1, congrats)
                if splash.MainLoop(screen):
                    self.Reset()
                    return False
                return True
        elif self.win_mode == ut.GameWinCondition.KILL_ALL:
            if len(self.enemies) == 0:
                title = 'Победа'
                text1 = 'Вы зверски всех убили!'
                congrats_id = random.randint(0, len(ut.UselessCongrats) - 1)
                congrats = ut.UselessCongrats[congrats_id]
                splash = gui.SplashScreen(title, text1, congrats)
                if splash.MainLoop(screen):
                    self.Reset()
                    return False
                return True

        elif self.win_mode == ut.GameWinCondition.GET_GOAL:
            if self.player.gold[0] > 0:
                title = 'Победа'
                text1 = 'Вы достигли цели!'
                congrats_id = random.randint(0, len(ut.UselessCongrats) - 1)
                congrats = ut.UselessCongrats[congrats_id]
                splash = gui.SplashScreen(title, text1, congrats)
                if splash.MainLoop(screen):
                    self.Reset()
                    return False
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

        self.init_map = self.map.copy()
        self.init_enemies = self.enemies.copy()


def __main__():
    '''Main game code'''
    NewUniverse = Universe(ut.BSIZE, ut.TILE)
    NewUniverse.ProcessGame(CollectorGame())


if __name__ == '__main__':
    __main__()
