import unittest

from battle.movement_tracker import MovementTracker
from battle.maptools.point import Point
from battle.map import Map, MapPlacementError
from battle.tile import Tile
from battle.maptools.direction import Direction
from battle.units import Soldier


class TestMovementTracker(unittest.TestCase):
    test_map = Map(2, 2, [Tile.blank(), Tile.blank(), Tile.blank(), Tile.blank()])

    def setUp(self):
        self.mover = MovementTracker(map_=self.test_map)
        self.soldier = Soldier()

    def tearDown(self):
        self.test_map.remove_all_units()

    def test_init(self):
        self.assertEqual(self.mover._map, self.test_map)
        self.assertEqual(self.mover._units, {})

    def test_get_point_is_none(self):
        self.assertIsNone(self.mover.get_point(self.soldier))

    def test_get_point_is_point(self):
        point = Point(0, 0)
        self.mover.set_point(self.soldier, point)

        self.assertEqual(self.mover.get_point(self.soldier), Point(0, 0))

    def test_set_point_sets_point_for_unit(self):
        pt1 = Point(0, 0)

        self.mover.set_point(self.soldier, pt1)
        self.assertEqual(self.mover.get_point(self.soldier), pt1)

    def test_set_point_new_point_removes_unit_from_old_pt(self):
        pt1 = Point(0, 0)
        pt2 = Point(0, 1)

        self.mover.set_point(self.soldier, pt1)
        self.mover.set_point(self.soldier, pt2)
        self.assertIsNone(self.test_map.get_unit(pt1))
        self.assertEqual(self.test_map.get_unit(pt2), self.soldier)

    def test_del_point_removes_from_unit_and_map(self):
        point = Point(1, 1)
        self.mover.set_point(self.soldier, point)

        self.assertTrue(self.test_map.get_unit(point))

        self.mover.del_point(self.soldier)
        self.assertFalse(self.test_map.get_unit(point))
        self.assertIsNone(self.test_map.get_unit(point))

    def test_move_true(self):
        self.mover.set_point(self.soldier, Point(0, 0))
        self.assertTrue(self.mover.move(self.soldier, Direction.N))
        self.assertEqual(self.mover.get_point(self.soldier), Point(0, 1))
        self.assertEqual(self.test_map.get_unit(Point(0, 1)), self.soldier)
        self.assertIsNone(self.test_map.get_unit(Point(0, 0)))
        self.assertEqual(self.soldier.get_move_points(), 2)

    def test_move_false(self):
        self.mover.set_point(self.soldier, Point(0, 0))
        self.assertFalse(self.mover.move(self.soldier, Direction.S))
        self.assertEqual(self.mover.get_point(self.soldier), Point(0, 0))
        self.assertEqual(self.test_map.get_unit(Point(0, 0)), self.soldier)
        self.assertEqual(self.soldier.get_move_points(), 3)

    def test_is_move_allowed_true(self):
        self.mover.set_point(self.soldier, Point(0, 0))
        self.assertTrue(self.mover.is_move_allowed(self.soldier, Direction.N))

    def test_is_move_allowed_false_no_point(self):
        self.assertFalse(self.mover.is_move_allowed(self.soldier, Direction.N))

    def test_is_move_allowed_false_map_cannot_place_unit(self):
        self.mover.set_point(self.soldier, Point(0, 0))
        new = MovementTracker(self.test_map)
        unit = Soldier()
        new.set_point(unit, Point(0, 1))
        self.assertFalse(self.test_map.can_place_unit(Point(0, 2)))
        self.assertFalse(self.test_map.can_place_unit(Point(0, 0)))

        self.assertFalse(new.is_move_allowed(self.soldier, Direction.N))
        self.assertFalse(new.is_move_allowed(self.soldier, Direction.S))

    def test_has_enough_move(self):
        self.assertTrue(self.mover.has_enough_move(self.soldier, 1))
        self.assertTrue(self.mover.has_enough_move(self.soldier, 3))
        self.assertFalse(self.mover.has_enough_move(self.soldier, 5))

