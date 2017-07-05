from battle import Soldier


class Weapon(object):
    def __init__(self, atk_dmg: int, range_: int, max_ammo: int):
        self._raise_error_for_bad_input(atk_dmg, range_)
        self._atk_dmg = atk_dmg
        self._range = range_
        self._current_ammo = max_ammo
        self._max_ammo = max_ammo

    @staticmethod
    def _raise_error_for_bad_input(atk_dmg, range_):
        if atk_dmg <= 0 or range_ < 0:
            raise ValueError('atk_dmg must be greater than 0. Range must be greater than or equal to 0.')

    @property
    def atk_dmg(self):
        return self._atk_dmg

    @property
    def range(self):
        return self._range

    @property
    def current_ammo(self):
        return self._current_ammo

    def refill_ammo(self):
        self._current_ammo = self._max_ammo

    def shoot(self, opponent: Soldier):
        raise NotImplementedError


class SniperRifle(Weapon):
    def __init__(self):
        dmg = 50
        range_ = 10
        ammo = 10
        super(SniperRifle, self).__init__(dmg, range_, ammo)
