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

    def test_get_movement_points_only_to_max_mv(self):
        map_ = Map(3, 3, [Tile() for _ in range(9)])
        answer = RangeFinder(map_).get_movement_points(Point(0, 0), 1)
        expected = {Point(0, 0): 0,
                    Point(0, 1): 1,
                    Point(1, 0): 1}
        self.assertEqual(answer, expected)

    def test_get_movement_points_only_includes_distances_on_map(self):
        map_ = Map(2, 2, [Tile() for _ in range(4)])
        answer = RangeFinder(map_).get_movement_points(Point(0, 0), 100)
        expected = {Point(0, 0): 0,
                    Point(0, 1): 1,
                    Point(1, 0): 1,
                    Point(1, 1): 2}
        self.assertEqual(answer, expected)

    def test_get_movement_points_non_uniform_elevation(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 1, Point(2, 0): 2,
                               Point(0, 1): 1, Point(1, 1): 2, Point(2, 1): 3,
                               Point(0, 2): 2, Point(1, 2): 3, Point(2, 2): 4}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)

        origin_1 = Point(1, 1)
        expected_1 = {Point(0, 0): 2, Point(1, 0): 1, Point(2, 0): 3,
                      Point(0, 1): 1, Point(1, 1): 0, Point(2, 1): 2,
                      Point(0, 2): 3, Point(1, 2): 2, Point(2, 2): 4}
        answer = RangeFinder(the_map).get_movement_points(origin_1, 5)
        self.assertEqual(answer, expected_1)

        origin_2 = Point(2, 1)
        expected_2 = {Point(0, 0): 3, Point(1, 0): 2, Point(2, 0): 1,
                      Point(0, 1): 2, Point(1, 1): 1, Point(2, 1): 0,
                      Point(0, 2): 4, Point(1, 2): 3, Point(2, 2): 2}
        answer = RangeFinder(the_map).get_movement_points(origin_2, 5)
        self.assertEqual(expected_2, answer)

    def test_get_movement_points_non_uniform_terrain(self):
        terrain_mvs = {Point(0, 0): 1, Point(1, 0): 2,
                       Point(0, 1): 4, Point(1, 1): 3}

        tiles = [Tile(point=point, terrain_mv=terrain) for point, terrain in terrain_mvs.items()]
        map_ = Map(2, 2, tiles)
        origin = Point(0, 0)
        expected = {Point(0, 0): 0, Point(1, 0): 1,
                    Point(0, 1): 1, Point(1, 1): 3}
        self.assertEqual(RangeFinder(map_).get_movement_points(origin, 5), expected)

        origin = Point(0, 1)
        expected = {Point(0, 0): 4, Point(1, 0): 5,
                    Point(0, 1): 0, Point(1, 1): 4}
        self.assertEqual(RangeFinder(map_).get_movement_points(origin, 5), expected)

    def test_get_movement_points_chooses_smallest_move_pts(self):

        elevations = {Point(0, 0): 0, Point(1, 0): 0,
                      Point(0, 1): 1, Point(1, 1): 2}

        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(2, 2, tiles)
        origin = Point(0, 1)
        expected = {Point(0, 0): 1, Point(1, 0): 2,  # point(1, 0) has two different ways from 0,1
                    Point(0, 1): 0, Point(1, 1): 2}  # one way costs 2 and one way costs 3
        self.assertEqual(RangeFinder(map_).get_movement_points(origin, 10), expected)

    def test_get_movement_points_chooses_smallest_move_pts_different_order(self):

        elevations = {Point(0, 0): 2, Point(1, 0): 0,
                      Point(0, 1): 1, Point(1, 1): 0}

        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(2, 2, tiles)
        origin = Point(0, 1)
        expected = {Point(0, 0): 2, Point(1, 0): 2,  # point(1, 0) has two different ways from 0,1
                    Point(0, 1): 0, Point(1, 1): 1}  # one way costs 2 and one way costs 3
        self.assertEqual(RangeFinder(map_).get_movement_points(origin, 10), expected)

    def test_get_movement_points_elevations_and_terrains(self):
        elevation_terrain = {Point(0, 0): (0, 3), Point(1, 0): (0, 4),
                             Point(0, 1): (1, 5), Point(1, 1): (2, 6)}
        tiles = [Tile(point=point, elevation=el_terrain[0], terrain_mv=el_terrain[1])
                 for point, el_terrain in elevation_terrain.items()]
        map_ = Map(2, 2, tiles)

        origin = Point(0, 1)
        expected = {Point(0, 0): 5, Point(1, 0): 8,
                    Point(0, 1): 0, Point(1, 1): 6}
        self.assertEqual(RangeFinder(map_).get_movement_points(origin, 10), expected)

        origin = Point(0, 0)
        expected = {Point(0, 0): 0, Point(1, 0): 3,
                    Point(0, 1): 4, Point(1, 1): 9}
        self.assertEqual(RangeFinder(map_).get_movement_points(origin, 10), expected)

    def test_get_movement_points_with_impassable_tile_in_place(self):
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
        self.assertEqual(RangeFinder(map_).get_movement_points(origin, 10), expected)

    def test_get_movement_points_obstacle_max_mv_lte_map_size(self):
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
        self.assertEqual(ranger.get_movement_points(origin, 4), expected_four)
        self.assertEqual(ranger.get_movement_points(origin, 3), expected_three)

    def test_get_movement_points_obstacle_lte_max_mv_will_continue_around_corner(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 3, Point(1, 1): 4, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 3, tiles)
        origin = Point(1, 2)
        expected_four = {                Point(1, 0): 4, Point(2, 0): 3, Point(3, 0): 4,
                                                         Point(2, 1): 2, Point(3, 1): 3,
                         Point(0, 2): 1, Point(1, 2): 0, Point(2, 2): 1, Point(3, 2): 2}

        expected_five = {Point(0, 0): 5, Point(1, 0): 4, Point(2, 0): 3, Point(3, 0): 4,
                         Point(0, 1): 5, Point(1, 1): 5, Point(2, 1): 2, Point(3, 1): 3,
                         Point(0, 2): 1, Point(1, 2): 0, Point(2, 2): 1, Point(3, 2): 2}

        ranger = RangeFinder(map_)
        self.assertEqual(ranger.get_movement_points(origin, 5), expected_five)
        self.assertEqual(ranger.get_movement_points(origin, 4), expected_four)

    def test_get_movement_points_after_going_around_obstacle_will_recalculate_min_distance_bottom_to_top(self):
        elevations = {Point(0, 0): 9, Point(1, 0): 0, Point(2, 0): 9, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 0, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 3, Point(2, 2): 0, Point(3, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 0, Point(2, 3): 0, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(1, 3)
        expected_six = {                Point(1, 0): 5,                 Point(3, 0): 5,
                        Point(0, 1): 3, Point(1, 1): 4, Point(2, 1): 3, Point(3, 1): 4,
                        Point(0, 2): 2, Point(1, 2): 4, Point(2, 2): 2, Point(3, 2): 3,
                        Point(0, 3): 1, Point(1, 3): 0, Point(2, 3): 1, Point(3, 3): 2}

        ranger = RangeFinder(map_)
        self.assertEqual(ranger.get_movement_points(origin, 6), expected_six)

    def test_get_movement_points_after_going_around_obstacle_will_recalculate_min_distance_top_to_bottom(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 3, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0,
                      Point(0, 3): 9, Point(1, 3): 0, Point(2, 3): 9, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(1, 0)
        expected_six = {Point(0, 0): 1, Point(1, 0): 0, Point(2, 0): 1, Point(3, 0): 2,
                        Point(0, 1): 2, Point(1, 1): 4, Point(2, 1): 2, Point(3, 1): 3,
                        Point(0, 2): 3, Point(1, 2): 4, Point(2, 2): 3, Point(3, 2): 4,
                                        Point(1, 3): 5,                 Point(3, 3): 5}

        ranger = RangeFinder(map_)
        self.assertEqual(ranger.get_movement_points(origin, 6), expected_six)

    def test_get_movement_points_after_going_around_obstacle_will_recalculate_min_distance_l_to_r(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 9,
                      Point(0, 1): 0, Point(1, 1): 3, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 9,
                      Point(0, 3): 0, Point(1, 3): 0, Point(2, 3): 0, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(0, 1)
        expected_six = {Point(0, 0): 1, Point(1, 0): 2, Point(2, 0): 3,
                        Point(0, 1): 0, Point(1, 1): 4, Point(2, 1): 4, Point(3, 1): 5,
                        Point(0, 2): 1, Point(1, 2): 2, Point(2, 2): 3,
                        Point(0, 3): 2, Point(1, 3): 3, Point(2, 3): 4, Point(3, 3): 5}

        ranger = RangeFinder(map_)
        self.assertEqual(ranger.get_movement_points(origin, 6), expected_six)

    def test_get_movement_points_after_going_around_obstacle_will_recalculate_min_distance_r_to_l(self):
        elevations = {Point(0, 0): 9, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 0, Point(2, 1): 3, Point(3, 1): 0,
                      Point(0, 2): 9, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 0, Point(2, 3): 0, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(3, 1)
        expected_six = {                Point(1, 0): 3, Point(2, 0): 2, Point(3, 0): 1,
                        Point(0, 1): 5, Point(1, 1): 4, Point(2, 1): 4, Point(3, 1): 0,
                                        Point(1, 2): 3, Point(2, 2): 2, Point(3, 2): 1,
                        Point(0, 3): 5, Point(1, 3): 4, Point(2, 3): 3, Point(3, 3): 2}

        ranger = RangeFinder(map_)
        self.assertEqual(ranger.get_movement_points(origin, 6), expected_six)

    def test_get_movement_points_goes_around_obstacle_and_recalculates_on_terrain(self):
        terrains = {Point(0, 0): 1, Point(1, 0): 1, Point(2, 0): 1, Point(3, 0): 1,
                    Point(0, 1): 1, Point(1, 1): 1, Point(2, 1): 1, Point(3, 1): 1,
                    Point(0, 2): 1, Point(1, 2): 4, Point(2, 2): 9, Point(3, 2): 1,
                    Point(0, 3): 1, Point(1, 3): 1, Point(2, 3): 5, Point(3, 3): 1}
        tiles = [Tile(point=point, terrain_mv=terrain) for point, terrain in terrains.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(1, 3)
        expected_six = {Point(0, 0): 4, Point(1, 0): 5, Point(2, 0): 6,
                        Point(0, 1): 3, Point(1, 1): 4, Point(2, 1): 5, Point(3, 1): 6,
                        Point(0, 2): 2, Point(1, 2): 1, Point(2, 2): 5,
                        Point(0, 3): 1, Point(1, 3): 0, Point(2, 3): 1, Point(3, 3): 6}

        ranger = RangeFinder(map_)
        self.assertEqual(ranger.get_movement_points(origin, 6), expected_six)


def pretty_print(answer):
    """
    when you want a nice printout of RangeFinder.<some_func> that returns a dictionary.

    Use this to see where your test answer differs from expected answer.
    """
    sorted_results = sorted(answer.items())
    max_pt = sorted_results[-1][0]
    blank_space = ' ' * len('{!r}: {}'.format(*sorted_results[0]))
    for y in range(max_pt.y + 1):
        to_print = [(pt, val) for pt, val in sorted_results if pt.y == y]
        for x in range(max_pt.x + 1):
            pt, val = to_print[0]
            if pt.x == x:
                print('{!r}: {}'.format(pt, val), end=', ')
                del to_print[0]
            else:
                print(blank_space, end=', ')
            x += 1
        print()
