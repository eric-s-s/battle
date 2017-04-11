from battle.unit_movement import UnitMovement
from battle.weapon import Weapon
from battle.map import Map
from battle.maptools.point import Point
from battle.maptools.direction import Direction

FIST = Weapon(1, 1)


class Soldier(object):
    def __init__(self, map_: Map = None, max_move: int = 3):
        self._max_health = 100
        self._current_health = self._max_health
        self._weapon = FIST
        self._movement = UnitMovement(map_=map_, max_move=max_move)

    def place(self, point: Point, map_: Map = None):
        if map_:
            self._movement.set_map(map_)
        self._movement.set_point(point)

    def move(self, direction: Direction):
        self._movement.move(direction)

    def get_health(self) -> int:
        return self._current_health

    def get_weapon(self) -> Weapon:
        return self._weapon

    def equip_weapon(self, weapon: Weapon):
        self._weapon = weapon

    def attack(self, opponent):
        dmg = self._weapon.atk_dmg
        opponent.receive_dmg(dmg)

    def is_dead(self) -> bool:
        return self._current_health <= 0

    def receive_dmg(self, dmg: int):
        if dmg < 0:
            raise ValueError('damage can\'t be less than zero')
        self._current_health -= dmg

    def heal(self, health_pts: int):
        """cannot heal past max"""
        if health_pts < 0:
            raise ValueError('health_pts can\'t be less than zero')
        if self.is_dead():
            return None
        self._current_health = min(self._current_health + health_pts, self._max_health)

    def rest(self):
        """heal and reset_move"""
        raise NotImplementedError


class Example(Soldier):
    def __init__(self, weapon: Weapon, **kwargs):
        super(Example, self).__init__(**kwargs)
        self.equip_weapon(weapon)



