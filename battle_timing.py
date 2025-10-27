from enum import Enum
import threading
import battle_context as bc

class Timing(Enum):
    START, ABOUT_TO_GET_HIT, CALC_DAMAGE, GOT_HIT, END = range(5)
    
    def __str__(self):
        string = ""
        if self == Timing.START:
            string = "Début du tour"
        elif self == Timing.ABOUT_TO_GET_HIT:
            string = "Attaque en cours"
        elif self == Timing.CALC_DAMAGE:
            string = "Calcul des dégâts"
        elif self == Timing.GOT_HIT:
            string = "A subi des dégâts"
        elif self == Timing.END:
            string = "Fin du tour"
        return "[Timing] → Unknown Timing" if string == "" else "[Timing] → " + string

timing_lock = threading.Lock()


    
def check_timing_talent(pokemon_1, pokemon_2, move = None, damage:int = 0):
    """Crée le context de l'état du combat,
    puis tente de déclencer les talents"""
    global current_timing
    ctx = bc.create_context(current_timing, pokemon_1, pokemon_2, move, damage)

    if pokemon_1.vit >= pokemon_2.vit:
        for p1, p2 in [(pokemon_1, pokemon_2), (pokemon_2, pokemon_1)]:
            if p1.ability:
                ctx = p1.ability.on_event(current_timing, ctx)
    else:
        for p1, p2 in [(pokemon_2, pokemon_1), (pokemon_1, pokemon_2)]:
            if p1.ability:
                ctx = p1.ability.on_event(current_timing, ctx)

    return ctx

def change_timing(default_timing=None):
    """ Change les timings comme présenté ci-dessous :
    Start_Turn -> About_To_Get_Hit -> Calc_Damage -> Got_Hit ->
    if second pokemon KO -> End_Turn
    else -> About_to_Get_Hit -> Calc_Damage -> Got_Hit -> End_Turn
    """
    global current_timing    
    with timing_lock:       
        if not default_timing:            
            timing_values = list(Timing)
            current_index = timing_values.index(current_timing)
            next_index = (current_index + 1) % len(timing_values)
            current_timing = timing_values[next_index]
        else:
            current_timing = default_timing

    print(current_timing)
    return current_timing


current_timing = Timing.START
timing_lock = threading.Lock()