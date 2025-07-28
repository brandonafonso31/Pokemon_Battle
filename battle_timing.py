from enum import Enum
import threading

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

def check_timing_talent(pokemon_1, pokemon_2):
    """Check if the timing is correct for the move"""
    timing_talent = pokemon_1.talent.timing
    with timing_lock:
        if current_timing == timing_talent :
            pokemon_1.talent.effect(pokemon_2)  
    return pokemon_1, pokemon_2
  
current_timing = Timing.Start
timing_lock = threading.Lock()
timing_thread = threading.Thread(target=lambda: None, daemon=True)
timing_thread.start()