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

    def get_movement_points(self, start, max_mv):
        movement_points = {start: 0}
        edges = {start}
        while not all_edges_gt_max_mv(movement_points, edges, max_mv):
            edges, movement_points = self._update_edges_and_move_points(edges, movement_points, max_mv)
        return {point: value for point, value in movement_points.items() if value <= max_mv}

    def _update_edges_and_move_points(self, edges, movement_points, max_mv):
        new_mv_pts = movement_points.copy()
        new_edges = edges.copy()
        for old_edge in edges:
            if new_mv_pts[old_edge] <= max_mv:
                new_edges.remove(old_edge)
                new_edge_mv_pts = self._get_movement_pts_for_new_edges(old_edge, new_mv_pts)
                new_edges.update(new_edge_mv_pts)
                new_mv_pts.update(new_edge_mv_pts)
        return new_edges, new_mv_pts

    def _get_movement_pts_for_new_edges(self, current_edge, current_movement_pts):
        new_edges = {}
        candidate_edges = current_edge.at_distance(1)
        for new_edge in candidate_edges:
            mv = self._get_mv_pts(current_edge, new_edge) + current_movement_pts[current_edge]
            if new_edge not in current_movement_pts or mv < current_movement_pts[new_edge]:
                new_edges[new_edge] = mv
        return new_edges

    def _get_mv_pts(self, start, finish):
        if self._map.can_place_unit(finish):
            return self._map.get_tile(start).move_pts(self._map.get_tile(finish))
        else:
            return float('inf')


def all_edges_gt_max_mv(points_dict, edges, max_mv):
    return all(points_dict[edge] > max_mv for edge in edges)


