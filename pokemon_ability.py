from battle_timing import Timing
from pokemon_type import Type
from math import floor

class Ability:
    def __init__(self, name, frequency = -1):
        self.name = name
        self.frequency = frequency
        self.used = 0

    def __str__(self):
        return self.name
    
    def on_event(self, timing, ctx):
        pass

    def can_trigger(self):
        return self.frequency == -1 or self.used < self.frequency
    
    def reset(self):
        self.used = 0
        
class Blaze(Ability):
    def __init__(self):
        super().__init__("Blaze")

    def on_event(self, timing, ctx):
        ratio_hp = ctx.attacker.hp/ctx.attacker.hp_max
        if timing == Timing.CALC_DAMAGE and (ratio_hp <= 1/3) and ctx.move.type == Type.FEU:
            ctx.damage *= 1.5
            ctx.damage = floor(ctx.damage)
            print(f"🔥 {ctx.attacker.name} active Brasier ! Dégâts augmentés.")
        return ctx

class Intimidate(Ability):
    def __init__(self):
        super().__init__("Intimidate", 1)
        
    def on_event(self, timing, ctx):
        if timing == Timing.START and self.can_trigger():
            ctx.defender.apply_buff_debuff("atk", -1)
            print(f"😤 {ctx.attacker.name} intimide {ctx.defender.name} ! L’attaque baisse.")
            
            self.used += 1
        return ctx
    
class Levitate(Ability):
    def __init__(self):
        super().__init__("Levitate")

    def on_event(self, timing, ctx):
        if timing == Timing.ABOUT_TO_GET_HIT and ctx.move.type == Type.SOL:
            ctx.cancel_attack = True
            ctx.damage = 0
            print(f"☁️ {ctx.defender.name} lévite et évite l'attaque Sol !")
        return ctx


abilities = {
    "Blaze": Blaze(),
    "Intimidate": Intimidate(),
    "Levitate": Levitate(),
}