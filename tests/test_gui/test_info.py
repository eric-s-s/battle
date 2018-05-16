import unittest


from battle.maptools.map import Map
from battle.maptools.tile import Tile
from battle.maptools.point import Point

from battle.players.team import Team
from battle.players.units import Soldier

from gui.info import InformationRetrieval


class TestInformationRetrieval(unittest.TestCase):
    def test_oops(self):
        self.assertEqual(2, 2)

