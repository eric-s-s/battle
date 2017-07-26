import unittest

from battle.maptools.airmap  import AirMap
from battle.maptools.point import Point
from battle.maptools.tile import Tile
from battle.units import Soldier


class TestAirMap(unittest.TestCase):
    def test_init(self):
        points_to_elevation = {Point(0, 0): float('inf'), Point(1, 0): 0, Point(2, 0): -1,
                               Point(0, 1): float('-inf'), Point(1, 1): 2, Point(2, 1): 2}
        the_map = AirMap(points_to_elevation)
        self.assertEqual(the_map.min_elevations, {Point(0, 0): float('inf'), Point(1, 0): 1, Point(2, 0): 0,
                               Point(0, 1): 1, Point(1, 1): 3, Point(2, 1): 3})
