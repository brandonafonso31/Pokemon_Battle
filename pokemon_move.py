from pokemon_type import Type
from collections import defaultdict

class Move:
    def __init__(self, name: str, type: Type, power: int, precision: int, pp: int, effect: str, prio: int):
        self.name = name
        self.type = type 
        
        self.power = power
        self.precision = precision
        self.pp = pp
        
        self.effect = effect
        self.prio = prio
    
    def __str__(self):
        return f"{self.name}" 
    
    def play_animation(self, window, attacker_sprite, defender_sprite, attacker_coords, defender_coords):
        if self.animation:
            self.animation(window, attacker_sprite, defender_sprite, attacker_coords, defender_coords)
    
        
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