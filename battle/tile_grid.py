from battle.point import Point
from battle.direction import Direction

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class TileGrid(object):
    def __init__(self, x_slots, y_slots):
        self._x_slots = x_slots
        self._y_slots = y_slots
        self._array = []
        self._populate_array()

    def _populate_array(self):
        for _ in range(self._y_slots):
            row = [None] * self._x_slots
            self._array.append(row)

    def get_size(self):
        return self._x_slots, self._y_slots

    def get_tile(self, point):

        return self._array[point.y][point.x]

    def has_tile(self, point):
        return self.is_in_grid(point) and self.get_tile(point) is not None

    def place_tile(self, tile, point):

        self._array[point.y][point.x] = tile
        adjacent = {N: point.north(), S: point.south(), W: point.west(), E: point.east()}
        for direction, coordinates in adjacent.items():
            if self.has_tile(coordinates):
                old_tile = self.get_tile(coordinates)
                tile.set(old_tile, direction)
                old_tile.set(tile, direction.opposite())

    def is_in_grid(self, point):
        return 0 <= point.x < self._x_slots and 0 <= point.y < self._y_slots

    def get_tiles_dictionary(self, point, distance):
        all_coordinates = get_coordinate_sets(point, distance)
        out = {num: [] for num in range(distance + 1)}
        for key, pt_list in all_coordinates.items():
            for pt in pt_list:
                if self.has_tile(pt):
                    out[key].append(self.get_tile(pt))
        return out


def get_coordinate_sets(origin, distances):
    return {distance: get_coordinates_from(origin, distance) for distance in range(distances + 1)}


def get_coordinates_from(origin, distance):
    out = []
    if distance == 0:
        return [origin]
    for delta_x in range(distance + 1):
        to_add = get_combos(delta_x, distance, origin)
        out += to_add
    return out


def get_combos(delta_x, distance, point):
    delta_y = distance - delta_x
    if delta_x == 0:
        to_add = [point.plus_y(delta_y), point.plus_y(- delta_y)]
    elif delta_y == 0:
        to_add = [point.plus_x(delta_x), point.plus_x(- delta_x)]
    else:
        to_add = [point.plus(delta_x, delta_y),
                  point.plus(- delta_x, delta_y),
                  point.plus(delta_x, - delta_y),
                  point.plus(- delta_x, - delta_y)]
    return to_add


from battle.tile import Tile

def create_test_grid(size):
    to_test = TileGrid(size, size)
    for x in range(size):
        for y in range(size):
            to_test.place_tile(Tile('{}, {}'.format(x, y)), Point(x, y))
    return to_test


def get_middle(test_grid):
    x, y = test_grid.get_size()
    return test_grid.get_tile(x // 2, y // 2)


