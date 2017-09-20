from battle.statstools.basestats import stats_factory

# WeaponStats = namedtuple('WeaponStats', 'dmg, action_pts, range, ammo')
WeaponStats = stats_factory('WeaponStats', ('dmg', None, False), ('action_pts', None, False), ('range', None, False),
                            ('ammo', None, True))


class OutOfAmmo(StopIteration):
    pass


class Weapon(object):
    def __init__(self, stats: WeaponStats) -> None:

        self._stats = stats

    @staticmethod
    def _raise_error_for_bad_input(atk_dmg, action_pts, range_):
        if atk_dmg <= 0 or action_pts <= 0 or range_ <= 0:
            raise ValueError('dmg, action_pts and range_ must be grater than zero.')

    @property
    def stats(self):
        return self._stats

    def use_weapon(self):
        if self._stats.current_ammo <= 0:
            raise OutOfAmmo()
        self._stats.current_ammo -= 1
        return self._stats.dmg

    def refill_ammo(self):
        self._stats.current_ammo = self._stats.ammo


class MeleeWeapon(Weapon):
    def __init__(self, dmg, action_pts, range_=1, ammo=float('inf')):
        stats = WeaponStats(dmg, action_pts, range_, ammo)
        super(MeleeWeapon, self).__init__(stats)


class RangedWeapon(Weapon):
    def __init__(self, dmg, action_pts, range_, ammo):
        stats = WeaponStats(dmg, action_pts, range_, ammo)
        super(RangedWeapon, self).__init__(stats)


