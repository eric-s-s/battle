from battle.maptools.direction import Direction
from battle.maptools.point import Point

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class MapPlacementError(ValueError):
    def __init__(self, *args, **kwargs):
        super(MapPlacementError, self).__init__(*args, **kwargs)


class Map(object):
    def __init__(self, width: int, height: int, tiles: list):
        self._all_points = Point(0, 0).to_rectangle(width, height)
        self._tiles = dict.fromkeys(self._all_points, None)
        self._units = dict.fromkeys(self._all_points, None)

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

    def is_on_map(self, point):
        return point in self._all_points

    def has_tile(self, point):
        return self.is_on_map(point) and self._tiles[point]

    def get_tile(self, point):
        return self._tiles[point]

    def can_place_unit(self, point):
        return self.has_tile(point) and self._units[point] is None

    def place_unit(self, unit, point):
        self._raise_unit_placement_error(point)
        self._units[point] = unit

    def _raise_unit_placement_error(self, point):
        if not self.can_place_unit(point):
            raise MapPlacementError('illegal unit placement')

    def get_unit(self, point):
        return self._units[point]

    def has_unit(self, point: Point) -> bool:
        return self._units[point] is not None

    def remove_unit(self, point: Point):
        self._units[point] = None

    def remove_all_units(self):
        for key in self._units:
            self._units[key] = None


def separate_tiles(tiles):
    has_point = []
    not_has_point = []
    for tile in tiles:
        if tile.has_point():
            has_point.append(tile)
        else:
            not_has_point.append(tile)
    return has_point, not_has_point


def _raise_too_many_tiles_error(tiles, points):
    if len(tiles) > len(points):
        raise MapPlacementError('not enough points on map')
