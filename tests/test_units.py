from tests.test_base_unit import TestBaseUnit
from battle.units import Soldier, FIST


class TestSoldier(TestBaseUnit):


    def setUp(self):
        self.unit = Soldier()

    def test_weapon_is_fist(self):
        """
                bad test.  cannot access private properties
                """
        self.assertIs(self.unit._weapon, FIST)

