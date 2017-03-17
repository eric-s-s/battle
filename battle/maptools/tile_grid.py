from battle.maptools.direction import Direction

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
        for direction in Direction:
            new_point = point.in_direction(direction)
            if self.has_tile(new_point):
                old_tile = self.get_tile(new_point)
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
    return {distance: origin.at_distance(distance) for distance in range(distances + 1)}
