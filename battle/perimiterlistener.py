from battle.rangefinder import RangeFinder
from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.units import Soldier


class PerimeterListener(object):
    def __init__(self, map_: Map) -> None:
        self._map = map_
        self._range_finder = RangeFinder(self._map)
        map_pts = Point(0, 0).to_rectangle(*self._map.get_size())
        self._watchers_at_point = dict.fromkeys(map_pts, set())

    def set_perimeter(self, unit: Soldier, point: Point):
        range_dict = self._get_range_dict(unit, point)
        for point in range_dict.keys():
            self._watchers_at_point[point].add(unit)

    def _get_range_dict(self, unit, point):
        max_range = unit.get_perimeter_size()
        if unit.get_weapon().is_ranged:
            range_dict = self._range_finder.get_attack_ranges_ranged(point, max_range)
        else:
            range_dict = self._range_finder.get_attack_ranges_melee(point, max_range)
        return range_dict

    def rm_perimeter(self, unit: Soldier):
        for units in self._watchers_at_point.values():
            units.discard(unit)

    def get_attackers(self, point: Point) -> set:
        return self._watchers_at_point[point].copy()
