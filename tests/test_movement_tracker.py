import unittest

from battle.movement_tracker import MovementTracker
from battle.maptools.point import Point
from battle.map import Map, MapPlacementError
from battle.tile import Tile
from battle.maptools.direction import Direction
from battle.units import Soldier


class TestBaseUnit(unittest.TestCase):
    test_map = Map(2, 2, [Tile.blank(), Tile.blank(), Tile.blank(), Tile.blank()])

    def setUp(self):
        self.mover = MovementTracker(map_=self.test_map)
        self.soldier = Soldier()

    def tearDown(self):
        self.test_map.remove_all_units()

    def test_default_init(self):
        self.assertFalse(self.unmapped.has_point())
        self.assertFalse(self.unmapped.has_map())
        self.assertEqual(self.unmapped.mv_pts, 3)

    def test_assignment_init(self):
        new_unit = MovementTracker(map_=self.test_map, max_move=6)
        self.assertTrue(new_unit.is_on_map(self.test_map))
        self.assertEqual(new_unit.mv_pts, 6)

    def test_get_point_is_none(self):
        self.assertIsNone(self.unmapped.get_point())

    def test_get_point_is_point(self):
        point = Point(0, 0)
        self.mover.set_point(point)

        self.assertEqual(self.mover.get_point(), Point(0, 0))

    def test_has_point_false(self):
        self.assertFalse(self.unmapped.has_point())

    def test_has_point_true(self):
        point = Point(1, 1)
        self.mover.set_point(point)
        self.assertTrue(self.mover.has_point())

    def test_set_point_raises_error_with_no_map(self):
        self.assertRaises(MapPlacementError, self.unmapped.set_point, Point(0, 0))

    def test_set_point_sets_point(self):
        pt1 = Point(0, 0)

        self.mover.set_point(pt1)
        self.assertEqual(self.mover.get_point(), pt1)

    def test_set_point_sets_unit_on_map(self):
        pt1 = Point(0, 0)

        self.mover.set_point(pt1)
        self.assertEqual(self.test_map.get_unit(pt1), self.mover)

    def test_set_point_new_point_removes_unit_from_old_pt(self):
        pt1 = Point(0, 0)
        pt2 = Point(0, 1)

        self.mover.set_point(pt1)
        self.mover.set_point(pt2)
        self.assertIsNone(self.test_map.get_unit(pt1))
        self.assertEqual(self.test_map.get_unit(pt2), self.mover)

    def test_del_point_removes_from_unit_and_map(self):
        point = Point(1, 1)
        self.mover.set_point(point)

        self.assertTrue(self.mover.has_point())

        self.mover.del_point()
        self.assertFalse(self.mover.has_point())
        self.assertIsNone(self.test_map.get_unit(point))

    def test_set_map(self):
        self.assertFalse(self.unmapped.has_map())
        map_ = Map(1, 1, [])
        self.unmapped.set_map(map_)
        self.assertTrue(self.unmapped.is_on_map(map_))

    def test_is_on_map_true(self):
        map_ = Map(1, 1, [])
        self.unmapped.set_map(map_)
        self.assertTrue(self.unmapped.is_on_map(map_))

    def test_is_on_map_false(self):
        map_ = Map(1, 1, [])
        self.assertFalse(self.unmapped.is_on_map(map_))
        self.unmapped.set_map(Map(1, 1, []))
        self.assertFalse(self.unmapped.is_on_map(map_))

    def test_has_map(self):
        self.assertFalse(self.unmapped.has_map())
        self.unmapped.set_map(Map(1, 1, []))
        self.assertTrue(self.unmapped.has_map())

    def test_is_move_allowed_true(self):
        self.mover.set_point(Point(0, 0))
        self.assertTrue(self.mover.is_move_allowed(Direction.N))

    def test_is_move_allowed_false_no_map_or_no_point(self):
        self.assertFalse(self.unmapped.is_move_allowed(Direction.N))
        self.assertFalse(self.mover.is_move_allowed(Direction.N))

    def test_is_move_allowed_false_map_cannot_place_unit(self):
        self.mover.set_point(Point(0, 0))
        new = MovementTracker(self.test_map)
        new.set_point(Point(0, 1))
        self.assertFalse(self.test_map.can_place_unit(Point(0, 2)))
        self.assertFalse(self.test_map.can_place_unit(Point(0, 0)))

        self.assertFalse(new.is_move_allowed(Direction.N))
        self.assertFalse(new.is_move_allowed(Direction.S))

    def test_has_enough_move(self):
        self.assertTrue(self.mover.has_enough_move(1))
        self.assertTrue(self.mover.has_enough_move(3))
        self.assertFalse(self.mover.has_enough_move(5))

    def test_move_true(self):
        self.mover.set_point(Point(0, 0))
        self.assertTrue(self.mover.move(Direction.N))
        self.assertEqual(self.mover.get_point(), Point(0, 1))
        self.assertEqual(self.test_map.get_unit(Point(0, 1)), self.mover)
        self.assertIsNone(self.test_map.get_unit(Point(0, 0)))
        self.assertEqual(self.mover.mv_pts, 2)

    def test_move_false(self):
        self.mover.set_point(Point(0, 0))
        self.assertFalse(self.mover.move(Direction.S))
        self.assertEqual(self.mover.get_point(), Point(0, 0))
        self.assertEqual(self.test_map.get_unit(Point(0, 0)), self.mover)
        self.assertEqual(self.mover.mv_pts, 3)
