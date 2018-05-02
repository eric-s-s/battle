from enum import Enum, auto


class ActionPriority(Enum):
    STAY = auto()
    GO = auto()
    ATTACK = auto()
    """
    write a bunch of priorities. the first step is brainstorming.
        - write descriptive ideas for what a bunch of priorities
        - ex:
            - go until first attack opportunity, always reserve pts for an attack, no matter what
            - go until first attack opportunity, make sure can get to minimum safe distance after attack.

    Write a SECOND list that is just an edited version of first list. cut out the ones you don't want
    for each element in second list, write several attempts at a short descriptive
    """
