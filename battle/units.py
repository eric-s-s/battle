from battle.base_unit import BaseUnit
from battle.weapon import Weapon

FIST = Weapon(1, 1)


class Soldier(BaseUnit):
    def __init__(self):
        self._max_health = 100
        self._max_move = 3
        self._current_health = self._max_health
        self._current_move = self._max_move
        self._weapon = FIST
        super(Soldier, self).__init__()

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
        raise NotImplementedError

    def move(self, move_pts: int):
        """cannot move if currentt is max"""
        raise NotImplementedError

    def can_move(self) -> bool:
        raise NotImplementedError
    
    def reset_move(self):
        raise NotImplementedError

    def rest(self):
        """heal and reset_move"""
        raise NotImplementedError




class Example(Soldier):
    def __init__(self, weapon: Weapon):
        super(Example, self).__init__()
        self.equip_weapon(weapon)



