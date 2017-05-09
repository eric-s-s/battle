import unittest

from battle.maptools.direction import Direction
from battle.maptools.point import Point
from battle.maptools.tile import Tile

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class MockTerrain(object):
    def __init__(self, name):
        self.name = name

    def copy(self):
        return MockTerrain(self.name)


class TestTile(unittest.TestCase):

    def setUp(self):
        self.terrain = MockTerrain('terrain')
        self.point = Point(1, 1)
        self.tile = Tile(self.terrain, self.point)

    def test_init(self):
        self.assertIs(self.tile.get_terrain(), self.terrain)
        self.assertIs(self.tile.get_point(), self.point)

    def test_init_point_defaults_to_none(self):
        new = Tile(self.terrain)
        self.assertIsNone(new.get_point())

    def test_class_method_blank(self):
        blank = Tile.blank()
        self.assertEqual(blank.get_terrain(), 'blank')
        self.assertFalse(blank.has_point())

    def test_has_point_true(self):
        self.assertTrue(self.tile.has_point())

    def test_has_point_false(self):
        self.assertFalse(get_tile('no point').has_point())

    def test_del_point(self):
        self.tile.del_point()
        self.assertIs(self.tile.get_point(), None)

    def test_move_points(self):
        self.assertEqual(self.tile.move_pts(Tile.blank()), 1)


def get_tile(terrain_name, point=None):
    return Tile(MockTerrain(terrain_name), point)


if __name__ == '__main__':
    unittest.main()
