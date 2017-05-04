from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.maptools.direction import Direction


class RangeFinder(object):
    def __init__(self, map_: Map):
        self._map = map_

    def get_all_points(self, origin: Point, max_distance: int) -> list:
        """not including point at origin!!!  use point.at_distance(int)"""
        points = []
        for distance in range(1, max_distance + 1):
            on_map_pts = [point for point in origin.at_distance(distance) if self._map.is_on_map(point)]
            points += on_map_pts
        return points

    def get_all_units(self, origin: Point, max_distance: int) -> list:
        """not including unit at origin!!!"""
        points = self.get_all_points(origin, max_distance)
        return [self._map.get_unit(point) for point in points if self._map.has_unit(point)]

    def get_distances(self, origin: Point, range_: int) -> dict:
        """get dict with keys Point and values mvpts from origin

                one method  = get all points/tiles in range 1
                create a dict of mv from origin to new point   use origin_tile.get_move_pts(range_1_tile)

                then for point tile in range_1 get all point in point.at_distance(1).  compute new move by adding it value in answer_dict + move from tile to
                new spot.  if new spot in answer dict, take the min.


                ."""
        pass

