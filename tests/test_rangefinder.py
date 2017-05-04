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
        self.assertEqual(answer, [Point(1, 0), Point(0, 1), Point(2, 0), Point(1, 1), Point(0, 2)])

    def test_get_all_points_does_not_include_points_not_on_map(self):
        answer = self.ranger.get_all_points(Point(0, 0), 1)
        self.assertEqual(answer, [Point(1, 0), Point(0, 1)])

    def test_get_all_points_includes_points_on_map_but_with_no_tile(self):
        new_map = Map(3, 3, [])
        self.assertFalse(new_map.has_tile(Point(0, 1)))
        ranger = RangeFinder(new_map)
        answer = ranger.get_all_points(Point(0, 0), 1)
        self.assertEqual(answer, [Point(1, 0), Point(0, 1)])

    def test_get_all_units_no_units(self):
        answer = self.ranger.get_all_units(Point(0, 0), 2)
        self.assertEqual(answer, [])

    def test_get_all_units_does_not_add_None(self):
        pass

    def test_get_all_units_all_points_occupied(self):
        soldiers = ['some gueys']
        for point in ['some points']:
            """put soldiers in one by one and then test two lists.  rememeber that the order of points will be important. you can sort your points00by distance first first."""
