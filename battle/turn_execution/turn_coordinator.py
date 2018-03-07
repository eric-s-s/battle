import random

from battle.maptools.vector import DangerOpportunity
from battle.maptools.footprint import FootPrint, FootPrintPackage, Token
from battle.maptools.map import Map
from battle.players.team import Team
from battle.players.units import Soldier
from battle.perimiterlistener import PerimeterListener
from battle.rangefinder import RangeFinder
from battle.movementcalculator import MovementCalculator


class Actionator(object):
    def __init__(self, unit: Soldier, action, perimeter_listener: PerimeterListener, map_: Map):
        self._unit = unit
        self._action = action
        self._pl = perimeter_listener
        self._map = map_

    def move(self, path):
        """
                get location
                get path  list of points
                    sigh range, enemy ally
                    attack range, enemy


                for point in path:
                    check pl
                jump to destination
                set pl

                pseudo-code
                """
        pass

    def attack(self):
        pass





class TurnCoordinator(object):
    def __init__(self, map_: Map, team_1: Team, team_2: Team):
        self._map = map_
        self._team_1 = team_1
        self._team_2 = team_2
        self._pm = PerimeterListener(self._map)
        self._mc = MovementCalculator(self._map)
        self._rf = RangeFinder(self._map)

        self._unmoved_units = []

    def get_ally_enemy(self, unit):
        if self._team_1.is_on_team(unit):
            return self._team_1, self._team_2
        return self._team_2, self._team_1

    def create_turn_order(self):
        team_1_list = self._team_1.deployed
        team_2_list = self._team_2.deployed
        turn_order = team_1_list + team_2_list
        random.shuffle(turn_order)
        self._unmoved_units = turn_order

    def get_action_list(self, unit: Soldier):
        point = self._map.get_point(unit)
        ally, enemy = self.get_ally_enemy(unit)
        vectors = self._map.get_tile(point).footprint_vectors()
        ally_vector = vectors.get(ally, DangerOpportunity.empty())
        enemy_vector = vectors.get(enemy, DangerOpportunity.empty())
        return unit.strategy.get_action(ally_vector, enemy_vector)

