import unittest

from battle.players.action import Action


class TestAction(unittest.TestCase):
    def test_all_members(self):
        all_members = ~Action.NULL
        self.assertEqual(all_members, (
            Action.GO |
            Action.STAY |
            Action.ATTACK |
    
            Action.ENEMY |
            Action.ALLY |
    
            Action.NEAREST |
            Action.FURTHEST |
    
            Action.STRONGEST |
            Action.WEAKEST |
    
            Action.HIGHEST |
            Action.LOWEST |
    
            Action.HEALTH |
            Action.WEAPON |
            Action.CONCENTRATION |
    
            Action.OPPORTUNITY |
            Action.DANGER |
    
            Action.TOWARDS |
            Action.AWAY
        ))

    def test_bool(self):
        for action in Action.to_list():
            self.assertTrue(bool(action|Action.STAY))
            if action == Action.NULL:
                self.assertFalse(bool(action))
            else:
                self.assertTrue(bool(action))

    def test_null_or(self):
        for action in Action.to_list():
            self.assertEqual(Action.NULL|action, action)

    def test_null_and(self):
        for action in Action.to_list():
            self.assertEqual(Action.NULL&action, Action.NULL)

    def test_has_any_other_is_one_value(self):
        test = Action.ENEMY|Action.DANGER
        self.assertTrue(test.has_any(Action.DANGER))
        self.assertTrue(test.has_any(Action.ENEMY))
        self.assertFalse(test.has_any(Action.ATTACK))

    def test_has_any_other_is_two_value(self):
        test = Action.ENEMY|Action.DANGER
        self.assertTrue(test.has_any(Action.DANGER|Action.ENEMY))
        self.assertTrue(test.has_any(Action.ENEMY|Action.ALLY))
        self.assertFalse(test.has_any(Action.ATTACK|Action.ALLY))

    def test_has_only_other_is_one_value(self):
        test = Action.ENEMY
        self.assertTrue(test.has_only(Action.ENEMY))

        self.assertFalse(test.has_only(Action.DANGER))
        self.assertFalse(test.has_only(Action.ATTACK))

    def test_has_only_other_is_two_value(self):
        test = Action.ENEMY|Action.DANGER
        self.assertTrue(test.has_only(Action.DANGER|Action.ENEMY))

        self.assertFalse(test.has_only(Action.ENEMY|Action.ALLY))
        self.assertFalse(test.has_only(Action.ATTACK|Action.ALLY))

    def test_has_only_test_value_has_more_than_other(self):
        test = Action.ENEMY | Action.DANGER
        self.assertFalse(test.has_only(Action.ENEMY))

    def test_has_at_least_other_is_one_value_true(self):
        other = Action.ENEMY
        self.assertTrue(other.has_at_least(other))
        self.assertTrue((other|Action.ALLY).has_at_least(other))
        self.assertTrue((other|Action.ALLY|Action.GO).has_at_least(other))

    def test_has_at_least_other_is_one_value_false(self):
        other = Action.ENEMY
        self.assertFalse(Action.ATTACK.has_at_least(other))
        self.assertFalse((Action.ATTACK | Action.ALLY).has_at_least(other))
        self.assertFalse((Action.ATTACK | Action.ALLY | Action.GO).has_at_least(other))

    def test_has_at_least_other_is_two_value_true(self):
        other = Action.ENEMY|Action.HEALTH
        self.assertTrue(other.has_at_least(other))
        self.assertTrue((other|Action.ALLY).has_at_least(other))
        self.assertTrue((other|Action.ALLY|Action.GO).has_at_least(other))

    def test_has_at_least_other_is_two_value_false(self):
        other = Action.ENEMY|Action.HEALTH
        self.assertFalse(Action.HEALTH.has_at_least(other))
        self.assertFalse((Action.HEALTH | Action.ALLY).has_at_least(other))
        self.assertFalse((Action.HEALTH | Action.ALLY | Action.GO).has_at_least(other))
        self.assertFalse((Action.LOWEST | Action.ALLY | Action.GO).has_at_least(other))

    def test_to_list(self):
        answer = [
            Action.ALLY,
            Action.ATTACK,
            Action.AWAY,
            Action.CONCENTRATION,
            Action.DANGER,
            Action.ENEMY,
            Action.FURTHEST,
            Action.GO,
            Action.HEALTH,
            Action.HIGHEST,
            Action.LOWEST,
            Action.NEAREST,
            Action.NULL,
            Action.OPPORTUNITY,
            Action.STAY,
            Action.STRONGEST,
            Action.TOWARDS,
            Action.WEAKEST,
            Action.WEAPON
        ]
        self.assertEqual(answer, Action.to_list())
        