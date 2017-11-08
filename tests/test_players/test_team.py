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
        self.team = Team('test', self.map)

    def test_init(self):
        tiles = [Tile() for _ in range(9)]
        the_map = Map(3, 3, tiles)
        team = Team('test', the_map)
        self.assertEqual(team.players, set())
    def test_players_returns_a_copy(self):
        x = self.team.players
        x.add(123)
        self.assertEqual(self.team.players, set())

    def test_add_player(self):
        unit = Soldier()
        self.team.add_player(unit)
        self.assertEqual(self.team.players, {unit})

    def test_add_player_dupe(self):
        unit = Soldier()
        self.team.add_player(unit)
        self.team.add_player(unit)
        self.assertEqual(self.team.players, {unit})

    def test_add_player_multiple_players(self):
        unit = Soldier()
        unit_2 = Soldier()
        self.team.add_player(unit)
        self.team.add_player(unit_2)
        self.assertEqual(self.team.players, {unit, unit_2})

    def test_del_player(self):
        unit = Soldier()
        unit_2 = Soldier()
        self.team.add_player(unit)
        self.team.add_player(unit_2)
        self.team.del_player(unit)
        self.assertEqual(self.team.players, {unit_2})

    def test_del_player_not_in_team(self):
        unit = Soldier()
        self.assertRaises(ValueError, self.team.del_player, unit)

    def test_is_on_team_true(self):
        unit = Soldier()
        self.team.add_player(unit)
        self.assertTrue(self.team.is_on_team(unit))

    def test_is_on_team_false(self):
        unit = Soldier()
        self.team.add_player(unit)
        self.assertFalse(self.team.is_on_team(Soldier()))

    def test_coordinates_units_not_on_map(self):
        unit = Soldier()
        unit_2 = Soldier()
        self.team.add_player(unit)
        self.team.add_player(unit_2)
        self.assertEqual(self.team.coordinates(), {unit: None, unit_2: None})

    def test_coordinates_units_on_map(self):
        unit = Soldier()
        unit_2 = Soldier()
        self.team.add_player(unit)
        self.team.add_player(unit_2)
        self.map.place_unit(unit, Point(0, 0))
        self.map.place_unit(unit_2, Point(0, 1))
        self.assertEqual(self.team.coordinates(), {unit: Point(0, 0), unit_2: Point(0, 1)})

