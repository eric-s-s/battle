import unittest

from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.units import Soldier
from battle.maptools.tile import Tile, ImpassableTile
from battle.movementcalculator import MovementCalculator
from battle.maptools.direction import Direction

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class TestMovementCalculator(unittest.TestCase):
    test_map = Map(3, 3, [Tile() for _ in range(9)])

    def test_get_movement_points_only_to_max_mv(self):
        map_ = Map(3, 3, [Tile() for _ in range(9)])
        answer = MovementCalculator(map_).get_movement_points(Point(0, 0), 1)
        expected = {Point(0, 0): 0, Point(0, 1): 1,
                    Point(1, 0): 1}
        self.assertEqual(answer, expected)

    def test_get_movement_points_with_path_only_to_max_mv(self):
        map_ = Map(3, 3, [Tile() for _ in range(9)])
        answer = MovementCalculator(map_).get_movement_points_with_path(Point(0, 0), 1)
        expected = {Point(0, 0): (0, []), Point(0, 1): (1, [N]),
                    Point(1, 0): (1, [E])}
        self.assertEqual(answer, expected)

    def test_get_movement_points_only_includes_distances_on_map(self):
        map_ = Map(2, 2, [Tile() for _ in range(4)])
        answer = MovementCalculator(map_).get_movement_points(Point(0, 0), 100)
        expected = {Point(0, 0): 0,
                    Point(0, 1): 1,
                    Point(1, 0): 1,
                    Point(1, 1): 2}
        self.assertEqual(answer, expected)

    def test_get_movement_points_with_path_only_includes_distances_on_map(self):
        map_ = Map(2, 2, [Tile() for _ in range(4)])
        answer = MovementCalculator(map_).get_movement_points_with_path(Point(0, 0), 100)
        expected = {Point(0, 0): (0, []),
                    Point(0, 1): (1, [N]),
                    Point(1, 0): (1, [E]),
                    Point(1, 1): (2, [E, N])}
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

    def test_get_movement_points_with_path_not_affected_by_unit_on_origin(self):
        map_ = Map(2, 2, [Tile() for _ in range(4)])
        origin = Point(0, 0)
        map_.place_unit(Soldier(), origin)
        answer = MovementCalculator(map_).get_movement_points_with_path(origin, 100)
        expected = {Point(0, 0): (0, []),
                    Point(0, 1): (1, [N]),
                    Point(1, 0): (1, [E]),
                    Point(1, 1): (2, [E, N])}
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

    def test_get_movement_points_with_path_non_uniform_elevation(self):
        points_to_elevation = {Point(0, 0): 0, Point(1, 0): 1, Point(2, 0): 2,
                               Point(0, 1): 1, Point(1, 1): 2, Point(2, 1): 3,
                               Point(0, 2): 2, Point(1, 2): 3, Point(2, 2): 4}
        tiles = [Tile(elevation=elevation, point=point) for point, elevation in points_to_elevation.items()]
        the_map = Map(3, 3, tiles)

        origin_1 = Point(1, 1)
        expected_1 = {Point(0, 0): (2, [S, W]), Point(1, 0): (1, [S]), Point(2, 0): (3, [S, E]),
                      Point(0, 1): (1, [W]), Point(1, 1): (0, []), Point(2, 1): (2, [E]),
                      Point(0, 2): (3, [W, N]), Point(1, 2): (2, [N]), Point(2, 2): (4, [E, N])}
        answer = MovementCalculator(the_map).get_movement_points_with_path(origin_1, 5)

        self.assertEqual(answer, expected_1)

        origin_2 = Point(2, 1)
        expected_2 = {Point(0, 0): (3, [S, W, W]), Point(1, 0): (2, [S, W]), Point(2, 0): (1, [S]),
                      Point(0, 1): (2, [W, W]), Point(1, 1): (1, [W]), Point(2, 1): (0, []),
                      Point(0, 2): (4, [W, W, N]), Point(1, 2): (3, [W, N]), Point(2, 2): (2, [N])}
        answer = MovementCalculator(the_map).get_movement_points_with_path(origin_2, 5)
        self.assertEqual(expected_2, answer)

    def test_get_movement_points_with_path_non_uniform_terrain(self):
        terrain_mvs = {Point(0, 0): 1, Point(1, 0): 2,
                       Point(0, 1): 4, Point(1, 1): 3}

        tiles = [Tile(point=point, terrain_mv=terrain) for point, terrain in terrain_mvs.items()]
        map_ = Map(2, 2, tiles)
        origin = Point(0, 0)
        expected = {Point(0, 0): (0, []), Point(1, 0): (1, [E]),
                    Point(0, 1): (1, [N]), Point(1, 1): (3, [E, N])}

        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 5), expected)

        origin = Point(0, 1)
        expected = {Point(0, 0): (4, [S]), Point(1, 0): (5, [S, E]),
                    Point(0, 1): (0, []), Point(1, 1): (4, [E])}
        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 5), expected)

    def test_get_movement_points_with_path_chooses_smallest_move_pts(self):

        elevations = {Point(0, 0): 0, Point(1, 0): 0,
                      Point(0, 1): 1, Point(1, 1): 2}

        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(2, 2, tiles)
        origin = Point(0, 1)
        expected = {Point(0, 0): (1, [S]), Point(1, 0): (2, [S, E]),  # point(1, 0) has two different ways from 0,1
                    Point(0, 1): (0, []), Point(1, 1): (2, [E])}  # one way costs 2 and one way costs 3
        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 10), expected)

    def test_get_movement_points_with_path_chooses_smallest_move_pts_different_order(self):

        elevations = {Point(0, 0): 2, Point(1, 0): 0,
                      Point(0, 1): 1, Point(1, 1): 0}

        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(2, 2, tiles)
        origin = Point(0, 1)
        expected = {Point(0, 0): (2, [S]), Point(1, 0): (2, [E, S]),  # point(1, 0) has two different ways from 0,1
                    Point(0, 1): (0, []), Point(1, 1): (1, [E])}  # one way costs 2 and one way costs 3
        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 10), expected)

    def test_get_movement_points_with_path_elevations_and_terrains(self):
        elevation_terrain = {Point(0, 0): (0, 3), Point(1, 0): (0, 4),
                             Point(0, 1): (1, 5), Point(1, 1): (2, 6)}
        tiles = [Tile(point=point, elevation=el_terrain[0], terrain_mv=el_terrain[1])
                 for point, el_terrain in elevation_terrain.items()]
        map_ = Map(2, 2, tiles)

        origin = Point(0, 1)
        expected = {Point(0, 0): (5, [S]), Point(1, 0): (8, [S, E]),
                    Point(0, 1): (0, []), Point(1, 1): (6, [E])}
        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 10), expected)

        origin = Point(0, 0)
        expected = {Point(0, 0): (0, []), Point(1, 0): (3, [E]),
                    Point(0, 1): (4, [N]), Point(1, 1): (9, [E, N])}
        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 10), expected)

    def test_get_movement_points_with_path_elevations_and_terrains_different_order(self):
        elevation_terrain = {Point(0, 0): (2, 6), Point(1, 0): (0, 4),
                             Point(0, 1): (1, 5), Point(1, 1): (0, 3)}
        tiles = [Tile(point=point, elevation=el_terrain[0], terrain_mv=el_terrain[1])
                 for point, el_terrain in elevation_terrain.items()]
        map_ = Map(2, 2, tiles)

        origin = Point(0, 1)
        expected = {Point(0, 0): (6, [S]), Point(1, 0): (8, [E, S]),
                    Point(0, 1): (0, []), Point(1, 1): (5, [E])}
        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 10), expected)

        origin = Point(1, 0)
        expected = {Point(0, 0): (6, [W]), Point(1, 0): (0, []),
                    Point(0, 1): (8, [N, W]), Point(1, 1): (4, [N])}
        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 10), expected)

    def test_get_movement_points_with_path_with_impassable_tile_in_place(self):
        elevations = {Point(0, 0): 2, Point(1, 0): 0, Point(2, 0): 3,
                      Point(0, 1): 1, Point(1, 1): 9, Point(2, 1): 2,
                      Point(0, 2): 2, Point(1, 2): 0, Point(2, 2): 1}
        tiles = [Tile(point=point, elevation=elevation) if elevation != 9 else ImpassableTile(point=point)
                 for point, elevation in elevations.items()]
        map_ = Map(3, 3, tiles)

        origin = Point(1, 2)
        expected = {Point(0, 0): (6, [W, S, S]), Point(1, 0): (7, [W, S, S, E]), Point(2, 0): (6, [E, S, S]),
                    Point(0, 1): (4, [W, S]),                                    Point(2, 1): (4, [E, S]),
                    Point(0, 2): (3, [W]),       Point(1, 2): (0, []),           Point(2, 2): (2, [E])}
        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 10), expected)

    def test_get_movement_points_with_path_with_occupied_space_in_place(self):
        elevations = {Point(0, 0): 2, Point(1, 0): 0, Point(2, 0): 3,
                      Point(0, 1): 1, Point(1, 1): 0, Point(2, 1): 2,
                      Point(0, 2): 2, Point(1, 2): 0, Point(2, 2): 1}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]

        map_ = Map(3, 3, tiles)

        occupied_point = Point(1, 1)
        origin = Point(1, 2)

        map_.place_unit(Soldier(), origin)
        map_.place_unit(Soldier(), occupied_point)

        expected = {Point(0, 0): (6, [W, S, S]), Point(1, 0): (7, [W, S, S, E]), Point(2, 0): (6, [E, S, S]),
                    Point(0, 1): (4, [W, S]),                                    Point(2, 1): (4, [E, S]),
                    Point(0, 2): (3, [W]),       Point(1, 2): (0, []),           Point(2, 2): (2, [E])}
        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 10), expected)

    def test_get_movement_points_with_path_obstacle_max_mv_lte_map_size(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 9, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 3, tiles)
        origin = Point(1, 2)
        expected_four = {
            Point(0, 0): (3, [W, S, S]), Point(1, 0): (4, [W, S, S, E]), Point(2, 0): (3, [E, S, S]), Point(3, 0): (4, [E, S, S, E]),
            Point(0, 1): (2, [W, S]),                                    Point(2, 1): (2, [E, S]),    Point(3, 1): (3, [E, S, E]),
            Point(0, 2): (1, [W]),       Point(1, 2): (0, []),           Point(2, 2): (1, [E]),       Point(3, 2): (2, [E, E])}

        expected_three = {
            Point(0, 0): (3, [W, S, S]),                      Point(2, 0): (3, [E, S, S]),
            Point(0, 1): (2, [W, S]),                         Point(2, 1): (2, [E, S]),   Point(3, 1): (3, [E, S, E]),
            Point(0, 2): (1, [W]),      Point(1, 2): (0, []), Point(2, 2): (1, [E]),      Point(3, 2): (2, [E, E])}

        calculator = MovementCalculator(map_)
        # pretty_print(expected)
        # pretty_print(MovementCalculator(map_).get_movement_points_with_path(origin, 10))
        self.assertEqual(calculator.get_movement_points_with_path(origin, 4), expected_four)
        self.assertEqual(calculator.get_movement_points_with_path(origin, 3), expected_three)

    def test_get_movement_points_with_path_obstacle_lte_max_mv_will_continue_around_corner(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 3, Point(1, 1): 4, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 3, tiles)
        origin = Point(1, 2)
        expected_four = {
                                   Point(1, 0): (4, [E, S, S, W]), Point(2, 0): (3, [E, S, S]), Point(3, 0): (4, [E, S, S, E]),
                                                                   Point(2, 1): (2, [E, S]),    Point(3, 1): (3, [E, S, E]),
            Point(0, 2): (1, [W]), Point(1, 2): (0, []),           Point(2, 2): (1, [E]),       Point(3, 2): (2, [E, E])
        }

        expected_five = {
            Point(0, 0): (5, [E, S, S, W, W]), Point(1, 0): (4, [E, S, S, W]), Point(2, 0): (3, [E, S, S]), Point(3, 0): (4, [E, S, S, E]),
            Point(0, 1): (5, [W, S]),          Point(1, 1): (5, [S]),          Point(2, 1): (2, [E, S]),    Point(3, 1): (3, [E, S, E]),
            Point(0, 2): (1, [W]),             Point(1, 2): (0, []),           Point(2, 2): (1, [E]),       Point(3, 2): (2, [E, E])
        }

        ranger = MovementCalculator(map_)
        self.assertEqual(ranger.get_movement_points_with_path(origin, 5), expected_five)
        self.assertEqual(ranger.get_movement_points_with_path(origin, 4), expected_four)

    def test_get_movement_points_with_path_after_going_around_obstacle_will_recalculate_min_distance_bottom_to_top(self):
        elevations = {Point(0, 0): 9, Point(1, 0): 0, Point(2, 0): 9, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 0, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 3, Point(2, 2): 0, Point(3, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 0, Point(2, 3): 0, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(1, 3)
        expected_six = {
                                         Point(1, 0): (5, [W, S, S, E, S]),                             Point(3, 0): (5, [E, S, S, E, S]),
            Point(0, 1): (3, [W, S, S]), Point(1, 1): (4, [W, S, S, E]),   Point(2, 1): (3, [E, S, S]), Point(3, 1): (4, [E, S, S, E]),
            Point(0, 2): (2, [W, S]),    Point(1, 2): (4, [S]),            Point(2, 2): (2, [E, S]),    Point(3, 2): (3, [E, S, E]),
            Point(0, 3): (1, [W]),       Point(1, 3): (0, []),             Point(2, 3): (1, [E]),       Point(3, 3): (2, [E, E])
        }

        calculator = MovementCalculator(map_)
        self.assertEqual(calculator.get_movement_points_with_path(origin, 6), expected_six)

    def test_get_movement_points_with_path_after_going_around_obstacle_will_recalculate_min_distance_top_to_bottom(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 3, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0,
                      Point(0, 3): 9, Point(1, 3): 0, Point(2, 3): 9, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(1, 0)
        expected_six = {
            Point(0, 0): (1, [W]),       Point(1, 0): (0, []),           Point(2, 0): (1, [E]),       Point(3, 0): (2, [E, E]),
            Point(0, 1): (2, [W, N]),    Point(1, 1): (4, [N]),          Point(2, 1): (2, [E, N]),    Point(3, 1): (3, [E, E, N]),
            Point(0, 2): (3, [W, N, N]), Point(1, 2): (4, [W, N, N, E]), Point(2, 2): (3, [E, N, N]), Point(3, 2): (4, [E, E, N, N]),
                                         Point(1, 3): (5, [W, N, N, E, N]),                           Point(3, 3): (5, [E, E, N, N, N])
        }

        ranger = MovementCalculator(map_)
        self.assertEqual(ranger.get_movement_points_with_path(origin, 6), expected_six)

    def test_get_movement_points_with_path_after_going_around_obstacle_will_recalculate_min_distance_l_to_r(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 9,
                      Point(0, 1): 0, Point(1, 1): 3, Point(2, 1): 0, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 9,
                      Point(0, 3): 0, Point(1, 3): 0, Point(2, 3): 0, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(0, 1)
        expected_six = {
            Point(0, 0): (1, [S]),    Point(1, 0): (2, [S, E]),    Point(2, 0): (3, [S, E, E]),
            Point(0, 1): (0, []),     Point(1, 1): (4, [E]),       Point(2, 1): (4, [S, E, E, N]), Point(3, 1): (5, [S, E, E, N, E]),
            Point(0, 2): (1, [N]),    Point(1, 2): (2, [N, E]),    Point(2, 2): (3, [N, E, E]),
            Point(0, 3): (2, [N, N]), Point(1, 3): (3, [N, E, N]), Point(2, 3): (4, [N, E, E, N]), Point(3, 3): (5, [N, E, E, N, E])
        }

        ranger = MovementCalculator(map_)
        self.assertEqual(ranger.get_movement_points_with_path(origin, 6), expected_six)

    def test_get_movement_points_with_path_after_going_around_obstacle_will_recalculate_min_distance_r_to_l(self):
        elevations = {Point(0, 0): 9, Point(1, 0): 0, Point(2, 0): 0, Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 0, Point(2, 1): 3, Point(3, 1): 0,
                      Point(0, 2): 9, Point(1, 2): 0, Point(2, 2): 0, Point(3, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 0, Point(2, 3): 0, Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(3, 1)
        expected_six = {
                                               Point(1, 0): (3, [S, W, W]),    Point(2, 0): (2, [S, W]),    Point(3, 0): (1, [S]),
            Point(0, 1): (5, [S, W, W, N, W]), Point(1, 1): (4, [S, W, W, N]), Point(2, 1): (4, [W]),       Point(3, 1): (0, []),
                                               Point(1, 2): (3, [N, W, W]),    Point(2, 2): (2, [N, W]),    Point(3, 2): (1, [N]),
            Point(0, 3): (5, [N, W, W, N, W]), Point(1, 3): (4, [N, W, W, N]), Point(2, 3): (3, [N, W, N]), Point(3, 3): (2, [N, N])}

        ranger = MovementCalculator(map_)
        self.assertEqual(ranger.get_movement_points_with_path(origin, 6), expected_six)

    def test_get_movement_points_with_path_goes_around_obstacle_and_recalculates_on_terrain(self):
        terrains = {Point(0, 0): 1, Point(1, 0): 1, Point(2, 0): 1, Point(3, 0): 1,
                    Point(0, 1): 1, Point(1, 1): 1, Point(2, 1): 1, Point(3, 1): 1,
                    Point(0, 2): 1, Point(1, 2): 4, Point(2, 2): 9, Point(3, 2): 1,
                    Point(0, 3): 1, Point(1, 3): 1, Point(2, 3): 5, Point(3, 3): 1}
        tiles = [Tile(point=point, terrain_mv=terrain) for point, terrain in terrains.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(1, 3)
        expected_six = {
            Point(0, 0): (4, [W, S, S, S]), Point(1, 0): (5, [W, S, S, S, E]), Point(2, 0): (6, [W, S, S, S, E, E]),
            Point(0, 1): (3, [W, S, S]),    Point(1, 1): (4, [W, S, S, E]),    Point(2, 1): (5, [W, S, S, E, E]),   Point(3, 1): (6, [W, S, S, E, E, E]),
            Point(0, 2): (2, [W, S]),       Point(1, 2): (1, [S]),             Point(2, 2): (5, [S, E]),
            Point(0, 3): (1, [W]),          Point(1, 3): (0, []),              Point(2, 3): (1, [E]),               Point(3, 3): (6, [E, E])
        }

        ranger = MovementCalculator(map_)
        self.assertEqual(ranger.get_movement_points_with_path(origin, 6), expected_six)

    def test_get_movement_points_with_path_regression_test(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 11, Point(2, 0): 0,  Point(3, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 11, Point(2, 1): 11, Point(3, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 11, Point(2, 2): 11, Point(3, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 0,  Point(2, 3): 0,  Point(3, 3): 0}
        tiles = [Tile(point=point, elevation=elevation * 10) for point, elevation in elevations.items()]
        map_ = Map(4, 4, tiles)
        origin = Point(0, 0)
        expected = {
            Point(0, 0): (0,  []),
            Point(0, 1): (1,  [N]),
            Point(0, 2): (2,  [N, N]),
            Point(0, 3): (3,  [N, N, N]),
            Point(1, 3): (4,  [N, N, N, E]),
            Point(2, 3): (5,  [N, N, N, E, E]),
            Point(3, 3): (6,  [N, N, N, E, E, E]),
            Point(3, 2): (7,  [N, N, N, E, E, E, S]),
            Point(3, 1): (8,  [N, N, N, E, E, E, S, S]),
            Point(3, 0): (9,  [N, N, N, E, E, E, S, S, S]),
            Point(2, 0): (10, [N, N, N, E, E, E, S, S, S, W]),
        }
        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 20), expected)

    def test_get_movement_points_with_path_regression_test_two(self):
        elevations = {Point(0, 0): 0, Point(1, 0): 11, Point(2, 0): 0,
                      Point(0, 1): 0, Point(1, 1): 11, Point(2, 1): 0,
                      Point(0, 2): 0, Point(1, 2): 11, Point(2, 2): 0,
                      Point(0, 3): 0, Point(1, 3): 11, Point(2, 3): 0,
                      Point(0, 4): 0, Point(1, 4): 0,  Point(2, 4): 0}
        tiles = [Tile(point=point, elevation=elevation * 10) for point, elevation in elevations.items()]
        map_ = Map(3, 5, tiles)
        origin = Point(0, 0)
        expected = {
            Point(0, 0): (0,  []),
            Point(0, 1): (1,  [N]),
            Point(0, 2): (2,  [N, N]),
            Point(0, 3): (3,  [N, N, N]),
            Point(0, 4): (4,  [N, N, N, N]),
        }
        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 4), expected)

        expected = {
            Point(0, 0): (0,  []),
            Point(0, 1): (1,  [N]),
            Point(0, 2): (2,  [N, N]),
            Point(0, 3): (3,  [N, N, N]),
            Point(0, 4): (4,  [N, N, N, N]),
            Point(1, 4): (5,  [N, N, N, N, E]),
            Point(2, 4): (6,  [N, N, N, N, E, E]),
            Point(2, 3): (7,  [N, N, N, N, E, E, S]),
            Point(2, 2): (8,  [N, N, N, N, E, E, S, S]),
            Point(2, 1): (9,  [N, N, N, N, E, E, S, S, S]),
            Point(2, 0): (10, [N, N, N, N, E, E, S, S, S, S]),
        }
        self.assertEqual(MovementCalculator(map_).get_movement_points_with_path(origin, 20), expected)
