import unittest

from battle.base_unit import BaseUnit
from battle.maptools.point import Point
from battle.map import Map

class TestBaseUnit(unittest.TestCase):

    def setUp(self):
        self.unit = BaseUnit()

    def test_unit_inits_with_no_point(self):
        self.assertFalse(self.unit.has_point())

    def test_get_point_is_none(self):
        self.assertIsNone(self.unit.get_point())

    def test_get_point_is_point(self):
        point = Point(0, 0)
        self.unit.set_point(point)

        self.assertEqual(self.unit.get_point(), Point(0, 0))

    def test_has_point_false(self):
        self.assertFalse(self.unit.has_point())

    def test_has_point_true(self):
        point = Point(1, 1)
        self.unit.set_point(point)
        self.assertTrue(self.unit.has_point())

    def test_set_point_sets_point(self):
        pt1 = Point(2, 2)
        pt2 = Point(3, 3)

        self.unit.set_point(pt1)
        self.assertEqual(self.unit.get_point(), pt1)

        self.unit.set_point(pt2)
        self.assertEqual(self.unit.get_point(), pt2)

    def test_del_point(self):
        point = Point(1, 2)
        self.unit.set_point(point)

        self.assertTrue(self.unit.has_point())

        self.unit.del_point()
        self.assertFalse(self.unit.has_point())

    def test_set_map(self):
        self.assertFalse(self.unit.has_map())
        map_ = Map(1, 1, [])
        self.unit.set_map(map_)
        self.assertTrue(self.unit.is_on_map(map_))

    def test_is_on_map_true(self):
        map_ = Map(1, 1, [])
        self.unit.set_map(map_)
        self.assertTrue(self.unit.is_on_map(map_))

    def test_is_on_map_false(self):
        map_ = Map(1, 1, [])
        self.assertFalse(self.unit.is_on_map(map_))
        self.unit.set_map(Map(1, 1, []))
        self.assertFalse(self.unit.is_on_map(map_))

    def test_has_map(self):
        self.assertFalse(self.unit.has_map())
        self.unit.set_map(Map(1, 1, []))
        self.assertTrue(self.unit.has_map())

