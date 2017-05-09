class Tile(object):
    @classmethod
    def blank(cls):
        return cls('blank')

    def __init__(self, terrain, point=None):
        self._terrain = terrain
        self._point = point

    def get_point(self):
        return self._point

    def del_point(self):
        self._point = None

    def set_point(self, new_point):
        self.del_point()
        self._point = new_point

    def has_point(self):
        return self._point is not None

    def get_terrain(self):
        return self._terrain

    def move_pts(self, other_tile):
        return 1



