import unittest

from battle.movement_tracker import MovementTracker
from battle.maptools.point import Point
from battle.map import Map
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

        point = Point(0, 0)
        self.mover.set_point(self.soldier, point)
        self.mover.del_point(self.soldier)
        self.assertIsNone(self.mover.get_point(self.soldier))

    def test_get_point_is_point(self):
        point = Point(0, 0)
        self.mover.set_point(self.soldier, point)

        self.assertEqual(self.mover.get_point(self.soldier), Point(0, 0))

    def test_set_point_sets_point_for_unit(self):
        pt1 = Point(0, 0)

        self.mover.set_point(self.soldier, pt1)
        self.assertEqual(self.mover.get_point(self.soldier), pt1)

    def test_set_point_sets_unit_on_map(self):
        point = Point(0, 0)

        self.mover.set_point(self.soldier, point)
        self.assertEqual(self.test_map.get_unit(point), self.soldier)

    def test_set_point_removes_unit_from_old_pt_and_place_unit_on_new_point(self):
        pt1 = Point(0, 0)
        pt2 = Point(0, 1)

        self.mover.set_point(self.soldier, pt1)
        self.mover.set_point(self.soldier, pt2)
        self.assertIsNone(self.test_map.get_unit(pt1))
        self.assertEqual(self.test_map.get_unit(pt2), self.soldier)
        self.assertEqual(self.mover.get_point(self.soldier), pt2)

    def test_del_point_removes_from_movement_tracker_and_map(self):
        point = Point(1, 1)
        self.mover.set_point(self.soldier, point)

        self.assertTrue(self.test_map.get_unit(point))

        self.mover.del_point(self.soldier)
        self.assertIsNone(self.test_map.get_unit(point))
        self.assertIsNone(self.mover.get_point(self.soldier))

    def test_is_placed(self):
        point = Point(0, 0)
        self.mover.set_point(self.soldier, point)

        self.assertTrue(self.mover.is_placed(self.soldier))

        self.mover.del_point(self.soldier)
        self.assertFalse(self.mover.is_placed(self.soldier))
        self.assertFalse(self.mover.is_placed(Soldier()))

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

    def test_move_unit_not_on_map(self):
        unit = Soldier()
        self.assertRaises(AttributeError, self.mover.move, unit, Direction.N)

    def test_is_move_allowed_true(self):
        self.mover.set_point(self.soldier, Point(0, 0))
        self.assertTrue(self.mover.is_move_allowed(self.soldier, Direction.N))

    def test_is_move_allowed_false_no_point(self):
        self.assertFalse(self.mover.is_move_allowed(self.soldier, Direction.N))

    def test_is_move_allowed_false_map_cannot_place_unit(self):
        self.mover.set_point(self.soldier, Point(0, 0))

        unit = Soldier()
        self.mover.set_point(unit, Point(0, 1))
        self.assertFalse(self.test_map.can_place_unit(Point(0, 2)))
        self.assertFalse(self.test_map.can_place_unit(Point(0, 0)))

        self.assertFalse(self.mover.is_move_allowed(self.soldier, Direction.N))
        self.assertFalse(self.mover.is_move_allowed(self.soldier, Direction.S))

        self.assertFalse(self.mover.is_move_allowed(unit, Direction.N))
        self.assertFalse(self.mover.is_move_allowed(unit, Direction.S))

    def test_two_trackers_can_share_one_map(self):
        self.mover.set_point(self.soldier, Point(0, 0))
        new_mover = MovementTracker(self.test_map)
        new_solder = Soldier()
        new_mover.set_point(new_solder, Point(0, 1))

        self.assertFalse(self.mover.is_move_allowed(self.soldier, Direction.N))
        self.assertFalse(new_mover.is_move_allowed(new_solder, Direction.S))

    def test_has_enough_move(self):
        self.assertTrue(self.mover.has_enough_move(self.soldier, 1))
        self.assertTrue(self.mover.has_enough_move(self.soldier, 3))
        self.assertFalse(self.mover.has_enough_move(self.soldier, 5))

    def test_get_move_pts_unit_not_on_map_raises_attribute_error(self):
        self.assertRaises(AttributeError, self.mover.get_move_pts, self.soldier, Direction.N)

    def test_get_move_pts_direction_not_on_map_raises_value_error(self):
        self.mover.set_point(self.soldier, Point(0, 1))
        self.assertRaises(ValueError, self.mover.get_move_pts, self.soldier, Direction.N)

    def test_get_move_pts_currently_always_returns_one(self):
        self.mover.set_point(self.soldier, Point(0, 0))
        self.assertEqual(self.mover.get_move_pts(self.soldier, Direction.N), 1)
        self.assertEqual(self.mover.get_move_pts(self.soldier, Direction.E), 1)
