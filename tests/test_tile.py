import unittest

from battle.maptools.direction import Direction
from battle.maptools.point import Point
from battle.tile import Tile, TileOccupationError

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class MockTerrain(object):
    def __init__(self, name):
        self.name = name

    def copy(self):
        return MockTerrain(self.name)


class TestTileOccupationError(unittest.TestCase):
    @staticmethod
    def raise_error(msg=''):
        if msg:
            raise TileOccupationError(msg)
        else:
            raise TileOccupationError

    def test_no_message(self):
        self.assertRaises(TileOccupationError, self.raise_error)

    def test_with_msg(self):
        self.assertRaises(TileOccupationError, self.raise_error, 'oops')

    def test_msg_content(self):
        with self.assertRaises(TileOccupationError) as cm:
            self.raise_error('hello')
        msg = cm.exception.args[0]
        self.assertEqual(msg, 'hello')


class TestTile(unittest.TestCase):

    def setUp(self):
        self.terrain = MockTerrain('terrain')
        self.point = Point(1, 1)
        self.tile = Tile(self.terrain, self.point)

    def test_init(self):
        self.assertIs(self.tile.get_terrain(), self.terrain)
        self.assertIs(self.tile.get_point(), self.point)

    def test_init_has_no_connections_to_other_tiles(self):
        for direction in Direction:
            self.assertIsNone(self.tile.get(direction))

    def test_init_point_defaults_to_none(self):
        new = Tile(self.terrain)
        self.assertIsNone(new.get_point())

    def test_class_method_blank(self):
        blank = Tile.blank()
        self.assertEqual(blank.get_terrain(), 'blank')
        self.assertEqual(blank.get_all(), [])
        self.assertFalse(blank.has_point())

    def test_has_point_true(self):
        self.assertTrue(self.tile.has_point())

    def test_has_point_false(self):
        self.assertFalse(get_tile('no point').has_point())

    def test_del_point(self):
        tiles = []
        for direction in Direction:
            tile = get_tile(direction.name)
            tiles.append(tile)
            self.tile.set(tile, direction)
        self.assertEqual(self.tile.get_all(), tiles)

        self.tile.del_point()
        self.assertEqual(self.tile.get_all(), [])
        self.assertIs(self.tile.get_point(), None)

    def test_set(self):
        new = get_tile('test')
        self.tile.set(new, N)
        self.assertIs(self.tile.get(N), new)

    def test_set_does_not_set_other_tile(self):
        new = get_tile('test')
        self.tile.set(new, N)
        self.assertIsNone(new.get(S))

    def test_get_empty(self):
        self.assertIsNone(self.tile.get(N))

    def test_get_non_empty(self):
        new = get_tile('test')
        self.tile.set(new, N)
        self.assertIs(self.tile.get(N), new)

    def test_get_all_empty(self):
        self.assertEqual(self.tile.get_all(), [])

    def test_get_all_some_empty(self):
        a = get_tile('a')
        b = get_tile('b')
        self.tile.set(a, N)
        self.tile.set(b, S)

        all_tiles = self.tile.get_all()

        self.assertIn(a, all_tiles)
        self.assertIn(b, all_tiles)

    def test_get_all_non_empty(self):
        a = get_tile('a')
        b = get_tile('b')
        c = get_tile('c')
        d = get_tile('d')
        self.tile.set(a, N)
        self.tile.set(b, S)
        self.tile.set(c, E)
        self.tile.set(d, W)

        all_tiles = self.tile.get_all()

        self.assertIn(a, all_tiles)
        self.assertIn(b, all_tiles)
        self.assertIn(c, all_tiles)
        self.assertIn(d, all_tiles)

    def test_has_tile_true(self):
        new = get_tile('test')
        self.tile.set(new, N)
        self.assertTrue(self.tile.has_tile(N))

    def test_has_tile_false(self):
        new = get_tile('test')
        self.tile.set(new, N)
        self.assertFalse(self.tile.has_tile(W))
        self.assertFalse(self.tile.has_tile(E))
        self.assertFalse(self.tile.has_tile(S))


def get_tile(terrain_name, point=None):
    return Tile(MockTerrain(terrain_name), point)



if __name__ == '__main__':
    unittest.main()
