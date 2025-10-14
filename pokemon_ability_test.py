from battle_timing import Timing
from pokemon_type import Type

class Ability:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
    def on_event(self, timing, ctx):
        pass


class Blaze(Ability):
    def __init__(self):
        super().__init__("Brasier")

    def on_event(self, timing, ctx):
        ratio_hp = ctx.attacker.hp/ctx.attacker.hp_max
        if timing == Timing.ABOUT_TO_GET_HIT and (ratio_hp <= 1/3) and ctx.move.type == Type.FEU:
            ctx.damage *= 1.5
            print(f"🔥 {ctx.attacker.name} active Brasier ! Dégâts augmentés.")
        return ctx

class Intimidation(Ability):
    def __init__(self):
        super().__init__("Intimidation")
        
    def on_event(self, timing, ctx):
        if timing == Timing.START:
            ctx.defender.apply_buff_debuff("atk", -1)
            print(f"😤 {ctx.attacker.name} intimide {ctx.defender.name} ! L’attaque baisse.")
        return ctx

