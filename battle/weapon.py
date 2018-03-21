from typing import Union
from battle.statstools.stat import PositiveStat


class OutOfAmmo(StopIteration):
    pass


class Weapon(object):
    def __init__(self, dmg: int, action_pts: int, range_: int, ammo: Union[int, float]) -> None:

        self._dmg = PositiveStat(dmg)
        self._action = PositiveStat(action_pts)
        self._range = PositiveStat(range_)
        self._ammo = PositiveStat(ammo)

    @property
    def dmg(self):
        return self._dmg.max

    @property
    def action_pts(self):
        return self._action.max

    @property
    def range(self):
        return self._range.max

    @property
    def ammo(self):
        return self._ammo.current

    @property
    def max_ammo(self):
        return self._ammo.max

    def use_weapon(self):
        if self.ammo <= 0:
            raise OutOfAmmo()
        self._ammo.modify_current(-1)
        return self.dmg

    def refill_ammo(self):
        self._ammo.reset()

    def is_melee_weapon(self):
        return isinstance(self, MeleeWeapon)


class MeleeWeapon(Weapon):
    def __init__(self, dmg, action_pts, range_=1, ammo=float('inf')):
        super(MeleeWeapon, self).__init__(dmg, action_pts, range_, ammo)


class RangedWeapon(Weapon):
    def __init__(self, dmg, action_pts, range_, ammo):
        super(RangedWeapon, self).__init__(dmg, action_pts, range_, ammo)
