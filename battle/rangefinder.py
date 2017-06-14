from typing import Dict, List

from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.units import Soldier




class RangeFinder(object):
    def __init__(self, map_: Map):
        self._map = map_

    def get_all_points(self, origin: Point, max_distance: int) -> Dict[int, List[Point]]:
        distances_to_points = dict.fromkeys(range(max_distance + 1), [])
        largest_map_distance = sum(self._map.get_size())

        stop_checking_map = min(largest_map_distance, max_distance) + 1

        for distance in range(stop_checking_map):
            on_map_pts = [point for point in origin.at_distance(distance) if self._map.is_on_map(point)]
            distances_to_points[distance] = on_map_pts
        return distances_to_points

    def get_all_units(self, origin: Point, max_distance: int) -> Dict[int, List[Soldier]]:
        distances_to_points = self.get_all_points(origin, max_distance)
        distances_to_units = {}
        for distance, points in distances_to_points.items():
            units = [self._map.get_unit(point) for point in points if self._map.has_unit(point)]
            distances_to_units[distance] = units
        return distances_to_units

    def proto_range_finder_no_tests_needs_work(self, origin: Point, max_mv: int) -> dict:
        point_to_mvpts = {origin: 0}

        distances = self.get_all_points(origin, max_mv)

        for distance in range(1, max_mv + 1):
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
        if self._map.can_place_unit(finish) and self._map.can_place_unit(start):
            return self._map.get_tile(start).move_pts(self._map.get_tile(finish))
        else:
            return float('inf')


def _any_edge_values_le_max_mv(edges, mv_pts_dict, max_mv):
    return any(mv_pts_dict[edge] <= max_mv for edge in edges)


def _remove_values_above_cutoff(dictionary, cutoff):
    return {point: mv_pts for point, mv_pts in dictionary.items() if mv_pts <= cutoff}
