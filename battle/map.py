from battle.maptools.direction import Direction
from battle.maptools.point import Point
from battle.tile import Tile, TileOccupationError
from battle.maptools.tile_grid import TileGrid

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class Map(object):
    def __init__(self, width, height, tile_array=None, units=None):
        if units is None:
            units = []
        self._units = units[:]
        self._grid = TileGrid(width, height)
        if tile_array is None:
            tile_array = get_blank_array(width, height)
        self._lay_tiles(tile_array)

    def _lay_tiles(self, tile_array):
        for y, row in enumerate(tile_array):
            for x, tile in enumerate(row):
                self._grid.place_tile(tile, Point(x, y))

    def get_tile(self, point):
        return self._grid.get_tile(point)

    def get_unit(self, x_y_):
        return self.get_tile(x_y_).pop_unit()

    def move_unit(self, point, direction):
        current = self.get_tile(point)
        destination = self.get_tile(point.in_direction(direction))




def get_blank_array(width, height):
    out = []
    for y in range(height):
        row = [Tile('{}, {}'.format(x, y)) for x in range(width)]
        out.append(row)
    return out
