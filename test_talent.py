from battle_timing import Timing

class Talent:
    registry = {}

    def __init__(self, name, description, timing: Timing, frequency=-1):
        self.name = name
        self.description = description
        self.timing = timing
        self.frequency = frequency
        self.used = 0

    def can_trigger(self):
        return self.frequency == -1 or self.used < self.frequency

    def trigger(self, pokemon_self, pokemon_other):
        if self.can_trigger():
            self.effect(pokemon_self, pokemon_other)
            self.used += 1

    def reset(self):
        self.used = 0

    def effect(self, pokemon_self, pokemon_other):
        pass

    @classmethod
    def register(cls, talent_cls):
        cls.registry[talent_cls.__name__] = talent_cls
        return talent_cls


@Talent.register
class Intimidation(Talent):
    def __init__(self):
        super().__init__("Intimidation", "Baisse l'attaque de l'ennemi de 1", Timing.START, frequency=1)

    def effect(self, pokemon_self, pokemon_other):
        pokemon_other.apply_buff_debuff("atk", scale=-1)
        print(f"{pokemon_self.name} intimide {pokemon_other.name} !")


@Talent.register
class Levitation(Talent):
    def __init__(self):
        super().__init__("Lévitation", "Immunité Sol", Timing.ABOUT_TO_GET_HIT)

    def effect(self, pokemon_self, pokemon_other):
        print(f"{pokemon_self.name} flotte et esquive les attaques Sol !")


# Maintenant, tu peux instancier un talent depuis le registre :
talent = Talent.registry["Intimidation"]()