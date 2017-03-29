from battle.base_unit import BaseUnit
from battle.weapon import Weapon

FIST = Weapon(1, 1)


class Soldier(BaseUnit):
    def __init__(self):
        self._health = 100
        self._move = 3
        self._weapon = FIST
        super(Soldier, self).__init__()

    def get_weapon(self) -> Weapon:
        return self._weapon

    def equip_weapon(self, weapon: Weapon):
        self._weapon = weapon

    def attack(self, opponent):
        dmg = self._weapon.atk_dmg
        opponent.receive_dmg(dmg)

    def is_dead(self) -> bool:
        return self._health <= 0

    def receive_dmg(self, dmg: int):
        self._health -= dmg

    def get_health(self) -> int:
        return self._health



