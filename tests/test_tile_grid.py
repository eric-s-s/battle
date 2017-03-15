import unittest

from battle.tile_grid import TileGrid
from battle.tile import Tile
from battle.direction import Direction

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class TestTileGrid(unittest.TestCase):
    def test_init_creates_grid_of_none(self):
        to_test = TileGrid(2, 3)
        self.assertIsNone(to_test.get_tile(0, 0))
        self.assertIsNone(to_test.get_tile(0, 1))
        self.assertIsNone(to_test.get_tile(0, 2))
        self.assertIsNone(to_test.get_tile(1, 0))
        self.assertIsNone(to_test.get_tile(1, 1))
        self.assertIsNone(to_test.get_tile(1, 2))

    def test_get_size(self):
        self.assertEqual(TileGrid(1, 2).get_size(), (1, 2))

    def test_is_in_grid_true(self):
        to_test = TileGrid(2, 2)
        self.assertTrue(to_test.is_in_grid(0, 0))
        self.assertTrue(to_test.is_in_grid(0, 1))
        self.assertTrue(to_test.is_in_grid(1, 0))
        self.assertTrue(to_test.is_in_grid(1, 1))

    def test_is_in_grid_false(self):
        to_test = TileGrid(2, 2)
        self.assertFalse(to_test.is_in_grid(-1, 0))
        self.assertFalse(to_test.is_in_grid(0, -1))
        self.assertFalse(to_test.is_in_grid(2, 0))
        self.assertFalse(to_test.is_in_grid(0, 2))

    def test_place_tile_adjacent_are_empty(self):
        to_test = TileGrid(3, 3)
        tile = Tile('test', ['a'])
        to_test.place_tile(tile, 1, 1)
        result = to_test.get_tile(1, 1)
        self.assertIs(result, tile)
        for direction in Direction:
            self.assertFalse(tile.has_tile(direction))

    def test_place_tile_pairs_adjacent_tiles(self):
        to_test = TileGrid(2, 2)
        n_w_tile = Tile('NW', [])
        n_e_tile = Tile('NE', [])
        s_w_tile = Tile('SW', [])

        to_test.place_tile(n_w_tile, 0, 0)
        to_test.place_tile(n_e_tile, 0, 1)
        to_test.place_tile(s_w_tile, 1, 0)

        self.assertIs(n_w_tile.get(E), n_e_tile)
        self.assertIs(n_e_tile.get(W), n_w_tile)
        self.assertIs(n_w_tile.get(S), s_w_tile)
        self.assertIs(s_w_tile.get(N), n_w_tile)

