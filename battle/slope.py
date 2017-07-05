from math import floor, ceil
from typing import Union
from battle.maptools.point import Point
from battle.maptools.map import Map


class Slopey(object):
    def __init__(self, map_: Map):
        self.map = map_

    def can_hit_target(self, target: Point, shooter: Point) -> bool:
        if self.is_target_below_shooter(target, shooter):
            return self.check_obstacle_higher(shooter, target)
        else:
            return self.check_obstacle_higher(target, shooter)

    def is_target_below_shooter(self, target: Point, shooter: Point) -> bool:
        pass

    def check_obstacle_higher(self, start: Point, finish: Point) -> bool:
        slope = get_slope(start, finish)
        if -1 < slope < 1:
            return self.check_by_bounding_ys(start, finish)
        else:
            return self.check_by_bounding_xs(start, finish)

    def check_by_bounding_ys(self, start: Point, finish: Point) -> bool:
        """
        use floor and ceil
        """
        pass

    def check_by_bounding_xs(self, start: Point, finish: Point) -> bool:
        pass

    def get_elevation(self, point: Point) -> Union[int, float]:
        if not self.map.has_tile(point):
            return float('-inf')
        return self.map.get_tile(point).get_elevation()


def get_slope(start: Point, finish: Point) -> float:
    del_x = finish.x - start.x
    del_y = finish.y - start.y
    if del_x == 0:
        return del_y * float('inf')
    return del_y / del_x


