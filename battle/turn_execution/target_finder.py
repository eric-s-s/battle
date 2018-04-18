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
        distance_to_points = self._rf.get_sight_ranges_units_only(self._map.get_point(unit), sight_range)
        ally_team = self.get_team(unit)
        del distance_to_points[0]

        for distance, points in distance_to_points.items():
            for point in points:
                possible = self._map.get_unit(point)
                if ally_team.is_on_team(possible):
                    allies_to_distances[possible] = distance
        return allies_to_distances

    def enemies_in_sight(self, unit: Soldier):
        """{unit: distance}"""
        enemies_to_distances = {}
        sight_range = unit.get_sight_range()
        distance_to_points = self._rf.get_sight_ranges_units_only(self._map.get_point(unit), sight_range)
        ally_team = self.get_team(unit)
        del distance_to_points[0]

        for distance, points in distance_to_points.items():
            for point in points:
                possible = self._map.get_unit(point)
                if not ally_team.is_on_team(possible):
                    enemies_to_distances[possible] = distance
        return enemies_to_distances

    def allies_in_range(self, unit: Soldier):
        """
        point, unit, distance, advantage - {unit: (distance, advantage)}
        """
        units_to_distance_advantage = {}
        weapon = unit.get_weapon()
        weapon_range = weapon.range
        is_melee = weapon.is_melee_weapon()
        ally_team = self.get_team(unit)

        if is_melee:
            range_method = self._rf.get_attack_ranges_melee_units_only
        else:
            range_method = self._rf.get_attack_ranges_ranged_units_only

        distance_to_point_advantage = range_method(self._map.get_point(unit), weapon_range)
        del distance_to_point_advantage[0]

        for distance, point_advantages in distance_to_point_advantage.items():
            for point, advantage in point_advantages:
                possible = self._map.get_unit(point)
                if ally_team.is_on_team(possible):
                    units_to_distance_advantage[possible] = (distance, advantage)
        return units_to_distance_advantage

    def enemies_in_range(self, unit: Soldier):
        """
                point, unit, distance, advantage - {unit: (distance, advantage)}
                """
        units_to_distance_advantage = {}
        weapon = unit.get_weapon()
        weapon_range = weapon.range
        is_melee = weapon.is_melee_weapon()
        ally_team = self.get_team(unit)

        if is_melee:
            range_method = self._rf.get_attack_ranges_melee_units_only
        else:
            range_method = self._rf.get_attack_ranges_ranged_units_only

        distance_to_point_advantage = range_method(self._map.get_point(unit), weapon_range)
        del distance_to_point_advantage[0]

        for distance, point_advantages in distance_to_point_advantage.items():
            for point, advantage in point_advantages:
                possible = self._map.get_unit(point)
                if not ally_team.is_on_team(possible):
                    units_to_distance_advantage[possible] = (distance, advantage)
        return units_to_distance_advantage

    def allies_at_move_points(self, unit: Soldier):
        """{unit: mvpts}"""
        pass

    def enemies_at_move_points(self, unit: Soldier):
        """{unit: mvpts}"""
        pass


