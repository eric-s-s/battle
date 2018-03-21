from typing import List

from battle.players.team import Team
from battle.players.units import Soldier
from battle.maptools.map import Map
from battle.rangefinder import RangeFinder


class TargetFinder(object):
    def __init__(self, map_: Map, teams: List[Team]):
        self._map = map_
        self._teams = teams[:]
        self._rf = RangeFinder(self._map)

    def get_team(self, unit: Soldier):
        for team in self._teams:
            if team.is_on_team(unit):
                return team

    def allies_in_sight(self, unit: Soldier):
        """{unit: distance}"""
        allies_to_distances = {}
        sight_range = unit.get_sight_range()
        distance_to_points = self._rf.get_sight_ranges(self._map.get_point(unit), sight_range)
        del distance_to_points[0]
        for distance, points in distance_to_points.items():
            for point in points:
                possible = self._map.get_unit(point)
                if possible is not None:
                    team = self.get_team(possible)
                    if team == self.get_team(unit):
                        allies_to_distances[possible] = distance
        return allies_to_distances

    def enemies_in_sight(self, unit: Soldier):
        """{unit: distance}"""
        output = {}
        distance_to_points = self._rf.get_sight_ranges(self._map.get_point(unit), 10)
        for distance, points in distance_to_points:
            for point in points:
                possible = self._map.get_unit(point)
                if possible is not None:
                    team = self.get_team(possible)
                    if team != self.get_team(unit):
                        output[possible] = distance
        return output

    def allies_in_range(self, unit: Soldier):
        """
        point, unit, distance, advantage - {unit: (distance, advantage)}
        """


    def enemies_in_range(self, unit: Soldier):
        """
                point, unit, distance, advantage - {unit: (distance, advantage)}
                """
        weapon = unit.get_weapon()
        weapon_range = weapon.range
        is_melee = weapon.is_melee_weapon()
        ally_team = self.get_team(unit)
        if is_melee:
            distance_to_point_advantage_list = self._rf.get_attack_ranges_melee(self._map.get_point(unit), weapon_range)
        else:
            distance_to_point_advantage_list = self._rf.get_attack_ranges_ranged(self._map.get_point(unit), weapon_range)

    def allies_at_move_points(self, unit: Soldier):
        """{unit: mvpts}"""
        pass

    def enemies_at_move_points(self, unit: Soldier):
        """{unit: mvpts}"""
        pass


