from math import floor, ceil
from typing import Union
from battle.maptools.point import Point
from battle.maptools.map import Map


class Slopey(object):
    def __init__(self, map_: Map):
        self.map = map_

    def can_hit_target(self, target: Point, shooter: Point) -> bool:
        if self.is_target_below_shooter(target, shooter):
            return not self.is_obstacle_higher_than_start(shooter, target)
        else:
            return not self.is_obstacle_higher_than_start(target, shooter)

    def is_target_below_shooter(self, target: Point, shooter: Point) -> bool:
        return self.get_elevation(target) < self.get_elevation(shooter)

    def is_obstacle_higher_than_start(self, start: Point, finish: Point) -> bool:
        slope = get_slope(start, finish)
        if -1 < slope < 1:
            return self.is_higher_than_start_by_bounding_ys(start, finish)
        else:
            return self.is_higher_than_start_by_bounding_xs(start, finish)

    def is_higher_than_start_by_bounding_ys(self, start: Point, finish: Point) -> bool:
        """
        use floor and ceil
        """
        slope = get_slope(start, finish)
        for x in get_deltas_between(start.x, finish.x):
            y_1 = floor(slope * x)
            y_2 = ceil(slope * x)
            if self.get_elevation(Point(x, int(y_1))) > self.get_elevation(start):
                return True
            if self.get_elevation(Point(x, int(y_2))) > self.get_elevation(start):
                return True
        return False

    def is_higher_than_start_by_bounding_xs(self, start: Point, finish: Point) -> bool:
        slope = get_slope(start, finish)
        for delta_y in get_deltas_between(start.y, finish.y):
            delta_x_1 = floor(delta_y / slope)
            delta_x_2 = ceil(delta_y / slope)
            if self.get_elevation(start.plus(delta_x_1, delta_y)) > self.get_elevation(start):
                return True
            if self.get_elevation(start.plus(delta_x_2, delta_y)) > self.get_elevation(start):
                return True
        return False

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


def get_deltas_between(a, b):
    change = b - a
    if change > 0:
        return range(1, change)
    else:
        return range(-1, change, -1)
