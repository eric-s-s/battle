from typing import List, Optional

from battle.maptools.tile import Tile
from battle.maptools.map import Map
from battle.players.team import Team
from battle.players.units import Soldier


class InformationRetrieval(object):
    def __init__(self, map_: Map, teams: List[Team]):
        self._map = map_
        colors = iter(['red', 'green', 'blue', 'yellow'])
        self._teams = {team: next(colors) for team in teams}

    def get_tile(self, pt) -> Tile:
        return self._map.get_tile(pt)

    def get_unit(self, pt) -> Soldier:
        return self._map.get_unit(pt)

    def get_team_color(self, unit: Optional[Soldier]) -> Optional[str]:
        if unit is None:
            return None
        for team, color in self._teams.items():
            if team.is_on_team(unit):
                return color
        return None



