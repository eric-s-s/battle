import unittest

from battle.maptools.direction import Direction
from battle.maptools.point import Point
from battle.maptools.tile import Tile

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


# class MockTerrain(object):
#     def __init__(self, name):
#         self.name = name
#
#     def copy(self):
#         return MockTerrain(self.name)


class TestTile(unittest.TestCase):

    def setUp(self):
        # self.terrain = MockTerrain('terrain')
        self.point = Point(1, 1)
        self.tile = Tile(point=self.point)

    def test_init(self):
        self.assertIs(self.tile.get_point(), self.point)

    def test_init_point_defaults_to_none(self):
        new = Tile()
        self.assertIsNone(new.get_point())

    def test_class_method_blank(self):
        blank = Tile.blank()
        self.assertEqual(blank.get_terrain_type(), 1)
        self.assertFalse(blank.has_point())

    def test_has_point_true(self):
        self.assertTrue(self.tile.has_point())

    def test_has_point_false(self):
        tile = Tile()
        self.assertFalse(tile.has_point())

    def test_del_point(self):
        self.tile.del_point()
        self.assertIs(self.tile.get_point(), None)

    def test_move_points(self):
        self.assertEqual(self.tile.move_pts(Tile.blank()), 1)

    def test_move_points_elevation_going_uphill(self):
        el_zero = Tile()
        el_one = Tile(elevation=1)
        el_two = Tile(elevation=2)
        self.assertEqual(el_zero.move_pts(el_one), 2)
        self.assertEqual(el_zero.move_pts(el_two), 3)
        self.assertEqual(el_one.move_pts(el_two), 2)

    def test_move_points_elevation_going_downhill_is_always_one(self):
        el_zero = Tile()
        el_one = Tile(elevation=1)
        el_two = Tile(elevation=2)
        self.assertEqual(el_two.move_pts(el_zero), 1)
        self.assertEqual(el_two.move_pts(el_one), 1)
        self.assertEqual(el_two.move_pts(el_one), 1)

    def test_move_points_terrain_multiplier_same_elevation(self):
        times_one = Tile()
        times_two = Tile(terrain_multiplier=2)
        times_three = Tile(terrain_multiplier=3)
        self.assertEqual(3, times_three.move_pts(times_one))
        self.assertEqual(3, times_three.move_pts(times_two))
        self.assertEqual(2, times_two.move_pts(times_one))
        self.assertEqual(1, times_one.move_pts(times_two))

    def test_move_points_different_elevation_and_multipliers(self):
        multiplier = 3
        el_zero = Tile(terrain_multiplier=multiplier)
        el_one = Tile(elevation=1, terrain_multiplier=multiplier)
        el_two = Tile(elevation=2, terrain_multiplier=multiplier)
        self.assertEqual(el_zero.move_pts(el_one), 2 * 3)
        self.assertEqual(el_zero.move_pts(el_two), 3 * 3)
        self.assertEqual(el_one.move_pts(el_two), 2 * 3)



if __name__ == '__main__':
    unittest.main()
