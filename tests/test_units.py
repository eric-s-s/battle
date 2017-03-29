from tests.test_base_unit import TestBaseUnit
from battle.units import Soldier, FIST
from battle.weapon import Weapon


class TestSoldier(TestBaseUnit):

    def setUp(self):
        self.unit = Soldier()

    def test_weapon_is_fist(self):
        """
                bad test.  cannot access private properties
                """
        self.assertIs(self.unit.get_weapon(), FIST)

    def test_equip_weapon(self):
        stick = Weapon(3, 2)
        self.unit.equip_weapon(stick)
        self.assertEqual(self.unit.get_weapon(), stick)

    def test_receive_dmg(self):
        self.unit.receive_dmg(99)



