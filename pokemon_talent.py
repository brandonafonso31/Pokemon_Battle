from battle_timing import Timing

class Talent:
    def __init__(self, name, description, effect, timing:Timing):
        self.name = name
        self.description = description
        self.effect = effect    # fonction callable that applies the effect
        self.timing = timing

    def __str__(self):
        return f"{self.name}"
    
def torche():
    """Talent: Torche"""
    def effect(pokemon):
        # When hit by a Fire-type move, the Pokémon's Special Attack is raised by 1 stage.
        pokemon.atk_spe += 1    #to change cause meh wrong implementation
        print(f"{pokemon.name}'s Special Attack rose!")

    return Talent("Torche", "Boosts the Special Attack when hit by a Fire-type move.", effect, Timing.ABOUT_TO_GET_HIT)

talents = {
    "torche": torche,
}