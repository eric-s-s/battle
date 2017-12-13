from battle.players.team import Team
from battle.players.units import Soldier
from battle.maptools.map import Map
from battle.maptools.tile import Tile
from battle.maptools.point import Point
import unittest


class TestTeam(unittest.TestCase):
    def setUp(self):
        tiles = [Tile() for _ in range(9)]
        self.map = Map(3, 3, tiles)
        self.team = Team(Point(1, 1), self.map)

    def test_init(self):
        tiles = [Tile() for _ in range(9)]
        the_map = Map(3, 3, tiles)
        team = Team(Point(0, 0), the_map)
        self.assertEqual(team.deployed, [])
        self.assertEqual(team.undeployed, [])
        self.assertEqual(team.home, Point(0, 0))

    def test_deployed_and_undeployed_returns_a_copy(self):
        x = self.team.undeployed
        x.append(123)
        self.assertEqual(self.team.undeployed, [])
        x = self.team.deployed
        x.append(123)
        self.assertEqual(self.team.deployed, [])

    def test_add_player(self):
        unit = Soldier()
        self.team.add_player(unit)
        self.assertEqual(self.team.undeployed, [unit])

    def test_add_player_dupe(self):
        unit = Soldier()
        self.team.add_player(unit)
        self.team.add_player(unit)
        self.assertEqual(self.team.undeployed, [unit])

    def test_add_player_multiple_players(self):
        unit = Soldier()
        unit_2 = Soldier()
        self.team.add_player(unit)
        self.team.add_player(unit_2)
        self.assertEqual(self.team.undeployed, [unit, unit_2])

    def test_unteam_player_undeployed(self):
        unit = Soldier()
        unit_2 = Soldier()
        self.team.add_player(unit)
        self.team.add_player(unit_2)
        self.team.unteam_player(unit)
        self.assertEqual(self.team.undeployed, [unit_2])

    def test_unteam_player_deployed(self):
        unit = Soldier()
        unit_2 = Soldier()
        self.team.add_player(unit)
        self.team.add_player(unit_2)
        self.team.spawn()
        self.team.spawn()
        self.team.unteam_player(unit)
        self.assertEqual(self.team.deployed, [unit_2])

    def test_unteam_player_not_in_team(self):
        unit = Soldier()
        self.assertRaises(ValueError, self.team.unteam_player, unit)

    def test_is_on_team_true(self):
        unit = Soldier()
        self.team.add_player(unit)
        self.assertTrue(self.team.is_on_team(unit))
        self.team.spawn()
        self.assertTrue(self.team.is_on_team(unit))

    def test_is_on_team_false(self):
        unit = Soldier()
        self.team.add_player(unit)
        self.assertFalse(self.team.is_on_team(Soldier()))

    def test_spawn(self):
        units = [Soldier(), Soldier(), Soldier()]
        for soldier in units:
            self.team.add_player(soldier)
        for _ in range(3):
            self.team.spawn()
        self.assertEqual(self.map.get_unit(Point(1, 0)), units[0])
        self.assertEqual(self.map.get_unit(Point(0, 1)), units[1])
        self.assertEqual(self.map.get_unit(Point(2, 1)), units[2])

        self.assertRaises(ValueError, self.team.spawn)

    def test_spawn_uses_undeployed_as_a_queue(self):
        units = [Soldier(), Soldier(), Soldier()]
        for soldier in units:
            self.team.add_player(soldier)
        self.assertEqual(self.team.undeployed, units)

        self.team.spawn()
        self.assertEqual(self.team.undeployed, units[1:])
        self.assertEqual(self.team.deployed, units[0:1])

        self.team.spawn()
        self.assertEqual(self.team.undeployed, units[2:])
        self.assertEqual(self.team.deployed, units[0:2])

        self.team.spawn()
        self.assertEqual(self.team.undeployed, [])
        self.assertEqual(self.team.deployed, units)

    def test_spawn_no_unplaced_players(self):
        unit = Soldier()
        self.team.add_player(unit)
        self.team.spawn()
        self.assertRaises(ValueError, self.team.spawn)

    def test_spawn_no_room_on_map(self):
        units = [Soldier() for _ in range(10)]
        for soldier in units:
            self.team.add_player(soldier)
        for _ in range(8):
            self.team.spawn()
        self.assertRaises(ValueError, self.team.spawn)

    def test_spawn_with_obstacles_at_distance_one(self):
        obstacles = self.team.home.at_distance(1)
        for point in obstacles:
            self.map.place_unit(Soldier(), point)

        units = [Soldier() for _ in range(3)]
        for soldier in units:
            self.team.add_player(soldier)
        for _ in range(len(units)):
            self.team.spawn()
        print(self.team.home.at_distance(1))
        print(self.team.home.at_distance(2))
        expected_points = [Point(0, 0), Point(2, 0), Point(0, 2)]
        for soldier, point in zip(units, expected_points):
            self.assertEqual(self.map.get_unit(point), soldier)

    def test_spawn_with_obstacles_some_at_distance_one_and_some_at_distance_two(self):
        obstacles = [Point(1, 0), Point(0, 1), Point(0, 0), Point(2, 2)]
        for point in obstacles:
            self.map.place_unit(Soldier(), point)

        units = [Soldier() for _ in range(3)]
        for soldier in units:
            self.team.add_player(soldier)
        for _ in range(len(units)):
            self.team.spawn()

        expected_points = [Point(2, 1), Point(1, 2), Point(2, 0)]
        for soldier, point in zip(units, expected_points):
            self.assertEqual(self.map.get_unit(point), soldier)

    def test_spawn_return_value(self):
        unit = Soldier()
        self.team.add_player(unit)
        self.assertEqual(self.team.spawn(), (unit, Point(1, 0)))
