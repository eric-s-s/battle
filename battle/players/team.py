from typing import List

from battle.maptools.map import Map
from battle.movement_tracker import MovementTracker
from battle.players.units import Soldier


class Team(object):
    def __init__(self, team_name, map_: Map):
        self._team_name = team_name
        self._team_players = set()
        self._map = map_
        self._mv_track = MovementTracker(self._map)

    @property
    def players(self):
        return self._team_players.copy()

    @property
    def mv_track(self):
        return self._mv_track

    def add_player(self, player: Soldier):
        self._team_players.add(player)

    def del_player(self, player: Soldier):
        try:
            self._team_players.remove(player)
        except KeyError:
            raise ValueError('player isn\'t in the team')

    def is_on_team(self, player: Soldier):
        return player in self.players

    def coordinates(self):
        t_coords = {}
        for player in self.players:
            t_coords[player] = self.mv_track.get_point(player)
        return t_coords

    def charge(self):
        raise NotImplementedError
