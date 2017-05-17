import unittest

from battle.maptools.direction import Direction
from battle.maptools.point import Point
from battle.maptools.tile import Tile, ImpassableTile

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class TestTile(unittest.TestCase):

    def setUp(self):
        self.point = Point(1, 1)
        self.tile = Tile(point=self.point)

    def test_init(self):
        the_tile = Tile(2, 10, self.point)
        self.assertIs(self.tile.get_point(), self.point)
        self.assertEqual(the_tile.get_terrain_mv(), 10)
        self.assertEqual(the_tile.get_elevation(), 2)

    def test_init_elevation_may_be_negative_terrain_mv_min_one(self):
        the_tile = Tile(-2, 0)
        self.assertEqual(the_tile.get_terrain_mv(), 1)
        self.assertEqual(the_tile.get_elevation(), -2)

    def test_default_init(self):
        new = Tile()
        self.assertIsNone(new.get_point())
        self.assertEqual(new.get_terrain_mv(), 1)
        self.assertEqual(new.get_elevation(), 0)

    def test_has_point_true(self):
        self.assertTrue(self.tile.has_point())

    def test_has_point_false(self):
        tile = Tile()
        self.assertFalse(tile.has_point())

    def test_set_point(self):
        tile = Tile()
        self.assertIsNone(tile.get_point())
        self.assertFalse(tile.has_point())

        tile.set_point(Point(1, 1))
        self.assertEqual(tile.get_point(), Point(1, 1))
        self.assertTrue(tile.has_point())

    def test_del_point(self):
        self.tile.del_point()
        self.assertIsNone(self.tile.get_point())

    def test_move_points_to_self(self):
        self.assertEqual(self.tile.move_pts(self.tile), 0)

    def test_move_points(self):
        self.assertEqual(self.tile.move_pts(Tile()), 1)

    def test_move_points_elevation_going_uphill(self):
        el_zero = Tile()
        el_one = Tile(elevation=1)
        el_two = Tile(elevation=2)
        self.assertEqual(el_zero.move_pts(el_one), 2)
        self.assertEqual(el_zero.move_pts(el_two), 3)
        self.assertEqual(el_one.move_pts(el_two), 2)

    def test_move_points_elevation_going_downhill_like_no_elevation_change(self):
        el_zero = Tile()
        el_one = Tile(elevation=1)
        el_two = Tile(elevation=2)
        self.assertEqual(el_two.move_pts(el_zero), 1)
        self.assertEqual(el_two.move_pts(el_one), 1)
        self.assertEqual(el_two.move_pts(el_one), 1)

    def test_move_points_terrain_mv_same_elevation(self):
        mv_one = Tile()
        mv_two = Tile(terrain_mv=2)
        mv_three = Tile(terrain_mv=3)
        self.assertEqual(3, mv_three.move_pts(mv_one))
        self.assertEqual(3, mv_three.move_pts(mv_two))
        self.assertEqual(2, mv_two.move_pts(mv_one))
        self.assertEqual(1, mv_one.move_pts(mv_two))

    def test_move_points_different_elevation_and_terrain_mv(self):
        terrain_mv = 3
        el_zero = Tile(terrain_mv=terrain_mv)
        el_one = Tile(elevation=1, terrain_mv=terrain_mv)
        el_two = Tile(elevation=2, terrain_mv=terrain_mv)
        self.assertEqual(el_zero.move_pts(el_one), 1 + 3)
        self.assertEqual(el_zero.move_pts(el_two), 2 + 3)
        self.assertEqual(el_one.move_pts(el_two), 1 + 3)

    def test_impassable_tile_init(self):
        tile = ImpassableTile(2, Point(1, 1))
        self.assertEqual(tile.get_terrain_mv(), 2)
        self.assertEqual(tile.get_point(), Point(1, 1))
        self.assertEqual(tile.get_elevation(), float('inf'))

    def test_impassable_tile_mv_points(self):
        high_mv_pts_tile = ImpassableTile(100)
        default_tile = ImpassableTile()
        self.assertEqual(self.tile.move_pts(high_mv_pts_tile), float('inf'))
        self.assertEqual(self.tile.move_pts(default_tile), float('inf'))

    def test_unit_could_move_off_of_impassable_tile(self):
        high_mv_pts_tile = ImpassableTile(100)
        default_tile = ImpassableTile()
        self.assertEqual(high_mv_pts_tile.move_pts(self.tile), 100)
        self.assertEqual(default_tile.move_pts(self.tile), 1)


if __name__ == '__main__':
    unittest.main()
