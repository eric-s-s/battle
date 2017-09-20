from battle.weapon import MeleeWeapon, RangedWeapon, Weapon


FIST = MeleeWeapon(dmg=1, action_pts=1)
GUN = RangedWeapon(dmg=5, action_pts=2, range_=5, ammo=10)


class Soldier(object):
    def __init__(self, max_action_pts: int = 3, max_health: int = 100, heal_pct: float = 5.0):
        self._max_health = max_health
        self._current_health = self._max_health
        self._max_action_pts = max_action_pts
        self._current_action_pts = self._max_action_pts
        self._healing_pct = heal_pct

        self._weapon = FIST

    def get_perimeter_size(self) -> int:
        return self._weapon.stats.range

    def get_action_points(self) -> int:
        return self._current_action_pts

    def can_move(self, mv_pts) -> bool:
        return mv_pts <= self._current_action_pts and not self.is_dead()

    def move(self, mv_pts):
        if mv_pts < 0:
            raise ValueError('mv_pts can\'t be less than zero')
        if self.can_move(mv_pts):
            self._current_action_pts -= mv_pts

    def reset_move_points(self):
        self._current_action_pts = self._max_action_pts

    def get_health(self) -> int:
        return self._current_health

    def get_weapon(self) -> Weapon:
        return self._weapon

    def equip_weapon(self, weapon: Weapon):
        self._weapon = weapon

    def attack(self, opponent):
        action_pts = self._weapon.stats.action_pts
        if self._current_action_pts < action_pts:
            return None
        self._current_action_pts -= action_pts
        dmg = self._weapon.use_weapon()
        opponent.receive_dmg(dmg)

    def is_dead(self) -> bool:
        return self._current_health <= 0

    def receive_dmg(self, dmg: int):
        if dmg < 0:
            raise ValueError('damage can\'t be less than zero')
        self._current_health -= dmg

    def heal(self, health_pts: int):
        """cannot heal past max"""
        if health_pts < 0:
            raise ValueError('health_pts can\'t be less than zero')
        if self.is_dead():
            return None
        self._current_health = min(self._current_health + health_pts, self._max_health)

    def rest(self):
        """heal and reset_move"""
        heal_points = int(round(self._max_health * self._healing_pct / 100.))
        self.heal(heal_points)
        self.reset_move_points()


class Example(Soldier):
    def __init__(self, weapon: Weapon, **kwargs):
        super(Example, self).__init__(**kwargs)
        self.equip_weapon(weapon)



