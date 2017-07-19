import unittest

from battle.slope import Slopey, get_slope, get_deltas_between
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

    def test_get_slope_pos_inf(self):
        point_1 = Point(0, 0)
        point_2 = Point(0, 2)
        slope = get_slope(point_1, point_2)

        self.assertEqual(slope, float('inf'))

    def test_get_slope_neg_inf(self):
        point_1 = Point(0, 2)
        point_2 = Point(0, 1)
        slope = get_slope(point_1, point_2)

        self.assertEqual(slope, float('-inf'))

    def test_get_slope_pos(self):
        point_1 = Point(1, 2)
        point_2 = Point(2, 4)
        slope = get_slope(point_1, point_2)
        self.assertEqual(slope, 2)

        point_1 = Point(1, 2)
        point_2 = Point(3, 3)
        slope = get_slope(point_1, point_2)
        self.assertEqual(slope, 0.5)

    def test_get_slope_neg(self):
        point_1 = Point(1, 2)
        point_2 = Point(0, 4)
        slope = get_slope(point_1, point_2)
        self.assertEqual(slope, -2)

        point_1 = Point(2, 2)
        point_2 = Point(0, 3)
        slope = get_slope(point_1, point_2)
        self.assertEqual(slope, -0.5)

    def test_get_slope_zero(self):
        point_1 = Point(2, 1)
        point_2 = Point(3, 1)
        slope = get_slope(point_1, point_2)
        self.assertEqual(slope, 0)

    def test_get_elevation(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 2,
                      Point(0, 1): -1, Point(1, 1): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(2, 2, tiles)
        slopey = Slopey(map_)
        self.assertEqual(slopey.get_elevation(Point(0, 0)), 1)
        self.assertEqual(slopey.get_elevation(Point(1, 0)), 2)
        self.assertEqual(slopey.get_elevation(Point(0, 1)), -1)
        self.assertEqual(slopey.get_elevation(Point(1, 1)), 0)

    def test_get_elevation_empty_tile(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 2,
                      Point(0, 1): -1, }
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(2, 2, tiles)
        slopey = Slopey(map_)
        self.assertEqual(slopey.get_elevation(Point(1, 1)), float('-inf'))
        self.assertEqual(slopey.get_elevation(Point(-1, -1)), float('-inf'))

    def test_is_obstacle_higher_than_start_y_axis_pos_direction_true(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 3, Point(2, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 2, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(1, 3)
        finish = Point(1, 0)
        self.assertTrue(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_y_axis_pos_direction_false(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 0, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 2, Point(2, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 2, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(1, 3)
        finish = Point(1, 0)
        self.assertFalse(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_y_axis_neg_direction_true(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 3, Point(2, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 2, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(1, 0)
        finish = Point(1, 3)
        self.assertTrue(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_y_axis_neg_direction_false(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 0, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 2, Point(2, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 2, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(1, 0)
        finish = Point(1, 3)

        self.assertFalse(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_slope_gt_one_true(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 3, Point(2, 2): 0,
                      Point(0, 3): 2, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 3)
        finish = Point(2, 0)
        self.assertTrue(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_slope_gt_one_false(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 1, Point(2, 2): 0,
                      Point(0, 3): 2, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 3)
        finish = Point(2, 0)
        self.assertFalse(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_slope_lt_one_pos_true(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 1, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 1, Point(2, 2): 0,
                      Point(0, 3): 2, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 0)
        finish = Point(2, 1)
        self.assertTrue(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_slope_lt_one_pos_false(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 0, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 1, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 1, Point(2, 2): 0,
                      Point(0, 3): 2, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 0)
        finish = Point(2, 1)
        self.assertFalse(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_slope_gt_neg_one_neg_true(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 2, Point(2, 2): 0,
                      Point(0, 3): 1, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 3)
        finish = Point(2, 2)
        self.assertTrue(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_slope_gt_neg_one_neg_false(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 1, Point(2, 2): 1,
                      Point(0, 3): 1, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 3)
        finish = Point(2, 2)
        self.assertFalse(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_slope_lt_neg_one_false(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 1, Point(2, 2): 1,
                      Point(0, 3): 2, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 3)
        finish = Point(1, 0)
        self.assertFalse(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_slope_lt_neg_one_true(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 0, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 3, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 1, Point(2, 2): 1,
                      Point(0, 3): 2, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 3)
        finish = Point(1, 0)
        self.assertTrue(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_x_axis_pos_direction_true(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 3, Point(2, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 2, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 0)
        finish = Point(2, 0)
        self.assertTrue(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_x_axis_pos_direction_false(self):
        elevations = {Point(0, 0): 2, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 3, Point(2, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 2, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 0)
        finish = Point(2, 0)
        self.assertFalse(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_x_axis_neg_direction_true(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 3, Point(2, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 2, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(2, 2)
        finish = Point(0, 2)
        self.assertTrue(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_obstacle_higher_than_start_x_axis_neg_direction_false(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 4, Point(1, 2): 3, Point(2, 2): 4,
                      Point(0, 3): 0, Point(1, 3): 2, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(2, 2)
        finish = Point(0, 2)
        self.assertFalse(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_target_below_shooter_true(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 3,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 4, Point(1, 2): 3, Point(2, 2): 4,
                      Point(0, 3): 0, Point(1, 3): 2, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        target = Point(1, 3)
        shooter = Point(2, 0)
        self.assertTrue(slopey.is_target_below_shooter(target, shooter))

    def test_is_target_below_shooter_false(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 3,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 4, Point(1, 2): 3, Point(2, 2): 4,
                      Point(0, 3): 0, Point(1, 3): 4, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        target = Point(1, 3)
        shooter = Point(2, 0)
        self.assertFalse(slopey.is_target_below_shooter(target, shooter))

    def test_is_higher_than_start_by_bounding_ys_slope_lt_one_pos_true(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 1, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 1, Point(2, 2): 0,
                      Point(0, 3): 2, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 0)
        finish = Point(2, 1)
        self.assertTrue(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_higher_than_start_by_bounding_ys_slope_lt_one_pos_false(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 0, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 1, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 1, Point(2, 2): 0,
                      Point(0, 3): 2, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 0)
        finish = Point(2, 1)
        self.assertFalse(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_higher_than_start_by_bounding_ys_slope_gt_neg_one_neg_true(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 2, Point(2, 2): 0,
                      Point(0, 3): 1, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 3)
        finish = Point(2, 2)
        self.assertTrue(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_higher_than_start_by_bounding_ys_slope_gt_neg_one_neg_false(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 1, Point(2, 2): 1,
                      Point(0, 3): 1, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 3)
        finish = Point(2, 2)
        self.assertFalse(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_higher_than_start_by_bounding_xs_slope_gt_one_true(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 3, Point(2, 2): 0,
                      Point(0, 3): 2, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 3)
        finish = Point(2, 0)
        self.assertTrue(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_higher_than_start_by_bounding_xs_slope_gt_one_false(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 1, Point(2, 2): 0,
                      Point(0, 3): 2, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 3)
        finish = Point(2, 0)
        self.assertFalse(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_higher_than_start_by_bounding_xs_slope_lt_neg_one_false(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 2, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 2, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 1, Point(2, 2): 1,
                      Point(0, 3): 2, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 3)
        finish = Point(1, 0)
        self.assertFalse(slopey.is_obstacle_higher_than_start(start, finish))

    def test_is_higher_than_start_by_bounding_xs_slope_lt_neg_one_true(self):
        elevations = {Point(0, 0): 1, Point(1, 0): 0, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 3, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 1, Point(2, 2): 1,
                      Point(0, 3): 2, Point(1, 3): 0, Point(2, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(3, 4, tiles)
        slopey = Slopey(map_)
        start = Point(0, 3)
        finish = Point(1, 0)
        self.assertTrue(slopey.is_obstacle_higher_than_start(start, finish))

    def test_get_deltas_between_b_gt_a(self):
        a = 2
        b = 6
        self.assertTrue(get_deltas_between(a, b), range(1, 4))

    def test_get_deltas_between_a_gt_b(self):
        a = 4
        b = 1
        self.assertTrue(get_deltas_between(a, b), range(-1, -3))




