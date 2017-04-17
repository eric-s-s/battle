from typing import Dict

from battle.maptools.point import Point
from battle.map import Map
from battle.maptools.direction import Direction
from battle.units import Soldier


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
            self._units[Soldier] = None

    def move(self, unit: Soldier, direction: Direction) -> bool:
        """cannot move if not can_move"""
        if not self.is_move_allowed(unit, direction):
            return False
        new_point = self.get_point(unit).in_direction(direction)
        mv_points = self.get_move_pts(unit, new_point)
        if not self.has_enough_move(unit, mv_points):
            return False
        unit.move(mv_points)
        self.set_point(unit, new_point)
        return True

    def is_move_allowed(self, unit: Soldier, direction: Direction) -> bool:
        point = self.get_point(unit)
        if not point:
            return False
        new_point = point.in_direction(direction)
        if not self._map.can_place_unit(new_point):
            return False
        return True

    def has_enough_move(self, unit: Soldier, mv_pts: int) -> bool:
        return unit.can_move(mv_pts)

    def get_move_pts(self, unit, new_point):
        new_tile = self._map.get_tile(new_point)
        move_points = self._map.get_tile(self.get_point(unit)).move_pts(new_tile)
        return move_points

