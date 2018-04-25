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
        """

                :param unit:
                :return: {unit: distance}
                """
        units_in_sight = self.units_in_sight(unit)
        return self.filter_for_allies(unit, units_in_sight)

    def enemies_in_sight(self, unit: Soldier):
        """

                :param unit:
                :return: {unit: distance}
                """
        units_in_sight = self.units_in_sight(unit)
        return self.filter_for_enemies(unit, units_in_sight)

    def allies_in_range(self, unit: Soldier):
        """

                :param unit:
                :return: {unit: (distance, advantage)}
                """
        units_in_range = self.units_in_range(unit)
        return self.filter_for_allies(unit, units_in_range)

    def enemies_in_range(self, unit: Soldier):
        """

                :param unit:
                :return: {unit: (distance, advantage)}
                """
        units_in_range = self.units_in_range(unit)
        return self.filter_for_enemies(unit, units_in_range)

    def units_in_sight(self, unit: Soldier):
        """

                :param unit:
                :return: units_to_distances
                """

        sight_range = unit.get_sight_range()
        origin = self._map.get_point(unit)
        distance_to_points = self._rf.get_sight_ranges_units_only(origin, sight_range)
        del distance_to_points[0]
        return {self._map.get_unit(point): distance
                for distance, points in distance_to_points.items()
                for point in points}

    def units_in_range(self, unit: Soldier):
        weapon = unit.get_weapon()
        weapon_range = weapon.range
        origin = self._map.get_point(unit)
        if weapon.is_melee_weapon():
            range_method = self._rf.get_attack_ranges_melee_units_only
        else:
            range_method = self._rf.get_attack_ranges_ranged_units_only
        distance_to_point_advantage = range_method(origin, weapon_range)
        del distance_to_point_advantage[0]
        return {self._map.get_unit(point_advantage[0]): (distance, point_advantage[1])
                for distance, point_advantage_list in distance_to_point_advantage.items()
                for point_advantage in point_advantage_list}

    def filter_for_allies(self, unit: Soldier, data: dict):
        team = self.get_team(unit)
        return {key: value for key, value in data.items() if team.is_on_team(key)}

    def filter_for_enemies(self, unit: Soldier, data: dict):
        team = self.get_team(unit)
        return {key: value for key, value in data.items() if not team.is_on_team(key)}

    def allies_at_move_points(self, unit: Soldier):
        """{unit: mvpts}"""
        pass

    def enemies_at_move_points(self, unit: Soldier):
        """{unit: mvpts}"""
        pass

    # def filter(self, unit: Soldier, max_val: int, values_filter):
    #     """
    #             your filter functions give keys of distance and values of [point | (point, advantage) | (point, path)]. You
    #             must then convert to {unit: [distance | (distance, advantage) | (distance, path)]
    #             :param unit:  durrrr
    #             :param max_val:  range, sight, move_points ...
    #             :param values_filter:   A METHOD!!!!  applies filter to max_val and returns appropriate values
    #             :return:  dictionary of unit: values returned by values filter
    #             """
    #     my_filter_function =
    #     unfiltered_dict = {}
    #     origin = self._map.get_point(unit)
    #     sight_dict = self._rf.get_sight_ranges_units_only(origin, max_val)
    #     melee_dict = self._rf.get_attack_ranges_melee_units_only(origin, max_val)
    #     ranged_dict = self._rf.get_attack_ranges_ranged_units_only(origin, max_val)
    #     path_dict = {}
    #     for
    #         unfiltered_dict



