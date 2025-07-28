from enum import Enum

class Timing(Enum):
    Start, ABOUT_TO_GET_HIT, GOT_HIT, END = range(4)
    
    def __str__(self):
        if self == Timing.Start:
            return "Début du tour"
        elif self == Timing.ABOUT_TO_GET_HIT:
            return "Attaque en cours"
        elif self == Timing.GOT_HIT:
            return "A subi des dégats"
        elif self == Timing.END:
            return "Fin du tour"
        return "Unknown Timing"