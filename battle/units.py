from battle.weapon import Weapon

FIST = Weapon(1)


class Soldier(object):
    def __init__(self):
        self._health = 100
        self._move = 3
        self._weapon = FIST

    def equip_weapon(self, weapon):
        self._weapon = weapon

    def attack(self, opponent):
        dmg = self._weapon.atk_dmg
        opponent.receive_dmg(dmg)

    def is_dead(self):
        return self._health <= 0

    def receive_dmg(self, dmg):
        self._health -= dmg




