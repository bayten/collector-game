'''
utils.py -- utilities and constants submodule
=============================================
This is module, which mainly consists of constants and utility functions.
'''

import pygame  # type: ignore
from enum import Enum
from typing import Tuple, List


BSIZE: Tuple[int, int] = (20, 20)
TILE: int = 40
FPS: int = 70
ANIMATION_ITER: float = 0.5
ENEMY_SLOW: int = 2

Coord = Tuple[int, int]
Size = Tuple[int, int]
Image = pygame.Surface
Event = pygame.event.Event
Clock = pygame.time.Clock
Trigger = Tuple[str, int, int]

PLAYER_CONFIG = ((0, 0), (3, 3), (0, 10))

GAME_FONT = 'CollectorGame/FortunataCYR.ttf'

UselessAdvices: List[str] = [
    'Шипы опасны',
    'Избегай врагов',
    'Собирай монетки',
    'У тебя есть бомбы',
    'Может, это не твоё?',
    'Мне тебя уже жалко'
]

UselessCongrats: List[str] = [
    'Неплохо, неплохо...',
    'Что-то ты можешь...',
    'И что, это всё?',
    'Неплохо (для новичка)'
]


class WinCondition(Enum):
    COLLECT_ALL = 0,
    KILL_ALL = 1,
    GET_GOAL = 2


class FieldBounds(Enum):
    RECT = 0,
    TORUS = 1


class ExplosionType(Enum):
    CROSS = 0,
    CIRCLE = 1


def sign(a) -> int:
    if a == 0:
        return 0
    if a > 0:
        return 1
    if a < 0:
        return -1
