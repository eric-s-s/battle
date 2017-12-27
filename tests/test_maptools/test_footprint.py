import unittest

from battle.maptools.footprint import FootPrint, Token, FootPrintPackage
from battle.maptools.direction import Direction
from battle.players.team import Team
from battle.maptools.point import Point
from battle.players.units import Soldier
from battle.maptools.map import Map
from battle.maptools.tile import Tile


class TestFootPrint(unittest.TestCase):
    def setUp(self):
        tiles = [Tile() for _ in range(25)]
        self.map = Map(5, 5, tiles)
        self.team_1 = Team(Point(1, 1), self.map)
        self.team_2 = Team(Point(0, 2), self.map)
        self.team_3 = Team(Point(4, 2), self.map)

    def test_token(self):
        """
                 DEAD = (2, 0)
                 DANGER = (1, 0)
                 NEUTRAL = (0, 0)
                 OBJECTIVE = (0, 1)
                 ATTACKING = (1, 2)
                """
        token_list = [Token.DEAD, Token.DANGER, Token.NEUTRAL, Token.OBJECTIVE, Token.ATTACKING]
        values_list = [(2, 0), (1, 0), (0, 0), (0, 1), (1, 2)]
        for token, value in zip(token_list, values_list):
            self.assertEqual(token.value, value)
        self.assertEqual(len(list(Token.__members__)), len(token_list))

    def test_footprint_init(self):
        footprint_1 = FootPrint(Token.DEAD, Direction.N, self.team_1)
        self.assertEqual(footprint_1.token, Token.DEAD)
        self.assertEqual(footprint_1.direction, Direction.N)
        self.assertEqual(footprint_1.team, self.team_1)

    def test_FootPrintPackage_default_init(self):
        fpp = FootPrintPackage()
        self.assertEqual(fpp.footprints, [])
        self.assertEqual(fpp._stack.maxlen, 10)

    def test_FootPrintPackage_init(self):
        fpp = FootPrintPackage(11)
        self.assertEqual(fpp.footprints, [])
        self.assertEqual(fpp._stack.maxlen, 11)

    def test_FootPrintPackage_push(self):
        fpp = FootPrintPackage()
        fp_1 = FootPrint(Token.DANGER, Direction.W, self.team_2)
        fp_2 = FootPrint(Token.NEUTRAL, Direction.N, self.team_3)
        fpp.push(fp_1)
        self.assertEqual(fpp.footprints, [fp_1])
        fpp.push(fp_2)
        self.assertEqual(fpp.footprints, [fp_2, fp_1])

    def test_FootPrintPackage_push_greater_than_max_size_one(self):
        fpp = FootPrintPackage(1)
        fp_1 = FootPrint(Token.DANGER, Direction.W, self.team_2)
        fp_2 = FootPrint(Token.NEUTRAL, Direction.N, self.team_3)
        fp_3 = FootPrint(Token.OBJECTIVE, Direction.S, self.team_1)
        fpp.push(fp_1)
        fpp.push(fp_2)
        self.assertEqual(fpp.footprints, [fp_2])
        fpp.push(fp_3)
        self.assertEqual(fpp.footprints, [fp_3])

    def test_FootPrintPackage_push_greater_than_max_size_two(self):
        fpp = FootPrintPackage(2)
        fp_1 = FootPrint(Token.DANGER, Direction.W, self.team_2)
        fp_2 = FootPrint(Token.NEUTRAL, Direction.N, self.team_3)
        fp_3 = FootPrint(Token.OBJECTIVE, Direction.S, self.team_1)
        fpp.push(fp_1)
        fpp.push(fp_2)
        self.assertEqual(fpp.footprints, [fp_2, fp_1])
        fpp.push(fp_3)
        self.assertEqual(fpp.footprints, [fp_3, fp_2])

    """write tests of what you want this stuff to do, and comment them out. Then, if you have time,
    write the code, uncommenting tests as you go."""
