from battle.players.units import Soldier
from battle.maptools.map import Map
from battle.movement_tracker import MovementTracker
from typing import List, Dict

class Teams(object):
    def __init__(self, t_name, map_: Map):
        self._team_name = t_name
        self._team_players = None #type: List[Soldier]
        self._map = map_
        self.mv_track = MovementTracker(self._map)

    def add_players(self, player: Soldier):
        if player.has_team():
            player.get_team().del_player(player)
        self._team_players.append(player)

    def del_player(self, player: Soldier):
        self._team_players.remove(player)

    def check_players(self):
        return self._team_players

    def team_coords(self):
        t_coords = {}
        for player in self.check_players():
            t_coords[player] = self.mv_track.get_point(player)
        return t_coords
    