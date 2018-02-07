from enum import Flag, auto


class Action(Flag):
    NULL = 0

    GO = auto()
    STAY = auto()
    ATTACK = auto()

    ENEMY = auto()
    ALLY = auto()

    NEAREST = auto()
    FURTHEST = auto()

    STRONGEST = auto()
    WEAKEST = auto()

    HIGHEST = auto()
    LOWEST = auto()

    HEALTH = auto()
    WEAPON = auto()
    CONCENTRATION = auto()

    OPPORTUNITY = auto()
    DANGER = auto()

    TOWARDS = auto()
    AWAY = auto()

    def has_any(self, other: "Action"):
        return bool(self & other)

    def has_only(self, other: "Action"):
        return self == other

    def has_at_least(self, other: "Action"):
        return (self & other) == other

    @classmethod
    def to_list(cls):
        return sorted(cls.__members__.values(), key= lambda action: action.name)
