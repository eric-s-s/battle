import unittest

from battle.basemap import BaseMap


class MockMap(BaseMap):
    def __init__(self, size):
        self._size = size
        super(MockMap, self).__init__()

    def set_terrain(self):
        pass


class TestBaseMap(unittest.TestCase):
    def setUp(self):
        self.map = MockMap(10)
