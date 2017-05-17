import unittest

from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.maptools.direction import Direction
from battle.units import Soldier
from battle.maptools.tile import Tile
from battle.rangefinder import RangeFinder


class TestRangeFinder(unittest.TestCase):
    test_map = Map(3, 3, [Tile.blank() for _ in range(9)])

    def setUp(self):
        self.ranger = RangeFinder(map_=self.test_map)
        self.soldier = Soldier()

    def tearDown(self):
        self.test_map.remove_all_units()

    def test_init(self):
        map_ = Map(2, 2, [Tile.blank(), Tile.blank(), Tile.blank(), Tile.blank()])
        range_finder = RangeFinder(map_)
        self.assertEqual(range_finder._map, map_ )

    def test_get_all_points_distance_gt_one(self):
        answer = self.ranger.get_all_points(Point(0, 0), 2)
        expected = {
            0: [Point(0, 0)],
            1: [Point(1, 0), Point(0, 1)],
            2: [Point(2, 0), Point(1, 1), Point(0, 2)]
        }
        self.assertEqual(answer, expected)

    def test_get_all_points_does_not_include_points_not_on_map(self):
        answer = self.ranger.get_all_points(Point(0, 0), 1)
        self.assertEqual(answer, {0: [Point(0, 0)],
                                  1: [Point(1, 0), Point(0, 1)]})

    def test_get_all_points_includes_points_on_map_but_with_no_tile(self):
        new_map = Map(3, 3, [])
        self.assertFalse(new_map.has_tile(Point(0, 1)))
        ranger = RangeFinder(new_map)
        answer = ranger.get_all_points(Point(0, 0), 1)
        self.assertEqual(answer, {0: [Point(0, 0)],
                                  1: [Point(1, 0), Point(0, 1)]})

    def test_get_all_units_no_units(self):
        answer = self.ranger.get_all_units(Point(0, 0), 2)
        self.assertEqual(answer, {0: [], 1: [], 2: []})

    def test_get_all_units_does_not_add_None(self):
        self.test_map.place_unit(self.soldier, Point(1, 1))
        answer = self.ranger.get_all_units(Point(0, 0), 2)
        self.assertEqual(answer, {0: [], 1: [], 2: [self.soldier]})

    def test_get_all_units_all_points_occupied(self):
        all_map_points = Point(0, 0).to_rectangle(3, 3)
        points_to_units = {point: Soldier() for point in all_map_points}
        values = list(points_to_units.values())
        self.assertIsNot(values[0], values[1])
        for point, unit in points_to_units.items():
            self.test_map.place_unit(unit, point)
        distance_to_points = self.ranger.get_all_points(Point(0, 0), 6)
        answer = {}
        for distance, points in distance_to_points.items():
            soldiers = [points_to_units[point] for point in points]
            answer[distance] = soldiers
        self.assertEqual(answer, self.ranger.get_all_units(Point(0, 0), 6))

        # """put soldiers in one by one and then test two lists.  rememeber that the order of points
        #     will be important. you can sort your points00by distance first first."""

    def test_get_distances_flat_tiles(self):
        map_ = Map(3, 3, [Tile() for _ in range(9)])
        answer = RangeFinder(map_).get_distances(Point(0, 0), 1)
        expected = {Point(0, 0): 1,
                    Point(0, 1): 1,
                    Point(1, 0): 1}
        self.assertEqual(answer, expected)

    def test_get_distance_non_flat_map(self):
        points = Point(0, 0).to_rectangle(3, 3)
        tiles = [Tile(elevation=(point.x + point.y), point=point) for point in points]
        the_map = Map(3, 3, tiles)
        point_el = [(Point(0, 0), 0), (Point(1, 0), 1), (Point(2, 0), 2),
                    (Point(0, 1), 1), (Point(1, 1), 2), (Point(2, 1), 3),
                    (Point(0, 2), 2), (Point(1, 2), 3), (Point(2, 2), 4)]
        origin = Point(1, 1)
        distance = {Point(0, 0): 2, Point(1, 0): 1, Point(2, 0): 3,
                    Point(0, 1): 1, Point(1, 1): 1, Point(2, 1): 2,
                    Point(0, 2): 3, Point(1, 2): 2, Point(2, 2): 4}


        origin = Point(2, 1)
        distance = {Point(0, 0): 3, Point(1, 0): 2, Point(2, 0): 1,
                    Point(0, 1): 2, Point(1, 1): 1, Point(2, 1): 1,
                    Point(0, 2): 4, Point(1, 2): 3, Point(2, 2): 2}


