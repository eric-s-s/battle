import random

from battle.maptools.footprint import FootPrint, FootPrintPackage, Token
from battle.maptools.map import Map
from battle.players.team import Team
from battle.players.units import Soldier
from battle.perimiterlistener import PerimeterListener
from battle.rangefinder import RangeFinder
from battle.movementcalculator import MovementCalculator


class Actionator(object):
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

    def create_turn_order(self):
        team_1_list = self._team_1.deployed
        team_2_list = self._team_2.deployed
        turn_order = team_1_list + team_2_list
        random.shuffle(turn_order)
        self._unmoved_units = turn_order

    def get_action_list(self, unit: Soldier):
        point = self._map.get_point(unit)
        tile = self._map.get_tile(point)
        fpp = FootPrintPackage()
        strategy = unit.strategy
        # get footprint
        # get vectors,
        # call unit.strategy with vectors and correct teams.

    # def find_next_action(self, ???):
