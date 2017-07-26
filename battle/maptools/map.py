from typing import Dict, List

from battle.maptools.direction import Direction
from battle.maptools.point import Point
from battle.maptools.tile import Tile, ImpassableTile
from battle.units import Soldier
from battle.maptools.groundmap import GroundMap, GroundMapPlacementError
from battle.maptools.airmap import AirMap

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class MapPlacementError(ValueError):
    def __init__(self, *args, **kwargs):
        super(MapPlacementError, self).__init__(*args, **kwargs)


class Map(object):
    def __init__(self, width: int, height: int, tiles: List[Tile]):
        try:
            self._ground_map = GroundMap(width, height, tiles)
            self._air_map = AirMap(width, height, tiles)
        except GroundMapPlacementError as error:
            message = error.args[0]
            raise MapPlacementError(message)

    def get_size(self):
        return self._ground_map.get_size()

    def is_on_map(self, point: Point) -> bool:
        return self._ground_map.is_on_map(point)

    def has_tile(self, point: Point) -> bool:
        return self._ground_map.has_tile(point)

    def get_tile(self, point: Point) -> Tile:
        return self._ground_map.get_tile(point)

    def can_place_unit(self, point: Point, elevation: int = None) -> bool:
        return self._ground_map.can_place_unit(point)

    def place_unit(self, unit: Soldier, point: Point, elevation: int = None):
        try:
            self._ground_map.place_unit(unit, point)
        except GroundMapPlacementError as error:
            message = error.args[0]
            raise MapPlacementError(message)

    def _raise_unit_placement_error(self, point: Point):
        if not self.can_place_unit(point):
            raise MapPlacementError('illegal unit placement')

    def get_unit(self, point: Point, elevation: int = None) -> Soldier:
        return self._ground_map.get_unit(point)

    def has_unit(self, point: Point, elevation: int = None) -> bool:
        return self._ground_map.has_unit(point)

    def remove_unit(self, point: Point, elevation: int = None):
        self._ground_map.remove_unit(point)

    def remove_all_units(self):
       self._ground_map.remove_all_units()


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
