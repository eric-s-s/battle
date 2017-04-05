from battle.maptools.direction import Direction
from battle.maptools.point import Point

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class MapPlacementError(ValueError):
    def __init__(self, *args, **kwargs):
        super(MapPlacementError, self).__init__(*args, **kwargs)


class Map(object):
    def __init__(self, width: int, height: int, tiles: list, units=None):
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

    def can_place_unit(self, point):
        return self.has_tile(point) and self._units[point] is None

    def place_unit(self, unit, point):
        self._raise_unit_placement_error(point)
        self._units[point] = unit
        unit.set_point(point)
        unit.set_map(self)

    def _raise_unit_placement_error(self, point):
        if not self.can_place_unit(point):
            raise MapPlacementError('illegal unit placement')

    def get_unit(self, point):
        return self._units[point]

    def remove_unit(self, unit):
        if unit.has_point():
            point = unit.get_point()
            self._units[point] = None
            unit.del_point()
        return unit

    def move_unit(self, unit, direction):
        movement_pts = 0

        if not unit.has_point():
            raise MapPlacementError('tried to move unit not on map')

        point = unit.get_point()
        new_point = point.in_direction(direction)
        if self.can_place_unit(new_point):
            movement_pts = 1
            self.remove_unit(unit)
            self.place_unit(unit, new_point)

        return movement_pts


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
