from battle_timing import Timing

class Talent:
    def __init__(self, name="None", description="No talent", effect=print, timing:Timing=Timing.Start, frequency = 1):
        self.name = name
        self.description = description
        self.effect = effect
        self.timing = timing
        self.frequency = frequency

    def __str__(self):
        return f"{self.name}"

def none():
    return Talent()
   
def intimidation():
    """Talent: Intimidation"""
    def effect(pokemon_1,pokemon_2):
        print(f"Le talent de {pokemon_1.name} influcence {pokemon_2.name}!")

    return Talent("Intimidation", "Baisse l'atk de l'ennemi de 1", effect, Timing.Start, frequency=1)

talents = {
    "None": none,
    "Intimidation": intimidation,
}