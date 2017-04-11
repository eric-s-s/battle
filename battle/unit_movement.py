from battle.maptools.point import Point
from battle.map import Map, MapPlacementError
from battle.maptools.direction import Direction


class UnitMovement(object):

    def __init__(self, map_: Map = None, max_move: int = 3):
        self._point = None  # type: Point
        self._map = map_
        self._max_move = max_move
        self._current_move_pts = self._max_move

    @property
    def mv_pts(self) -> int:
        return self._current_move_pts

    def get_point(self) -> Point:
        return self._point

    def has_point(self) -> bool:
        return self._point is not None

    def set_point(self, point: Point):
        self._raise_no_map_error()
        self.del_point()
        self._map.place_unit(self, point)
        self._point = point

    def _raise_no_map_error(self):
        if not self.has_map():
            raise MapPlacementError('unit not assigned to any map.')

    def del_point(self):
        if self.has_point():
            self._map.remove_unit(self._point)
            self._point = None

    def set_map(self, map_: Map):
        self._map = map_

    def has_map(self) -> bool:
        return self._map is not None

    def is_on_map(self, map_: Map) -> bool:
        return self._map is map_

    def move(self, direction) -> bool:
        """cannot move if not can_move"""
        if not self.is_move_allowed(direction):
            return False
        new_point = self._point.in_direction(direction)
        mv_points = self.get_move_pts(new_point)
        if not self.has_enough_move(mv_points):
            return False
        self._current_move_pts -= mv_points
        self.set_point(new_point)
        return True

    def is_move_allowed(self, direction: Direction) -> bool:
        if not self.has_map() or not self.has_point():
            return False
        new_point = self._point.in_direction(direction)
        if not self._map.can_place_unit(new_point):
            return False
        return True

    def has_enough_move(self, mv_pts: int) -> bool:
        return self._current_move_pts >= mv_pts

    def get_move_pts(self, new_point):
        new_tile = self._map.get_tile(new_point)
        move_points = self._map.get_tile(self._point).move_pts(new_tile)
        return move_points

    def reset_movement_pts(self):
        self._current_move_pts = self._max_move
