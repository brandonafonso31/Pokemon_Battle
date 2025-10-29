from enum import Enum

class Status(Enum):
    BURN,FREEZE,PARALYSIS,POISON,SLEEP,CONFUSION,TAUNT,CURSE,FEAR,TRAP = range(10)