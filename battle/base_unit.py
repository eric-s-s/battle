from battle.maptools.point import Point
from battle.map import Map
from battle.maptools.direction import Direction


class BaseUnit(object):

    def __init__(self):
        self._point = None  # type: Point
        self._map = None  # type: Map
        self._max_move = 3
        self._current_move_pts = self._max_move

    def get_point(self) -> Point:
        return self._point

    def has_point(self) -> bool:
        return self._point is not None

    def set_point(self, point: Point):
        self._point = point

    def del_point(self):
        self._point = None

    def set_map(self, map_ : Map):
        self._map = map_

    def has_map(self) -> bool:
        return self._map is not None

    def is_on_map(self, map_: Map) -> bool:
        return self._map is map_

    def move(self, direction) -> bool:
        """cannot move if not can_move"""
        if not self.can_move(direction):
            return False
        #do stuf
        return True

    def can_move(self, direction: Direction) -> bool:
        if not self.has_map() or not self.has_point():
            return False
        new_point = self._point.in_direction(direction)
        if not self._map.can_place_unit(new_point):
            return False
        new_tile = self._map.get_tile(new_point)
        move_points = self._map.get_tile(self._point).move_pts(new_tile)
        return move_points <= self._current_move_pts


    def reset_movement_pts(self):
        self._current_move_pts = self._max_move
