from typing import Dict, List

from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.units import Soldier
from battle.maptools.direction import Direction


class RangeFinder(object):
    def __init__(self, map_: Map):
        self._map = map_

    def get_all_points(self, origin: Point, max_distance: int) -> Dict[int, List[Point]]:
        """not including point at origin!!!  use point.at_distance(int)"""
        distances_to_points = {}

        for distance in range(0, max_distance + 1):
            on_map_pts = [point for point in origin.at_distance(distance) if self._map.is_on_map(point)]
            distances_to_points[distance] = on_map_pts
        return distances_to_points

    def get_all_units(self, origin: Point, max_distance: int) -> Dict[int, List[Soldier]]:
        """not including unit at origin!!!"""
        distances_to_points = self.get_all_points(origin, max_distance)
        distances_to_units = {}
        for distance, points in distances_to_points.items():
            units = [self._map.get_unit(point) for point in points if self._map.has_unit(point)]
            distances_to_units[distance] = units
        return distances_to_units

    def get_distances(self, origin: Point, range_: int) -> dict:
        """get dict with keys Point and values mvpts from origin

                one method  = get all points/tiles in range 1
                create a dict of mv from origin to new point   use origin_tile.get_move_pts(range_1_tile)

                then for point tile in range_1 get all point in point.at_distance(1).  compute new move by adding it value in answer_dict + move from tile to
                new spot.  if new spot in answer dict, take the min.

                output =

                ."""
        point_to_mvpts = {origin: 0}

        distances = self.get_all_points(origin, range_)

        for distance in range(1, range_ + 1):
            points = distances[distance]
            for point in points:
                neighbors = point.at_distance(1)
                point_value = float('inf')
                for neighbor_pt in neighbors:
                    if neighbor_pt in point_to_mvpts:
                        origin_to_neighbor = point_to_mvpts[neighbor_pt]
                        neighbor_to_point = self._map.get_tile(neighbor_pt).move_pts(self._map.get_tile(point))
                        point_value = min(point_value, neighbor_to_point + origin_to_neighbor)
                    point_to_mvpts[point] = point_value
        return point_to_mvpts





