from typing import Dict

from battle.maptools.direction import Direction
from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.players.units import Soldier


class MovementTracker(object):

    def __init__(self, map_: Map):
        self._map = map_
        self._units = {}  # type: Dict[Soldier, Point]

    def get_point(self, unit: Soldier) -> Point:
        return self._units.get(unit)

    def set_point(self, unit: Soldier, point: Point):
        self.del_point(unit)
        self._map.place_unit(unit, point)
        self._units[unit] = point

    def del_point(self, unit: Soldier):
        point = self.get_point(unit)
        if point:
            self._map.remove_unit(point)
            self._units[unit] = None

    def is_placed(self, unit: Soldier) -> bool:
        return not self.get_point(unit) is None

    def move(self, unit: Soldier, direction: Direction) -> bool:
        """cannot move if not can_move"""
        if not self.is_placed(unit):
            raise AttributeError('unit is not on the map')
        if not self.is_move_allowed(unit, direction):
            return False
        new_point = self.get_point(unit).in_direction(direction)
        mv_points = self.get_move_pts(unit, direction)
        if not self.has_enough_move(unit, mv_points):
            return False
        unit.move(mv_points)
        self.set_point(unit, new_point)
        return True

    def is_move_allowed(self, unit: Soldier, direction: Direction) -> bool:
        if not self.is_placed(unit):
            return False
        point = self.get_point(unit)
        new_point = point.in_direction(direction)
        if not self._map.can_place_unit(new_point):
            return False
        return True

    def has_enough_move(self, unit: Soldier, mv_pts: int) -> bool:
        return unit.can_act(mv_pts)

    def get_move_pts(self, unit: Soldier, direction: Direction) -> int:
        point = self.get_point(unit)
        new_point = point.in_direction(direction)
        if not self._map.has_tile(new_point):
            raise ValueError('target point does not have a tile')
        current_tile = self._map.get_tile(point)
        new_tile = self._map.get_tile(new_point)
        move_points = current_tile.move_pts(new_tile)
        return move_points
