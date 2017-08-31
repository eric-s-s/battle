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
        start_movement_values = {start: (0, [])}
        max_val = (max_mv, [Direction.N] * self._map.get_size()[0])

        raw_movement_values = self._create_raw_movement_values(edges, max_val, start_movement_values)

        return _remove_values_above_cutoff(raw_movement_values, max_val)

    def get_movement_points(self, start: Point, max_mv: int) -> Dict[Point, int]:
        edges = {start}
        start_movement_values = {start: 0}
        max_val = max_mv

        raw_movement_values = self._create_raw_movement_values(edges, max_val, start_movement_values)

        return _remove_values_above_cutoff(raw_movement_values, max_val)

    def _create_raw_movement_values(self, edges_to_investigate, max_val, movement_values):
        new_movement_values = movement_values.copy()
        while _any_edge_values_le_max(edges_to_investigate, new_movement_values, max_val):
            temp_edges = set()
            for edge in edges_to_investigate:
                new_movement_values, new_edges = self._get_updated_mv_values_and_new_edges(edge, max_val, new_movement_values)
                temp_edges.update(new_edges)
            edges_to_investigate = temp_edges.copy()
        return new_movement_values

    def _get_updated_mv_values_and_new_edges(self, edge, max_val, move_values):
        new_edges = set()
        updated_mv_values = move_values.copy()
        base_move_value = updated_mv_values[edge]
        if base_move_value < max_val:
            for direction in Direction:

                if isinstance(max_val, tuple):
                    new_edge, new_move_val = self._get_candidates_with_path(base_move_value, edge, direction)
                else:
                    new_edge, new_move_val = self._get_candidates_without_path(base_move_value, edge, direction)

                if new_edge not in updated_mv_values or new_move_val < updated_mv_values[new_edge]:
                    new_edges.add(new_edge)
                    updated_mv_values[new_edge] = new_move_val

        return updated_mv_values, new_edges

    def _get_candidates_with_path(self, base_move_value, edge, direction):
        candidate_edge = edge.in_direction(direction)
        move_pts = self._get_mv_pts(edge, candidate_edge) + base_move_value[0]
        path = base_move_value[1][:]
        path.append(direction)
        candidate_move_value = (move_pts, path)
        return candidate_edge, candidate_move_value

    def _get_candidates_without_path(self, base_move_value, edge, direction):
        candidate_edge = edge.in_direction(direction)
        candidate_move_value = self._get_mv_pts(edge, candidate_edge) + base_move_value
        return candidate_edge, candidate_move_value

    def _get_mv_pts(self, start, finish):
        if self._map.can_place_unit(finish):
            return self._map.get_tile(start).move_pts(self._map.get_tile(finish))
        else:
            return float('inf')


def _any_edge_values_le_max(edges, mv_pts_dict, max_mv):
    return any(mv_pts_dict[edge] <= max_mv for edge in edges)


def _remove_values_above_cutoff(dictionary, cutoff):
    return {point: mv_pts for point, mv_pts in dictionary.items() if mv_pts <= cutoff}
