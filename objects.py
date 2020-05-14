import utils as ut
import images


class BasicObject:
    def __init__(self, img, pos=(0, 0), speed=(0, 0)):
        self.img = img
        self.pos = pos
        self.init_pos = pos[0], pos[1]
        self.speed = speed
        self.init_speed = speed[0], speed[1]
        if isinstance(img, list):
            self.draw_count = pos[1] % len(img)
        self.is_dead = False

    def copy(self):
        copy_object = BasicObject(self.img.copy(), self.pos, self.speed)
        return copy_object

    def reset(self):
        self.pos = self.init_pos[0], self.init_pos[1]
        self.speed = self.init_speed[0], self.init_speed[1]
        self.is_dead = False

    def draw(self, surface):
        '''Draw object on the surface'''
        draw_pos = (self.pos[0]*ut.TILE, self.pos[1]*ut.TILE)
        surface.blit(self.img[int(self.draw_count)], draw_pos)
        self.draw_count = (self.draw_count+ut.ANIMATION_ITER) % len(self.img)

    def action(self, map, tempies):
        '''Proceed some action'''
        new_x, new_y = self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]
        self.pos = (new_x, new_y)

    def logic(self, player, map, enemies, tempies):
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''
        pass

    def destroy(self, map, tempies):
        ''''''
        pass


class Player(BasicObject):
    def __init__(self, pos=(0, 0), bombs=(0, 3), gold=(0, 0),
                 fbounds=ut.FieldBounds.RECT):
        super().__init__(images.MAN_IMG, pos)
        self.fbounds = fbounds
        self.sight = (0, 0)

        self.limg = images.LMAN_IMG
        self.fimg = images.FMAN_IMG

        self.set_bomb = False
        self.bombs = bombs
        self.init_bombs = bombs

        self.duration = 5

        self.gold = gold
        self.init_gold = gold

        self.bonus = None

    def reset(self):
        super().reset()
        self.sight = (0, 0)

        self.set_bomb = False
        self.bombs = self.init_bombs
        self.duration = 5

        self.gold = self.init_gold

        self.bonus = None

    def draw(self, surface):
        '''Draw object on the surface'''
        draw_pos = (self.pos[0] * ut.TILE, self.pos[1] * ut.TILE)
        if self.bonus is None:
            surface.blit(self.img[int(self.draw_count)], draw_pos)
        else:
            # TODO: process player sprites correctly according to bonus
            surface.blit(self.limg[int(self.draw_count)], draw_pos)
        self.draw_count = (self.draw_count+ut.ANIMATION_ITER) % 2

    def action(self, map, tempies):
        '''Proceed some action'''
        new_x, new_y = self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]
        self.pos = (new_x, new_y)
        if self.set_bomb:
            self.set_bomb = False
            if self.bombs[0] > 0 and self.speed[0] == 0 and self.speed[1] == 0:
                self.bombs = self.bombs[0]-1, self.bombs[1]
                bomb_pos_x = self.pos[0] + self.sight[0]
                bomb_pos_y = self.pos[1] + self.sight[1]
                map.append(Bomb((bomb_pos_x, bomb_pos_y), self.duration*5))

    def logic(self, player, map, enemies, tempies):
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
    def __init__(self, pos=(0, 0), is_super=False):
        if is_super:
            super().__init__(images.SWALL_IMG, pos, (0, 0))
        else:
            super().__init__(images.WALL_IMG, pos, (0, 0))
        self.is_super = is_super

    def copy(self):
        copy_object = Wall(self.pos, self.is_super)
        return copy_object

    def draw(self, surface):
        draw_pos = (self.pos[0] * ut.TILE, self.pos[1] * ut.TILE)
        surface.blit(self.img, draw_pos)

    def logic(self, player, map, enemies, tempies):
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

        for temp_effect in tempies:
            if temp_effect.includes(self.pos):
                pass


class Spikes(BasicObject):
    def __init__(self, pos=(0, 0), is_activated=True):
        super().__init__(images.SPIKE_IMG, pos, (0, 0))
        self.dimg = images.DSPIKE_IMG
        self.is_triggered = False
        self.is_activated = is_activated
        self.is_init_activated = is_activated

    def copy(self):
        copy_object = Spikes(self.pos, self.is_activated)
        copy_object.is_triggered = self.is_triggered
        return copy_object

    def reset(self):
        super().reset()
        self.is_activated = self.is_init_activated

    def draw(self, surface):
        draw_pos = (self.pos[0] * ut.TILE, self.pos[1] * ut.TILE)
        if self.is_activated:
            surface.blit(self.img, draw_pos)
        else:
            surface.blit(self.dimg, draw_pos)

    def logic(self, player, map, enemies, tempies):
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

        for temp_effect in tempies:
            if temp_effect.includes(self.pos):
                pass


class Enemy(BasicObject):
    def __init__(self, pos=(0, 0), speed=(0, 0), fbounds=ut.FieldBounds.RECT):
        super().__init__(images.ENEMY_IMG, pos, speed)
        self.fbounds = fbounds
        self.slow_count = 0

    def copy(self):
        copy_object = Enemy(self.pos, self.speed, self.fbounds)
        return copy_object

    def action(self, map, tempies):
        '''Proceed some action'''
        self.slow_count = (self.slow_count+1) % ut.ENEMY_SLOW
        x, y = self.pos
        if self.slow_count == 0:
            x += self.speed[0]
            y += self.speed[1]
        self.pos = x, y

    def logic(self, player, map, enemies, tempies):
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

        for temp_effect in tempies:
            if temp_effect.includes(self.pos):
                pass


class Explosion(BasicObject):
    def __init__(self, pos=(0, 0), esize=2, duration=(0, 7),
                 etype=ut.ExplosionType.CROSS, fbounds=ut.FieldBounds.RECT):
        super().__init__(images.BOOM_IMG, pos, (0, 0))
        self.esizex = pos[0]-esize, pos[0]+esize
        self.esizey = pos[1]-esize, pos[1]+esize
        self.duration = duration
        self.etype = etype
        self.fbounds = fbounds

    def draw(self, surface):
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

    def action(self, map, tempies):
        curr_duration = self.duration[0]
        curr_duration += 1
        if curr_duration >= self.duration[1]:
            self.is_dead = True
        self.duration = curr_duration, self.duration[1]

    def includes(self, pos):
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

    def logic(self, player, map, enemies, tempies):
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''

        if self.includes(player.pos):
            player.is_dead = True

        for map_object in map:
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
    def __init__(self, pos=(0, 0), duration=20, bomb_range=2):
        super().__init__(images.BBOMB_IMG, pos, (0, 0))
        self.duration = duration
        self.bomb_range = bomb_range

    def action(self, map, tempies):
        self.duration -= 1
        if self.duration <= 0:
            self.is_dead = True

    def logic(self, player, map, enemies, tempies):
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

        for temp_effect in tempies:
            if temp_effect.includes(self.pos):
                pass

    def destroy(self, map, tempies):
        tempies.append(Explosion(self.pos, self.bomb_range))


class Gold(BasicObject):
    def __init__(self, pos=(0, 0), inc_val=1):
        super().__init__(images.MONEY_IMG, pos, (0, 0))
        self.inc_val = inc_val

    def copy(self):
        copy_object = Gold(self.pos, self.inc_val)
        return copy_object

    def logic(self, player, map, enemies, tempies):
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''
        if player.pos[0] == self.pos[0] and player.pos[1] == self.pos[1]:
            player.gold = player.gold[0]+self.inc_val, player.gold[1]
            self.is_dead = True

        for temp_effect in tempies:
            if temp_effect.includes(self.pos):
                pass

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
