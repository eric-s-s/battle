from typing import Dict, List, Union, Optional

from battle.maptools.direction import Direction
from battle.maptools.point import Point
from battle.maptools.tile import Tile
from battle.players.units import Soldier

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class MapPlacementError(ValueError):
    def __init__(self, *args):
        super(MapPlacementError, self).__init__(*args)


class Map(object):
    def __init__(self, width: int, height: int, tiles: List[Tile]):
        self._all_points = Point(0, 0).to_rectangle(width, height)
        self._tiles = dict.fromkeys(self._all_points, None)  # type: Dict[Point, Tile]
        self._points_to_units = {}  # type: Dict[Point, Soldier]
        self._units_to_points = {}  # type: Dict[Soldier, Point]

        self._lay_tiles(tiles)

    def _lay_tiles(self, tiles: List[Tile]):
        pointed, pointless = separate_tiles(tiles)
        self._lay_pointed_tiles(pointed)
        self._lay_pointless_tiles(pointless)

    def _lay_pointed_tiles(self, tiles: List[Tile]):
        for tile in tiles:
            self._raise_placement_error(tile)
            point = tile.get_point()
            self._tiles[point] = tile

    def _raise_placement_error(self, tile: Tile):
        point = tile.get_point()
        if not self.is_on_map(point) or self.has_tile(point):
            raise MapPlacementError('Occupied or missing')

    def _lay_pointless_tiles(self, tiles: List[Tile]):
        available_points = [key for key in self._all_points if not self._tiles[key]]
        _raise_too_many_tiles_error(tiles, available_points)
        for tile in tiles:
            point = available_points.pop(0)
            tile.set_point(point)
            self._tiles[point] = tile

    def get_elevation(self, point: Point) -> Union[int, float]:
        if not self.has_tile(point):
            return float('-inf')
        return self.get_tile(point).get_elevation()

    def get_size(self):
        last_point = self._all_points[-1]
        return last_point.x + 1, last_point.y + 1

    def is_on_map(self, point: Point) -> bool:
        return point in self._all_points

    def has_tile(self, point: Point) -> bool:
        return self.is_on_map(point) and self._tiles[point]

    def get_tile(self, point: Point) -> Optional[Tile]:
        return self._tiles[point]

    def can_place_unit(self, point: Point) -> bool:
        return self.has_tile(point) and self._points_to_units.get(point) is None

    def place_unit(self, unit: Soldier, point: Point):
        self._raise_unit_placement_error(point, unit)
        self._points_to_units[point] = unit
        self._units_to_points[unit] = point

    def _raise_unit_placement_error(self, point: Point, unit: Soldier):
        if not self.can_place_unit(point) or self.get_point(unit):
            raise MapPlacementError('illegal unit placement')

    def get_unit(self, point: Point) -> Optional[Soldier]:
        return self._points_to_units.get(point)

    def get_point(self, unit: Soldier) -> Point:
        return self._units_to_points.get(unit)

    def has_unit(self, point: Point) -> bool:
        return self._points_to_units.get(point) is not None

    def remove_unit(self, point: Point):
        unit = self._points_to_units[point]
        self._points_to_units[point] = None
        if unit is not None:
            del self._units_to_points[unit]

    def remove_all_units(self):
        self._points_to_units = {}
        self._units_to_points = {}


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
