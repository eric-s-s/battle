from collections import deque, namedtuple
from typing import Dict
from enum import Enum
from battle.maptools.direction import Direction
from battle.maptools.vector import Vector


DangerOpportunity = namedtuple('DangerOpportunity', ['danger', 'opportunity'])


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

    @property
    def danger(self):
        return self.value[0]

    @property
    def opportunity(self):
        return self.value[1]


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

    def vectorize(self):
        danger = Vector.from_dir_and_mag(self.direction, self.token.danger)
        opportunity = Vector.from_dir_and_mag(self.direction, self.token.opportunity)
        return DangerOpportunity(danger=danger, opportunity=opportunity)


class FootPrintPackage(object):
    def __init__(self, max_size=10):
        self._stack = deque([], maxlen=max_size)

    def push(self, footprint: FootPrint):
        self._stack.appendleft(footprint)

    @property
    def footprints(self):
        return list(self._stack)

    def team_vectors(self):
        answer = {}  # type: Dict['Team', DangerOpportunity]
        for footprint in self._stack:
            team = footprint.team
            if team in answer:
                current = answer[team]
                vectors = footprint.vectorize()  # type: DangerOpportunity
                new_danger = current.danger.add(vectors.danger)
                new_opportunity = current.opportunity.add(vectors.opportunity)
                answer[team] = DangerOpportunity(danger=new_danger, opportunity=new_opportunity)
            else:
                answer[team] = footprint.vectorize()

        return answer




    # @property
    # def team_matrices(self):
    #     """returns data for each team's traffic/direction, danger/direction, opportunity/direction"""
    #     data = []
    #     for foot_print in self.footprints:

    #
    # def calculate_danger_and_opportunity(self):
    #     pass

