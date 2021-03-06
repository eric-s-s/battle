from math import floor, ceil
from battle.maptools.point import Point
from battle.maptools.map import Map


class LineOfSight(object):
    def __init__(self, map_: Map):
        self.map = map_

    def can_sight_target(self, target: Point, shooter: Point) -> bool:
        if self.is_target_below_shooter(target, shooter):
            return not self.is_obstacle_higher_than_start(shooter, target)
        else:
            return not self.is_obstacle_higher_than_start(target, shooter)

    def is_target_below_shooter(self, target: Point, shooter: Point) -> bool:
        return self.map.get_elevation(target) < self.map.get_elevation(shooter)

    def is_target_above_shooter(self, target: Point, shooter: Point) -> bool:
        return self.map.get_elevation(target) > self.map.get_elevation(shooter)

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
        for delta_x in get_deltas_between(start.x, finish.x):
            delta_y_1 = floor(slope * delta_x)
            delta_y_2 = ceil(slope * delta_x)
            if self.map.get_elevation(start.plus(delta_x, delta_y_1)) > self.map.get_elevation(start):
                return True
            if self.map.get_elevation(start.plus(delta_x, delta_y_2)) > self.map.get_elevation(start):
                return True
        return False

    def is_higher_than_start_by_bounding_xs(self, start: Point, finish: Point) -> bool:
        slope = get_slope(start, finish)
        for delta_y in get_deltas_between(start.y, finish.y):
            delta_x_1 = floor(delta_y / slope)
            delta_x_2 = ceil(delta_y / slope)
            if self.map.get_elevation(start.plus(delta_x_1, delta_y)) > self.map.get_elevation(start):
                return True
            if self.map.get_elevation(start.plus(delta_x_2, delta_y)) > self.map.get_elevation(start):
                return True
        return False


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
