import unittest

from battle.maptools.vector import Vector
from battle.maptools.direction import Direction

N, S, E, W = Direction


class TestVector(unittest.TestCase):
    def test_init(self):
        v = Vector(2, 5)
        self. assertEqual(v.x, 2)
        self.assertEqual(v.y, 5)

        v = Vector(0, 0)
        self. assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)

        v = Vector(-2, -5)
        self. assertEqual(v.x, -2)
        self.assertEqual(v.y, -5)

    def test_from_dir_and_mag(self):
        v = Vector.from_dir_and_mag(N, 10)
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 10)

        v = Vector.from_dir_and_mag(S, 10)
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, -10)

        v = Vector.from_dir_and_mag(E, 10)
        self.assertEqual(v.x, 10)
        self.assertEqual(v.y, 0)

        v = Vector.from_dir_and_mag(W, 10)
        self.assertEqual(v.x, -10)
        self.assertEqual(v.y, 0)

    def test_add(self):
        v1 = Vector(3, 6)
        v2 = Vector(-1, 2)
        v3 = v1.add(v2)
        self.assertEqual(v3.x, 2)
        self.assertEqual(v3.y, 8)

    def test_direction_tuple_positive(self):
        v = Vector(2, 3)
        self.assertEqual(v.direction_tuple(), ((E, 2), (N, 3)))

    def test_direction_tuple_zero(self):
        v = Vector(0, 0)
        self.assertEqual(v.direction_tuple(), ((E, 0), (N, 0)))

    def test_direction_tuple_negative(self):
        v = Vector(-2, -3)
        self.assertEqual(v.direction_tuple(), ((W, 2), (S, 3)))

    def test_eq_true(self):
        self.assertTrue(Vector(1, 2).__eq__(Vector(1, 2)))

    def test_eq_false(self):
        self.assertFalse(Vector(2, 2).__eq__(Vector(1, 2)))
        self.assertFalse(Vector(1, 1).__eq__(Vector(1, 2)))

    def test_ne_false(self):
        self.assertFalse(Vector(1, 2).__ne__(Vector(1, 2)))

    def test_ne_true(self):
        self.assertTrue(Vector(2, 2).__ne__(Vector(1, 2)))
        self.assertTrue(Vector(1, 1).__ne__(Vector(1, 2)))

    def test_repr(self):
        self.assertEqual(repr(Vector(1, -1)), 'Vector(1, -1)')

