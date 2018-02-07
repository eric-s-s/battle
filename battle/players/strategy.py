import random
from typing import List

from battle.maptools.footprint import DangerOpportunity
from battle.players.action import Action


class Strategy(object):
    def __init__(self):
        pass

    def get_action(self, ally: DangerOpportunity, enemy: DangerOpportunity) -> List[Action]:
        actions = []
        ally_danger = ally.danger
        ally_opportunity = ally.opportunity
        enemy_danger = enemy.danger
        enemy_opportunity = enemy.opportunity
        return actions


class BasicStrategy(Strategy):
    def __init__(self):
        super(BasicStrategy, self).__init__()

    def get_action(self, ally, enemy):
        return random.choice(list(Action.to_list()))
