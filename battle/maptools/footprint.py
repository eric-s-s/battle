from collections import deque
from enum import Enum
from battle.maptools.direction import Direction
from battle.maptools.vector import Vector



class Token(Enum):
    """
        :values (int, int):  (danger, opportunity)
        """
    DEAD = (2, 0)
    DANGER = (1, 0)
    NEUTRAL = (0, 0)
    OBJECTIVE = (0, 1)
    ATTACKING = (1, 2)
    # put in more.


class FootPrint(object):
    def __init__(self, token: Token, direction: Direction, team):
        self._token = token
        self._direction = direction
        self._team = team

    @property
    def token(self):
        return self._token

    @property
    def direction(self):
        return self._direction

    @property
    def team(self):
        return self._team


class FootPrintPackage(object):
    def __init__(self, max_size=10):
        self._stack = deque([], maxlen=max_size)

    def push(self, footprint: FootPrint):
        self._stack.appendleft(footprint)

    @property
    def footprints(self):
        return list(self._stack)




    # @property
    # def team_matrices(self):
    #     """returns data for each team's traffic/direction, danger/direction, opportunity/direction"""
    #     data = []
    #     for foot_print in self.footprints:

    #
    # def calculate_danger_and_opportunity(self):
    #     pass

