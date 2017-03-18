import unittest

from battle.map import Map
from battle.maptools.point import Point
from battle.maptools.direction import Direction
from battle.tile import Tile


class MockUnit(object):
    def __init__(self, name, point=None):
        self.name = name
        self.point = point

    def has_point(self):
        return self.point is not None

    def set_point(self, point):
        self.point = point

    def del_point(self):
        self.point = None

    def move(self, direction):
        self.point = self.point.in_direction(direction)


class TestMap(unittest.TestCase):
    def setUp(self):
        width = 5
        height = 3
        self.tiles = get_tiles_without_points(width, height)
        self.map = Map(width, height, self.tiles)

    def test_init_pointless_tiles(self):
        for point in Point(0, 0).to_rectangle(5, 3):
            self.assertIs(self.map.get_tile(point), self.tiles.pop(0))

    def test_init_pointed_tiles(self):
        width = 5
        height = 3
        tiles = get_tiles_with_points(width, height)
        test_map = Map(width, height, tiles)
        for point in Point(0, 0).to_rectangle(width, height):
            self.assertIs(test_map.get_tile(point), tiles.pop(0))

    def test_init_mixed_tiles(self):
        width = 2
        height = 2
        tiles = [Tile('(0, 0)', Point(0, 0)), Tile('(0, 1)'), Tile('(1, 0)'), Tile('(1, 1)', Point(1, 1))]
        self.assertFalse(tiles[1].has_point())

        test_map = Map(width, height, tiles)
        for tile in tiles:
            self.assertTrue(tile.has_point())
        for point in Point(0, 0).to_rectangle(width, height):
            self.assertIs(test_map.get_tile(point), tiles.pop(0))



def get_tiles_without_points(width, height):
    pt_list = get_pt_list(width, height)
    return [Tile(str(pt)) for pt in pt_list]


def get_tiles_with_points(width, height):
    pt_list = get_pt_list(width, height)
    return [Tile(str(pt), pt) for pt in pt_list]


def get_pt_list(width, height):
    return Point(0, 0).to_rectangle(width, height)


