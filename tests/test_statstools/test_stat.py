import unittest


from battle.statstools.stat import Stat, PositiveStat


class TestStat(unittest.TestCase):

    def test_init_and_getters(self):
        stat = Stat(3)
        self.assertEqual(stat.max, 3)
        self.assertEqual(stat.static_max, 3)
        self.assertEqual(stat.current, 3)

    def test_init_and_getter_negative(self):
        neg = Stat(-3)
        self.assertEqual(neg.max, -3)
        self.assertEqual(neg.static_max, -3)
        self.assertEqual(neg.current, -3)

    def test_init_and_getter_zero(self):
        zero = Stat(0)
        self.assertEqual(zero.max, 0)
        self.assertEqual(zero.static_max, 0)
        self.assertEqual(zero.current, 0)

    def test_modifier_changes_max_and_not_static_max(self):
        stat = Stat(3)
        stat.modifier(4)
        self.assertEqual(stat.max, 7)
        self.assertEqual(stat.static_max, 3)

        stat.modifier(-10)
        self.assertEqual(stat.max, -7)
        self.assertEqual(stat.static_max, 3)

    def test_modify_current(self):
        stat = Stat(3)

        stat.modify_current(-2)
        self.assertEqual(stat.current, 1)
        self.assertEqual(stat.max, 3)

        stat.modify_current(-2)
        self.assertEqual(stat.current, -1)
        self.assertEqual(stat.max, 3)

    def test_modify_current_maxes_out_at_max_and_not_static_max(self):
        stat = Stat(1)
        stat.modifier(2)
        self.assertEqual(stat.max, 3)
        self.assertEqual(stat.static_max, 1)

        stat.modify_current(2)
        self.assertEqual(stat.current, 3)

        stat.modify_current(-2)
        self.assertEqual(stat.current, 1)

        stat.modify_current(100)
        self.assertEqual(stat.current, 3)

    def test_modifier_reduce_current_if_too_big(self):
        stat = Stat(3)
        self.assertEqual(stat.current, 3)
        stat.modifier(-1)
        self.assertEqual(stat.current, 2)
        stat.modify_current(-1)
        self.assertEqual(stat.current, 1)
        stat.modifier(-3)
        self.assertEqual(stat.current, 0)

    def test_modifier_does_not_reduce_current_if_not_too_big(self):
        stat = Stat(3)
        stat.modify_current(-3)
        self.assertEqual(stat.current, 0)
        stat.modifier(-2)
        self.assertEqual(stat.max, 1)
        self.assertEqual(stat.current, 0)

    def test_hard_reset_resets_everything(self):
        stat = Stat(3)
        stat.modifier(10)
        stat.modify_current(-3)
        stat.hard_reset()
        self.assertEqual(stat.max, 3)
        self.assertEqual(stat.static_max, 3)
        self.assertEqual(stat.current, 3)

    def test_reset_resets_current_to_max(self):
        stat = Stat(3)
        stat.modify_current(-3)
        stat.modifier(3)
        self.assertEqual(stat.max, 6)
        self.assertEqual(stat.current, 0)
        stat.reset()
        self.assertEqual(stat.max, 6)
        self.assertEqual(stat.current, 6)

    # TODO test with subclass
    def test_adjust(self):
        stat = Stat(3)
        new = stat.adjust(3)
        self.assertIsNot(stat, new)
        self.assertEqual(new.max, 6)
        self.assertEqual(new.static_max, 6)
        self.assertEqual(new.current, 6)

    def test_PositiveStat_init(self):
        stat = PositiveStat(-3)
        self.assertEqual(stat.static_max, 0)
        self.assertEqual(stat.max, 0)
        self.assertEqual(stat.current, 0)

        stat = PositiveStat(3)
        self.assertEqual(stat.current, 3)
        self.assertEqual(stat.max, 3)
        self.assertEqual(stat.static_max, 3)

    def test_PositiveStat_modify_current(self):
        stat = PositiveStat(3)
        stat.modify_current(1)
        self.assertEqual(stat.current, 3)

        stat.modify_current(-2)
        self.assertEqual(stat.current, 1)

        stat.modify_current(-2)
        self.assertEqual(stat.current, 0)

    def test_PositiveStat_modifier(self):
        stat = PositiveStat(3)
        stat.modifier(2)
        self.assertEqual(stat.max, 5)

        stat.modifier(-1)
        self.assertEqual(stat.max, 2)

        stat.modifier(-4)
        self.assertEqual(stat.max, 0)

    def test_PositiveStat_current_relies_max(self):
        stat = PositiveStat(3)
        stat.modifier(-100)
        self.assertEqual(stat.max, 0)
        self.assertEqual(stat.current, 0)

    def test_infinite_stat(self):
        inf = float('inf')
        stat = Stat(inf)
        stat.modifier(-100)
        self.assertEqual(stat.max, inf)
        self.assertEqual(stat.current, inf)

        stat.modify_current(-100)
        self.assertEqual(stat.current, inf)

        stat = PositiveStat(inf)
        stat.modifier(-100)
        self.assertEqual(stat.max, inf)
        self.assertEqual(stat.current, inf)

        stat.modify_current(-100)
        self.assertEqual(stat.current, inf)

    def test_neg_infinite_stat(self):
        neg_inf = float('-inf')
        stat = Stat(neg_inf)
        stat.modifier(-100)
        self.assertEqual(stat.max, neg_inf)
        self.assertEqual(stat.current, neg_inf)

        stat.modify_current(-100)
        self.assertEqual(stat.current, neg_inf)

        stat = PositiveStat(neg_inf)
        stat.modifier(-100)
        self.assertEqual(stat.max, 0)
        self.assertEqual(stat.current, 0)

        stat.modify_current(-100)
        self.assertEqual(stat.current, 0)


