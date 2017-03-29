from tests.test_base_unit import TestBaseUnit
from battle.units import Soldier, FIST
from battle.weapon import Weapon


class TestSoldier(TestBaseUnit):

    def setUp(self):
        self.unit = Soldier()

    def test_init_default_settings(self):
        self.assertIs(self.unit.get_weapon(), FIST)
        self.assertEqual(self.unit.get_health(), 100)

    def test_equip_weapon(self):
        stick = Weapon(3, 2)
        self.unit.equip_weapon(stick)
        self.assertEqual(self.unit.get_weapon(), stick)

    def test_receive_dmg(self):
        self.unit.receive_dmg(99)
        self.assertEqual(self.unit.get_health(), 1)

        self.unit.receive_dmg(2)
        self.assertEqual(self.unit.get_health(), -1)

        self.unit.receive_dmg(0)
        self.assertEqual(self.unit.get_health(), -1)

    def test_receive_dmg_negative_number_raises_value_error(self):
        self.assertRaises(ValueError, self.unit.receive_dmg, -10)

    def test_attack(self):
        opponent = Soldier()
        self.assertEqual(self.unit.get_weapon().atk_dmg, 1)

        self.unit.attack(opponent)
        self.assertEqual(opponent.get_health(), 99)

        self.unit.attack(opponent)
        self.assertEqual(opponent.get_health(), 98)

    def test_attack_with_different_weapon(self):
        opponent = Soldier()
        self.unit.equip_weapon(Weapon(10, 1))
        self.assertEqual(self.unit.get_weapon().atk_dmg, 10)

        self.unit.attack(opponent)
        self.assertEqual(opponent.get_health(), 90)

        self.unit.attack(opponent)
        self.assertEqual(opponent.get_health(), 80)

    def test_is_dead_true(self):
        self.unit.receive_dmg(self.unit.get_health())
        self.assertTrue(self.unit.is_dead())

        self.unit.receive_dmg(1)
        self.assertTrue(self.unit.is_dead())

    def test_is_dead_false(self):
        self.assertFalse(self.unit.is_dead())

        self.unit.receive_dmg(self.unit.get_health() - 1)
        self.assertFalse(self.unit.is_dead())





