from enum import Enum
BSIZE = 20, 20
TILE = 40
FPS = 70
ANIMATION_ITER = 0.5
ENEMY_SLOW = 2


class GameWinCondition(Enum):
    COLLECT_ALL = 0,
    KILL_ALL = 1,
    GET_GOAL = 2


class FieldBounds(Enum):
    RECT = 0,
    TORUS = 1


class ExplosionType(Enum):
    CROSS = 0,
    CIRCLE = 1
