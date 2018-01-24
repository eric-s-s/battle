from enum import Enum
import random


class Action(Enum):
    ATTACK = 1
    RETREAT = 2
    FORTIFY = 3
    AVOID = 4

    @classmethod
    def to_list(cls):
        return list(cls.__members__.values())


class Strategy(object):
    def __init__(self, team, map_):
        self._team = team
        self._map = map_

    def get_action(self) -> Action:
        raise NotImplementedError

    def act(self, action):
        raise NotImplementedError

    
class BasicStrategy(Strategy):
    def __init__(self, team, map_):
        super(BasicStrategy, self).__init__(team, map_)

    def get_action(self):
        return random.choice(list(Action.to_list()))

    def act(self, action):
        pass
