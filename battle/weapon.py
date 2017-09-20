from collections import namedtuple
from typing import Union


WeaponStats = namedtuple('WeaponStats', 'dmg, action_pts, range, ammo')


class OutOfAmmo(StopIteration):
    pass


class Weapon(object):
    def __init__(self, stats: WeaponStats) -> None:

        self._current_ammo = stats.ammo
        self._stats = stats

    @staticmethod
    def _raise_error_for_bad_input(atk_dmg, action_pts, range_):
        if atk_dmg <= 0 or action_pts <= 0 or range_ <= 0:
            raise ValueError('dmg, action_pts and range_ must be grater than zero.')

    @property
    def stats(self):
        return self._stats

    @property
    def current_ammo(self):
        return self._current_ammo

    def use_weapon(self):
        if self._current_ammo <= 0:
            raise OutOfAmmo()
        self._current_ammo -= 1
        return self._stats.dmg

    def refill_ammo(self):
        self._current_ammo = self._stats.ammo


class MeleeWeapon(Weapon):
    def __init__(self, dmg, action_pts, range_=1, ammo=float('inf')):
        stats = WeaponStats(dmg, action_pts, range_, ammo)
        super(MeleeWeapon, self).__init__(stats)


class RangedWeapon(Weapon):
    def __init__(self, dmg, action_pts, range_, ammo):
        stats = WeaponStats(dmg, action_pts, range_, ammo)
        super(RangedWeapon, self).__init__(stats)


