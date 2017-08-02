from typing import Dict, List, Tuple

from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.units import Soldier
from battle.lineofsight import LineOfSight


class RangeFinder(object):
    def __init__(self, map_: Map):
        self._map = map_
        self._sighter = LineOfSight(map_)

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

    def get_attack_ranges_ranged(self, origin: Point, range_: int) -> dict:
        distance_point_dict = self.get_sight_ranges(origin, range_)
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
        return {0: [(origin, 0)]}

    def get_movement_points(self, start: Point, max_mv: int) -> Dict[Point, int]:
        edges = {start}
        movement_points = {start: 0}

        while _any_edge_values_le_max_mv(edges, movement_points, max_mv):
            temp_edges = set()
            for edge in edges:
                movement_points, new_edges = self._get_updated_mv_pts_and_new_edges(edge, max_mv, movement_points)
                temp_edges.update(new_edges)
            edges = temp_edges.copy()

        return _remove_values_above_cutoff(movement_points, max_mv)

    def _get_updated_mv_pts_and_new_edges(self, edge, max_mv, movement_points):
        new_edges = set()
        mv_pts_update = movement_points.copy()
        edge_to_start = mv_pts_update[edge]
        if edge_to_start < max_mv:
            for possible_edge in edge.at_distance(1):
                mv_pts = self._get_mv_pts(edge, possible_edge) + edge_to_start
                if possible_edge not in mv_pts_update or mv_pts < mv_pts_update[possible_edge]:
                    new_edges.add(possible_edge)
                    mv_pts_update[possible_edge] = mv_pts
        return mv_pts_update, new_edges

    def _get_mv_pts(self, start, finish):
        if self._map.can_place_unit(finish):
            return self._map.get_tile(start).move_pts(self._map.get_tile(finish))
        else:
            return float('inf')


def _any_edge_values_le_max_mv(edges, mv_pts_dict, max_mv):
    return any(mv_pts_dict[edge] <= max_mv for edge in edges)


def _remove_values_above_cutoff(dictionary, cutoff):
    return {point: mv_pts for point, mv_pts in dictionary.items() if mv_pts <= cutoff}
