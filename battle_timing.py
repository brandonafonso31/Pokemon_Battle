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

def apply_timing_effect(pokemon_using_talent, pokemon_2):
    timing_talent = pokemon_using_talent.talent.timing
    talent = pokemon_using_talent.talent
    with timing_lock:
        #print(f"Timing actuel: {current_timing}, Timing talent: {timing_talent}")
        if current_timing == timing_talent:
            talent.trigger(pokemon_using_talent, pokemon_2)
            
    return pokemon_using_talent, pokemon_2 
    
def check_timing_talent(pokemon_1, pokemon_2):
    """Check if the timing is correct for the move"""
    if pokemon_1.vit >= pokemon_2.vit:
        pokemon_1, pokemon_2 = apply_timing_effect(pokemon_1, pokemon_2)
        pokemon_2, pokemon_1 = apply_timing_effect(pokemon_2, pokemon_1)
    else:
        pokemon_2, pokemon_1 = apply_timing_effect(pokemon_2, pokemon_1)
        pokemon_1, pokemon_2 = apply_timing_effect(pokemon_1, pokemon_2)         
    return pokemon_1, pokemon_2
  
current_timing = Timing.Start
timing_lock = threading.Lock()