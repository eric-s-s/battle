"""
this module is temporary.  It is testing out some basic ideas for Tile and enabling move_pts

"""


class Tile(object):
    @classmethod
    def blank(cls):
        return cls()

    def __init__(self, elevation=0, terrain_multiplier=1, point=None):
        self._elevation = elevation
        self._terrain_multiplier = terrain_multiplier
        self._point = point

    def get_elevation(self):
        return self._elevation

    def get_terrain_type(self):
        return self._terrain_multiplier

    def get_point(self):
        return self._point

    def del_point(self):
        self._point = None

    def set_point(self, new_point):
        self.del_point()
        self._point = new_point

    def has_point(self):
        return self._point is not None

    def move_pts(self, other_tile):
        basic_move = max(1, other_tile.get_elevation() - self._elevation + 1)
        return self._terrain_multiplier * basic_move



