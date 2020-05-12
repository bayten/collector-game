import utils as ut
import images


class BasicObject:
    def __init__(self, img, pos=(0, 0), ipos=(0, 0), speed=(0, 0),
                 ispeed=(0, 0)):
        self.img = img
        self.pos = pos
        self.init_pos = ipos
        self.speed = speed
        self.init_speed = ispeed
        self.drop_item = None
        self.draw_count = pos[1] % len(img)

    def reset(self):
        self.pos = self.init_pos.copy()
        self.speed = self.init_speed.copy()

    def draw(self, surface):
        '''Draw object on the surface'''
        draw_pos = (self.pos[0]*ut.TILE, self.pos[1]*ut.TILE)
        surface.blit(self.img[self.draw_count], draw_pos)
        self.draw_count = (self.draw_count+1) % len(self.img)

    def action(self):
        '''Proceed some action'''
        new_x, new_y = self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]
        self.pos = (new_x, new_y)

    def logic(self, player, map_objs, danger_objs, collect_objs):
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''
        self.pos[0] = max(0, min(self.pos[0], ut.BSIZE[0]-1))
        self.pos[1] = max(0, min(self.pos[1], ut.BSIZE[1]-1))

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
    def __init__(self, pos=(0, 0), ipos=(0, 0), gold=(0, 0)):
        super().__init__(images.MAN_IMG, pos, ipos)
        self.bonus_img = images.FMAN_IMG
        self.gold = gold
        self.has_bonus = False

    def draw(self, surface):
        '''Draw object on the surface'''
        draw_pos = (self.pos[0] * ut.TILE, self.pos[1] * ut.TILE)
        if (self.has_bonus):
            surface.blit(self.bonus_img[self.draw_count], draw_pos)
        else:
            surface.blit(self.img[self.draw_count], draw_pos)
        self.draw_count = (self.draw_count+1) % 2

    def logic(self, player, map, danger_objs, collect_objs):
        '''Interact with game surface

        - Check if ball is out of surface, repose it and change acceleration''
        '''
        self.pos[0] = max(0, min(self.pos[0], ut.BSIZE[0]-1))
        self.pos[1] = max(0, min(self.pos[1], ut.BSIZE[1]-1))


class Wall(BasicObject):
    def __init__(self, pos=(0, 0), init_pos=(0, 0), is_super=False):
        if is_super:
            super().__init__(images.SWALL_IMG, pos, init_pos, (0, 0), (0, 0))
        else:
            super().__init__(images.WALL_IMG, pos, init_pos, (0, 0), (0, 0))
        self.is_super = is_super

    def draw(self, surface):
        draw_pos = (self.pos[0] * ut.TILE, self.pos[1] * ut.TILE)
        surface.blit(self.img[self.draw_count], draw_pos)

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
    def __init__(self, pos=(0, 0), ipos=(0, 0), speed=(0, 0), ispeed=(0, 0),
                 inc_val=1):
        super().__init__(images.MONEY_IMG, pos, ipos, speed, ispeed)
        self.inc_val = inc_val

# class FireBonus(BonusObject):
#     def __init__(self, pos=(0, 0), ipos=(0, 0), speed=(0, 0),
#                  ispeed=(0, 0), inc_val=10):
#         super().__init__(BONUS_IMG, pos, ipos, speed, ispeed, inc_val)
