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
        """
        Here is a strategy to get correct answer.

        Think of searching until you find all the final edges.

        ex:
        elevations = {Point(0, 0): 9, Point(1, 0): 0,
                      Point(0, 1): 1, Point(1, 1): 0}
        start = Point(1, 1)
        max_mv = 5
        answer_with_final_edges = {
                                                 Point(1, -1): inf,
                               Point(0, 0): 9,   Point(1, 0): 1, Point(2, 0): inf,
            Point(-1, 1): inf, Point(0, 1): 2,   Point(1, 1): 0, Point(2, 1): inf,
                               Point(0, 2): inf, Point(1, 2): inf
        }
        You know you're done when all the edges of your map are final edges.
        final_edges = {Point(1, -1), Point(0, 0), Point(2, 0), Point(-1, 1), Point(2, 1), Point(0, 2), Point(1, 2)}
        return a dictionary with all the final edges removed. i.e.
        answer = {
                            Point(1, 0): 1,
            Point(0, 1): 2, Point(1, 1): 0
        }

        read the new tests to see what you should be doing.  feel free to @unittest.expectedFailure over various tests
        so that you can work on things one at a time.  i made a "pretty_print" function in the tests so that you
        print out your answer to see what the heck it's doing.

        SPOILERS BELOW.  iF YOU WANT TO TRY ON YOUR OWN, DELETE WITHOUT READING (you can always look at the closed
        PR on github to see it later).  THE "NOTES:" PART IS LESS SPOILERY THAN THE NUMBERED LIST.

        edges is a set that is the newest parts of exploration.
        for each pt in edges:
        1 - check to see if the pt is a final edge (it's got more mv_pts than max_mv)
        2 - for each pt that's not a final edge,
            a - remove it from edges set
            b - for each adjacent pt to the removed point,
                check if it's a new edge (think about why a pt would be considered a new edge)
            c - add each new edge to the edges and update it's value in the movement_points dict
        3 - if all your edges are final edges, you're done
        4 - snip all the finished edges from the dictionary and return that dictionary

        notes:
        use "_get_mv_pts" below. it's convenient
        in tests, if you want to see what you made, use "pretty_print"
        remember when you're updating the edges that YOU CANNOT CHANGE A SET WHILE YOU'RE ITERATING THROUGH IT. make
        a copy of the set to update and then make that the new set of edges.
        """
        edges = {start}  # this is a set.  if you don't know what that is, read the python documentation.
        movement_points = {start: 0}

    def _get_mv_pts(self, start, finish):
        if self._map.can_place_unit(finish):
            return self._map.get_tile(start).move_pts(self._map.get_tile(finish))
        else:
            return float('inf')
