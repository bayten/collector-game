from enum import Enum
BSIZE = 20, 20
TILE = 40
FPS = 15
ANIMATION_ITER = 0.2


class LVLObject(Enum):
    WALL = 1,
    GOLD = 2


class GameWinCondition(Enum):
    COLLECT_ALL = 0,
    KILL_ALL = 1


class FieldBounds(Enum):
    RECT = 0,
    TORUS = 1
