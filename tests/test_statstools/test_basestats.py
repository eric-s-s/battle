import unittest

from battle.statstools.basestats import stats_factory, BaseStats


class TestBaseStats(unittest.TestCase):
    def test_init_new_single_param_class_no_default_no_current_with_without_kwarg(self):
        TestStats = stats_factory('TestStats', ('a', None, False))

        tst = TestStats(3)
        self.assertEqual(tst.__dict__, {'_a': 3})

        tst = TestStats(a=3)
        self.assertEqual(tst.__dict__, {'_a': 3})

        self.assertEqual(TestStats.__name__, 'TestStats')

        self.assertIsInstance(tst, BaseStats)

    def test_init_ignores_extra_params_and_kwargs_if_correct_one_provided(self):
        TestStats = stats_factory('TestStats', ('a', None, False))

        tst = TestStats(3, 10)
        self.assertEqual(tst.__dict__, {'_a': 3})

        tst = TestStats(a=3, b=10)
        self.assertEqual(tst.__dict__, {'_a': 3})

    def test_init_single_value_default(self):
        NoDefaultStats = stats_factory('NoDefaultStats', ('a', None, False))
        DefaultStats = stats_factory('DefaultStats', ('a', 100, False))

        with self.assertRaises(AttributeError):
            NoDefaultStats()

        self.assertEqual(DefaultStats().__dict__, {'_a': 100})

    def test_init_needs_current_value_set_to_true(self):
        Stats = stats_factory('Stats', ('a', None, True))
        self.assertEqual(Stats(5).__dict__, {'_a': 5, 'current_a': 5})

        DefaultStats = stats_factory('DefaultStats', ('a', 100, True))
        self.assertEqual(DefaultStats().__dict__, {'_a': 100, 'current_a': 100})

    def test_init_multiple_params(self):
        Stats = stats_factory('Stats', ('a', None, True), ('b', 10, False), ('c', 100, True))

        tst = Stats(a=3, b=6)
        self.assertEqual(tst.__dict__, {'_a': 3, 'current_a': 3, '_b': 6, '_c': 100, 'current_c': 100})

        tst = Stats(3, 6, 10)
        self.assertEqual(tst.__dict__, {'_a': 3, 'current_a': 3, '_b': 6, '_c': 10, 'current_c': 10})

        tst = Stats(a=3, c=10)
        self.assertEqual(tst.__dict__, {'_a': 3, 'current_a': 3, '_b': 10, '_c': 10, 'current_c': 10})

        tst = Stats(c=10, a=3, b=6)
        self.assertEqual(tst.__dict__, {'_a': 3, 'current_a': 3, '_b': 6, '_c': 10, 'current_c': 10})

    def test_init_WEIRD_CASE_COULD_BE_TROUBLE(self):
        Stats = stats_factory('Stats', ('a', None, True), ('b', 10, False), ('c', None, True))
        tst = Stats(3, c=6)
        self.assertEqual(tst.__dict__, {'_a': 3, 'current_a': 3, '_b': 10, '_c': 6, 'current_c': 6})

    def test_creates_property_getters_for_each_value(self):
        Stats = stats_factory('Stats', ('a', None, True), ('b', 10, False), ('c', 100, True))
        tst = Stats(2)
        self.assertEqual(tst.a, 2)
        self.assertEqual(tst.b, 10)
        self.assertEqual(tst.c, 100)
        with self.assertRaises(AttributeError):
            tst.a = 5
        with self.assertRaises(AttributeError):
            tst.b = 5
        with self.assertRaises(AttributeError):
            tst.c = 5

    def test_eq_against_similar_object_but_not_from_base_stats(self):
        class Stats(object):
            def __init__(self, a):
                self._a = a

        TrueStats = stats_factory('Stats', ('a', None, False))
        true_stats = TrueStats(3)
        false_stats = Stats(3)

        self.assertEqual(true_stats.__class__.__name__, false_stats.__class__.__name__)
        self.assertEqual(true_stats.__dict__, false_stats.__dict__)

        self.assertNotEqual(true_stats, false_stats)

    def test_eq_against_other_with_same_class_name_and_is_base_stats(self):
        Stats = stats_factory('Stats', ('a', None, True), ('b', 10, False), ('c', 100, True))
        OtherStats = stats_factory('Stats', ('a', None, True), ('b', 10, False), ('c', 100, True))

        stats = Stats(5)
        similar_stats = OtherStats(5)

        self.assertEqual(stats, similar_stats)
        self.assertEqual(stats.__dict__, similar_stats.__dict__)
        self.assertEqual(stats.__class__.__name__, similar_stats.__class__.__name__)

        self.assertNotEqual(stats.__class__, similar_stats.__class__)

    def test_eq_false_by_dict_value(self):
        Stats = stats_factory('Stats', ('a', None, True), ('b', 10, False), ('c', 100, True))

        stats = Stats(5)
        different_init = Stats(500)
        changed_value = Stats(5)
        changed_value.current_a = 50

        self.assertNotEqual(stats, different_init)
        self.assertNotEqual(stats, changed_value)

    def test_update_returns_new_instance_with_updated_value(self):
        Stats = stats_factory('Stats', ('a', None, True), ('b', 10, False))
        stats = Stats(5)
        new_stats = stats.update('b', -2)
        new_new_stats = new_stats.update('b', 1000)
        self.assertIsNot(stats, new_stats)
        self.assertIs(type(stats), Stats)
        self.assertIs(type(new_stats), Stats)
        self.assertIs(type(new_new_stats), Stats)
        self.assertEqual(stats.__dict__, {'_a': 5, '_b': 10, 'current_a': 5})
        self.assertEqual(new_stats.__dict__, {'_a': 5, '_b': -2, 'current_a': 5})
        self.assertEqual(new_new_stats.__dict__, {'_a': 5, '_b': 1000, 'current_a': 5})

    def test_update_also_reset_current_val(self):
        Stats = stats_factory('Stats', ('a', None, True), ('b', 10, False))
        stats = Stats(5)
        new_stats = stats.update('a', -2)
        self.assertEqual(new_stats.a, -2)
        self.assertEqual(new_stats.current_a, -2)

    def test_update_raises_attribute_error(self):
        Stats = stats_factory('Stats', ('a', None, True), ('b', 10, False))
        stats = Stats(5)
        self.assertRaises(AttributeError, stats.update, 'oops', 100)


