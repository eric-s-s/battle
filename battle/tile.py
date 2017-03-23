from battle.maptools.direction import Direction as Dir


class TileOccupationError(ValueError):
    def __init__(self, msg='', *args, **kwargs):
        super(TileOccupationError, self).__init__(msg, *args, **kwargs)


class Tile(object):
    @classmethod
    def blank(cls):
        return cls('blank')

    def __init__(self, terrain, point=None):
        self._terrain = terrain
        self._point = point
        self._directions = {Dir.N: None,
                            Dir.S: None,
                            Dir.E: None,
                            Dir.W: None}

    def get_point(self):
        return self._point

    def del_point(self):
        self._point = None
        for direction in Dir:
            self.set(None, direction)

    def set_point(self, new_point):
        self.del_point()
        self._point = new_point

    def has_point(self):
        return self._point is not None

    def get_terrain(self):
        return self._terrain

    def get(self, direction):
        return self._directions[direction]

    def get_all(self):
        return [self.get(direction) for direction in Dir if self.has_tile(direction)]

    def set(self, tile, direction):
        self._directions[direction] = tile

    def has_tile(self, direction):
        return not self._directions[direction] is None





