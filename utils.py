from enum import Enum

BSIZE = 20, 20
TILE = 40
FPS = 1

class LVLObject(Enum):
    WALL = 1,
    GOLD = 2

class GameWinCondition(Enum):
    COLLECT_ALL = 1,
    KILL_ALL = 2
