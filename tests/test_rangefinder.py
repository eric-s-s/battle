import unittest

from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.units import Soldier
from battle.maptools.tile import Tile, ImpassableTile
from battle.rangefinder import RangeFinder


class TestRangeFinder(unittest.TestCase):
    test_map = Map(3, 3, [Tile() for _ in range(9)])

    def setUp(self):
        self.ranger = RangeFinder(map_=self.test_map)
        self.soldier = Soldier()

    def tearDown(self):
        self.test_map.remove_all_units()

    def test_init(self):
        map_ = Map(2, 2, [Tile(), Tile(), Tile(), Tile()])
        range_finder = RangeFinder(map_)
        self.assertEqual(range_finder._map, map_)

    def test_get_all_points_distance_zero(self):
        origin = Point(1, 1)
        self.assertEqual(self.ranger.get_all_points(origin, 0), {0: [origin]})

    def test_get_all_points_distance(self):
        origin = Point(0, 0)
        answer = self.ranger.get_all_points(origin, 2)
        expected = {
            0: [origin],
            1: [Point(1, 0), Point(0, 1)],
            2: [Point(2, 0), Point(1, 1), Point(0, 2)]
        }
        self.assertEqual(answer, expected)

    def test_get_all_points_does_not_include_points_not_on_map(self):
        answer = self.ranger.get_all_points(Point(0, 0), 1)
        self.assertEqual(answer, {0: [Point(0, 0)],
                                  1: [Point(1, 0), Point(0, 1)]})

    def test_get_all_points_shortcut_for_distances_beyond_map(self):
        expected = dict.fromkeys(range(0, 101), [])
        expected[0] = [Point(1, 1)]
        expected[1] = [Point(1, 0), Point(0, 1), Point(2, 1), Point(1, 2)]
        expected[2] = [Point(0, 0), Point(2, 0), Point(0, 2), Point(2, 2)]
        self.assertEqual(self.ranger.get_all_points(Point(1, 1), 100), expected)

    def test_get_all_points_includes_points_on_map_but_with_no_tile(self):
        new_map = Map(3, 3, [])
        self.assertFalse(new_map.has_tile(Point(0, 1)))
        ranger = RangeFinder(new_map)
        answer = ranger.get_all_points(Point(0, 0), 1)
        self.assertEqual(answer, {0: [Point(0, 0)],
                                  1: [Point(1, 0), Point(0, 1)]})

    def test_get_all_units_no_units(self):
        answer = self.ranger.get_all_units(Point(0, 0), 2)
        self.assertEqual(answer, {0: [], 1: [], 2: []})

    def test_get_all_units_does_not_add_None(self):
        self.test_map.place_unit(self.soldier, Point(1, 1))
        answer = self.ranger.get_all_units(Point(0, 0), 2)
        self.assertEqual(answer, {0: [], 1: [], 2: [self.soldier]})

    def test_get_all_units_all_points_occupied(self):
        all_map_points = Point(0, 0).to_rectangle(3, 3)
        points_to_units = {point: Soldier() for point in all_map_points}
        values = list(points_to_units.values())
        self.assertIsNot(values[0], values[1])
        for point, unit in points_to_units.items():
            self.test_map.place_unit(unit, point)
        distance_to_points = self.ranger.get_all_points(Point(0, 0), 6)
        answer = {}
        for distance, points in distance_to_points.items():
            soldiers = [points_to_units[point] for point in points]
            answer[distance] = soldiers
        self.assertEqual(answer, self.ranger.get_all_units(Point(0, 0), 6))

    def test_get_distances_flat_tiles(self):
        map_ = Map(3, 3, [Tile() for _ in range(9)])
        answer = RangeFinder(map_).get_move_points(Point(0, 0), 1)
        expected = {Point(0, 0): 0,
                    Point(0, 1): 1,
                    Point(1, 0): 1}
        self.assertEqual(answer, expected)

    def test_get_distances_only_includes_distances_on_map(self):
        map_ = Map(2, 2, [Tile() for _ in range(4)])
        answer = RangeFinder(map_).get_move_pts_two(Point(0, 0), 100)
        expected = {Point(0, 0): 0,
                    Point(0, 1): 1,
                    Point(1, 0): 1,
                    Point(1, 1): 2}
        self.assertEqual(answer, expected)

    def test_get_distance_non_uniform_elevation(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 1, Point(2, 0): 2,
                               Point(0, 1): 1, Point(1, 1): 2, Point(2, 1): 3,
                               Point(0, 2): 2, Point(1, 2): 3, Point(2, 2): 4}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)

        origin_1 = Point(1, 1)
        expected_1 = {Point(0, 0): 2, Point(1, 0): 1, Point(2, 0): 3,
                      Point(0, 1): 1, Point(1, 1): 0, Point(2, 1): 2,
                      Point(0, 2): 3, Point(1, 2): 2, Point(2, 2): 4}
        answer = RangeFinder(the_map).get_move_pts_two(origin_1, 5)
        self.assertEqual(answer, expected_1)

        origin_2 = Point(2, 1)
        expected_2 = {Point(0, 0): 3, Point(1, 0): 2, Point(2, 0): 1,
                      Point(0, 1): 2, Point(1, 1): 1, Point(2, 1): 0,
                      Point(0, 2): 4, Point(1, 2): 3, Point(2, 2): 2}
        answer = RangeFinder(the_map).get_move_points(origin_2, 5)
        self.assertEqual(expected_2, answer)

    def test_get_distance_non_uniform_terrain(self):
        terrain_mvs = {Point(0, 0): 1, Point(1, 0): 2,
                       Point(0, 1): 4, Point(1, 1): 3}

        tiles = [Tile(point=point, terrain_mv=terrain) for point, terrain in terrain_mvs.items()]
        map_ = Map(2, 2, tiles)
        origin = Point(0, 0)
        expected = {Point(0, 0): 0, Point(1, 0): 1,
                    Point(0, 1): 1, Point(1, 1): 3}
        self.assertEqual(RangeFinder(map_).get_move_pts_two(origin, 5), expected)

        origin = Point(0, 1)
        expected = {Point(0, 0): 4, Point(1, 0): 5,
                    Point(0, 1): 0, Point(1, 1): 4}
        self.assertEqual(RangeFinder(map_).get_move_pts_two(origin, 5), expected)

    def test_get_distance_chooses_smallest_move_pts(self):

        elevations = {Point(0, 0): 0, Point(1, 0): 0,
                      Point(0, 1): 1, Point(1, 1): 2}

        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(2, 2, tiles)
        origin = Point(0, 1)
        expected = {Point(0, 0): 1, Point(1, 0): 2,  # point(1, 0) has two different ways from 0,1
                    Point(0, 1): 0, Point(1, 1): 2}  # one way costs 2 and one way costs 3
        self.assertEqual(RangeFinder(map_).get_move_pts_two(origin, 2), expected)

    def test_get_distance_chooses_smallest_move_pts_different_order(self):

        elevations = {Point(0, 0): 2, Point(1, 0): 0,
                      Point(0, 1): 1, Point(1, 1): 0}

        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(2, 2, tiles)
        origin = Point(0, 1)
        expected = {Point(0, 0): 2, Point(1, 0): 2,  # point(1, 0) has two different ways from 0,1
                    Point(0, 1): 0, Point(1, 1): 1}  # one way costs 2 and one way costs 3
        self.assertEqual(RangeFinder(map_).get_move_pts_two(origin, 2), expected)

    def test_get_distance_elevations_and_terrains(self):
        elevation_terrain = {Point(0, 0): (0, 3), Point(1, 0): (0, 4),
                             Point(0, 1): (1, 5), Point(1, 1): (2, 6)}
        tiles = [Tile(point=point, elevation=el_terrain[0], terrain_mv=el_terrain[1])
                 for point, el_terrain in elevation_terrain.items()]
        map_ = Map(2, 2, tiles)

        origin = Point(0, 1)
        expected = {Point(0, 0): 5, Point(1, 0): 8,
                    Point(0, 1): 0, Point(1, 1): 6}
        self.assertEqual(RangeFinder(map_).get_move_pts_two(origin, 10), expected)

        origin = Point(0, 0)
        expected = {Point(0, 0): 0, Point(1, 0): 3,
                    Point(0, 1): 4, Point(1, 1): 9}
        self.assertEqual(RangeFinder(map_).get_move_pts_two(origin, 10), expected)

    # TODO FIIIIIIIIIIIIIIIIIIIIIIIIIIIIXXXXXXXXXXXXXXXXXX
    # @unittest.expectedFailure
    def test_get_distance_with_impassable_tile_in_place(self):
        elevations = {Point(0, 0): 2, Point(1, 0): 0, Point(2, 0): 3,
                      Point(0, 1): 1, Point(1, 1): 9, Point(2, 1): 2,
                      Point(0, 2): 2, Point(1, 2): 0, Point(2, 2): 1}
        tiles = [Tile(point=point, elevation=elevation) if elevation != 9 else ImpassableTile(point=point)
                 for point, elevation in elevations.items()]
        map_ = Map(3, 3, tiles)

        origin = Point(1, 2)
        expected = {Point(0, 0): 6, Point(1, 0): 7, Point(2, 0): 6,
                    Point(0, 1): 4,                 Point(2, 1): 4,
                    Point(0, 2): 3, Point(1, 2): 0, Point(2, 2): 2}
        self.assertEqual(RangeFinder(map_).get_move_pts_two(origin, 10), expected)
        # This fails on Point(1, 0): float('inf') . This happens because it never checks from Point(0, 0)
        # or Point(2, 0).  They are at distance= 3, but Point(1, 0) is at distance=2.

    def test_get_mv_points_obstacle_four(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 9, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 3, tiles)
        origin = Point(1, 2)
        expected_four = {Point(0, 0): 3, Point(1, 0): 4, Point(2, 0): 3, Point(3, 0): 4,
                         Point(0, 1): 2,                 Point(2, 1): 2, Point(3, 1): 3,
                         Point(0, 2): 1, Point(1, 2): 0, Point(2, 2): 1, Point(3, 2): 2}

        expected_three = {Point(0, 0): 3,                 Point(2, 0): 3,
                          Point(0, 1): 2,                 Point(2, 1): 2, Point(3, 1): 3,
                          Point(0, 2): 1, Point(1, 2): 0, Point(2, 2): 1, Point(3, 2): 2}

        ranger = RangeFinder(map_)
        self.assertEqual(ranger.get_move_pts_two(origin, 4), expected_four)
        self.assertEqual(ranger.get_move_pts_two(origin, 3), expected_three)

    def test_get_mv_points_obstacle_four_next(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 9, Point(1, 1): 9, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 3, tiles)
        origin = Point(1, 2)
        expected_four = {Point(0, 0): 3, Point(1, 0): 4, Point(2, 0): 3, Point(3, 0): 4,
                         Point(0, 1): 2,                 Point(2, 1): 2, Point(3, 1): 3,
                         Point(0, 2): 1, Point(1, 2): 0, Point(2, 2): 1, Point(3, 2): 2}

        expected_three = {Point(0, 0): 3,                 Point(2, 0): 3,
                          Point(0, 1): 2,                 Point(2, 1): 2, Point(3, 1): 3,
                          Point(0, 2): 1, Point(1, 2): 0, Point(2, 2): 1, Point(3, 2): 2}

        ranger = RangeFinder(map_)

        answer = ranger.get_move_pts_two(origin, 3)

        for point in sorted(answer):
            print(point,': ', answer[point])

        """
        for each point, if it's < max_mv, search it's neighbors to see if the can be added. if it has a better result,
         replace original and search that point too.
        """

