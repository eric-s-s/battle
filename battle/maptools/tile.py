from typing import Union
from battle.maptools.point import Point
from battle.maptools.footprint import FootPrintPackage, FootPrint


class Tile(object):
    def __init__(self, elevation: Union[int, float] = 0, terrain_mv: int = 1, point: Point = None, max_footprints=10):
        if elevation != float('inf'):
            elevation = int(elevation)
        self._elevation = elevation

        self._terrain_mv = max(terrain_mv, 1)
        self._point = point
        self._fpp = FootPrintPackage(max_size=max_footprints)

    def add_footprint(self, footprint: FootPrint):
        self._fpp.push(footprint)

    def footprint_vectors(self):
        return self._fpp.team_vectors()

    def get_elevation(self) -> Union[int, float]:
        return self._elevation

    def get_terrain_mv(self) -> int:
        return self._terrain_mv

    def get_point(self) -> Point:
        return self._point

    def del_point(self) -> None:
        self._point = None

    def set_point(self, new_point) -> None:
        self.del_point()
        self._point = new_point

    def has_point(self) -> bool:
        return self._point is not None

    def move_pts(self, other_tile) -> Union[int, float]:
        if other_tile is self:
            return 0
        basic_move = max(0, other_tile.get_elevation() - self._elevation)
        return self._terrain_mv + basic_move


class ImpassableTile(Tile):
    def __init__(self, terrain_mv=1, point=None):
        elevation = float('inf')
        super(ImpassableTile, self).__init__(elevation, terrain_mv, point)
