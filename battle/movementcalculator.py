from typing import Dict, Tuple, List

from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.maptools.direction import Direction


PtsToMvAndPath = Dict[Point, Tuple[Point, List[Direction]]]


class MovementCalculator(object):
    def __init__(self, map_: Map):
        self._map = map_

    def get_movement_points_with_path(self, start: Point, max_mv: int) -> PtsToMvAndPath:
        """

        {Point: (distance, [directions from origin]}
        """
        edges = {start}
        mv_pts_and_path = {start: (0, [])}

        while _any_edge_values_le_max_mv(edges, mv_pts_and_path, (max_mv, [])):
            temp_edges = set()
            for edge in edges:
                mv_pts_and_path, new_edges = self._get_updated_pts_and_dir_and_new_edges(edge, max_mv, mv_pts_and_path)
                temp_edges.update(new_edges)
            edges = temp_edges.copy()

        return _remove_values_above_cutoff_pts_path_dict(mv_pts_and_path, max_mv)

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

    def _get_updated_pts_and_dir_and_new_edges(self, edge, max_mv, mv_pts_and_path):
        new_edges = set()
        mv_pts_update = mv_pts_and_path.copy()
        pts_from_origin, path_from_origin = mv_pts_update[edge]
        if pts_from_origin < max_mv:
            for new_direction in Direction:
                possible_edge = edge.in_direction(new_direction)
                possible_pts = self._get_mv_pts(edge, possible_edge) + pts_from_origin
                possible_path = path_from_origin[:]
                possible_path.append(new_direction)
                if possible_edge not in mv_pts_update or (possible_pts, possible_path) < mv_pts_update[possible_edge]:
                    new_edges.add(possible_edge)

                    mv_pts_update[possible_edge] = (possible_pts, possible_path)
        return mv_pts_update, new_edges

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


def _remove_values_above_cutoff_pts_path_dict(dictionary, cutoff):
    return {point: pts_path for point, pts_path in dictionary.items() if pts_path[0] <= cutoff}