from pokemon_type import Type
from collections import defaultdict
from move_target import Target

class Move:
    def __init__(self, name: str, type: Type, power: int, precision: int, pp: int, effect: str, prio: int, target:Target = Target.OPPONENT,animation = None):
        self.name = name
        self.type = type 
        
        self.power = power
        self.precision = precision
        self.pp = pp
        
        self.effect = effect
        self.prio = prio
        
        self.target = target
        self.animation = animation
    
    def __str__(self):
        return f"{self.name}" 
        
class StatusMove(Move):
    def __init__(self, name: str, type: Type, precision: int, pp: int, effect: str, prio: int):
        super().__init__(name, type, None, precision, pp, effect, prio)

class PhysicalMove(Move):
    def __init__(self, name: str, type: Type, power: int, precision: int, pp: int, effect: str, prio: int):
        super().__init__(name, type, power, precision, pp, effect, prio)

class SpecialMove(Move):
    def __init__(self, name: str, type: Type, power: int, precision: int, pp: int, effect: str, prio: int):
        super().__init__(name, type, power, precision, pp, effect, prio)


# plutôt mettre les trucs comme ça dans un csv, peut-être même toute l'attaque (power, pp, precision, prio ...)
dico_effect_move = {    
    "Lance-Flammes" : f"L'ennemi reçoit un torrent de flammes. A 10% de chance de brûler la cible.",
    
    "Crocs Givre" : f"Le lanceur utilise une morsure glaciale. A 10% de chance de geler ou d'apeurer la cible.",
    
    "Cage-Éclair" : f"Un faible choc électrique frappe l'ennemi. Paralyse la cible."
} 

dico_effect_move = defaultdict(str,dico_effect_move)