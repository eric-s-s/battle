
class Stat(object):
    def __init__(self, stat):
        self._max = stat
        self._current = stat
        self._modifier = 0

    @property
    def static_max(self):
        return self._max

    @property
    def max(self):
        return self._max + self._modifier

    @property
    def current(self):
        return self._current

    def modify_current(self, mod):
        self._current = min(self._current + mod, self.max)

    def hard_reset(self):
        self._modifier = 0
        self._current = self._max

    def reset(self):
        self._current = self.max

    def modifier(self, mod):
        self._modifier = mod
        self._current = min(self._current, self.max)

    def adjust(self, modifier):
        return Stat(self._max + modifier)


class PositiveStat(Stat):
    def __init__(self, stat):
        super(PositiveStat, self).__init__(max(stat, 0))

    def modify_current(self, mod):
        super(PositiveStat, self).modify_current(mod)
        self._current = max(self._current, 0)

    def modifier(self, mod):
        new_mod = max(mod, -self._max)
        super(PositiveStat, self).modifier(new_mod)
