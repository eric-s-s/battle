
from enum import Enum


class Signals(Enum):
    DANGER = 1
    NEUTRAL = 0
    DEAD = 2
    GOAL = -1


class FootPrint(object):
    def __init__(self, signal, direction, team):
        self._signal = signal
        self._direction = direction
        self._team = team
        self._age = 0

    def dissipate(self):
        self._age += 1
