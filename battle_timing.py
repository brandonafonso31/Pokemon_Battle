from enum import Enum
import threading

class Timing(Enum):
    START, ABOUT_TO_GET_HIT, GOT_HIT, END = range(4)
    
    def __str__(self):
        string = ""
        if self == Timing.START:
            string = "Début du tour"
        elif self == Timing.ABOUT_TO_GET_HIT:
            string = "Attaque en cours"
        elif self == Timing.GOT_HIT:
            string = "A subi des dégats"
        elif self == Timing.END:
            string = "Fin du tour"
        return "[Timing] → Unknown Timing" if string == "" else "[Timing] → " + string

timing_lock = threading.Lock()


def apply_timing_effect(pokemon_using_talent, pokemon_2):
    talent = pokemon_using_talent.talent
    timing_talent = talent.timing
    with timing_lock:
        if current_timing == timing_talent:
            talent.trigger(pokemon_using_talent, pokemon_2)
            
    return pokemon_using_talent, pokemon_2
    
def check_timing_talent(pokemon_1, pokemon_2):
    """Check if the timing is correct for the talent"""
    if pokemon_1.vit >= pokemon_2.vit:
        pokemon_1, pokemon_2 = apply_timing_effect(pokemon_1, pokemon_2)
        pokemon_2, pokemon_1 = apply_timing_effect(pokemon_2, pokemon_1)
    else:
        pokemon_2, pokemon_1 = apply_timing_effect(pokemon_2, pokemon_1)
        pokemon_1, pokemon_2 = apply_timing_effect(pokemon_1, pokemon_2)         
    return pokemon_1, pokemon_2

def change_timing(default_timing = None):
    """ Change les timings comme présenté ci-dessous\n
    Start_Turn -> About_To_Get_Hit -> Got_Hit -> \n
    if second pokemon KO -> End_Turn else -> About_to_Get_Hit -> Got_Hit -> End_Turn """
    global current_timing    
    with timing_lock:       
        if not default_timing:            
            timing_values = list(Timing)
            current_index = timing_values.index(current_timing)

            # passe au timing suivant (cycle circulaire)
            next_index = (current_index + 1) % len(timing_values)
            current_timing = timing_values[next_index]
        else:
            current_timing = default_timing

    print(current_timing)
    return current_timing

current_timing = Timing.START
timing_lock = threading.Lock()