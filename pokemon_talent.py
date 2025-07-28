from battle_timing import Timing

class Talent:
    def __init__(self, name, description, effect, timing:Timing=Timing.Start, frequency = 1):
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

def none():
    def effect(pokemon_1, pokemon_2):
        """No effect talent"""
        print(f"Aucun talent")
        return pokemon_1, pokemon_2
    return Talent("None","No talent",effect, Timing.Start, frequency=0)
   
def intimidation():
    """Talent: Intimidation"""
    def effect(pokemon_1,pokemon_2):
        print(f"Le talent de {pokemon_1.name} influcence {pokemon_2.name}!")

    return Talent("Intimidation", "Baisse l'atk de l'ennemi de 1", effect, Timing.Start, frequency=1)

talents = {
    "None": none,
    "Intimidation": intimidation,
}