from battle.weapon import Weapon


class EquipmentManager(object):
    def __init__(self):
        self._weapon = None  # type: Weapon
        self._armor = None  # type: Weapon
        self._equipment = {}

    def equip_weapon(self, weapon: Weapon) -> None:
        self._weapon = weapon


