import unittest

from battle.maptools.direction import Direction

N, W, S, E = Direction.N, Direction.W, Direction.S, Direction.E


class TestDirection(unittest.TestCase):

    def test_is_assertion(self):
        self.assertIs(N, Direction.N)
        self.assertIs(S, Direction.S)
        self.assertIs(W, Direction.W)
        self.assertIs(E, Direction.E)

    def test_not_is_assertion(self):
        self.assertIsNot(N, S)

    def test_equality_FAILS(self):
        self.assertTrue(N.__eq__(N))
        self.assertIs(NotImplemented, N.__eq__(S))

        self.assertTrue(N == N)
        self.assertFalse(N == S)
        self.assertTrue(N != S)
        self.assertFalse(N != N)

    def test_enum_not_equal_value_or_name(self):
        self.assertNotEqual(N, 'N')
        self.assertNotEqual('N', N)
        self.assertNotEqual(N, (0, 1))
        self.assertNotEqual((0, 1), N)

    def test_opposite(self):
        self.assertIs(N.opposite(), S)
        self.assertIs(S.opposite(), N)
        self.assertIs(E.opposite(), W)
        self.assertIs(W.opposite(), E)

    def test_left(self):
        self.assertIs(N.left(), W)
        self.assertIs(W.left(), S)
        self.assertIs(S.left(), E)
        self.assertIs(E.left(), N)

    def test_right(self):
        self.assertIs(N.right(), E)
        self.assertIs(E.right(), S)
        self.assertIs(S.right(), W)
        self.assertIs(W.right(), N)

    def test_repr(self):
        self.assertEqual(repr(N), 'Direction.N')
        self.assertEqual(repr(S), 'Direction.S')
        self.assertEqual(repr(E), 'Direction.E')
        self.assertEqual(repr(W), 'Direction.W')

    def test_value_N(self):
        self.assertEqual(N.value, (0, 1))

    def test_value_S(self):
        self.assertEqual(S.value, (0, -1))

    def test_value_E(self):
        self.assertEqual(E.value, (1, 0))

    def test_value_W(self):
        self.assertEqual(W.value, (-1, 0))

    def test_iterator(self):
        order = [N, S, E, W]
        index = 0
        for direction in Direction:
            self.assertIs(order[index], direction)
            index += 1
