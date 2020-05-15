import utils as ut
from typing import List, Tuple
import images


class BasicObject:
    def __init__(self, img: List[ut.Image],
                 pos: ut.Coord = (0, 0),
                 speed: ut.Coord = (0, 0)) -> None:
        self.img: List[ut.Image] = img
        self.pos: ut.Coord = pos
        self.init_pos: ut.Coord = pos
        self.speed: ut.Coord = speed
        self.init_speed: ut.Coord = speed
        self.draw_count: float = pos[1] % len(img)
        self.is_dead: bool = False

    def copy(self) -> 'BasicObject':
        copy_object = BasicObject(self.img.copy(), self.pos, self.speed)
        return copy_object

    def reset(self) -> None:
        self.pos = self.init_pos[0], self.init_pos[1]
        self.speed = self.init_speed[0], self.init_speed[1]
        self.is_dead = False

    def draw(self, surface: ut.Image) -> None:
        '''Draw object on the surface'''
        draw_pos = (self.pos[0]*ut.TILE, self.pos[1]*ut.TILE)
        surface.blit(self.img[int(self.draw_count)], draw_pos)
        self.draw_count = (self.draw_count+ut.ANIMATION_ITER) % len(self.img)

    def action(self, level_map: List['BasicObject'],
               tempies: List['TempEffect']) -> None:
        '''Proceed some action'''
        new_x: int = self.pos[0] + self.speed[0]
        new_y: int = self.pos[1] + self.speed[1]
        self.pos = (new_x, new_y)

    def logic(self, player: 'Player',
              level_map: List['BasicObject'],
              enemies: List['Enemy'],
              tempies: List['TempEffect']) -> None:
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''
        pass

    def destroy(self, level_map: List['BasicObject'],
                tempies: List['TempEffect']) -> None:
        ''''''
        pass


class TempEffect(BasicObject):
    def __init__(self, img: List[ut.Image],
                 pos: ut.Coord,
                 speed: ut.Coord) -> None:
        super().__init__(img, pos, speed)

    def includes(self, pos: ut.Coord) -> bool:
        return False


class Enemy(BasicObject):
    def __init__(self, pos: ut.Coord = (0, 0),
                 speed: ut.Coord = (0, 0),
                 fbounds: ut.FieldBounds = ut.FieldBounds.RECT) -> None:
        super().__init__(images.ENEMY_IMG, pos, speed)
        self.fbounds: ut.FieldBounds = fbounds
        self.slow_count: int = 0

    def copy(self) -> 'Enemy':
        copy_object = Enemy(self.pos, self.speed, self.fbounds)
        return copy_object

    def action(self, level_map: List[BasicObject],
               tempies: List[TempEffect]) -> None:
        '''Proceed some action'''
        self.slow_count = (self.slow_count+1) % ut.ENEMY_SLOW
        x, y = self.pos
        if self.slow_count == 0:
            x += self.speed[0]
            y += self.speed[1]
        self.pos = x, y

    def logic(self, player: 'Player',
              level_map: List[BasicObject],
              enemies: List['Enemy'],
              tempies: List[TempEffect]) -> None:
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''
        x, y = self.pos
        vx, vy = self.speed
        if self.fbounds == ut.FieldBounds.RECT:
            if x < 0 or x >= ut.BSIZE[0]:
                x = max(0, min(x, ut.BSIZE[0] - 1))
                vx *= -1
            if y < 0 or y >= ut.BSIZE[1]:
                y = max(0, min(y, ut.BSIZE[1] - 1))
                vy *= -1

        elif self.fbounds == ut.FieldBounds.TORUS:
            x = (x + ut.BSIZE[0]) % ut.BSIZE[0]
            y = (y + ut.BSIZE[1]) % ut.BSIZE[1]
        self.speed = vx, vy
        self.pos = x, y

        if player.pos[0] == self.pos[0] and player.pos[1] == self.pos[1]:
            player.is_dead = True

        for enemy in enemies:
            if enemy is self:
                continue
            if enemy.pos[0] == self.pos[0] and enemy.pos[1] == self.pos[1]:
                old_x = self.pos[0]-self.speed[0]
                old_y = self.pos[1]-self.speed[1]
                old_enemy_x = enemy.pos[0] - enemy.speed[0]
                old_enemy_y = enemy.pos[1] - enemy.speed[1]

                new_vx, new_vy = self.speed
                new_enemy_vx, new_enemy_vy = enemy.speed
                if old_x != old_enemy_x:
                    new_vx *= -1
                    new_enemy_vx *= -1
                if old_y != old_enemy_y:
                    new_vy *= -1
                    new_enemy_vy *= -1

                self.pos = old_x, old_y
                self.speed = new_vx, new_vy

                enemy.pos = old_enemy_x, old_enemy_y
                enemy.speed = new_enemy_vx, new_enemy_vy


class Player(BasicObject):
    def __init__(self, pos: ut.Coord = (0, 0),
                 bombs: Tuple[int, int] = (0, 3),
                 gold: Tuple[int, int] = (0, 0),
                 fbounds: ut.FieldBounds = ut.FieldBounds.RECT) -> None:
        super().__init__(images.MAN_IMG, pos)
        self.fbounds: ut.FieldBounds = fbounds
        self.sight: ut.Coord = (0, 0)

        self.limg: List[ut.Image] = images.LMAN_IMG
        self.fimg: List[ut.Image] = images.FMAN_IMG

        self.set_bomb: bool = False
        self.bombs: Tuple[int, int] = bombs
        self.init_bombs: Tuple[int, int] = bombs

        self.duration: int = 5

        self.gold: Tuple[int, int] = gold
        self.init_gold: Tuple[int, int] = gold

        self.bonus: None = None

    def reset(self) -> None:
        super().reset()
        self.sight = (0, 0)

        self.set_bomb = False
        self.bombs = self.init_bombs
        self.duration = 5

        self.gold = self.init_gold

        self.bonus = None

    def draw(self, surface: ut.Image) -> None:
        '''Draw object on the surface'''
        draw_pos = (self.pos[0] * ut.TILE, self.pos[1] * ut.TILE)
        if self.bonus is None:
            surface.blit(self.img[int(self.draw_count)], draw_pos)
        else:
            # TODO: process player sprites correctly according to bonus
            surface.blit(self.limg[int(self.draw_count)], draw_pos)
        self.draw_count = (self.draw_count+ut.ANIMATION_ITER) % 2

    def action(self, level_map: List[BasicObject],
               tempies: List[TempEffect]) -> None:
        '''Proceed some action'''
        new_x, new_y = self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]
        self.pos = (new_x, new_y)
        if self.set_bomb and level_map:
            self.set_bomb = False
            if self.bombs[0] > 0 and self.speed[0] == 0 and self.speed[1] == 0:
                self.bombs = self.bombs[0]-1, self.bombs[1]
                bomb_pos_x = self.pos[0] + self.sight[0]
                bomb_pos_y = self.pos[1] + self.sight[1]
                new_bomb = Bomb((bomb_pos_x, bomb_pos_y), self.duration*5)
                level_map.append(new_bomb)

    def logic(self, player: 'Player',
              level_map: List[BasicObject],
              enemies: List[Enemy],
              tempies: List[TempEffect]) -> None:
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''
        x, y = self.pos
        if self.fbounds == ut.FieldBounds.RECT:
            x = max(0, min(x, ut.BSIZE[0]-1))
            y = max(0, min(y, ut.BSIZE[1]-1))
        elif self.fbounds == ut.FieldBounds.TORUS:
            x = (x+ut.BSIZE[0]) % ut.BSIZE[0]
            y = (y+ut.BSIZE[1]) % ut.BSIZE[1]

        self.pos = (x, y)


class Wall(BasicObject):
    def __init__(self, pos: ut.Coord = (0, 0), is_super: bool = False) -> None:
        if is_super:
            super().__init__([images.SWALL_IMG], pos, (0, 0))
        else:
            super().__init__([images.WALL_IMG], pos, (0, 0))
        self.is_super: bool = is_super

    def copy(self) -> 'Wall':
        copy_object = Wall(self.pos, self.is_super)
        return copy_object

    def draw(self, surface: ut.Image) -> None:
        draw_pos = (self.pos[0] * ut.TILE, self.pos[1] * ut.TILE)
        surface.blit(self.img[0], draw_pos)

    def logic(self, player: Player,
              level_map: List[BasicObject],
              enemies: List[Enemy],
              tempies: List[TempEffect]) -> None:
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''
        if player.pos[0] == self.pos[0] and player.pos[1] == self.pos[1]:
            # TODO: add bonuses
            new_x = player.pos[0]-player.speed[0]
            new_y = player.pos[1]-player.speed[1]
            player.pos = (new_x, new_y)
        for enemy in enemies:
            if enemy.pos[0] == self.pos[0] and enemy.pos[1] == self.pos[1]:
                old_x = enemy.pos[0] - enemy.speed[0]
                old_y = enemy.pos[1] - enemy.speed[1]

                new_vx, new_vy = enemy.speed
                if old_x != self.pos[0]:
                    new_vx *= -1
                if old_y != self.pos[1]:
                    new_vy *= -1

                enemy.pos = old_x, old_y
                enemy.speed = new_vx, new_vy


class Spikes(BasicObject):
    def __init__(self, pos: ut.Coord = (0, 0),
                 is_activated: bool = True) -> None:
        super().__init__([images.SPIKE_IMG], pos, (0, 0))
        self.dimg: List[ut.Image] = [images.DSPIKE_IMG]
        self.is_triggered: bool = False
        self.is_activated: bool = is_activated
        self.is_init_activated: bool = is_activated

    def copy(self) -> 'Spikes':
        copy_object = Spikes(self.pos, self.is_activated)
        return copy_object

    def reset(self) -> None:
        super().reset()
        self.is_activated = self.is_init_activated

    def draw(self, surface: ut.Image) -> None:
        draw_pos = (self.pos[0] * ut.TILE, self.pos[1] * ut.TILE)
        if self.is_activated:
            surface.blit(self.img[0], draw_pos)
        else:
            surface.blit(self.dimg[0], draw_pos)

    def logic(self, player: Player,
              level_map: List[BasicObject],
              enemies: List[Enemy],
              tempies: List[TempEffect]) -> None:
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''
        if player.pos[0] == self.pos[0] and player.pos[1] == self.pos[1]:
            if self.is_activated:
                player.is_dead = True
            elif not self.is_triggered:
                self.is_triggered = True
        elif self.is_triggered and not self.is_activated:
            self.is_activated = True


class Explosion(TempEffect):
    def __init__(self, pos: ut.Coord = (0, 0),
                 esize: int = 2, duration: Tuple[int, int] = (0, 7),
                 etype: ut.ExplosionType = ut.ExplosionType.CROSS,
                 fbounds: ut.FieldBounds = ut.FieldBounds.RECT) -> None:
        super().__init__(images.BOOM_IMG, pos, (0, 0))
        self.esizex: Tuple[int, int] = (pos[0]-esize, pos[0]+esize)
        self.esizey: Tuple[int, int] = (pos[1]-esize, pos[1]+esize)
        self.duration: Tuple[int, int] = duration
        self.etype: ut.ExplosionType = etype
        self.fbounds: ut.FieldBounds = fbounds

    def draw(self, surface: ut.Image) -> None:
        if self.duration[0] <= 2:
            img_to_draw = self.img[self.duration[0]]
        elif self.duration[1]-self.duration[0] <= 3:
            img_to_draw = self.img[self.duration[0]-self.duration[1]]
        else:
            img_to_draw = self.img[3+self.duration[0] % 2]

        if self.etype is ut.ExplosionType.CROSS:
            for x in range(self.esizex[0], self.esizex[1]+1):
                if self.fbounds == ut.FieldBounds.RECT:
                    if x < 0 or x >= ut.BSIZE[0]:
                        continue
                elif self.fbounds == ut.FieldBounds.TORUS:
                    x = (x + ut.BSIZE[0]) % ut.BSIZE[0]
                draw_pos = (x * ut.TILE, self.pos[1] * ut.TILE)
                surface.blit(img_to_draw, draw_pos)

            for y in range(self.esizey[0], self.esizey[1]+1):
                if self.fbounds == ut.FieldBounds.RECT:
                    if y < 0 or y >= ut.BSIZE[1]:
                        continue
                elif self.fbounds == ut.FieldBounds.TORUS:
                    y = (y + ut.BSIZE[0]) % ut.BSIZE[0]
                draw_pos = (self.pos[0] * ut.TILE, y * ut.TILE)
                surface.blit(img_to_draw, draw_pos)
        elif self.etype is ut.ExplosionType.CIRCLE:
            pass

    def action(self, level_map: List[BasicObject],
               tempies: List[TempEffect]) -> None:
        curr_duration: int = self.duration[0]
        curr_duration += 1
        if curr_duration >= self.duration[1]:
            self.is_dead = True
        self.duration = curr_duration, self.duration[1]

    def includes(self, pos: ut.Coord) -> bool:
        if self.etype == ut.ExplosionType.CROSS:
            if self.fbounds == ut.FieldBounds.RECT:
                if pos[0] == self.pos[0]:
                    if self.esizey[0] <= pos[1] <= self.esizey[1]:
                        return True
                elif pos[1] == self.pos[1]:
                    if self.esizex[0] <= pos[0] <= self.esizex[1]:
                        return True
            elif self.fbounds == ut.FieldBounds.TORUS:
                pass

        elif self.etype == ut.ExplosionType.CIRCLE:
            pass
        return False

    def logic(self, player: Player,
              level_map: List[BasicObject],
              enemies: List[Enemy],
              tempies: List[TempEffect]) -> None:
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''

        if self.includes(player.pos):
            player.is_dead = True

        for map_object in level_map:
            if self.includes(map_object.pos):
                if isinstance(map_object, Wall):
                    if map_object.is_super is False:
                        map_object.is_dead = True
                if isinstance(map_object, Gold):
                    map_object.is_dead = True
                    player.is_dead = True
                if isinstance(map_object, Spikes):
                    if map_object.is_activated:
                        map_object.is_activated = False
                        map_object.is_triggered = False

        for enemy in enemies:
            if self.includes(enemy.pos):
                enemy.is_dead = True


class Bomb(BasicObject):
    def __init__(self, pos: ut.Coord = (0, 0),
                 duration: int = 20, bomb_range: int = 2) -> None:
        super().__init__(images.BBOMB_IMG, pos, (0, 0))
        self.duration: int = duration
        self.bomb_range: int = bomb_range

    def action(self, level_map: List[BasicObject],
               tempies: List[TempEffect]) -> None:
        self.duration -= 1
        if self.duration <= 0:
            self.is_dead = True

    def logic(self, player: Player,
              level_map: List[BasicObject],
              enemies: List[Enemy],
              tempies: List[TempEffect]) -> None:
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''

        if player.pos[0] == self.pos[0] and player.pos[1] == self.pos[1]:
            # TODO: add bonuses
            new_x = player.pos[0] - player.speed[0]
            new_y = player.pos[1] - player.speed[1]
            player.pos = (new_x, new_y)

        for enemy in enemies:
            if enemy.pos[0] == self.pos[0] and enemy.pos[1] == self.pos[1]:
                old_x = enemy.pos[0] - enemy.speed[0]
                old_y = enemy.pos[1] - enemy.speed[1]

                new_vx, new_vy = enemy.speed
                if old_x != self.pos[0]:
                    new_vx *= -1
                if old_y != self.pos[1]:
                    new_vy *= -1

                enemy.pos = old_x, old_y
                enemy.speed = new_vx, new_vy

    def destroy(self, level_map: List[BasicObject],
                tempies: List[TempEffect]) -> None:
        tempies.append(Explosion(self.pos, self.bomb_range))


class Gold(BasicObject):
    def __init__(self, pos: ut.Coord = (0, 0),
                 inc_val: int = 1) -> None:
        super().__init__(images.MONEY_IMG, pos, (0, 0))
        self.inc_val = inc_val

    def copy(self) -> 'Gold':
        copy_object = Gold(self.pos, self.inc_val)
        return copy_object

    def logic(self, player: Player,
              level_map: List[BasicObject],
              enemies: List[Enemy],
              tempies: List[TempEffect]) -> None:
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''
        if player.pos[0] == self.pos[0] and player.pos[1] == self.pos[1]:
            player.gold = player.gold[0]+self.inc_val, player.gold[1]
            self.is_dead = True

# class FireBonus(BonusObject):
#     def __init__(self, pos=(0, 0), ipos=(0, 0), speed=(0, 0),
#                  ispeed=(0, 0), inc_val=10):
#         super().__init__(BONUS_IMG, pos, ipos, speed, ispeed, inc_val)

# class LightningBonus(BonusObject):
#     def __init__(self, pos=(0, 0), ipos=(0, 0), speed=(0, 0),
#                  ispeed=(0, 0), inc_val=10):
#         super().__init__(BONUS_IMG, pos, ipos, speed, ispeed, inc_val)

# class IceBonus(BonusObject):
#     def __init__(self, pos=(0, 0), ipos=(0, 0), speed=(0, 0),
#                  ispeed=(0, 0), inc_val=10):
#         super().__init__(BONUS_IMG, pos, ipos, speed, ispeed, inc_val)


# class CrystalBonus(BonusObject):
#     def __init__(self, pos=(0, 0), ipos=(0, 0), speed=(0, 0),
#                  ispeed=(0, 0), inc_val=10):
#         super().__init__(BONUS_IMG, pos, ipos, speed, ispeed, inc_val)
