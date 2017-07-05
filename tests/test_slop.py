import unittest

from battle.slope import Slopey, get_slope
from battle.maptools.tile import Tile
from battle.maptools.map import Map
from battle.maptools.point import Point

from tests.test_rangefinder import pretty_print


class TestSlopey(unittest.TestCase):
    def setUp(self):
        elevations = {Point(0, 0): 9, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 0, Point(2, 1): 3, Point(3, 1): 0,
                      Point(0, 2): 9, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 0, Point(2, 3): 0, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        self.map_ = Map(4, 4, tiles)

    def test_get_slope_neg_inf(self):
        pass

    def test_get_slope_pos_inf(self):
        pass


