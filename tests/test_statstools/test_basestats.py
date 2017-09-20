import unittest

from battle.statstools.basestats import stats_factory


class TestBaseStats(unittest.TestCase):
    def test_init_new_single_param_class_no_default_no_current_with_without_kwarg(self):
        TestStats = stats_factory('TestStats', ('a', None, False))

        tst = TestStats(3)
        self.assertEqual(tst.__dict__, {'_a': 3})

        tst = TestStats(a=3)
        self.assertEqual(tst.__dict__, {'_a': 3})

        self.assertEqual(TestStats.__name__, 'TestStats')

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
        Stats = stats_factory('Stats', ('a', None, True), ('b', 10, False), ('c', 100, False))






