from enum import Enum

class Target(Enum):
    ALL, ALL_BUT_ME, ALLY, ALL_ALLY, OPPONENT, ALL_OPPONENT = range(6)
    
    def __str__(self):
        if self == Target.ALL:
            return "All"
        elif self == Target.ALL_BUT_ME:
            return "All but me"
        elif self == Target.ALLY:
            return "Ally"
        elif self == Target.ALL_ALLY:
            return "All Ally"
        elif self == Target.OPPONENT:
            return "Opponent"
        elif self == Target.ALL_OPPONENT:
            return "All Opponent"
        return "Unknown Target"