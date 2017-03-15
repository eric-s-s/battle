from battle.direction import Direction as Dir


class Tile(object):
    def __init__(self, terrain, units):
        self._terrain = terrain
        self._units = units[:]
        self._directions = {Dir.N: None,
                            Dir.S: None,
                            Dir.E: None,
                            Dir.W: None}

    def get_units(self):
        pass

    def get_terrain(self):
        pass

    def get(self, direction):
        return self._directions[direction]

    def set(self, tile, direction):
        self._directions[direction] = tile

    def has_tile(self, direction):
        return not self._directions[direction] is None

    def get_tiles_at_distance(self, distance):
        too_close = [self]