from battle.maptools.direction import Direction
from battle.maptools.point import Point
from battle.tile import Tile, TileOccupationError
from battle.maptools.tile_grid import TileGrid

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class MapPlacementError(ValueError):
    def __init__(self, *args, **kwargs):
        super(MapPlacementError, self).__init__(*args, **kwargs)


class Map(object):
    def __init__(self, width, height, tiles=None, units=None):
        self._all_points = Point(0, 0).to_rectangle(width, height)
        self._tiles = dict.fromkeys(self._all_points, None)
        self._lay_tiles(tiles)

    def _lay_tiles(self, tiles):
        pointed, pointless = separate_tiles(tiles)
        self._lay_pointed_tiles(pointed)
        self._lay_pointless_tiles(pointless)

    def _lay_pointed_tiles(self, tiles):
        for tile in tiles:
            self._raise_placement_error(tile)
            self.connect(tile)

    def _raise_placement_error(self, tile):
        point = tile.get_point()
        if not self.is_on_map(point) or self.has_tile(point):
            raise MapPlacementError('Occupied or missing')

    def _lay_pointless_tiles(self, tiles):
        available_points = [key for key in self._all_points if not self._tiles[key]]
        _raise_too_many_tiles_error(tiles, available_points)
        for tile in tiles:
            tile.set_point(available_points.pop(0))
            self.connect(tile)

    def connect(self, pointed_tile):
        point = pointed_tile.get_point()
        self._tiles[point] = pointed_tile
        for direction in Direction:
            connect_point = point.in_direction(direction)
            if self.has_tile(connect_point):
                old_tile = self.get_tile(connect_point)
                pointed_tile.set(old_tile, direction)
                old_tile.set(pointed_tile, direction.opposite())

    def is_on_map(self, point):
        return point in self._all_points

    def has_tile(self, point):
        return self.is_on_map(point) and self._tiles[point]

    def get_tile(self, point):
        return self._tiles[point]

    def get_unit(self, x_y_):
        return self.get_tile(x_y_).pop_unit()

    def move_unit(self, point, direction):
        current = self.get_tile(point)
        destination = self.get_tile(point.in_direction(direction))


def separate_tiles(tiles):
    haves = []
    have_nots = []
    for tile in tiles:
        if tile.has_point():
            haves.append(tile)
        else:
            have_nots.append(tile)
    return haves, have_nots


def _raise_too_many_tiles_error(tiles, points):
    if len(tiles) > len(points):
        raise MapPlacementError('not enough points on map')
