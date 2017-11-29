from typing import List
from battle.maptools.point import Point
from battle.maptools.map import Map
from battle.players.units import Soldier, Base


class Team(object):
    def __init__(self, home: Point, map_: Map):
        self._placed_units = []
        self._unplaced_units = []
        self._map = map_
        self._home = home
        self._base = Base()
        self._map.place_unit(self._base, self._home)

    @property
    def home(self):
        return self._home

    @property
    def base(self):
        return self._base

    @property
    def players(self):
        return self._placed_units[:] + self._unplaced_units[:]

    def add_player(self, player: Soldier):
        if not self.is_on_team(player):
            self._unplaced_units.append(player)

    def unteam_player(self, player: Soldier):
        if player in self._placed_units:
            index = self._placed_units.index(player)
            del self._placed_units[index]
        elif player in self._unplaced_units:
            index = self._unplaced_units.index(player)
            del self._unplaced_units[index]
        else:
            raise ValueError('Player is not on the team')

    def is_on_team(self, player: Soldier):
        return player in self.players

    def spawn(self):
        if not self._unplaced_units:
            raise ValueError('No unplaced units!')
        unit = self._unplaced_units.pop(0)
        max_distance = sum(self._map.get_size())
        current_distance = 1
        while current_distance <= max_distance:
            candidates = self.home.at_distance(current_distance)
            for candidate in candidates:
                if self._map.can_place_unit(candidate):
                    self._map.place_unit(unit, candidate)
                    self._placed_units.append(unit)
                    return unit, candidate
            current_distance += 1
        raise ValueError('No space for you!')
