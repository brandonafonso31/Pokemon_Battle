from enum import Enum

class Timing(Enum):
    Start, GOT_HIT, END = range(3)
    
    def __str__(self):
        if self == Timing.Start:
            return "Début du tour"
        elif self == Timing.GOT_HIT:
            return "A subi des dégats"
        elif self == Timing.END:
            return "Fin du tour"
        return "Unknown Timing"