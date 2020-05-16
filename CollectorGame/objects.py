"""
objects.py -- submodule for game object classes
===============================================
This is module, which mainly consists of game object classes.
"""

from typing import List, Tuple

import CollectorGame.images as images
import CollectorGame.utils as ut


class BasicObject:
    """Basic game object with position, speed and self-image"""

    def __init__(self, img: List[ut.Image],
                 pos: ut.Coord = (0, 0),
                 speed: ut.Coord = (0, 0)) -> None:
        """Initialise game object"""

        self.img: List[ut.Image] = img if img else [images.BACK_IMG]
        x = max(0, min(pos[0], ut.BSIZE[0]-1))
        y = max(0, min(pos[1], ut.BSIZE[1]-1))
        self.pos: ut.Coord = (x, y)
        self.init_pos: ut.Coord = self.pos

        vx = ut.sign(speed[0])*min(abs(speed[0]), ut.BSIZE[0]-1)
        vy = ut.sign(speed[1])*min(abs(speed[1]), ut.BSIZE[1]-1)
        self.speed: ut.Coord = (vx, vy)
        self.init_speed: ut.Coord = self.speed
        self.draw_count: float = pos[1] % len(self.img)
        self.is_dead: bool = False

    def copy(self) -> 'BasicObject':
        """Create new copy of object"""
        copied_img = [img_sprite.copy() for img_sprite in self.img]
        copy_object = BasicObject(copied_img, self.pos, self.speed)
        return copy_object

    def reset(self) -> None:
        """Reset parameters of game object to initial values"""
        self.pos = self.init_pos[0], self.init_pos[1]
        self.speed = self.init_speed[0], self.init_speed[1]
        self.draw_count: float = self.pos[1] % len(self.img)
        self.is_dead = False

    def draw(self, surface: ut.Image) -> None:
        """Draw object on the surface"""
        draw_pos = (self.pos[0]*ut.TILE, self.pos[1]*ut.TILE)
        surface.blit(self.img[int(self.draw_count)], draw_pos)
        self.draw_count = (self.draw_count+ut.ANIMATION_ITER) % len(self.img)

    def action(self, level_map: List['BasicObject'],
               tempies: List['TempEffect']) -> None:
        """Perform action of game object"""
        new_x: int = self.pos[0] + self.speed[0]
        new_y: int = self.pos[1] + self.speed[1]
        self.pos = (new_x, new_y)

    def logic(self, player: 'Player',
              level_map: List['BasicObject'],
              enemies: List['Enemy'],
              tempies: List['TempEffect']) -> None:
        """Process interaction of game object with other objects"""
        x, y = self.pos
        if x < 0 or x >= ut.BSIZE[0]:
            x %= ut.BSIZE[0]
        if y < 0 or y >= ut.BSIZE[1]:
            y %= ut.BSIZE[1]

        vx, vy = self.speed
        if abs(vx) >= ut.BSIZE[0]:
            vx = 0
        if abs(vy) >= ut.BSIZE[1]:
            vy = 0

        self.pos = x, y
        self.speed = vx, vy

    def destroy(self, level_map: List['BasicObject'],
                tempies: List['TempEffect']) -> None:
        """Prepare for future deletion of game object"""
        pass


class TempEffect(BasicObject):
    """Basic temporary game effect object"""

    def __init__(self, img: List[ut.Image],
                 pos: ut.Coord,
                 speed: ut.Coord) -> None:
        """Initialise temporary game effect"""
        super().__init__(img, pos, speed)

    def includes(self, pos: ut.Coord) -> bool:
        """Check if given position is included in effect's area"""
        return False


class Enemy(BasicObject):
    """Basic enemy object"""
    def __init__(self, pos: ut.Coord = (0, 0),
                 speed: ut.Coord = (0, 0),
                 fbounds: ut.FieldBounds = ut.FieldBounds.RECT) -> None:
        """Initialise Enemy object"""
        super().__init__(images.ENEMY_IMG, pos, speed)
        self.fbounds: ut.FieldBounds = fbounds
        self.slow_count: int = 0

    def copy(self) -> 'Enemy':
        """Create new copy of Enemy object"""
        copy_object = Enemy(self.pos, self.speed, self.fbounds)
        return copy_object

    def action(self, level_map: List[BasicObject],
               tempies: List[TempEffect]) -> None:
        """Perform enemy action"""
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
        """Process enemy interaction with other objects"""
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
    """Object, representing player"""
    def __init__(self, pos: ut.Coord = (0, 0),
                 bombs: Tuple[int, int] = (0, 3),
                 gold: Tuple[int, int] = (0, 0),
                 fbounds: ut.FieldBounds = ut.FieldBounds.RECT) -> None:
        """Initialise Player object"""
        super().__init__(images.MAN_IMG, pos)
        self.fbounds: ut.FieldBounds = fbounds
        self.sight: ut.Coord = (0, 0)

        self.limg: List[ut.Image] = images.LMAN_IMG
        self.fimg: List[ut.Image] = images.FMAN_IMG

        self.set_bomb: bool = False
        new_bombs = max(0, min(bombs[0], bombs[1])), bombs[1]
        self.bombs: Tuple[int, int] = new_bombs
        self.init_bombs: Tuple[int, int] = self.bombs

        self.duration: int = 5

        new_gold = max(0, min(gold[0], gold[1])), gold[1]
        self.gold: Tuple[int, int] = new_gold
        self.init_gold: Tuple[int, int] = self.gold

        self.bonus: None = None

    def reset(self) -> None:
        """Reset parameters of player to initial values"""
        super().reset()
        self.sight = (0, 0)

        self.set_bomb = False
        self.bombs = self.init_bombs
        self.duration = 5

        self.gold = self.init_gold

        self.bonus = None

    def draw(self, surface: ut.Image) -> None:
        """Draw player on the surface"""
        draw_pos = (self.pos[0] * ut.TILE, self.pos[1] * ut.TILE)
        if self.bonus is None:
            surface.blit(self.img[int(self.draw_count)], draw_pos)
        else:
            # TODO: process player sprites correctly according to bonus
            surface.blit(self.limg[int(self.draw_count)], draw_pos)
        self.draw_count = (self.draw_count+ut.ANIMATION_ITER) % 2

    def action(self, level_map: List[BasicObject],
               tempies: List[TempEffect]) -> None:
        """Perform player's action"""
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
        """Process player interaction with other objects"""
        x, y = self.pos
        if self.fbounds == ut.FieldBounds.RECT:
            x = max(0, min(x, ut.BSIZE[0]-1))
            y = max(0, min(y, ut.BSIZE[1]-1))
        elif self.fbounds == ut.FieldBounds.TORUS:
            x = (x+ut.BSIZE[0]) % ut.BSIZE[0]
            y = (y+ut.BSIZE[1]) % ut.BSIZE[1]

        self.pos = (x, y)


class Wall(BasicObject):
    """Wall game object """
    def __init__(self, pos: ut.Coord = (0, 0), is_super: bool = False) -> None:
        """Initialise Wall object"""
        if is_super:
            super().__init__([images.SWALL_IMG], pos, (0, 0))
        else:
            super().__init__([images.WALL_IMG], pos, (0, 0))
        self.is_super: bool = is_super

    def copy(self) -> 'Wall':
        """Create a copy of Wall object"""
        copy_object = Wall(self.pos, self.is_super)
        return copy_object

    def draw(self, surface: ut.Image) -> None:
        """Draw Wall object on the surface"""
        draw_pos = (self.pos[0] * ut.TILE, self.pos[1] * ut.TILE)
        surface.blit(self.img[0], draw_pos)

    def logic(self, player: Player,
              level_map: List[BasicObject],
              enemies: List[Enemy],
              tempies: List[TempEffect]) -> None:
        """Process Wall interaction with other objects"""
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
    """Spikes game object."""
    def __init__(self, pos: ut.Coord = (0, 0),
                 is_activated: bool = True) -> None:
        """Initialise Spikes"""
        super().__init__([images.SPIKE_IMG], pos, (0, 0))
        self.dimg: List[ut.Image] = [images.DSPIKE_IMG]
        self.is_triggered: bool = False
        self.is_activated: bool = is_activated
        self.is_init_activated: bool = is_activated

    def copy(self) -> 'Spikes':
        """Create new copy of Spikes object"""
        copy_object = Spikes(self.pos, self.is_activated)
        return copy_object

    def reset(self) -> None:
        """Reset Spikes object to initial values"""
        super().reset()
        self.is_activated = self.is_init_activated

    def draw(self, surface: ut.Image) -> None:
        """Draw Spikes object on the surface"""
        draw_pos = (self.pos[0] * ut.TILE, self.pos[1] * ut.TILE)
        if self.is_activated:
            surface.blit(self.img[0], draw_pos)
        else:
            surface.blit(self.dimg[0], draw_pos)

    def logic(self, player: Player,
              level_map: List[BasicObject],
              enemies: List[Enemy],
              tempies: List[TempEffect]) -> None:
        """Process Spikes interaction with other objects"""
        if player.pos[0] == self.pos[0] and player.pos[1] == self.pos[1]:
            if self.is_activated:
                player.is_dead = True
            elif not self.is_triggered:
                self.is_triggered = True
        elif self.is_triggered and not self.is_activated:
            self.is_activated = True


class Explosion(TempEffect):
    """Explosion object - temporary effect from the bomb"""
    def __init__(self, pos: ut.Coord = (0, 0),
                 esize: int = 2, duration: Tuple[int, int] = (0, 7),
                 etype: ut.ExplosionType = ut.ExplosionType.CROSS,
                 fbounds: ut.FieldBounds = ut.FieldBounds.RECT) -> None:
        """Initialise Explosion object"""
        super().__init__(images.BOOM_IMG, pos, (0, 0))
        self.esizex: Tuple[int, int] = (pos[0]-esize, pos[0]+esize)
        self.esizey: Tuple[int, int] = (pos[1]-esize, pos[1]+esize)
        self.duration: Tuple[int, int] = duration
        self.etype: ut.ExplosionType = etype
        self.fbounds: ut.FieldBounds = fbounds

    def draw(self, surface: ut.Image) -> None:
        """Draw Explosion object on the surface"""
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
        """Perform Explosion's action"""
        curr_duration: int = self.duration[0]
        curr_duration += 1
        if curr_duration >= self.duration[1]:
            self.is_dead = True
        self.duration = curr_duration, self.duration[1]

    def includes(self, pos: ut.Coord) -> bool:
        """Check if given position is included in Explosion's area"""
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
        """Process Explosion interaction with other objects"""

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
    """Bomb game object"""
    def __init__(self, pos: ut.Coord = (0, 0),
                 duration: int = 20, bomb_range: int = 2) -> None:
        """Initialise Bomb object"""

        super().__init__(images.BBOMB_IMG, pos, (0, 0))
        self.duration: int = duration
        self.bomb_range: int = bomb_range

    def action(self, level_map: List[BasicObject],
               tempies: List[TempEffect]) -> None:
        """Perform Bomb action"""

        self.duration -= 1
        if self.duration <= 0:
            self.is_dead = True

    def logic(self, player: Player,
              level_map: List[BasicObject],
              enemies: List[Enemy],
              tempies: List[TempEffect]) -> None:
        """Process Bomb interaction with other objects"""

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
        """Prepare for future deletion of Bomb object"""
        tempies.append(Explosion(self.pos, self.bomb_range))


class Gold(BasicObject):
    """Coin game object"""
    def __init__(self, pos: ut.Coord = (0, 0),
                 inc_val: int = 1) -> None:
        """Initialise Gold object"""
        super().__init__(images.MONEY_IMG, pos, (0, 0))
        self.inc_val = inc_val

    def copy(self) -> 'Gold':
        """Create new copy of Gold object"""
        copy_object = Gold(self.pos, self.inc_val)
        return copy_object

    def logic(self, player: Player,
              level_map: List[BasicObject],
              enemies: List[Enemy],
              tempies: List[TempEffect]) -> None:
        """Process Gold interaction with other objects"""
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
