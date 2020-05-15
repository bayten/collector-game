#!/usr/bin/env python3
"""
run_me.py -- main module
======================
This is main module, which contains main game classes and launches the game.
"""
import pygame  # type: ignore
import random
from typing import List, Optional

import CollectorGame.images as images
import CollectorGame.utils as ut
import CollectorGame.objects as objs
import CollectorGame.gui as gui

DEF_PLAYER_CONFIG = ((0, 0), (3, 3), (0, 10))


class GameMode:
    """Basic game mode"""
    def __init__(self) -> None:
        """Set game mode up"""
        self.back_img: Optional[ut.Image] = None
        pass

    def Events(self, event: ut.Event,
               screen: ut.Image) -> bool:
        """Event parser"""
        return False

    def Draw(self, screen: ut.Image) -> None:
        """Draw game objects"""
        if self.back_img:
            screen.blit(self.back_img, (0, 0))

    def Logic(self) -> None:
        """Process interactions of game objects"""
        pass

    def Action(self) -> None:
        """Process actions of game objects"""
        pass

    def GameStateCheck(self, screen: ut.Image) -> bool:
        """ Check for win-lose condition """
        return False

    def Leave(self) -> None:
        """What to do when leaving this mode"""
        pass

    def Init(self) -> None:
        """What to do when entering this mode"""
        wx = ut.BSIZE[0]*ut.TILE
        wy = ut.BSIZE[1]*ut.TILE
        self.back_img = pygame.Surface((wx, wy))
        for tx in range(ut.BSIZE[0]):
            for ty in range(ut.BSIZE[1]):
                self.back_img.blit(images.BACK_IMG, (tx*ut.TILE, ty*ut.TILE))


class Universe:
    """Game universe: manager of game modes"""

    def __init__(self, sz: ut.Size,
                 tile: int):
        """Run an universe with display and game clock"""
        pygame.init()
        screen_size: ut.Size = (int(sz[0] * tile), int(sz[1] * tile))
        self.screen: ut.Image = pygame.display.set_mode(screen_size)
        self.game_clock: ut.Clock = pygame.time.Clock()
        self.time_delay: int = int(1000./ut.FPS)
        self.game_mode: Optional[GameMode] = None

    def ProcessGame(self, game_mode: GameMode) -> None:
        """Play given game mode"""
        self.game_mode = game_mode
        self.Start()
        self.MainLoop()
        self.Finish()

    def Start(self) -> None:
        """Start running game mode"""
        if self.game_mode:
            self.game_mode.Init()

    def MainLoop(self):
        """Process in loop all game mode's procedures"""
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
        """Finish game mode"""
        pygame.quit()


class CollectorGame(GameMode):
    """Primary game mode with objects"""

    def __init__(self, player: objs.Player = objs.Player(*DEF_PLAYER_CONFIG),
                 level_map: Optional[List[objs.BasicObject]] = None,
                 enemies: Optional[List[objs.Enemy]] = None,
                 tempies: Optional[List[objs.TempEffect]] = None,
                 win_mode: ut.WinCondition = ut.WinCondition.COLLECT_ALL
                 ) -> None:
        """New game with objects"""
        GameMode.__init__(self)
        self.player: objs.Player = player

        self.level_map: Optional[List[objs.BasicObject]] = level_map
        map_copy = None
        if self.level_map:
            map_copy = [map_object.copy() for map_object in self.level_map]
        self.init_map: Optional[List[objs.BasicObject]] = map_copy

        self.enemies: Optional[List[objs.Enemy]] = enemies
        enemy_copy = None
        if self.enemies:
            enemy_copy = [enemy.copy() for enemy in self.enemies]
        self.init_enemies: Optional[List[objs.Enemy]] = enemy_copy

        self.tempies: Optional[List[objs.TempEffect]] = tempies
        self.win_mode: ut.WinCondition = win_mode

    def Events(self, events: ut.Event,
               screen: ut.Image) -> bool:
        """Event parser: process all events from previous tick"""
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

    def Action(self) -> None:
        """Process actions of all game objects"""
        if self.level_map is None or \
           self.tempies is None or \
           self.enemies is None:
            return

        for map_object in self.level_map:
            map_object.action(self.level_map, self.tempies)

        for enemy in self.enemies:
            enemy.action(self.level_map, self.tempies)

        for temp_effect in self.tempies:
            temp_effect.action(self.level_map, self.tempies)

        self.player.action(self.level_map, self.tempies)

    def Logic(self) -> None:
        """Process logic of all game objects"""
        if self.level_map is None or \
           self.tempies is None or \
           self.enemies is None:
            return

        in_params = (self.player, self.level_map, self.enemies, self.tempies)
        self.player.logic(*in_params)

        for map_object in self.level_map:
            map_object.logic(*in_params)

        for tmp_effect in self.tempies:
            tmp_effect.logic(*in_params)
        for enemy in self.enemies:
            enemy.logic(*in_params)

        self.Destroy()

    def Draw(self, surface: ut.Image) -> None:
        """Draw all game objects"""
        if self.level_map is None or \
           self.tempies is None or \
           self.enemies is None:
            return

        GameMode.Draw(self, surface)
        for map_object in self.level_map:
            map_object.draw(surface)
        for enemy in self.enemies:
            enemy.draw(surface)
        for tmp_effect in self.tempies:
            tmp_effect.draw(surface)

        self.player.draw(surface)

    def Destroy(self) -> None:
        """Eliminate all marked objects from the game"""
        if self.level_map is None or \
           self.tempies is None or \
           self.enemies is None:
            return

        for idx, tmp_effect in enumerate(self.tempies):
            if tmp_effect.is_dead:
                tmp_effect.destroy(self.level_map, self.tempies)
                del self.tempies[idx]

        for idx, map_object in enumerate(self.level_map):
            if map_object.is_dead:
                map_object.destroy(self.level_map, self.tempies)
                del self.level_map[idx]

        for idx, enemy in enumerate(self.enemies):
            if enemy.is_dead:
                enemy.destroy(self.level_map, self.tempies)
                del self.enemies[idx]

    def Reset(self) -> None:
        """Restart game from the very beginning"""
        if self.init_map is None or \
           self.init_enemies is None:
            return

        self.player.reset()
        self.level_map = [map_object.copy() for map_object in self.init_map]
        self.enemies = [enemy.copy() for enemy in self.init_enemies]
        self.tempies = []

    def GameStateCheck(self, screen: ut.Image) -> bool:
        """Check for win-lose condition + splash screen"""
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

        elif self.win_mode == ut.WinCondition.COLLECT_ALL:
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
        elif self.win_mode == ut.WinCondition.KILL_ALL and self.enemies:
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

        elif self.win_mode == ut.WinCondition.GET_GOAL:
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
        """What to do when entering this mode"""
        super().Init()
        self.level_map = []
        self.enemies = []
        self.tempies = []

        for x in range(10):
            rand_pos = (random.randint(1, 19), random.randint(1, 19))
            self.level_map.append(objs.Spikes(rand_pos, False))

        for x in range(10):
            rand_pos = (random.randint(1, 19), random.randint(1, 19))
            self.level_map.append(objs.Gold(rand_pos))

        for x in range(5):
            rand_pos = (random.randint(1, 19), random.randint(1, 19))
            rand_speed = (random.randint(-1, 1), random.randint(-1, 1))
            self.enemies.append(objs.Enemy(rand_pos, rand_speed))

        self.init_map = [m.copy() for m in self.level_map]
        self.init_enemies = [e.copy() for e in self.enemies]


def run_game() -> None:
    """Main game code"""
    NewUniverse = Universe(ut.BSIZE, ut.TILE)
    NewUniverse.ProcessGame(CollectorGame())
