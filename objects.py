import utils as ut
import images


class BasicObject:
    def __init__(self, img, pos=(0, 0), speed=(0, 0)):
        self.img = img
        self.pos = pos
        self.init_pos = pos[0], pos[1]
        self.speed = speed
        self.init_speed = speed[0], speed[1]
        self.drop_item = None
        if isinstance(img, list):
            self.draw_count = pos[1] % len(img)
        self.is_dead = False

    def reset(self):
        self.pos = self.init_pos[0], self.init_pos[1]
        self.speed = self.init_speed[0], self.init_speed[1]

    def draw(self, surface):
        '''Draw object on the surface'''
        draw_pos = (self.pos[0]*ut.TILE, self.pos[1]*ut.TILE)
        surface.blit(self.img[int(self.draw_count)], draw_pos)
        self.draw_count = (self.draw_count+ut.ANIMATION_ITER) % len(self.img)

    def action(self):
        '''Proceed some action'''
        new_x, new_y = self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]
        self.pos = (new_x, new_y)

    def logic(self, player, map, enemies, tempies):
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''
        pass

    def destroy(self):
        ''''''
        pass


# class Obstacle(BasicObject):
#     pass

# class DangerObject(BasicObject):
#     def __init__(self, img, pos=(0, 0), ipos=(0, 0), speed=(0, 0),
#                  ispeed=(0, 0)):
#         super().__init__(img, pos, ipos, speed, ispeed)
#
# class BonusObject(BasicObject):
#     def __init__(self, img, pos=(0, 0), ipos=(0, 0), speed=(0, 0),
#                  ispeed=(0, 0), inc_val=1):
#         super().__init__(img, pos, init_pos, speed, init_speed)
#         self.inc_val = inc_val


class Player(BasicObject):
    def __init__(self, pos=(0, 0), gold=(0, 0), fbounds=ut.FieldBounds.RECT):
        super().__init__(images.MAN_IMG, pos)
        self.bonus_img = images.FMAN_IMG
        self.gold = gold
        self.has_bonus = False
        self.fbounds = fbounds

    def draw(self, surface):
        '''Draw object on the surface'''
        draw_pos = (self.pos[0] * ut.TILE, self.pos[1] * ut.TILE)
        if (self.has_bonus):
            surface.blit(self.bonus_img[int(self.draw_count)], draw_pos)
        else:
            surface.blit(self.img[int(self.draw_count)], draw_pos)
        self.draw_count = (self.draw_count+ut.ANIMATION_ITER) % 2

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
                new_x = enemy.pos[0] - enemy.speed[0]
                new_y = enemy.pos[1] - enemy.speed[1]
                enemy.pos = (new_x, new_y)
                # TODO: add communication with other walls
                enemy.speed = (-enemy.speed[0], -enemy.speed[1])

        for temp_effect in tempies:
            if temp_effect.includes(self.pos):
                pass

# class Enemy(DangerObject, Obstacle):
#     def __init__(self, pos=(0, 0), ipos=(0, 0), speed=(0, 0), is_dead=False):
#         super().__init__(ENEMY_IMG, pos, ipos, speed)
#         self.dead_img = DEATH_IMG
#         self.is_dead = is_dead
#
# class Bomb(DangerObject, Obstacle):
#     def __init__(self, pos=(0, 0), ipos=(0, 0), speed=(0, 0),
#                  is_lit = False):
#         super().__init__(BOMB_IMG, pos, ipos, speed)
#         self.lit_img = BBOMB_IMG
#         self.is_lit = is_lit


class Gold(BasicObject):
    def __init__(self, pos=(0, 0), speed=(0, 0), inc_val=1):
        super().__init__(images.MONEY_IMG, pos, speed)
        self.inc_val = inc_val

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

# class CrystalBonus(BonusObject):
#     def __init__(self, pos=(0, 0), ipos=(0, 0), speed=(0, 0),
#                  ispeed=(0, 0), inc_val=10):
#         super().__init__(BONUS_IMG, pos, ipos, speed, ispeed, inc_val)
