from battle.maptools.point import Point


class BaseUnit(object):

    def __init__(self):
        self._point = None

    def get_point(self) -> Point:
        return self._point

    def has_point(self) -> bool:
        return self._point is not None

    def set_point(self, point: Point):
        self._point = point

    def del_point(self):
        self._point = None
