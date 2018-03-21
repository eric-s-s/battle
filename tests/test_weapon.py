import unittest

from battle.weapon import Weapon, MeleeWeapon, RangedWeapon, OutOfAmmo


class TestWeapon(unittest.TestCase):
    def setUp(self):
        self.ranged = RangedWeapon(dmg=3, action_pts=4, range_=5, ammo=5)
        self.melee = MeleeWeapon(dmg=4, action_pts=2)

    def test_init_and_getters(self):
        new = Weapon(dmg=2, action_pts=3, range_=4, ammo=5)
        self.assertEqual(new.ammo, 5)
        self.assertEqual(new.max_ammo, 5)
        self.assertEqual(new.dmg, 2)
        self.assertEqual(new.action_pts, 3)
        self.assertEqual(new.range, 4)

    def test_use_weapon_inf_ammo(self):
        dmg = self.melee.use_weapon()
        self.assertEqual(dmg, 4)
        self.assertEqual(self.melee.ammo, float('inf'))

    def test_use_weapon_non_inf_ammo(self):
        self.assertEqual(self.ranged.ammo, 5)
        self.assertEqual(self.ranged.use_weapon(), 3)
        self.assertEqual(self.ranged.ammo, 4)

    def test_use_weapon_no_ammo(self):
        for _ in range(5):
            self.ranged.use_weapon()

        self.assertRaises(OutOfAmmo, self.ranged.use_weapon)

    def test_refill_ammo_inf(self):
        self.melee.use_weapon()
        self.melee.refill_ammo()
        self.assertEqual(self.melee.ammo, float('inf'))

    def test_refill_ammo_not_inf(self):
        self.ranged.use_weapon()
        self.ranged.refill_ammo()
        self.assertEqual(self.ranged.ammo, 5)

        for _ in range(5):
            self.ranged.use_weapon()

        self.ranged.refill_ammo()
        self.assertEqual(self.ranged.ammo, 5)

    def test_melee_init_defaults(self):
        new = MeleeWeapon(2, 3)
        self.assertEqual(new.dmg, 2)
        self.assertEqual(new.action_pts, 3)
        self.assertEqual(new.range, 1)
        self.assertEqual(new.ammo, float('inf'))

    def test_melee_init_no_defaults(self):
        new = MeleeWeapon(2, 3, 4, 5)
        self.assertEqual(new.dmg, 2)
        self.assertEqual(new.action_pts, 3)
        self.assertEqual(new.range, 4)
        self.assertEqual(new.ammo, 5)

    def test_ranged_init(self):
        new = RangedWeapon(2, 3, 4, 5)
        self.assertEqual(new.dmg, 2)
        self.assertEqual(new.action_pts, 3)
        self.assertEqual(new.range, 4)
        self.assertEqual(new.ammo, 5)

    def test_is_melee_weapon(self):
        melee = MeleeWeapon(1, 2, 3)
        ranged = RangedWeapon(2, 3, 4, 5)
        self.assertTrue(melee.is_melee_weapon())
        self.assertFalse(ranged.is_melee_weapon())
