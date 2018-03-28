import unittest

from battle.turn_execution.target_finder import TargetFinder


from battle.maptools.map import Map
from battle.players.units import Soldier
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

    def test_allies_in_sight_only_allies_at_correct_distance(self):
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

    def test_allies_in_sight_only_allies_in_sight_range(self):
        pass

    def test_allies_in_sight_only_allies_in_unobstructed_view(self):
        pass




