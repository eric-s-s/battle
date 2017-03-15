import unittest

from battle.tile import Tile


class TestTile(unittest.TestCase):
    def setUp(self):
        self.center = self.create_tiles(distance=5)

    def create_tiles(self, distance):
        center = make_basic_tile()
        steps = {0: center}
        for step in range(distance):
            new_tiles = get_tiles_next_list_of_tiles



def make_basic_tile()
    terrain = 'basic_terrain'
    units = ['a', 'b', 'c']
    return Tile(terrain, units[:])

