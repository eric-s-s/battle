import unittest

from battle.movement_tracker import MovementTracker
from battle.map import Map, MapPlacementError
from battle.maptools.point import Point
from battle.tile import Tile
from battle.units import Soldier


class TestMap(unittest.TestCase):
    def setUp(self):
        self.unit = Soldier()
        self.width = 5
        self.height = 3
        self.tiles = get_tiles_without_points(self.width, self.height)
        self.map = Map(self.width, self.height, self.tiles)

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

    def test_init_raises_error_point_outside_map(self):
        tiles = get_tiles_with_points(1, 3)
        self.assertRaises(MapPlacementError, Map, 2, 2, tiles)

    def test_init_raises_error_two_tiles_same_point(self):
        tiles = [Tile('a', Point(0, 0)), Tile('b', Point(0, 0))]
        self.assertRaises(MapPlacementError, Map, 2, 2, tiles)

    def test_init_raises_error_if_more_tiles_than_points(self):
        tiles = get_tiles_without_points(5, 5)
        self.assertRaises(MapPlacementError, Map, 2, 2, tiles)

    def test_init_does_if_tiles_do_not_fill_points(self):
        tiles = get_tiles_without_points(3, 2)
        test_map = Map(3, 3, tiles)
        for point in Point(0, 0).to_rectangle(3, 2):
            self.assertIs(test_map.get_tile(point), tiles.pop(0))
        for point in Point(0, 2).to_rectangle(3, 1):
            self.assertFalse(test_map.has_tile(point))

    def test_is_on_map_true(self):
        points = Point(0, 0).to_rectangle(self.width, self.height)
        for point in points:
            self.assertTrue(self.map.is_on_map(point))

    def test_is_on_map_false(self):
        points = [Point(-1, -1), Point(5, 5), Point(1, 10), Point(10, 1)]
        for point in points:
            self.assertFalse(self.map.is_on_map(point))

    def test_has_tile_off_map(self):
        self.assertFalse(self.map.has_tile(Point(-1, -1)))

    def test_has_tile_empty_map_point(self):
        self.assertFalse(Map(2, 2, []).has_tile(Point(0, 0)))

    def test_has_tile_true(self):
        self.assertTrue(self.map.has_tile(Point(0, 0)))

    def test_get_tile(self):
        self.assertIs(self.map.get_tile(Point(0, 0)), self.tiles[0])

    def test_get_tile_none(self):
        self.assertIsNone(Map(2, 2, []).get_tile(Point(1, 1)))

    def test_can_place_unit_true(self):
        self.assertTrue(self.map.can_place_unit(Point(1, 1)))

    def test_can_place_unit_false_by_not_on_map(self):
        self.assertFalse(self.map.can_place_unit(Point(10, 1)))

    def test_can_place_unit_false_by_no_tile(self):
        self.assertFalse(Map(2, 2, []).can_place_unit(Point(1, 1)))

    def test_can_place_unit_false_by_occupied_by_unit(self):
        self.map.place_unit(self.unit, Point(1, 1))
        self.assertFalse(self.map.can_place_unit(Point(1, 1)))

    def test_place_unit_error_by_not_on_map(self):
        self.assertRaises(MapPlacementError, self.map.place_unit, self.unit, Point(10, 1))

    def test_place_unit_error_by_no_tile(self):
        test_map = Map(2, 2, [])
        self.assertRaises(MapPlacementError, test_map.place_unit, self.unit, Point(1, 1))

    def test_place_unit_error_by_occupied_by_unit(self):
        unit_2 = Soldier()
        self.map.place_unit(self.unit, Point(1, 1))
        self.assertRaises(MapPlacementError, self.map.place_unit, unit_2, Point(1, 1))

    def test_place_unit(self):
        self.map.place_unit(self.unit, Point(1, 1))

        self.assertIs(self.map.get_unit(Point(1, 1)), self.unit)

    def test_remove_unit(self):
        self.map.place_unit(self.unit, Point(1, 1))
        self.map.remove_unit(Point(1, 1))
        self.assertTrue(self.map.can_place_unit(Point(1, 1)))

    def test_remove_all_units(self):
        unit1 = MovementTracker(self.map)


def get_tiles_without_points(width, height):
    pt_list = get_pt_list(width, height)
    return [Tile(str(pt)) for pt in pt_list]


def get_tiles_with_points(width, height):
    pt_list = get_pt_list(width, height)
    return [Tile(str(pt), pt) for pt in pt_list]


def get_pt_list(width, height):
    return Point(0, 0).to_rectangle(width, height)


