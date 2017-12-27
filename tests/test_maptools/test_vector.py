import unittest

from battle.maptools.vector import Vector
from battle.maptools.direction import Direction

N, S, E, W = Direction


class TestVector(unittest.TestCase):
    def test_demo(self):
        v0 = Vector.from_dir_and_mag(S, 10)
        v1 = Vector.from_dir_and_mag(N, 5)
        v2 = Vector.from_dir_and_mag(W, 3)
        v3 = v2.add(v1).add(v0)
        self.assertEqual(v3.x, -3)
        self.assertEqual(v3.y, -5)
        self.assertEqual(v3.direction_tuple(), ((W, 3), (S, 5)))


