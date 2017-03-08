from enum import Enum


class Direction(Enum):
    N = 'n'
    S = 's'
    W = 'w'
    E = 'e'

    def opposite(self):
        opposites = {self.N: self.S, self.S: self.N, self.E: self.W, self.W: self.E}
        return opposites[self]

    def left(self):
        lefts = {self.N: self.W, self.W: self.S, self.S: self.E, self.E: self.N}
        return lefts[self]

    def right(self):
        rights = {self.N: self.E, self.E: self.S, self.S: self.W, self.W: self.N}
        return rights[self]


class BaseMap(object):
    def __init__(self):
        self.set_terrain()

    def set_terrain(self):
        raise NotImplementedError

    def get_size(self):
        raise NotImplementedError

    def distance(self, tile_1, tile_2):
        raise NotImplementedError

    def adjacent_tiles(self, tile):
        raise NotImplementedError

    def get_terrain(self, tile):
        raise NotImplementedError

    def get_units(self, tile):
        raise NotImplementedError


class Tile(object):
    def __init__(self, map_, map_location):
        self._map = map_
        self._map_loc = map_location
        self._directions = {Direction.N: None,
                            Direction.S: None,
                            Direction.E: None,
                            Direction.W: None}

    def get_units(self):
        pass

    def get_terrain(self):
        pass

    def get(self, direction):
        return self._directions[direction]

    def set(self, tile, direction):
        self._directions[direction] = tile





