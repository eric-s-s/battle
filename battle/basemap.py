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









