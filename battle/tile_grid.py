from battle.direction import Direction

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class TileGrid(object):
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._array = []
        self._populate_array()

    def _populate_array(self):
        for _ in range(self._rows):
            row = [None] * self._cols
            self._array.append(row)

    def get_size(self):
        return self._rows, self._cols

    def get_tile(self, row, col):
        return self._array[row][col]

    def has_tile(self, row, col):
        return self.is_in_grid(row, col) and self.get_tile(row, col) is not None

    def place_tile(self, tile, row, col):
        self._array[row][col] = tile
        adjacent = {N: (row - 1, col), S: (row + 1, col), W: (row, col - 1), E: (row, col + 1)}
        for direction, coordinates in adjacent.items():
            if self.has_tile(*coordinates):
                old_tile = self.get_tile(*coordinates)
                tile.set(old_tile, direction)
                old_tile.set(tile, direction.opposite())

    def is_in_grid(self, row, col):
        return 0 <= row < self._rows and 0 <= col < self._cols

