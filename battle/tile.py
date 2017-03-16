from battle.direction import Direction as Dir


class TileOccupationError(ValueError):
    def __init__(self, msg='', *args, **kwargs):
        super(TileOccupationError, self).__init__(msg, *args, **kwargs)


class Tile(object):
    def __init__(self, terrain, unit=None):
        self._terrain = terrain
        self._unit = unit
        self._directions = {Dir.N: None,
                            Dir.S: None,
                            Dir.E: None,
                            Dir.W: None}

    def get_unit(self):
        return self._unit

    def is_empty(self):
        return self._unit is None

    def remove_unit(self):
        self._unit = None

    def assign_unit(self, unit):
        if not self.is_empty():
            raise TileOccupationError('Occupied!')
        self._unit = unit

    def pop_unit(self):
        out = self._unit
        self._unit = None
        return out

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

    def distance_dictionary(self, distance):
        if distance == 1:
            return {0: [self], 1: self.get_all()}
        base_dict = self.distance_dictionary(distance - 1)
        to_add = []
        too_close = base_dict[distance - 2]
        for tile in base_dict[distance - 1]:
            raw_list = tile.get_all()
            exclude = to_add + too_close
            to_concat = [el for el in raw_list if el not in exclude]
            to_add += to_concat
        base_dict[distance] = to_add
        return base_dict




