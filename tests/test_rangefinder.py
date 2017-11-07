import unittest

from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.maptools.tile import Tile
from battle.players.units import Soldier
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

    def test_get_all_usable_points_distance_zero(self):
        origin = Point(1, 1)
        self.assertEqual(self.ranger.get_all_usable_points(origin, 0), {0: [origin]})

    def test_get_all_usable_points_distance(self):
        origin = Point(0, 0)
        answer = self.ranger.get_all_usable_points(origin, 2)
        expected = {
            0: [origin],
            1: [Point(1, 0), Point(0, 1)],
            2: [Point(2, 0), Point(1, 1), Point(0, 2)]
        }
        self.assertEqual(answer, expected)

    def test_get_all_usable_points_does_not_include_points_not_on_map(self):
        answer = self.ranger.get_all_usable_points(Point(0, 0), 1)
        self.assertEqual(answer, {0: [Point(0, 0)],
                                  1: [Point(1, 0), Point(0, 1)]})

    def test_get_all_usable_points_shortcut_for_distances_beyond_map(self):
        expected = dict.fromkeys(range(0, 101), [])
        expected[0] = [Point(1, 1)]
        expected[1] = [Point(1, 0), Point(0, 1), Point(2, 1), Point(1, 2)]
        expected[2] = [Point(0, 0), Point(2, 0), Point(0, 2), Point(2, 2)]
        self.assertEqual(self.ranger.get_all_usable_points(Point(1, 1), 100), expected)

    def test_get_all_usable_points_does_not_include_points_on_map_with_no_tile(self):
        new_map = Map(3, 3, [Tile(point=Point(0, 0)), Tile(point=Point(1, 0))])
        self.assertFalse(new_map.has_tile(Point(0, 1)))
        self.assertTrue(new_map.has_tile(Point(0, 0)))
        self.assertTrue(new_map.has_tile(Point(1, 0)))
        ranger = RangeFinder(new_map)
        answer = ranger.get_all_usable_points(Point(0, 0), 1)
        self.assertEqual(answer, {0: [Point(0, 0)],
                                  1: [Point(1, 0)]})

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
        distance_to_points = self.ranger.get_all_usable_points(Point(0, 0), 6)
        answer = {}
        for distance, points in distance_to_points.items():
            soldiers = [points_to_units[point] for point in points]
            answer[distance] = soldiers
        self.assertEqual(answer, self.ranger.get_all_units(Point(0, 0), 6))

    def test_get_sight_ranges(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 1, Point(2, 0): 1,
                               Point(0, 1): 1, Point(1, 1): 2, Point(2, 1): 2,
                               Point(0, 2): 2, Point(1, 2): 1, Point(2, 2): 4}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        origin = Point(0, 1)
        answer = RangeFinder(the_map).get_sight_ranges(origin, 5)
        expected = dict.fromkeys(range(0, 6), [])
        expected[0] = [origin]
        expected[1] = sorted([Point(0, 0), Point(1, 1), Point(0, 2)])
        expected[2] = sorted([Point(1, 0), Point(2, 1), Point(1, 2)])
        expected[3] = sorted([Point(2, 2)])

        self.assertEqual(answer, expected)

    def test_get_sight_ranges_missing_tile(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 1, Point(2, 0): 1,
                               Point(0, 1): 1, Point(1, 1): 2, Point(2, 1): 2,
                               Point(0, 2): 2,                 Point(2, 2): 4}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        self.assertTrue(the_map.is_on_map(Point(1, 2)))
        self.assertFalse(the_map.has_tile(Point(1, 2)))

        origin = Point(0, 1)
        answer = RangeFinder(the_map).get_sight_ranges(origin, 5)
        expected = dict.fromkeys(range(0, 6), [])
        expected[0] = [origin]
        expected[1] = sorted([Point(0, 0), Point(1, 1), Point(0, 2)])
        expected[2] = sorted([Point(1, 0), Point(2, 1)])
        expected[3] = sorted([Point(2, 2)])

        self.assertEqual(answer, expected)

    def test_get_sight_ranges_distance_zero(self):
        origin = Point(0, 1)
        answer = self.ranger.get_sight_ranges(origin, 0)
        expected = {0: [origin]}

        self.assertEqual(answer, expected)

    def test_get_sight_ranges_occupied_tiles_are_fine(self):
        points_to_elevation = {Point(0, 0): 1, Point(1, 0): 4,
                               Point(0, 1): 5}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        for key in points_to_elevation:
            the_map.place_unit(Soldier(), key)
        origin = Point(0, 0)
        expected = {0: [origin],
                    1: [Point(1, 0), Point(0, 1)]}
        self.assertEqual(expected, RangeFinder(the_map).get_sight_ranges(origin, 1))

    def test_get_attack_ranges_ranged_no_points_off_map(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): -1, Point(2, 0): 1,
                               Point(0, 1): 1, Point(1, 1): 2, Point(2, 1): 2,
                               Point(0, 2): 2, Point(1, 2): 4, Point(2, 2): 4}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        origin = Point(1, 1)
        expected = {0: [(origin, 0)],
                    1: [(Point(1, 0), 1), (Point(0, 1), 1),(Point(2, 1), 0), (Point(1, 2), -1)],
                    2: [(Point(0, 0), 1), (Point(2, 0), 1), (Point(0, 2), 0), (Point(2, 2), -1)]}

        self.assertEqual(expected, RangeFinder(the_map).get_attack_ranges_ranged(origin, 2))

    def test_get_attack_ranges_missing_tiles(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): -1,
                               Point(0, 1): 1, Point(1, 1): 2, Point(2, 1): 2,
                               Point(0, 2): 2,                 Point(2, 2): 4}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        origin = Point(1, 1)
        expected = {0: [(origin, 0)],
                    1: [(Point(1, 0), 1), (Point(0, 1), 1), (Point(2, 1), 0)],
                    2: [(Point(0, 0), 1), (Point(0, 2), 0), (Point(2, 2), -1)]}
        self.assertEqual(expected, RangeFinder(the_map).get_attack_ranges_ranged(origin, 2))

    def test_get_attack_ranges_ranged_with_obstacles(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 5, Point(2, 0): 0,
                               Point(0, 1): 1, Point(1, 1): 1, Point(2, 1): 2,
                               Point(0, 2): 2, Point(1, 2): 4, Point(2, 2): 4}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        origin = Point(0, 0)
        expected = {0: [(origin, 0)],
                    1: [(Point(1, 0), -1), (Point(0, 1), -1)],
                    2: [(Point(1, 1), -1), (Point(0, 2), -1)],
                    3: [(Point(1, 2), -1)],
                    4: [(Point(2, 2), -1)]}
        self.assertEqual(expected, RangeFinder(the_map).get_attack_ranges_ranged(origin, 4))

    def test_get_attack_ranges_ranged_occupied_tiles_are_fine(self):
        points_to_elevation = {Point(0, 0): 1, Point(1, 0): 4,
                               Point(0, 1): 5}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        for key in points_to_elevation:
            the_map.place_unit(Soldier(), key)
        origin = Point(0, 0)
        expected = {0: [(origin, 0)],
                    1: [(Point(1, 0), -1), (Point(0, 1), -1)]}
        self.assertEqual(expected, RangeFinder(the_map).get_attack_ranges_ranged(origin, 1))

    def test_get_attack_ranges_melee_target_advantage_values(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): -1, Point(2, 0): 1,
                               Point(0, 1): 1, Point(1, 1): 2, Point(2, 1): 2,
                               Point(0, 2): 2, Point(1, 2): 4, Point(2, 2): 4}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        origin = Point(1, 1)
        expected = {0: [(origin, 0)],
                    1: [(Point(1, 0), 1), (Point(0, 1), 1), (Point(2, 1), 0), (Point(1, 2), -1)],
                    2: [(Point(0, 0), 1), (Point(2, 0), 1), (Point(0, 2), 0), (Point(2, 2), -1)]}
        self.assertEqual(expected, RangeFinder(the_map).get_attack_ranges_melee(origin, 2))

    def test_get_attack_ranges_melee_target_too_high(self):
        points_to_elevation = {Point(0, 0): 1, Point(1, 0): 4,
                               Point(0, 1): 5}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        origin = Point(0, 0)
        expected = {0: [(origin, 0)],
                    1: [(Point(1, 0), -1)]}
        self.assertEqual(expected, RangeFinder(the_map).get_attack_ranges_melee(origin, 1))

    def test_get_attack_ranges_melee_target_too_low(self):
        points_to_elevation = {Point(0, 0): 1, Point(1, 0): -3,
                               Point(0, 1): -2}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        origin = Point(0, 0)
        expected = {0: [(origin, 0)],
                    1: [(Point(0, 1), 1)]}
        self.assertEqual(expected, RangeFinder(the_map).get_attack_ranges_melee(origin, 1))

    def test_get_attack_ranges_melee_default_distance(self):
        points_to_elevation = {Point(0, 0): -2, Point(1, 0): -1, Point(2, 0): 1,
                               Point(0, 1): 1, Point(1, 1): 2, Point(2, 1): 2,
                               Point(0, 2): -1, Point(1, 2): 4, Point(2, 2): 0}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        origin = Point(1, 1)
        expected = {0: [(origin, 0)],
                    1: [(Point(1, 0), 1), (Point(0, 1), 1), (Point(2, 1), 0), (Point(1, 2), -1)]}
        self.assertEqual(expected, RangeFinder(the_map).get_attack_ranges_melee(origin))

    def test_get_attack_ranges_melee_set_distance_value(self):
        points_to_elevation = {Point(0, 0): -2, Point(1, 0): -1, Point(2, 0): 1,
                               Point(0, 1): 1, Point(1, 1): 2, Point(2, 1): 2,
                               Point(0, 2): -1, Point(1, 2): 4, Point(2, 2): 0}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        origin = Point(1, 1)
        expected = {0: [(origin, 0)],
                    1: [(Point(1, 0), 1), (Point(0, 1), 1), (Point(2, 1), 0), (Point(1, 2), -1)],
                    2: [(Point(2, 0), 1), (Point(0, 2), 1), (Point(2, 2), 1)]}
        self.assertEqual(expected, RangeFinder(the_map).get_attack_ranges_melee(origin, 2))

    def test_get_attack_ranges_melee_set_distance_value_with_obstacle(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 5, Point(2, 0): 0,
                               Point(0, 1): 1, Point(1, 1): 1, Point(2, 1): 2,
                               Point(0, 2): 2, Point(1, 2): 3, Point(2, 2): 3}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        origin = Point(0, 0)
        expected = {0: [(origin, 0)],
                    1: [(Point(0, 1), -1)],
                    2: [(Point(1, 1), -1), (Point(0, 2), -1)],
                    3: [(Point(1, 2), -1)],
                    4: [(Point(2, 2), -1)]}
        self.assertEqual(expected, RangeFinder(the_map).get_attack_ranges_melee(origin, 4))

    def test_get_attack_ranges_melee_occupied_tiles_are_fine(self):
        points_to_elevation = {Point(0, 0): 1, Point(1, 0): 4,
                               Point(0, 1): 5}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        for key in points_to_elevation:
            the_map.place_unit(Soldier(), key)
        origin = Point(0, 0)
        expected = {0: [(origin, 0)],
                    1: [(Point(1, 0), -1)]}
        self.assertEqual(expected, RangeFinder(the_map).get_attack_ranges_melee(origin, 1))


def pretty_print(answer):
    """
    when you want a nice printout of RangeFinder.<some_func> that returns a dictionary.

    Use this to see where your test answer differs from expected answer.
    """
    print(pretty_string(answer) + '\n\n')


def pretty_string(answer):
    y_vals = [pt.y for pt in answer]
    x_vals = [pt.x for pt in answer]

    blank_space = ' ' * len('{!r}: {}'.format(*next(iter(answer.items()))))
    rows = []
    for row in range(min(y_vals), max(y_vals) + 1):
        row_entries = []
        for column in range(min(x_vals), max(x_vals) + 1):
            point = Point(column, row)
            if point not in answer:
                row_entries.append(blank_space)
            else:
                row_entries.append('{!r}: {}'.format(point, answer[point]))
        rows.append(', '.join(row_entries))
    return '\n'.join(rows)


class TestPrettyString(unittest.TestCase):
    def test_basic_square(self):

        test = {Point(0, 0): 6, Point(1, 0): 5,
                Point(0, 1): 4, Point(1, 1): 3,
                Point(0, 2): 2, Point(1, 2): 1}
        expected = ('Point(0, 0): 6, Point(1, 0): 5\n' +
                    'Point(0, 1): 4, Point(1, 1): 3\n' +
                    'Point(0, 2): 2, Point(1, 2): 1')
        self.assertEqual(pretty_string(test), expected)

    def test_basic_square_negative_values(self):

        test = {Point(-1, -1): 6, Point(0, -1): 5,
                Point(-1, 0): 6, Point(0, 0): 5,
                Point(-1, 1): 4, Point(0, 1): 3,
                Point(-1, 2): 2, Point(0, 2): 1}
        expected = ('Point(-1, -1): 6, Point(0, -1): 5\n' +
                    'Point(-1, 0): 6, Point(0, 0): 5\n' +
                    'Point(-1, 1): 4, Point(0, 1): 3\n' +
                    'Point(-1, 2): 2, Point(0, 2): 1')
        self.assertEqual(pretty_string(test), expected)

    def test_missing_corners_right(self):
        test = {Point(0, 0): 6,
                                Point(1, 1): 3,
                Point(0, 2): 2}
        expected = ('Point(0, 0): 6,               \n' +
                    '              , Point(1, 1): 3\n' +
                    'Point(0, 2): 2,               ')
        self.assertEqual(pretty_string(test), expected)

    def test_missing_corners_left(self):
        test = {                Point(1, 0): 5,
                Point(0, 1): 4,
                                Point(1, 2): 1}
        expected = ('              , Point(1, 0): 5\n' +
                    'Point(0, 1): 4,               \n' +
                    '              , Point(1, 2): 1')
        self.assertEqual(pretty_string(test), expected)

    def test_missing_row(self):
        test = {Point(0, 0): 6, Point(1, 0): 5,

                Point(0, 2): 2, Point(1, 2): 1}
        expected = ('Point(0, 0): 6, Point(1, 0): 5\n' +
                    '              ,               \n' +
                    'Point(0, 2): 2, Point(1, 2): 1')
        self.assertEqual(pretty_string(test), expected)

    def test_missing_column(self):

        test = {Point(0, 0): 6,                 Point(2, 0): 10,
                Point(0, 1): 4,                 Point(2, 1): 20,
                Point(0, 2): 2,                 Point(2, 2): 30}
        expected = ('Point(0, 0): 6,               , Point(2, 0): 10\n' +
                    'Point(0, 1): 4,               , Point(2, 1): 20\n' +
                    'Point(0, 2): 2,               , Point(2, 2): 30')
        self.assertEqual(pretty_string(test), expected)
