from unittest import TestCase

from battle.weapon import RangedWeapon, MeleeWeapon
from battle.units import Soldier, FIST
from battle.perimiterlistener import PerimeterListener
from battle.rangefinder import RangeFinder
from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.maptools.tile import Tile


class TestPerimeterListener(TestCase):
    def setUp(self):
        self.gun = RangedWeapon(2, 2, 2, 2)
        self.melee = Soldier()
        self.melee.equip_weapon(FIST)

        self.ranged = Soldier()
        self.ranged.equip_weapon(self.gun)

    def test_set_up(self):
        self.assertEqual(self.gun.stats.range, 2)
        self.assertIsInstance(self.gun, RangedWeapon)

        self.assertEqual(FIST.stats.range, 1)
        self.assertIsInstance(FIST, MeleeWeapon)

        self.assertEqual(self.melee.get_weapon(), FIST)
        self.assertEqual(self.melee.get_perimeter_size(), 1)

        self.assertEqual(self.ranged.get_weapon(), self.gun)
        self.assertEqual(self.ranged.get_perimeter_size(), 2)

    def test_init_creates_empty_table_with_unique_sets(self):
        points = [Point(0, 0), Point(1, 0), Point(2, 0),
                  Point(0, 1), Point(1, 1), Point(2, 1)]
        tiles = [Tile(point=pt) for pt in points]
        map_ = Map(3, 2, tiles)

        listener = PerimeterListener(map_)

        expected = {pt: set() for pt in points}
        self.assertEqual(listener._watchers_at_point, expected)
        listener._watchers_at_point[Point(0, 0)].add(1)
        self.assertEqual(listener._watchers_at_point[Point(1, 0)], set())

    def test_set_perimeter_melee(self):

        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 5, Point(2, 0): 0,
                               Point(0, 1): 1, Point(1, 1): 1, Point(2, 1): 2,
                               Point(0, 2): 2, Point(1, 2): 3, Point(2, 2): 3}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)

        origin = Point(1, 1)
        expected_ranges = {0: [(Point(1, 1), 0)],
                           1: [(Point(0, 1), 0), (Point(2, 1), -1), (Point(1, 2), -1)]}
        self.assertEqual(RangeFinder(map_=the_map).get_attack_ranges_melee(origin, range_=1), expected_ranges)

        listener = PerimeterListener(the_map)
        listener.set_perimeter(self.melee, origin)
        expected = {key: set() for key in points_to_elevation}
        expected[Point(0, 1)] = {self.melee}
        expected[Point(2, 1)] = {self.melee}
        expected[Point(1, 2)] = {self.melee}
        self.assertEqual(listener._watchers_at_point, expected)

    def test_set_perimeter_ranged(self):

        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 5, Point(2, 0): 0,
                               Point(0, 1): 1, Point(1, 1): 1, Point(2, 1): 2,
                               Point(0, 2): 2, Point(1, 2): 3, Point(2, 2): 3}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)

        origin = Point(0, 0)
        expected_ranges = {0: [(Point(0, 0), 0)],
                           1: [(Point(1, 0), -1), (Point(0, 1), -1)],
                           2: [(Point(1, 1), -1), (Point(0, 2), -1)]}
        self.assertEqual(RangeFinder(map_=the_map).get_attack_ranges_ranged(origin, range_=2), expected_ranges)

        listener = PerimeterListener(the_map)
        listener.set_perimeter(self.ranged, origin)
        expected = {key: set() for key in points_to_elevation}
        expected[Point(0, 1)] = {self.ranged}
        expected[Point(1, 0)] = {self.ranged}
        expected[Point(0, 2)] = {self.ranged}
        expected[Point(1, 1)] = {self.ranged}
        self.assertEqual(listener._watchers_at_point, expected)

    def test_set_perimeter_two_units(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 5, Point(2, 0): 0,
                               Point(0, 1): 1, Point(1, 1): 1, Point(2, 1): 2,
                               Point(0, 2): 2, Point(1, 2): 3, Point(2, 2): 3}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        listener = PerimeterListener(the_map)
        melee_pt = Point(1, 1)
        ranged_pt = Point(0, 0)
        listener.set_perimeter(self.melee, melee_pt)
        listener.set_perimeter(self.ranged, ranged_pt)

        expected = {key: set() for key in points_to_elevation}
        expected[Point(0, 1)] = {self.ranged, self.melee}
        expected[Point(1, 0)] = {self.ranged}
        expected[Point(0, 2)] = {self.ranged}
        expected[Point(1, 1)] = {self.ranged}

        expected[Point(2, 1)] = {self.melee}
        expected[Point(1, 2)] = {self.melee}

        self.assertEqual(listener._watchers_at_point, expected)

    def test_get_attackers(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 5, Point(2, 0): 0,
                               Point(0, 1): 1, Point(1, 1): 1, Point(2, 1): 2,
                               Point(0, 2): 2, Point(1, 2): 3, Point(2, 2): 3}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        listener = PerimeterListener(the_map)
        melee_pt = Point(1, 1)
        ranged_pt = Point(0, 0)
        listener.set_perimeter(self.melee, melee_pt)
        listener.set_perimeter(self.ranged, ranged_pt)

        self.assertEqual(listener.get_attackers(Point(2, 2)), set())
        self.assertEqual(listener.get_attackers(Point(0, 1)), {self.ranged, self.melee})
        self.assertEqual(listener.get_attackers(Point(0, 2)), {self.ranged})
        self.assertEqual(listener.get_attackers(Point(1, 2)), {self.melee})

    def test_rm_perimeter_one_unit(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 5, Point(2, 0): 0,
                               Point(0, 1): 1, Point(1, 1): 1, Point(2, 1): 2,
                               Point(0, 2): 2, Point(1, 2): 3, Point(2, 2): 3}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        listener = PerimeterListener(the_map)
        melee_pt = Point(1, 1)
        listener.set_perimeter(self.melee, melee_pt)

        empty = {pt: set() for pt in points_to_elevation}
        non_empty = {pt: set() for pt in points_to_elevation}
        non_empty[Point(0, 1)] = {self.melee}
        non_empty[Point(2, 1)] = {self.melee}
        non_empty[Point(1, 2)] = {self.melee}

        self.assertEqual(listener._watchers_at_point, non_empty)

        listener.rm_perimeter(self.melee)

        self.assertEqual(listener._watchers_at_point, empty)

    def test_rm_perimeter_two_units(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 5, Point(2, 0): 0,
                               Point(0, 1): 1, Point(1, 1): 1, Point(2, 1): 2,
                               Point(0, 2): 2, Point(1, 2): 3, Point(2, 2): 3}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)
        listener = PerimeterListener(the_map)
        melee_pt = Point(1, 1)
        ranged_pt = Point(0, 0)
        listener.set_perimeter(self.melee, melee_pt)
        listener.set_perimeter(self.ranged, ranged_pt)

        with_ranged = {pt: set() for pt in points_to_elevation}
        with_ranged[Point(0, 1)] = {self.ranged, self.melee}
        with_ranged[Point(1, 0)] = {self.ranged}
        with_ranged[Point(0, 2)] = {self.ranged}
        with_ranged[Point(1, 1)] = {self.ranged}

        with_ranged[Point(2, 1)] = {self.melee}
        with_ranged[Point(1, 2)] = {self.melee}

        no_ranged = {pt: set() for pt in points_to_elevation}
        no_ranged[Point(0, 1)] = {self.melee}
        no_ranged[Point(2, 1)] = {self.melee}
        no_ranged[Point(1, 2)] = {self.melee}

        self.assertEqual(listener._watchers_at_point, with_ranged)

        listener.rm_perimeter(self.ranged)

        self.assertEqual(listener._watchers_at_point, no_ranged)
