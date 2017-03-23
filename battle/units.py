from battle.weapon import Weapon
from battle.base_unit import BaseUnit

FIST = Weapon(1, 1)


class Soldier(BaseUnit):
    def __init__(self):
        self._health = 100
        self._move = 3
        self._weapon = FIST
        self._point = None

    def get_point(self):
        return self._point

    def has_point(self):
        return self._point is not None

    def set_point(self, point):
        self._point = point

    def del_point(self):
        self._point = None

    def equip_weapon(self, weapon):
        self._weapon = weapon

    def attack(self, opponent):
        dmg = self._weapon.atk_dmg
        opponent.receive_dmg(dmg)

    def is_dead(self):
        return self._health <= 0

    def receive_dmg(self, dmg):
        self._health -= dmg




