from battle_timing import Timing

class Talent:
    def __init__(self, name, description, effect, timing:Timing, frequency = 1):
        self.name = name
        self.description = description
        self.effect = effect
        self.timing = timing
        self.frequency = frequency

    def __str__(self):
        return f"{self.name}"
    
def intimidation(pokemon_1,pokemon_2):
    """Talent: Torche"""
    def effect():
        print(f"{pokemon_1.name}'s Talent!")

    return Talent("Intimidation", "Baisse l'atk de l'ennemi de 1", effect, Timing.Start, frequency=1)

talents = {
    "Intimidation": intimidation,
}