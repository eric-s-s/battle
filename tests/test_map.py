import unittest

from battle.map import Map, MapPlacementError
from battle.maptools.point import Point
from battle.maptools.direction import Direction
from battle.tile import Tile


class MockUnit(object):
    def __init__(self, name, point=None):
        self.name = name
        self.point = point

    def get_point(self):
        return self.point

    def has_point(self):
        return self.point is not None

    def set_point(self, point):
        self.point = point

    def del_point(self):
        self.point = None


class TestMap(unittest.TestCase):
    def setUp(self):
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

    def test_connect(self):
        sw = Tile('a', Point(0, 0))
        se = Tile('a', Point(1, 0))
        nw = Tile('a', Point(0, 1))
        ne = Tile('a', Point(1, 1))

        test_map = Map(2, 2, [sw])
        all_points = [Point(0, 0), Point(1, 0),
                      Point(1, 0), Point(1, 1)]
        for point in all_points[1:]:
            self.assertFalse(test_map.has_tile(point))

        test_map.connect(nw)
        self.assertIs(nw.get(Direction.S), sw)
        self.assertIs(sw.get(Direction.N), nw)
        test_map.connect(se)
        test_map.connect(ne)
        self.assertIs(nw.get(Direction.E), ne)
        self.assertIs(ne.get(Direction.W), nw)

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
        self.map.place_unit(MockUnit('test'), Point(1, 1))
        self.assertFalse(self.map.can_place_unit(Point(1, 1)))

    def test_place_unit_error_by_not_on_map(self):
        self.assertRaises(MapPlacementError, self.map.place_unit, MockUnit('test'), Point(10, 1))

    def test_place_unit_error_by_no_tile(self):
        test_map = Map(2, 2, [])
        self.assertRaises(MapPlacementError, test_map.place_unit, MockUnit('test'), Point(1, 1))

    def test_place_unit_error_by_occupied_by_unit(self):
        self.map.place_unit(MockUnit('test'), Point(1, 1))
        self.assertRaises(MapPlacementError, self.map.place_unit, MockUnit('test'), Point(1, 1))

    def test_place_unit_sets_unit_point(self):
        unit = MockUnit('test')
        self.assertFalse(unit.has_point())
        self.map.place_unit(unit, Point(1, 1))

        self.assertEqual(unit.get_point(), Point(1, 1))
        self.assertIs(self.map.get_unit(Point(1, 1)), unit)

    def test_remove_unit(self):
        unit = MockUnit('test')
        self.map.place_unit(unit, Point(1, 1))
        self.map.remove_unit(unit)
        self.assertTrue(self.map.can_place_unit(Point(1, 1)))
        self.assertFalse(unit.has_point())

    def test_move_unit_success_returns_movement_pts(self):
        unit = MockUnit('test')
        self.map.place_unit(unit, Point(1, 1))
        movement_pts = self.map.move_unit(unit, Direction.N)
        self.assertEqual(movement_pts, 1)

    def test_move_unit_success_moves_unit(self):
        unit = MockUnit('test')
        self.map.place_unit(unit, Point(1, 1))
        self.map.move_unit(unit, Direction.N)
        self.assertEqual(unit.get_point(), Point(1, 2))
        self.assertIs(self.map.get_unit(Point(1, 2)), unit)

    def test_move_unit_success_removes_from_old_point(self):
        unit = MockUnit('test')
        self.map.place_unit(unit, Point(1, 1))
        self.map.move_unit(unit, Direction.N)
        self.assertIsNone(self.map.get_unit(Point(1, 1)))

    def test_move_unit_other_directions(self):
        unit = MockUnit('test')
        self.map.place_unit(unit, Point(1, 1))

        self.map.move_unit(unit, Direction.S)
        self.assertEqual(unit.get_point(), Point(1, 0))

        self.map.move_unit(unit, Direction.E)
        self.assertEqual(unit.get_point(), Point(2, 0))

        self.map.move_unit(unit, Direction.W)
        self.assertEqual(unit.get_point(), Point(1, 0))

    def test_move_unit_fail_movement_pts_is_zero(self):
        unit = MockUnit('test')
        unit_2 = MockUnit('blocker')
        self.map.place_unit(unit, Point(1, 1))
        self.map.place_unit(unit_2, Point(1, 2))

        movement_pts = self.map.move_unit(unit, Direction.N)
        self.assertEqual(movement_pts, 0)

    def test_move_unit_fail_units_do_not_move(self):
        unit = MockUnit('test')
        unit_2 = MockUnit('blocker')
        self.map.place_unit(unit, Point(1, 1))
        self.map.place_unit(unit_2, Point(1, 2))
        self.map.move_unit(unit, Direction.N)

        self.assertEqual(unit.get_point(), Point(1, 1))
        self.assertIs(self.map.get_unit(Point(1, 2)), unit_2)
        self.assertIs(self.map.get_unit(Point(1, 1)), unit)

    def test_movie_unit_fail_by_no_tile(self):
        unit = MockUnit('test')
        test_map = Map(3, 3, [Tile('1, 1', Point(1, 1))])
        test_map.place_unit(unit, Point(1, 1))
        movement_pts = test_map.move_unit(unit, Direction.S)
        self.assertEqual(movement_pts, 0)

    def test_movie_unit_fail_by_off_board(self):
        unit = MockUnit('test')
        self.map.place_unit(unit, Point(0, 0))
        movement_pts = self.map.move_unit(unit, Direction.S)
        self.assertEqual(movement_pts, 0)


def get_tiles_without_points(width, height):
    pt_list = get_pt_list(width, height)
    return [Tile(str(pt)) for pt in pt_list]


def get_tiles_with_points(width, height):
    pt_list = get_pt_list(width, height)
    return [Tile(str(pt), pt) for pt in pt_list]


def get_pt_list(width, height):
    return Point(0, 0).to_rectangle(width, height)


