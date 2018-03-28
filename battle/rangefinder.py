from typing import Dict, List, Tuple

from battle.lineofsight import LineOfSight
from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.players.units import Soldier


class RangeFinder(object):
    def __init__(self, map_: Map):
        self._map = map_
        self._sighter = LineOfSight(map_)

    def get_all_usable_points_units_only(self, origin: Point, max_distance: int) -> Dict[int, List[Point]]:
        distances_to_points = {key: [] for key in range(max_distance+1)}
        largest_map_distance = sum(self._map.get_size())

        stop_checking_map = min(largest_map_distance, max_distance) + 1

        for distance in range(stop_checking_map):
            on_map_pts = [point for point in origin.at_distance(distance)
                          if self._map.has_unit(point)]
            distances_to_points[distance] = on_map_pts
        return distances_to_points

    def get_all_usable_points(self, origin: Point, max_distance: int) -> Dict[int, List[Point]]:
        distances_to_points = dict.fromkeys(range(max_distance + 1), [])
        largest_map_distance = sum(self._map.get_size())

        stop_checking_map = min(largest_map_distance, max_distance) + 1

        for distance in range(stop_checking_map):
            on_map_pts = [point for point in origin.at_distance(distance)
                          if self._map.is_on_map(point) and self._map.has_tile(point)]
            distances_to_points[distance] = on_map_pts
        return distances_to_points

    def get_all_units(self, origin: Point, max_distance: int) -> Dict[int, List[Soldier]]:
        distances_to_points = self.get_all_usable_points(origin, max_distance)
        distances_to_units = {}
        for distance, points in distances_to_points.items():
            units = [self._map.get_unit(point) for point in points if self._map.has_unit(point)]
            distances_to_units[distance] = units
        return distances_to_units

    def get_sight_ranges(self, origin: Point, max_distance: int) -> dict:
        points = self.get_all_usable_points(origin, max_distance)
        return {key: [point for point in val if self._sighter.can_sight_target(point, origin)]
                for key, val in points.items()}

    def get_sight_ranges_units_only(self, origin: Point, max_distance: int) -> dict:
        points = self.get_all_usable_points_units_only(origin, max_distance)
        return {key: [point for point in val if self._sighter.can_sight_target(point, origin)]
                for key, val in points.items()}

    def get_attack_ranges_ranged(self, origin: Point, range_: int) -> dict:
        distance_point_dict = self.get_sight_ranges(origin, range_)
        new_dict = {distance: self._get_advantage_list(origin, points)
                    for distance, points in distance_point_dict.items()}
        return new_dict

    def get_attack_ranges_ranged_units_only(self, origin: Point, range_: int) -> dict:
        distance_point_dict = self.get_sight_ranges_units_only(origin, range_)
        new_dict = {distance: self._get_advantage_list(origin, points)
                    for distance, points in distance_point_dict.items()}
        return new_dict

    def _get_advantage_list(self, shooter: Point, targets: List[Point]) -> List[Tuple[Point, int]]:
        return [(point, self._get_advantage_value(shooter, point)) for point in targets]

    def _get_advantage_value(self, shooter: Point, target: Point) -> int:
        shooter_el = self._map.get_elevation(shooter)
        target_el = self._map.get_elevation(target)
        if shooter_el > target_el:
            return 1
        elif shooter_el < target_el:
            return -1
        else:
            return 0

    def get_attack_ranges_melee(self, origin: Point, range_: int = 1) -> dict:
        """return dict of ranges: [(point, advantage_value)]
                elevation limit is +/- 3"""
        raw_answer = self.get_attack_ranges_ranged(origin, range_)

        answer = {distance: self._filter_by_melee_reach(point_advantage_list, origin)
                  for distance, point_advantage_list in raw_answer.items()}
        return answer

    def get_attack_ranges_melee_units_only(self, origin: Point, range_: int = 1) -> dict:
        """return dict of ranges: [(point, advantage_value)]
                elevation limit is +/- 3"""
        raw_answer = self.get_attack_ranges_ranged_units_only(origin, range_)

        answer = {distance: self._filter_by_melee_reach(point_advantage_list, origin)
                  for distance, point_advantage_list in raw_answer.items()}
        return answer

    def _filter_by_melee_reach(self, point_advantage_list, origin):
        melee_reach_limit = 3
        new_list = [point_advantage for point_advantage in point_advantage_list if
                    self._is_elevation_in_range(origin, point_advantage[0], melee_reach_limit)]
        return new_list

    def _is_elevation_in_range(self, shooter: Point, target: Point, el_range: int):
        shooter_el = self._map.get_elevation(shooter)
        target_el = self._map.get_elevation(target)
        distance = abs(shooter_el - target_el)
        if distance <= el_range:
            return True
        else:
            return False
