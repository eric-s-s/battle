import unittest

from battle.turn_execution.target_finder import TargetFinder

from battle.maptools.map import Map
from battle.players.units import Soldier
from battle.weapon import MeleeWeapon, RangedWeapon
from battle.players.team import Team
from battle.maptools.point import Point
from battle.maptools.tile import Tile


class TestTargetFinder(unittest.TestCase):

    def setUp(self):

        self.map_length = 20
        self.map = Map(self.map_length, self.map_length, [Tile() for _ in range(self.map_length**2)])
        self.team_a = Team(Point(self.map_length-1, 0), self.map)
        self.team_b = Team(Point(0, self.map_length-1), self.map)

        team_size = 3
        self.a_units = [Soldier() for _ in range(team_size)]
        self.b_units = [Soldier() for _ in range(team_size)]

        for a_unit, b_unit in zip(self.a_units, self.b_units):
            self.team_a.add_player(a_unit)
            self.team_b.add_player(b_unit)

    def test_get_team(self):
        teams = [self.team_a, self.team_b]
        test = TargetFinder(self.map, teams)
        for unit in self.a_units + self.b_units:
            test_team = test.get_team(unit)
            self.assertTrue(test_team.is_on_team(unit))

    def test_init_copies_team_list(self):
        teams = [self.team_a, self.team_b]
        test = TargetFinder(self.map, teams)
        teams[0] = 'not a team'
        teams[1] = 'nope'
        for unit in self.a_units + self.b_units:
            test_team = test.get_team(unit)
            self.assertTrue(test_team.is_on_team(unit))

    def test_allies_in_sight_answer_excludes_non_allies(self):
        all_units = self.a_units + self.b_units
        for index, unit in enumerate(all_units):
            self.map.place_unit(unit, Point(index, index))
        test_unit = all_units[0]
        self.assertEqual(test_unit.get_sight_range(), 10)

        teams = [self.team_a, self.team_b]
        test = TargetFinder(self.map, teams)
        answer = test.allies_in_sight(test_unit)
        expected = {
            self.a_units[1]: 2,
            self.a_units[2]: 4
        }
        self.assertEqual(answer, expected)

    def test_allies_in_sight_no_allies(self):
        all_units = self.a_units[0:1] + self.b_units
        for index, unit in enumerate(all_units):
            self.map.place_unit(unit, Point(index, index))
        test_unit = all_units[0]

        teams = [self.team_a, self.team_b]
        test = TargetFinder(self.map, teams)
        answer = test.allies_in_sight(test_unit)
        self.assertEqual(answer, {})

    def test_allies_in_sight_by_obstructed_view(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 1, Point(2, 0): 0}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 1, tiles)

        origin, in_sight, out_of_sight = self.a_units
        the_map.place_unit(origin, Point(0, 0))
        the_map.place_unit(in_sight, Point(1, 0))
        the_map.place_unit(out_of_sight, Point(2, 0))

        tf = TargetFinder(the_map, [self.team_a, self.team_b])

        answer = tf.allies_in_sight(origin)
        expected = {
            in_sight: 1,
        }
        self.assertEqual(answer, expected)

    def test_allies_in_sight_by_sight_range(self):
        origin, in_sight, out_of_sight = self.a_units
        self.map.place_unit(origin, Point(0, 0))
        self.map.place_unit(in_sight, Point(10, 0))
        self.map.place_unit(out_of_sight, Point(11, 0))
        tf = TargetFinder(self.map, [self.team_a, self.team_b])

        answer = tf.allies_in_sight(origin)
        expected = {
           in_sight: 10,
        }
        self.assertEqual(answer, expected)

        self.map.remove_unit(Point(10, 0))
        self.map.remove_unit(Point(11, 0))
        self.map.place_unit(in_sight, Point(5, 5))
        self.map.place_unit(out_of_sight, Point(5, 6))
        answer = tf.allies_in_sight(origin)
        self.assertEqual(answer, expected)

    def test_allies_in_sight_different_sight_range(self):
        class NewSoldier(Soldier):
            def get_sight_range(self):
                return 3

        short_sighted = NewSoldier()
        self.team_a.add_player(short_sighted)

        in_sight, also_in_sight, out_of_sight = self.a_units
        self.map.place_unit(short_sighted, Point(0, 0))
        self.map.place_unit(in_sight, Point(3, 0))
        self.map.place_unit(also_in_sight, Point(2, 1))
        self.map.place_unit(out_of_sight, Point(4, 0))
        tf = TargetFinder(self.map, [self.team_a, self.team_b])

        answer = tf.allies_in_sight(short_sighted)
        expected = {
            in_sight: 3,
            also_in_sight: 3
        }
        self.assertEqual(answer, expected)

    def test_enemies_in_sight_answer_excludes_non_enemies(self):
        all_units = self.a_units + self.b_units
        for index, unit in enumerate(all_units):
            self.map.place_unit(unit, Point(index, index))
        test_unit = all_units[3]
        self.assertEqual(test_unit.get_sight_range(), 10)

        teams = [self.team_a, self.team_b]
        test = TargetFinder(self.map, teams)
        answer = test.enemies_in_sight(test_unit)
        expected = {
            self.a_units[0]: 6,
            self.a_units[1]: 4,
            self.a_units[2]: 2
        }
        self.assertEqual(answer, expected)

    def test_enemies_in_sight_no_enemies(self):
        all_units = self.b_units
        for index, unit in enumerate(all_units):
            self.map.place_unit(unit, Point(index, index))
        test_unit = all_units[2]

        teams = [self.team_a, self.team_b]
        test = TargetFinder(self.map, teams)
        answer = test.enemies_in_sight(test_unit)
        self.assertEqual(answer, {})

    def test_enemies_in_sight_by_obstructed_view(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 1, Point(2, 0): 0}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 1, tiles)

        origin = self.a_units[0]
        in_sight, out_of_sight = self.b_units[0:2]
        the_map.place_unit(origin, Point(0, 0))
        the_map.place_unit(in_sight, Point(1, 0))
        the_map.place_unit(out_of_sight, Point(2, 0))

        tf = TargetFinder(the_map, [self.team_a, self.team_b])

        answer = tf.enemies_in_sight(origin)
        expected = {
            in_sight: 1,
        }
        self.assertEqual(answer, expected)

    def test_enemies_in_sight_by_sight_range(self):
        origin= self.a_units[0]
        in_sight, out_of_sight = self.b_units[0:2]
        self.map.place_unit(origin, Point(0, 0))
        self.map.place_unit(in_sight, Point(10, 0))
        self.map.place_unit(out_of_sight, Point(11, 0))
        tf = TargetFinder(self.map, [self.team_a, self.team_b])

        answer = tf.enemies_in_sight(origin)
        expected = {
           in_sight: 10,
        }
        self.assertEqual(answer, expected)

        self.map.remove_unit(Point(10, 0))
        self.map.remove_unit(Point(11, 0))
        self.map.place_unit(in_sight, Point(5, 5))
        self.map.place_unit(out_of_sight, Point(5, 6))
        answer = tf.enemies_in_sight(origin)
        self.assertEqual(answer, expected)

    def test_enemies_in_sight_different_sight_range(self):
        class NewSoldier(Soldier):
            def get_sight_range(self):
                return 3

        short_sighted = NewSoldier()
        self.team_a.add_player(short_sighted)

        in_sight, also_in_sight, out_of_sight = self.b_units
        self.map.place_unit(short_sighted, Point(0, 0))
        self.map.place_unit(in_sight, Point(3, 0))
        self.map.place_unit(also_in_sight, Point(2, 1))
        self.map.place_unit(out_of_sight, Point(4, 0))
        tf = TargetFinder(self.map, [self.team_a, self.team_b])

        answer = tf.enemies_in_sight(short_sighted)
        expected = {
            in_sight: 3,
            also_in_sight: 3
        }
        self.assertEqual(answer, expected)

    def test_allies_in_range_answer_excludes_non_allies(self):
        all_units = self.a_units + self.b_units
        for index, unit in enumerate(all_units):
            self.map.place_unit(unit, Point(index, index))
        test_unit = all_units[0]
        test_unit.equip_weapon(RangedWeapon(10, 10, 10, 10))

        teams = [self.team_a, self.team_b]
        test = TargetFinder(self.map, teams)
        answer = test.allies_in_range(test_unit)
        expected = {
            self.a_units[1]: (2, 0),
            self.a_units[2]: (4, 0)
        }
        self.assertEqual(answer, expected)

    def test_allies_in_range_no_allies(self):
        all_units = self.a_units[0:1] + self.b_units
        for index, unit in enumerate(all_units):
            self.map.place_unit(unit, Point(index, index))
        test_unit = all_units[0]
        test_unit.equip_weapon(RangedWeapon(10, 10, 10, 10))

        teams = [self.team_a, self.team_b]
        test = TargetFinder(self.map, teams)
        answer = test.allies_in_range(test_unit)
        self.assertEqual(answer, {})

    def test_allies_in_range_by_obstructed_view(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 1, Point(2, 0): 0}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 1, tiles)

        origin, in_range, out_of_sight = self.a_units
        origin.equip_weapon(RangedWeapon(10, 10, 10, 10))

        the_map.place_unit(origin, Point(0, 0))
        the_map.place_unit(in_range, Point(1, 0))
        the_map.place_unit(out_of_sight, Point(2, 0))

        tf = TargetFinder(the_map, [self.team_a, self.team_b])

        answer = tf.allies_in_range(origin)
        expected = {
            in_range: (1, -1),
        }
        self.assertEqual(answer, expected)

    def test_allies_in_range_by_weapon_range(self):
        origin, in_range, out_of_range = self.a_units
        for weapon_range in range(1, 5):
            self.map.remove_all_units()
            self.map.place_unit(origin, Point(0, 0))

            self.map.place_unit(in_range, Point(weapon_range, 0))
            self.map.place_unit(out_of_range, Point(weapon_range + 1, 0))
            tf = TargetFinder(self.map, [self.team_a, self.team_b])
            origin.equip_weapon(RangedWeapon(1, 1, weapon_range, 1))

            answer = tf.allies_in_range(origin)
            expected = {
               in_range: (weapon_range, 0),
            }
            self.assertEqual(answer, expected)

    def test_allies_in_range_advantage(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): -1, Point(2, 0): 1}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 1, tiles)

        origin, below, above = self.a_units
        origin.equip_weapon(RangedWeapon(10, 10, 10, 10))

        the_map.place_unit(origin, Point(0, 0))
        the_map.place_unit(below, Point(1, 0))
        the_map.place_unit(above, Point(2, 0))

        tf = TargetFinder(the_map, [self.team_a, self.team_b])

        answer = tf.allies_in_range(origin)
        expected = {
            below: (1, 1),
            above: (2, -1)
        }
        self.assertEqual(answer, expected)

    def test_allies_in_range_melee_weapon(self):
        points_to_elevation = {                Point(1, 0): -3,
                               Point(0, 1): 4, Point(1, 1): 0, Point(2, 1): -4,
                                               Point(1, 2): 3                 }
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)

        origin, below, above = self.a_units
        far_below = Soldier()
        far_above = Soldier()
        self.team_a.add_player(far_above)
        self.team_a.add_player(far_below)
        origin.equip_weapon(MeleeWeapon(10, 10, 10, 10))

        the_map.place_unit(origin, Point(1, 1))
        the_map.place_unit(below, Point(1, 0))
        the_map.place_unit(above, Point(1, 2))
        the_map.place_unit(far_above, Point(0, 1))
        the_map.place_unit(far_below, Point(2, 1))

        tf = TargetFinder(the_map, [self.team_a, self.team_b])

        answer = tf.allies_in_range(origin)
        expected = {
            below: (1, 1),
            above: (1, -1)
        }
        self.assertEqual(answer, expected)

    def test_enemies_in_range_answer_excludes_non_enemies(self):
        all_units = self.a_units + self.b_units
        for index, unit in enumerate(all_units):
            self.map.place_unit(unit, Point(index, index))
        test_unit = all_units[3]
        test_unit.equip_weapon(RangedWeapon(10, 10, 10, 10))

        teams = [self.team_a, self.team_b]
        test = TargetFinder(self.map, teams)
        answer = test.enemies_in_range(test_unit)
        expected = {
            self.a_units[0]: (6, 0),
            self.a_units[1]: (4, 0),
            self.a_units[2]: (2, 0)
        }
        self.assertEqual(answer, expected)

    def test_enemies_in_range_no_enemies(self):
        all_units = self.b_units
        for index, unit in enumerate(all_units):
            self.map.place_unit(unit, Point(index, index))
        test_unit = all_units[2]

        teams = [self.team_a, self.team_b]
        test = TargetFinder(self.map, teams)
        answer = test.enemies_in_range(test_unit)
        self.assertEqual(answer, {})

    def test_enemies_in_range_by_obstructed_view(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 1, Point(2, 0): 0}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 1, tiles)

        origin = self.a_units[0]
        in_range, out_of_range = self.b_units[0:2]
        the_map.place_unit(origin, Point(0, 0))
        the_map.place_unit(in_range, Point(1, 0))
        the_map.place_unit(out_of_range, Point(2, 0))
        origin.equip_weapon(RangedWeapon(10, 10, 1, 1))

        tf = TargetFinder(the_map, [self.team_a, self.team_b])

        answer = tf.enemies_in_range(origin)
        expected = {
            in_range: (1, -1),
        }
        self.assertEqual(answer, expected)

    def test_enemies_in_range_by_weapon_range(self):
        origin = self.a_units[0]
        in_range, out_of_range = self.b_units[0:2]
        self.map.place_unit(origin, Point(0, 0))
        self.map.place_unit(in_range, Point(10, 0))
        self.map.place_unit(out_of_range, Point(11, 0))
        origin.equip_weapon(RangedWeapon(10, 10, 10, 10))
        tf = TargetFinder(self.map, [self.team_a, self.team_b])

        answer = tf.enemies_in_range(origin)
        expected = {
           in_range: (10, 0),
        }
        self.assertEqual(answer, expected)

        self.map.remove_unit(Point(10, 0))
        self.map.remove_unit(Point(11, 0))
        self.map.place_unit(in_range, Point(5, 5))
        self.map.place_unit(out_of_range, Point(5, 6))
        answer = tf.enemies_in_range(origin)
        self.assertEqual(answer, expected)

""" homeworkd:  DO THE TESTS FOR ALL FOUR range METHIDS"""



