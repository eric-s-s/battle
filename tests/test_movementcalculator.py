import unittest

from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.units import Soldier
from battle.maptools.tile import Tile, ImpassableTile
from battle.movementcalculator import MovementCalculator


class TestMovementCalculator(unittest.TestCase):
    test_map = Map(3, 3, [Tile() for _ in range(9)])

    def test_get_movement_points_only_to_max_mv(self):
        map_ = Map(3, 3, [Tile() for _ in range(9)])
        answer = MovementCalculator(map_).get_movement_points(Point(0, 0), 1)
        expected = {Point(0, 0): 0, Point(0, 1): 1,
                    Point(1, 0): 1}
        self.assertEqual(answer, expected)

    def test_get_movement_points_only_includes_distances_on_map(self):
        map_ = Map(2, 2, [Tile() for _ in range(4)])
        answer = MovementCalculator(map_).get_movement_points(Point(0, 0), 100)
        expected = {Point(0, 0): 0,
                    Point(0, 1): 1,
                    Point(1, 0): 1,
                    Point(1, 1): 2}
        self.assertEqual(answer, expected)

    def test_get_movement_points_not_affected_by_unit_on_origin(self):
        map_ = Map(2, 2, [Tile() for _ in range(4)])
        origin = Point(0, 0)
        map_.place_unit(Soldier(), origin)
        answer = MovementCalculator(map_).get_movement_points(origin, 100)
        expected = {Point(0, 0): 0,
                    Point(0, 1): 1,
                    Point(1, 0): 1,
                    Point(1, 1): 2}
        self.assertEqual(answer, expected)

    def test_get_movement_points_non_uniform_elevation(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 1, Point(2, 0): 2,
                               Point(0, 1): 1, Point(1, 1): 2, Point(2, 1): 3,
                               Point(0, 2): 2, Point(1, 2): 3, Point(2, 2): 4}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)

        origin_1 = Point(1, 1)
        expected_1 = {Point(0, 0): 2, Point(1, 0): 1, Point(2, 0): 3,
                      Point(0, 1): 1, Point(1, 1): 0, Point(2, 1): 2,
                      Point(0, 2): 3, Point(1, 2): 2, Point(2, 2): 4}
        answer = MovementCalculator(the_map).get_movement_points(origin_1, 5)
        self.assertEqual(answer, expected_1)

        origin_2 = Point(2, 1)
        expected_2 = {Point(0, 0): 3, Point(1, 0): 2, Point(2, 0): 1,
                      Point(0, 1): 2, Point(1, 1): 1, Point(2, 1): 0,
                      Point(0, 2): 4, Point(1, 2): 3, Point(2, 2): 2}
        answer = MovementCalculator(the_map).get_movement_points(origin_2, 5)
        self.assertEqual(expected_2, answer)

    def test_get_movement_points_non_uniform_terrain(self):
        terrain_mvs = {Point(0, 0): 1, Point(1, 0): 2,
                       Point(0, 1): 4, Point(1, 1): 3}

        tiles = [Tile(point=point, terrain_mv=terrain) for point, terrain in terrain_mvs.items()]
        map_ = Map(2, 2, tiles)
        origin = Point(0, 0)
        expected = {Point(0, 0): 0, Point(1, 0): 1,
                    Point(0, 1): 1, Point(1, 1): 3}
        self.assertEqual(MovementCalculator(map_).get_movement_points(origin, 5), expected)

        origin = Point(0, 1)
        expected = {Point(0, 0): 4, Point(1, 0): 5,
                    Point(0, 1): 0, Point(1, 1): 4}
        self.assertEqual(MovementCalculator(map_).get_movement_points(origin, 5), expected)

    def test_get_movement_points_chooses_smallest_move_pts(self):

        elevations = {Point(0, 0): 0, Point(1, 0): 0,
                      Point(0, 1): 1, Point(1, 1): 2}

        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(2, 2, tiles)
        origin = Point(0, 1)
        expected = {Point(0, 0): 1, Point(1, 0): 2,  # point(1, 0) has two different ways from 0,1
                    Point(0, 1): 0, Point(1, 1): 2}  # one way costs 2 and one way costs 3
        self.assertEqual(MovementCalculator(map_).get_movement_points(origin, 10), expected)

    def test_get_movement_points_chooses_smallest_move_pts_different_order(self):

        elevations = {Point(0, 0): 2, Point(1, 0): 0,
                      Point(0, 1): 1, Point(1, 1): 0}

        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(2, 2, tiles)
        origin = Point(0, 1)
        expected = {Point(0, 0): 2, Point(1, 0): 2,  # point(1, 0) has two different ways from 0,1
                    Point(0, 1): 0, Point(1, 1): 1}  # one way costs 2 and one way costs 3
        self.assertEqual(MovementCalculator(map_).get_movement_points(origin, 10), expected)

    def test_get_movement_points_elevations_and_terrains(self):
        elevation_terrain = {Point(0, 0): (0, 3), Point(1, 0): (0, 4),
                             Point(0, 1): (1, 5), Point(1, 1): (2, 6)}
        tiles = [Tile(point=point, elevation=el_terrain[0], terrain_mv=el_terrain[1])
                 for point, el_terrain in elevation_terrain.items()]
        map_ = Map(2, 2, tiles)

        origin = Point(0, 1)
        expected = {Point(0, 0): 5, Point(1, 0): 8,
                    Point(0, 1): 0, Point(1, 1): 6}
        self.assertEqual(MovementCalculator(map_).get_movement_points(origin, 10), expected)

        origin = Point(0, 0)
        expected = {Point(0, 0): 0, Point(1, 0): 3,
                    Point(0, 1): 4, Point(1, 1): 9}
        self.assertEqual(MovementCalculator(map_).get_movement_points(origin, 10), expected)

    def test_get_movement_points_with_impassable_tile_in_place(self):
        elevations = {Point(0, 0): 2, Point(1, 0): 0, Point(2, 0): 3,
                      Point(0, 1): 1, Point(1, 1): 9, Point(2, 1): 2,
                      Point(0, 2): 2, Point(1, 2): 0, Point(2, 2): 1}
        tiles = [Tile(point=point, elevation=elevation) if elevation != 9 else ImpassableTile(point=point)
                 for point, elevation in elevations.items()]
        map_ = Map(3, 3, tiles)

        origin = Point(1, 2)
        expected = {Point(0, 0): 6, Point(1, 0): 7, Point(2, 0): 6,
                    Point(0, 1): 4,                 Point(2, 1): 4,
                    Point(0, 2): 3, Point(1, 2): 0, Point(2, 2): 2}
        self.assertEqual(MovementCalculator(map_).get_movement_points(origin, 10), expected)

    def test_get_movement_points_with_occupied_space_in_place(self):
        elevations = {Point(0, 0): 2, Point(1, 0): 0, Point(2, 0): 3,
                      Point(0, 1): 1, Point(1, 1): 0, Point(2, 1): 2,
                      Point(0, 2): 2, Point(1, 2): 0, Point(2, 2): 1}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]

        map_ = Map(3, 3, tiles)

        occupied_point = Point(1, 1)
        origin = Point(1, 2)

        map_.place_unit(Soldier(), origin)
        map_.place_unit(Soldier(), occupied_point)

        expected = {Point(0, 0): 6, Point(1, 0): 7, Point(2, 0): 6,
                    Point(0, 1): 4,                 Point(2, 1): 4,
                    Point(0, 2): 3, Point(1, 2): 0, Point(2, 2): 2}
        self.assertEqual(MovementCalculator(map_).get_movement_points(origin, 10), expected)

    def test_get_movement_points_obstacle_max_mv_lte_map_size(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 9, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 3, tiles)
        origin = Point(1, 2)
        expected_four = {Point(0, 0): 3, Point(1, 0): 4, Point(2, 0): 3, Point(3, 0): 4,
                         Point(0, 1): 2,                 Point(2, 1): 2, Point(3, 1): 3,
                         Point(0, 2): 1, Point(1, 2): 0, Point(2, 2): 1, Point(3, 2): 2}

        expected_three = {Point(0, 0): 3,                 Point(2, 0): 3,
                          Point(0, 1): 2,                 Point(2, 1): 2, Point(3, 1): 3,
                          Point(0, 2): 1, Point(1, 2): 0, Point(2, 2): 1, Point(3, 2): 2}

        ranger = MovementCalculator(map_)
        self.assertEqual(ranger.get_movement_points(origin, 4), expected_four)
        self.assertEqual(ranger.get_movement_points(origin, 3), expected_three)

    def test_get_movement_points_obstacle_lte_max_mv_will_continue_around_corner(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 3, Point(1, 1): 4, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 3, tiles)
        origin = Point(1, 2)
        expected_four = {                Point(1, 0): 4, Point(2, 0): 3, Point(3, 0): 4,
                                                         Point(2, 1): 2, Point(3, 1): 3,
                         Point(0, 2): 1, Point(1, 2): 0, Point(2, 2): 1, Point(3, 2): 2}

        expected_five = {Point(0, 0): 5, Point(1, 0): 4, Point(2, 0): 3, Point(3, 0): 4,
                         Point(0, 1): 5, Point(1, 1): 5, Point(2, 1): 2, Point(3, 1): 3,
                         Point(0, 2): 1, Point(1, 2): 0, Point(2, 2): 1, Point(3, 2): 2}

        ranger = MovementCalculator(map_)
        self.assertEqual(ranger.get_movement_points(origin, 5), expected_five)
        self.assertEqual(ranger.get_movement_points(origin, 4), expected_four)

    def test_get_movement_points_after_going_around_obstacle_will_recalculate_min_distance_bottom_to_top(self):
        elevations = {Point(0, 0): 9, Point(1, 0): 0, Point(2, 0): 9, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 0, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 3, Point(2, 2): 0, Point(3, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 0, Point(2, 3): 0, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(1, 3)
        expected_six = {                Point(1, 0): 5,                 Point(3, 0): 5,
                        Point(0, 1): 3, Point(1, 1): 4, Point(2, 1): 3, Point(3, 1): 4,
                        Point(0, 2): 2, Point(1, 2): 4, Point(2, 2): 2, Point(3, 2): 3,
                        Point(0, 3): 1, Point(1, 3): 0, Point(2, 3): 1, Point(3, 3): 2}

        ranger = MovementCalculator(map_)
        self.assertEqual(ranger.get_movement_points(origin, 6), expected_six)

    def test_get_movement_points_after_going_around_obstacle_will_recalculate_min_distance_top_to_bottom(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 3, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0,
                      Point(0, 3): 9, Point(1, 3): 0, Point(2, 3): 9, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(1, 0)
        expected_six = {Point(0, 0): 1, Point(1, 0): 0, Point(2, 0): 1, Point(3, 0): 2,
                        Point(0, 1): 2, Point(1, 1): 4, Point(2, 1): 2, Point(3, 1): 3,
                        Point(0, 2): 3, Point(1, 2): 4, Point(2, 2): 3, Point(3, 2): 4,
                                        Point(1, 3): 5,                 Point(3, 3): 5}

        ranger = MovementCalculator(map_)
        self.assertEqual(ranger.get_movement_points(origin, 6), expected_six)

    def test_get_movement_points_after_going_around_obstacle_will_recalculate_min_distance_l_to_r(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 9,
                      Point(0, 1): 0, Point(1, 1): 3, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 9,
                      Point(0, 3): 0, Point(1, 3): 0, Point(2, 3): 0, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(0, 1)
        expected_six = {Point(0, 0): 1, Point(1, 0): 2, Point(2, 0): 3,
                        Point(0, 1): 0, Point(1, 1): 4, Point(2, 1): 4, Point(3, 1): 5,
                        Point(0, 2): 1, Point(1, 2): 2, Point(2, 2): 3,
                        Point(0, 3): 2, Point(1, 3): 3, Point(2, 3): 4, Point(3, 3): 5}

        ranger = MovementCalculator(map_)
        self.assertEqual(ranger.get_movement_points(origin, 6), expected_six)

    def test_get_movement_points_after_going_around_obstacle_will_recalculate_min_distance_r_to_l(self):
        elevations = {Point(0, 0): 9, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 0, Point(2, 1): 3, Point(3, 1): 0,
                      Point(0, 2): 9, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 0, Point(2, 3): 0, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(3, 1)
        expected_six = {                Point(1, 0): 3, Point(2, 0): 2, Point(3, 0): 1,
                        Point(0, 1): 5, Point(1, 1): 4, Point(2, 1): 4, Point(3, 1): 0,
                                        Point(1, 2): 3, Point(2, 2): 2, Point(3, 2): 1,
                        Point(0, 3): 5, Point(1, 3): 4, Point(2, 3): 3, Point(3, 3): 2}

        ranger = MovementCalculator(map_)
        self.assertEqual(ranger.get_movement_points(origin, 6), expected_six)

    def test_get_movement_points_goes_around_obstacle_and_recalculates_on_terrain(self):
        terrains = {Point(0, 0): 1, Point(1, 0): 1, Point(2, 0): 1, Point(3, 0): 1,
                    Point(0, 1): 1, Point(1, 1): 1, Point(2, 1): 1, Point(3, 1): 1,
                    Point(0, 2): 1, Point(1, 2): 4, Point(2, 2): 9, Point(3, 2): 1,
                    Point(0, 3): 1, Point(1, 3): 1, Point(2, 3): 5, Point(3, 3): 1}
        tiles = [Tile(point=point, terrain_mv=terrain) for point, terrain in terrains.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(1, 3)
        expected_six = {Point(0, 0): 4, Point(1, 0): 5, Point(2, 0): 6,
                        Point(0, 1): 3, Point(1, 1): 4, Point(2, 1): 5, Point(3, 1): 6,
                        Point(0, 2): 2, Point(1, 2): 1, Point(2, 2): 5,
                        Point(0, 3): 1, Point(1, 3): 0, Point(2, 3): 1, Point(3, 3): 6}

        ranger = MovementCalculator(map_)
        self.assertEqual(ranger.get_movement_points(origin, 6), expected_six)