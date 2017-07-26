import unittest

from battle.maptools.groundmap  import GroundMap, GroundMapPlacementError
from battle.maptools.point import Point
from battle.maptools.tile import Tile
from battle.units import Soldier


class TestGroundMap(unittest.TestCase):
    def setUp(self):
        self.unit = Soldier()
        self.width = 5
        self.height = 3
        self.tiles = get_tiles_without_points(self.width, self.height)
        self.map = GroundMap(self.width, self.height, self.tiles)

    def test_init_pointless_tiles(self):
        for point in Point(0, 0).to_rectangle(5, 3):
            self.assertIs(self.map.get_tile(point), self.tiles.pop(0))

    def test_init_pointed_tiles(self):
        width = 5
        height = 3
        tiles = get_tiles_with_points(width, height)
        test_map = GroundMap(width, height, tiles)
        for point in Point(0, 0).to_rectangle(width, height):
            self.assertIs(test_map.get_tile(point), tiles.pop(0))

    def test_init_mixed_tiles(self):
        width = 2
        height = 2
        tiles = [Tile(point=Point(0, 0)), Tile(), Tile(), Tile(point=Point(1, 1))]
        self.assertFalse(tiles[1].has_point())

        test_map = GroundMap(width, height, tiles)
        for tile in tiles:
            self.assertTrue(tile.has_point())
        for point in Point(0, 0).to_rectangle(width, height):
            self.assertIs(test_map.get_tile(point), tiles.pop(0))

    def test_init_raises_error_point_outside_map(self):
        tiles = get_tiles_with_points(1, 3)
        self.assertRaises(GroundMapPlacementError, GroundMap, 2, 2, tiles)

    def test_init_raises_error_two_tiles_same_point(self):
        tiles = [Tile(point=Point(0, 0)), Tile(point=Point(0, 0))]
        self.assertRaises(GroundMapPlacementError, GroundMap, 2, 2, tiles)

    def test_init_raises_error_if_more_tiles_than_points(self):
        tiles = get_tiles_without_points(5, 5)
        self.assertRaises(GroundMapPlacementError, GroundMap, 2, 2, tiles)

    def test_init_if_tiles_do_not_fill_points(self):
        tiles = get_tiles_without_points(3, 2)
        test_map = GroundMap(3, 3, tiles)
        for point in Point(0, 0).to_rectangle(3, 2):
            self.assertIs(test_map.get_tile(point), tiles.pop(0))
        for point in Point(0, 2).to_rectangle(3, 1):
            self.assertFalse(test_map.has_tile(point))

    def test_get_all_elevations(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): -1,
                               Point(0, 1): 1, }
        tiles = [Tile(elevation=elevation, point=point, terrain_mv=100)
                 for point, elevation in points_to_elevation.items()]
        the_map = GroundMap(2, 2, tiles)
        self.assertEqual(the_map.get_all_elevations(),
                         {Point(0, 0): 0, Point(1, 0): -1, Point(0, 1): 1, Point(1, 1): float('-inf')})

    def test_get_size(self):
        to_test = GroundMap(3, 5, [])
        self.assertEqual(to_test.get_size(), (3, 5))

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
        self.assertFalse(GroundMap(2, 2, []).has_tile(Point(0, 0)))

    def test_has_tile_true(self):
        self.assertTrue(self.map.has_tile(Point(0, 0)))

    def test_get_tile(self):
        self.assertIs(self.map.get_tile(Point(0, 0)), self.tiles[0])

    def test_get_tile_none(self):
        self.assertIsNone(GroundMap(2, 2, []).get_tile(Point(1, 1)))

    def test_can_place_unit_true(self):
        self.assertTrue(self.map.can_place_unit(Point(1, 1)))

    def test_can_place_unit_false_by_not_on_map(self):
        self.assertFalse(self.map.can_place_unit(Point(10, 1)))

    def test_can_place_unit_false_by_no_tile(self):
        self.assertFalse(GroundMap(2, 2, []).can_place_unit(Point(1, 1)))

    def test_can_place_unit_false_by_occupied_by_unit(self):
        self.map.place_unit(self.unit, Point(1, 1))
        self.assertFalse(self.map.can_place_unit(Point(1, 1)))

    def test_place_unit_error_by_not_on_map(self):
        self.assertRaises(GroundMapPlacementError, self.map.place_unit, self.unit, Point(10, 1))

    def test_place_unit_error_by_no_tile(self):
        test_map = GroundMap(2, 2, [])
        self.assertRaises(GroundMapPlacementError, test_map.place_unit, self.unit, Point(1, 1))

    def test_place_unit_error_by_occupied_by_unit(self):
        unit_2 = Soldier()
        self.map.place_unit(self.unit, Point(1, 1))
        self.assertRaises(GroundMapPlacementError, self.map.place_unit, unit_2, Point(1, 1))

    def test_place_unit(self):
        self.map.place_unit(self.unit, Point(1, 1))
        self.assertIs(self.map.get_unit(Point(1, 1)), self.unit)

    def test_has_unit_point_not_on_map_false(self):
        self.assertFalse(self.map.has_unit(Point(-1, -1)))

    def test_has_unit_false(self):
        self.assertFalse(self.map.has_unit(Point(1, 1)))

    def test_has_unit_true(self):
        self.map.place_unit(Soldier(), Point(1, 1))
        self.assertTrue(self.map.has_unit(Point(1, 1)))
        self.assertFalse(self.map.has_unit(Point(2, 1)))

    def test_get_unit_is_none_when_no_unit(self):
        self.assertIsNone(self.map.get_unit(Point(1, 1)))

    def test_get_unit(self):
        unit = Soldier()
        point = Point(1, 1)
        self.map.place_unit(unit, point)
        self.assertIs(unit, self.map.get_unit(point))

        self.assertIsNone(self.map.get_unit(Point(0, 0)))

    def test_remove_unit(self):
        self.map.place_unit(self.unit, Point(1, 1))
        self.map.remove_unit(Point(1, 1))
        self.assertTrue(self.map.can_place_unit(Point(1, 1)))

    def test_remove_all_units(self):
        points = Point(0, 0).to_rectangle(2, 2)
        for point in points:
            self.map.place_unit(Soldier(), point)
        self.map.remove_all_units()

        for point in points:
            self.assertFalse(self.map.has_unit(point))


def get_tiles_without_points(width, height):
    pt_list = get_pt_list(width, height)
    return [Tile() for _ in pt_list]


def get_tiles_with_points(width, height):
    pt_list = get_pt_list(width, height)
    return [Tile(point=pt) for pt in pt_list]


def get_pt_list(width, height):
    return Point(0, 0).to_rectangle(width, height)
