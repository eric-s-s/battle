import unittest

from battle.weapon import Weapon


class TestWeapon(unittest.TestCase):
    def test_init(self):
        new = Weapon(1, 2)
        self.assertEqual(new.atk_dmg, 1)
        self.assertEqual(new.range, 2)

    def test_init_with_negative_atk_dmg(self):
        self.assertRaises(ValueError, Weapon, -1, 1)

    def test_init_with_zero_atk_dmg(self):
        self.assertRaises(ValueError, Weapon, 0, 1)

    def test_init_with_negative_range(self):
        self.assertRaises(ValueError, Weapon, 1, -1)

    def test_init_with_zero_range(self):
        new = Weapon(1, 0)
        self.assertEqual(new.range, 0)

