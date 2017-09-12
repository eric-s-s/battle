from collections import namedtuple
from typing import Union


WeaponStats = namedtuple('WeaponStats', 'dmg, action_pts, range, max_ammo, ammo')


class OutOfAmmo(StopIteration):
    pass


class Weapon(object):
    def __init__(self, dmg: int, action_pts: int, range_: int,
                 max_ammo: Union[int, float], ranged: bool):
        self._raise_error_for_bad_input(dmg, action_pts, range_)
        self._atk_dmg = dmg
        self._range = range_
        self._current_ammo = max_ammo
        self._max_ammo = max_ammo
        self._ranged = ranged
        self._action_pts = action_pts

    @staticmethod
    def _raise_error_for_bad_input(atk_dmg, action_pts, range_):
        if atk_dmg <= 0 or action_pts <= 0 or range_ <= 0:
            raise ValueError('dmg, action_pts and range_ must be grater than zero.')

    def get_stats(self):
        return WeaponStats(dmg=self._atk_dmg,
                           action_pts=self._action_pts,
                           range=self._range,
                           max_ammo=self._max_ammo,
                           ammo=self._current_ammo
                           )

    @property
    def is_ranged(self):
        return self._ranged

    def use_weapon(self):
        if self._current_ammo <= 0:
            raise OutOfAmmo()
        self._current_ammo -= 1
        return self._atk_dmg

    def refill_ammo(self):
        self._current_ammo = self._max_ammo


class MeleeWeapon(Weapon):
    def __init__(self, dmg, action_pts, range_=1, max_ammo=float('inf')):
        super(MeleeWeapon, self).__init__(dmg, action_pts, range_, max_ammo, ranged=False)


class RangedWeapon(Weapon):
    def __init__(self, dmg, action_pts, range_, max_ammo):
        super(RangedWeapon, self).__init__(dmg, action_pts, range_, max_ammo, ranged=True)


