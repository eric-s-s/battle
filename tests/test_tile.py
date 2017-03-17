import unittest

from battle.maptools.direction import Direction
from battle.maptools.tile_grid import TileGrid
from battle.tile import Tile, TileOccupationError

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class MockUnit(object):
    def __init__(self, name):
        self.name = name

    def copy(self):
        return MockUnit(self.name)


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
        self.unit = MockUnit('unit')
        self.tile = Tile(self.terrain, self.unit)

    def test_init(self):
        self.assertIs(self.tile.get_terrain(), self.terrain)
        self.assertIs(self.tile.get_unit(), self.unit)

    def test_init_has_no_connections_to_other_tiles(self):
        for direction in Direction:
            self.assertIsNone(self.tile.get(direction))

    def test_init_unit_defaults_to_none(self):
        new = Tile(self.terrain)
        self.assertIsNone(new.get_unit())

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

    def test_is_empty_true(self):
        new = get_tile('test')
        self.assertTrue(new.is_empty())

    def test_is_empty_false(self):
        new = get_tile('test', 'a unit')
        self.assertFalse(new.is_empty())

    def test_get_unit(self):
        no_unit = get_tile('test')
        self.assertIsNone(no_unit.get_unit())
        self.assertIs(self.tile.get_unit(), self.unit)
        self.assertIs(self.tile.get_unit(), self.unit)

    def test_remove_unit(self):
        no_unit = get_tile('test')
        no_unit.remove_unit()
        self.tile.remove_unit()
        self.assertTrue(no_unit.is_empty())
        self.assertTrue(self.tile.is_empty())

    def test_pop_unit_empty(self):
        no_unit = get_tile('test')
        self.assertIsNone(no_unit.pop_unit())
        self.assertTrue(no_unit.is_empty())

    def test_pop_unit_non_empty(self):
        self.assertIs(self.tile.pop_unit(), self.unit)
        self.assertTrue(self.tile.is_empty())

    def test_assign_unit_to_empty(self):
        no_unit = get_tile('test')
        no_unit.assign_unit(self.unit)
        self.assertIs(no_unit.get_unit(), self.unit)
        self.assertFalse(no_unit.is_empty())

    def test_assign_unit_to_non_empty_raises_error(self):
        self.assertRaises(TileOccupationError, self.tile.assign_unit, self.unit)


def create_tile_grid(size):
    to_test = TileGrid(size, size)
    for x in range(size):
        for y in range(size):
            to_test.place_tile(Tile('{}, {}'.format(x, y)), x, y)
    return to_test


def get_middle(test_grid):
    x, y = test_grid.get_size()
    return test_grid.get_tile(x // 2, y // 2)


def get_tile(terrain_name, unit_name=None):
    if unit_name is None:
        unit = None
    else:
        unit = MockUnit(unit_name)
    return Tile(MockTerrain(terrain_name), unit)


def connect(tile_1, tile_2, direction):
    tile_1.set(tile_2, direction)
    tile_2.set(tile_1, direction.opposite())


if __name__ == '__main__':
    unittest.main()
