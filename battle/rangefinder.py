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

    def get_move_points(self, origin: Point, max_mv: int) -> dict:
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

    def get_move_pts_two(self, start, max_mv):
        points_to_mvpts = {start: 0}
        edges = {start}
        while not edges_gt_max(points_to_mvpts, edges, max_mv):
            temp_edges = edges.copy()
            for point in edges:
                if points_to_mvpts[point] <= max_mv:
                    temp_edges.discard(point)
                    candidate_edges = point.at_distance(1)
                    for new_edge in candidate_edges:
                        mv = self.get_mv_pts(point, new_edge) + points_to_mvpts[point]
                        if new_edge not in points_to_mvpts:
                            points_to_mvpts[new_edge] = mv
                            temp_edges.add(new_edge)
                        elif mv < points_to_mvpts[new_edge]:
                            points_to_mvpts[new_edge] = mv
                            temp_edges.add(new_edge)

            edges = temp_edges.copy()
        return {point: value for point, value in points_to_mvpts.items() if value <= max_mv}

    def get_mv_pts(self, start, finish):
        if self._map.can_place_unit(finish):
            return self._map.get_tile(start).move_pts(self._map.get_tile(finish))
        else:
            return float('inf')


def edges_gt_max(points_dict, edges, max_mv):
    return all(points_dict[edge] > max_mv for edge in edges)


