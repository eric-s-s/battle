import unittest
from battle.units import Soldier, FIST, GUN
from battle.weapon import MeleeWeapon


class TestSoldier(unittest.TestCase):

    def setUp(self):
        self.soldier = Soldier()

    def test_init_default_settings(self):
        self.assertIs(self.soldier.get_weapon(), FIST)
        self.assertEqual(self.soldier.get_health(), 100)
        self.assertEqual(self.soldier.get_action_points(), 3)
        self.assertEqual(self.soldier._healing_pct, 5.0)

    def test_init_set_parameters(self):
        unit = Soldier(5, 200, 10.0)
        self.assertEqual(unit.get_health(), 200)
        self.assertEqual(unit.get_action_points(), 5)
        self.assertEqual(unit._healing_pct, 10.0)

    def test_get_perimeter_size(self):
        unit = Soldier()
        self.assertEqual(unit.get_perimeter_size(), 1)
        unit.equip_weapon(GUN)
        self.assertEqual(unit.get_perimeter_size(), 5)

    def test_equip_weapon(self):
        stick = MeleeWeapon(3, 2)
        self.soldier.equip_weapon(stick)
        self.assertEqual(self.soldier.get_weapon(), stick)

    def test_receive_dmg(self):
        self.soldier.receive_dmg(99)
        self.assertEqual(self.soldier.get_health(), 1)

        self.soldier.receive_dmg(2)
        self.assertEqual(self.soldier.get_health(), -1)

        self.soldier.receive_dmg(0)
        self.assertEqual(self.soldier.get_health(), -1)

    def test_receive_dmg_negative_number_raises_value_error(self):
        self.assertRaises(ValueError, self.soldier.receive_dmg, -10)

    def test_attack(self):
        opponent = Soldier()
        self.assertEqual(self.soldier.get_weapon().stats.dmg, 1)

        self.soldier.attack(opponent)
        self.assertEqual(opponent.get_health(), 99)

        self.soldier.attack(opponent)
        self.assertEqual(opponent.get_health(), 98)

    def test_attack_with_different_weapon(self):
        opponent = Soldier()
        new_weapon = MeleeWeapon(10, 1)
        self.soldier.equip_weapon(new_weapon)
        self.assertEqual(self.soldier.get_weapon().stats.dmg, 10)

        self.soldier.attack(opponent)
        self.assertEqual(opponent.get_health(), 90)

        self.soldier.attack(opponent)
        self.assertEqual(opponent.get_health(), 80)

    def test_attack_uses_ammo_and_action_points(self):
        opponent = Soldier()
        self.soldier.equip_weapon(GUN)
        self.assertEqual(self.soldier.get_weapon().stats.current_ammo, 10)
        self.assertEqual(self.soldier.get_weapon().stats.action_pts, 2)
        self.assertEqual(self.soldier.get_action_points(), 3)

        self.soldier.attack(opponent)

        self.assertEqual(self.soldier.get_weapon().stats.current_ammo, 9)
        self.assertEqual(self.soldier.get_action_points(), 1)

    # TODO test attack losing ammo, test attack out of ammo, test attack uses action points

    def test_is_dead_true(self):
        self.soldier.receive_dmg(self.soldier.get_health())
        self.assertTrue(self.soldier.is_dead())

        self.soldier.receive_dmg(1)
        self.assertTrue(self.soldier.is_dead())

    def test_is_dead_false(self):
        self.assertFalse(self.soldier.is_dead())

        self.soldier.receive_dmg(self.soldier.get_health() - 1)
        self.assertFalse(self.soldier.is_dead())

    def test_heal_lt_max_health(self):
        self.soldier.receive_dmg(2)
        self.soldier.heal(0)
        self.soldier.heal(1)
        self.assertEqual(self.soldier.get_health(), 99)

    def test_heal_eq_max_health(self):
        self.soldier.receive_dmg(2)
        self.soldier.heal(2)
        self.assertEqual(self.soldier.get_health(), 100)

    def test_heal_gt_max_health(self):
        self.soldier.receive_dmg(2)
        self.soldier.heal(3)
        self.assertEqual(self.soldier.get_health(), 100)

    def test_heal_dead_person(self):
        self.soldier.receive_dmg(120)
        self.soldier.heal(100)
        self.assertEqual(self.soldier.get_health(), -20)

    def test_heal_neg_health(self):
        self.assertRaises(ValueError, self.soldier.heal, -1)

    def test_can_move(self):
        self.assertTrue(self.soldier.can_move(3))
        self.assertTrue(self.soldier.can_move(0))
        self.assertFalse(self.soldier.can_move(4))

    def test_can_move_dead(self):
        self.soldier.receive_dmg(1000)
        self.assertFalse(self.soldier.can_move(0))

    def test_move(self):
        self.soldier.move(2)
        self.assertEqual(self.soldier.get_action_points(), 1)
        self.soldier.reset_move_points()

    def test_reset_move(self):
        self.soldier.move(2)
        self.soldier.reset_move_points()
        self.assertEqual(self.soldier.get_action_points(), 3)

    def test_rest_alive(self):
        self.soldier.move(2)
        self.soldier.receive_dmg(6)
        self.soldier.rest()
        self.assertEqual(self.soldier.get_action_points(), 3)
        self.assertEqual(self.soldier.get_health(), 99)

    def test_rest_dead(self):
        self.soldier.move(2)
        self.soldier.receive_dmg(1000)
        self.soldier.rest()
        self.assertEqual(self.soldier.get_action_points(), 3)
        self.assertEqual(self.soldier.get_health(), -900)




