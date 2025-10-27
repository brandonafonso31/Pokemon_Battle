from battle_timing import Timing
import utils

class Ability:
    def __init__(self, name, description, effect, timing:Timing, frequency):
        self.name = name
        self.description = description
        self.effect = effect
        self.timing = timing
        self.frequency = frequency
        self.used = 0

    def __str__(self):
        return f"{self.name}"
    
    def can_trigger(self):
        return self.frequency == 0 or self.used < self.frequency

    def trigger(self, pokemon_self, pokemon_other):
        if self.can_trigger():
            self.effect(pokemon_self, pokemon_other)
            self.used += 1
            
    def reset(self):
        self.used = 0
    
def intimidation():
    """Talent: Intimidation"""
    def effect(pokemon_1,pokemon_2):
        pokemon_2.apply_buff_debuff("atk", scale=-1)
        txt = f"Le talent de {pokemon_1.name} influcence {pokemon_2.name}!"
        print(txt)
        # utils.print_log_ingame(manager,txt,reset=True)

    return Ability("Intimidation", "Baisse l'atk de l'ennemi de 1", effect, Timing.START, frequency=1)
    
abilities = {
    "Intimidation": intimidation,
}