import tkinter as tk

from gui.info import InformationRetrieval

from battle.maptools.tile import Tile

from battle.maptools.point import Point

from battle.maptools.footprint import FootPrint, FootPrintPackage


class TileDisplay(tk.Frame):
    def __init__(self, point: Point, info: InformationRetrieval, *args, **kwargs):

        self._point = point
        self._info = info
        super(TileDisplay, self).__init__(*args, **kwargs)

        self._tile = info.get_tile(point)
        self.elevation = self._tile.get_elevation()
        self.terrain = self._tile.get_terrain_mv()

    def set_display(self):
        unit = self._info.get_unit(self._point)
        color = self._info.get_team_color(unit)

    def get_fp(self):
        return self._tile.footprint_vectors()



