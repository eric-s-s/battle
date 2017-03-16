import unittest

from battle.point import Point
from battle.direction import Direction

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class TestPoint(unittest.TestCase):
    def test_init(self):
        point = Point(1, 2)
        self.assertEqual(point.x, 1)
        self.assertEqual(point.y, 2)

    def test_eq_true(self):
        point_1 = Point(1, 2)
        point_2 = Point(1, 2)
        self.assertTrue(point_1.__eq__(point_2))

    def test_eq_false(self):
        point_1 = Point(1, 2)
        point_2 = Point(1, 1)
        self.assertFalse(point_1.__eq__(point_2))
        self.assertFalse(point_1.__eq__((1, 2)))

    def test_ne_true(self):
        point_1 = Point(1, 2)
        point_2 = Point(1, 1)
        self.assertTrue(point_1.__ne__(point_2))
        self.assertTrue(point_1.__ne__((1, 2)))

    def test_ne_false(self):
        point_1 = Point(1, 2)
        point_2 = Point(1, 2)
        self.assertFalse(point_1.__ne__(point_2))

    def test_north(self):
        point = Point(1, 2)
        self.assertEqual(point.north(), Point(1, 3))

    def test_south(self):
        point = Point(1, 2)
        self.assertEqual(point.south(), Point(1, 1))

    def test_east(self):
        point = Point(1, 2)
        self.assertEqual(point.east(), Point(2, 2))

    def test_west(self):
        point = Point(1, 2)
        self.assertEqual(point.west(), Point(0, 2))

    def test_plus_x_zero(self):
        point = Point(1, 2)
        self.assertEqual(point.plus_x(0), point)

    def test_plus_x_pos(self):
        self.assertEqual(Point(1, 1).plus_x(5), Point(6, 1))

    def test_plus_x_neg(self):
        self.assertEqual(Point(1, 1).plus_x(-5), Point(-4, 1))

    def test_plus_y_zero(self):
        point = Point(1, 2)
        self.assertEqual(point.plus_y(0), point)

    def test_plus_y_pos(self):
        self.assertEqual(Point(1, 1).plus_y(5), Point(1, 6))

    def test_plus_y_neg(self):
        self.assertEqual(Point(1, 1).plus_y(-5), Point(1, -4))

    def test_plus_zero_zero(self):
        self.assertEqual(Point(1, 1).plus(0, 0), Point(1, 1))

    def test_plus_neg_pos(self):
        self.assertEqual(Point(1, 1).plus(-2, 2), Point(-1, 3))

    def test_plus_pos_neg(self):
        self.assertEqual(Point(1, 1).plus(2, -2), Point(3, -1))




if __name__ == '__main__':
    unittest.main()
