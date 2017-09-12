import unittest

from battle.weapon import Weapon, MeleeWeapon, RangedWeapon, WeaponStats, OutOfAmmo


class TestWeapon(unittest.TestCase):
    def setUp(self):
        self.ranged = RangedWeapon(dmg=3, action_pts=4, range_=5, max_ammo=5)
        self.melee = MeleeWeapon(dmg=4, action_pts=2)

    def test_init(self):
        new = Weapon(dmg=2, action_pts=3, range_=4, max_ammo=5, ranged=True)
        stats = WeaponStats(dmg=2, action_pts=3, range=4, max_ammo=5, ammo=5)
        self.assertEqual(new.get_stats(), stats)
        self.assertEqual(new.is_ranged, True)

    def test_init_with_bad_negative_values(self):
        self.assertRaises(ValueError, Weapon, -1, 1, 1, 1, True)
        self.assertRaises(ValueError, Weapon, 1, -1, 1, 1, True)
        self.assertRaises(ValueError, Weapon, 1, 1, -1, 1, True)

    def test_init_with_bad_zero_values(self):
        self.assertRaises(ValueError, Weapon, 0, 1, 1, 1, True)
        self.assertRaises(ValueError, Weapon, 1, 0, 1, 1, True)
        self.assertRaises(ValueError, Weapon, 1, 1, 0, 1, True)

    def test_use_weapon_inf_ammo(self):
        dmg = self.melee.use_weapon()
        self.assertEqual(dmg, 4)
        self.assertEqual(self.melee.get_stats().ammo, float('inf'))

    def test_use_weapon_non_inf_ammo(self):
        self.assertEqual(self.ranged.get_stats().ammo, 5)
        self.assertEqual(self.ranged.use_weapon(), 3)
        self.assertEqual(self.ranged.get_stats().ammo, 4)

    def test_use_weapon_no_ammo(self):
        for _ in range(5):
            self.ranged.use_weapon()

        self.assertRaises(OutOfAmmo, self.ranged.use_weapon)

    def test_refill_ammo_inf(self):
        self.melee.use_weapon()
        self.melee.refill_ammo()
        self.assertEqual(self.melee.get_stats().ammo, float('inf'))

    def test_refill_ammo_not_inf(self):
        self.ranged.use_weapon()
        self.ranged.refill_ammo()
        self.assertEqual(self.ranged.get_stats().ammo, 5)

        for _ in range(5):
            self.ranged.use_weapon()

        self.ranged.refill_ammo()
        self.assertEqual(self.ranged.get_stats().ammo, 5)

    def test_melee_init_defaults(self):
        new = MeleeWeapon(2, 3)
        stats = WeaponStats(dmg=2, action_pts=3, range=1, max_ammo=float('inf'), ammo=float('inf'))
        self.assertEqual(new.get_stats(), stats)
        self.assertFalse(new.is_ranged)

    def test_melee_init_no_defaults(self):
        new = MeleeWeapon(2, 3, 4, 5)
        stats = WeaponStats(dmg=2, action_pts=3, range=4, max_ammo=5, ammo=5)
        self.assertEqual(new.get_stats(), stats)
        self.assertFalse(new.is_ranged)

    def test_ranged_init(self):
        new = RangedWeapon(1, 2, 3, 4)
        stats = WeaponStats(dmg=1, action_pts=2, range=3, max_ammo=4, ammo=4)
        self.assertEqual(new.get_stats(), stats)
        self.assertTrue(new.is_ranged)
