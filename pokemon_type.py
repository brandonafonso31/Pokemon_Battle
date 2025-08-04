from enum import Enum

class Type(Enum):
    NORMAL,FEU,EAU,PLANTE,ELECTRIQUE,COMBAT,ROCHE,SOL,FEE,PSY,TENEBRE,SPECTRE,POISON,INSECTE,VOL,DRAGON,ACIER,GLACE = range(18)
    
    def __str__(self):
        return self.name
    
    def color(self):
        if self == Type.NORMAL:
            return "#FFFFFF"
        elif self == Type.FEU:
            return "#FF0000"
        elif self == Type.EAU:
            return "#0000FF"
        elif self == Type.PLANTE:
            return "#00FF00"
        elif self == Type.ELECTRIQUE:
            return "#FFFF00"
        elif self == Type.SOL or self == Type.ROCHE:
            return "#663300"
        elif self == Type.COMBAT:
            return "#A14708"
        elif self == Type.FEE:
            return "#F016F0"
        elif self == Type.PSY:
            return "#981098"
        elif self == Type.TENEBRE:
            return "#2C2828"
        elif self == Type.SPECTRE:
            return "#36035D"
        elif self == Type.POISON:
            return "#57109A"
        elif self == Type.INSECTE:
            return "#008000"
        elif self == Type.VOL:
            return "#008080"
        elif self == Type.DRAGON:
            return "#2A4AA2"
        elif self == Type.ACIER:
            return "#CDCDCD"
        elif self == Type.GLACE:
            return "#00FFFF"
        else:
            return "#000000"
        
"""
print(Type.GLACE)           # Type.GLACE
print(Type.GLACE.name)      # "GLACE"
print(Type.GLACE.value)     # 17
print(Type.GLACE.color())   # "#00FFFF"

# Comparaison
if mon_type == Type.FEU:
    print("C'est un type feu")

# Parcourir tous les types
for t in Type:
    print(t.name, t.value)
"""

# Colonne: attaquant | Ligne Défenseur
# type_table[0][0] = 1 --> le type 0 (normal) est neutre sur le type 0 (normal)
# type_table[1][6] = 1 --> le type 1 (feu) est neutre sur le type 6 (roche)

type_table = [
    [1,1,1,1,1,1,0.5,1,1,1,1,0,1,1,1,1,0.5,1],              # normal
    [1,0.5,0.5,2,1,1,0.5,1,1,1,1,1,1,2,1,0.5,2,2],          # feu
    [1,2,0.5,0.5,1,1,2,2,1,1,1,1,1,1,1,0.5,1,1],            # eau
    [1,0.5,2,0.5,1,1,2,2,1,1,1,1,0.5,0.5,0.5,0.5,0.5,1],    # plante
    [1,1,2,0.5,0.5,1,1,0,1,1,1,1,1,1,2,0.5,1,1],            # electrique
    [2,1,1,1,1,1,2,1,0.5,0.5,2,0,0.5,0.5,0.5,1,2,2],        # combat
    [1,2,1,1,1,0.5,1,0.5,1,1,1,1,1,2,2,1,0.5,2],            # roche
    [1,2,1,0.5,2,1,2,1,1,1,1,1,2,0.5,0,1,2,1],              # sol
    [1,0.5,1,1,1,2,1,1,1,1,2,1,0.5,1,1,2,0.5,1],            # fee
    [1,1,1,1,1,2,1,1,1,0.5,0,1,2,1,1,1,0.5,1],              # psy
    [1,1,1,1,1,0.5,1,1,0.5,2,0.5,2,1,1,1,1,1,1],            # tenebre
    [0,1,1,1,1,1,1,1,1,2,0.5,2,1,1,1,1,1,1],                # spectre
    [1,1,1,2,1,1,0.5,0.5,2,1,1,0.5,0.5,1,1,1,0,1],          # poison
    [1,0.5,1,2,1,0.5,1,1,0.5,2,2,0.5,0.5,1,0.5,1,0.5,1],    # insecte
    [1,1,1,2,0.5,2,0.5,1,1,1,1,1,1,2,1,1,0.5,1],            # vol
    [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,2,0.5,1],                # dragon
    [1,0.5,0.5,1,0.5,1,2,1,2,1,1,1,1,1,1,1,0.5,2],          # acier
    [1,0.5,0.5,2,1,1,1,2,1,1,1,1,1,1,2,2,0.5,0.5]           # glace
]

def get_multiplicateur(type_atk,type_def):
    return type_table[type_atk.value][type_def.value]

def get_double_multiplicateur(type_atk,type1_def,type2_def):
    return get_multiplicateur(type_atk,type1_def) * get_multiplicateur(type_atk,type2_def)

# ASSERT all types :

# Normal attack
assert get_multiplicateur(Type.NORMAL, Type.NORMAL) == 1
assert get_multiplicateur(Type.NORMAL, Type.FEU) == 1
assert get_multiplicateur(Type.NORMAL, Type.EAU) == 1 
assert get_multiplicateur(Type.NORMAL, Type.PLANTE) == 1
assert get_multiplicateur(Type.NORMAL, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.NORMAL, Type.COMBAT) == 1
assert get_multiplicateur(Type.NORMAL, Type.ROCHE) == 0.5
assert get_multiplicateur(Type.NORMAL, Type.SOL) == 1
assert get_multiplicateur(Type.NORMAL, Type.FEE) == 1
assert get_multiplicateur(Type.NORMAL, Type.PSY) == 1
assert get_multiplicateur(Type.NORMAL, Type.TENEBRE) == 1
assert get_multiplicateur(Type.NORMAL, Type.SPECTRE) == 0
assert get_multiplicateur(Type.NORMAL, Type.POISON) == 1
assert get_multiplicateur(Type.NORMAL, Type.INSECTE) == 1
assert get_multiplicateur(Type.NORMAL, Type.VOL) == 1
assert get_multiplicateur(Type.NORMAL, Type.DRAGON) == 1
assert get_multiplicateur(Type.NORMAL, Type.ACIER) == 0.5
assert get_multiplicateur(Type.NORMAL, Type.GLACE) == 1

# Feu attack
assert get_multiplicateur(Type.FEU, Type.NORMAL) == 1
assert get_multiplicateur(Type.FEU, Type.FEU) == 0.5
assert get_multiplicateur(Type.FEU, Type.EAU) == 0.5
assert get_multiplicateur(Type.FEU, Type.PLANTE) == 2
assert get_multiplicateur(Type.FEU, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.FEU, Type.COMBAT) == 1
assert get_multiplicateur(Type.FEU, Type.ROCHE) == 0.5
assert get_multiplicateur(Type.FEU, Type.SOL) == 1
assert get_multiplicateur(Type.FEU, Type.FEE) == 1
assert get_multiplicateur(Type.FEU, Type.PSY) == 1
assert get_multiplicateur(Type.FEU, Type.TENEBRE) == 1
assert get_multiplicateur(Type.FEU, Type.SPECTRE) == 1
assert get_multiplicateur(Type.FEU, Type.POISON) == 1
assert get_multiplicateur(Type.FEU, Type.INSECTE) == 2
assert get_multiplicateur(Type.FEU, Type.VOL) == 1
assert get_multiplicateur(Type.FEU, Type.DRAGON) == 0.5
assert get_multiplicateur(Type.FEU, Type.ACIER) == 2
assert get_multiplicateur(Type.FEU, Type.GLACE) == 2

# Eau attack
assert get_multiplicateur(Type.EAU, Type.NORMAL) == 1
assert get_multiplicateur(Type.EAU, Type.FEU) == 2
assert get_multiplicateur(Type.EAU, Type.EAU) == 0.5
assert get_multiplicateur(Type.EAU, Type.PLANTE) == 0.5
assert get_multiplicateur(Type.EAU, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.EAU, Type.COMBAT) == 1
assert get_multiplicateur(Type.EAU, Type.ROCHE) == 2
assert get_multiplicateur(Type.EAU, Type.SOL) == 2
assert get_multiplicateur(Type.EAU, Type.FEE) == 1
assert get_multiplicateur(Type.EAU, Type.PSY) == 1
assert get_multiplicateur(Type.EAU, Type.TENEBRE) == 1
assert get_multiplicateur(Type.EAU, Type.SPECTRE) == 1
assert get_multiplicateur(Type.EAU, Type.POISON) == 1
assert get_multiplicateur(Type.EAU, Type.INSECTE) == 1
assert get_multiplicateur(Type.EAU, Type.VOL) == 1
assert get_multiplicateur(Type.EAU, Type.DRAGON) == 0.5
assert get_multiplicateur(Type.EAU, Type.ACIER) == 1
assert get_multiplicateur(Type.EAU, Type.GLACE) == 1

# Plante attack
assert get_multiplicateur(Type.PLANTE, Type.NORMAL) == 1
assert get_multiplicateur(Type.PLANTE, Type.FEU) == 0.5
assert get_multiplicateur(Type.PLANTE, Type.EAU) == 2
assert get_multiplicateur(Type.PLANTE, Type.PLANTE) == 0.5
assert get_multiplicateur(Type.PLANTE, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.PLANTE, Type.COMBAT) == 1
assert get_multiplicateur(Type.PLANTE, Type.ROCHE) == 2
assert get_multiplicateur(Type.PLANTE, Type.SOL) == 2
assert get_multiplicateur(Type.PLANTE, Type.FEE) == 1
assert get_multiplicateur(Type.PLANTE, Type.PSY) == 1
assert get_multiplicateur(Type.PLANTE, Type.TENEBRE) == 1
assert get_multiplicateur(Type.PLANTE, Type.SPECTRE) == 1
assert get_multiplicateur(Type.PLANTE, Type.POISON) == 0.5
assert get_multiplicateur(Type.PLANTE, Type.INSECTE) == 0.5
assert get_multiplicateur(Type.PLANTE, Type.VOL) == 0.5
assert get_multiplicateur(Type.PLANTE, Type.DRAGON) == 0.5
assert get_multiplicateur(Type.PLANTE, Type.ACIER) == 0.5
assert get_multiplicateur(Type.PLANTE, Type.GLACE) == 1

# Electrique attack
assert get_multiplicateur(Type.ELECTRIQUE, Type.NORMAL) == 1
assert get_multiplicateur(Type.ELECTRIQUE, Type.FEU) == 1
assert get_multiplicateur(Type.ELECTRIQUE, Type.EAU) == 2
assert get_multiplicateur(Type.ELECTRIQUE, Type.PLANTE) == 0.5
assert get_multiplicateur(Type.ELECTRIQUE, Type.ELECTRIQUE) == 0.5
assert get_multiplicateur(Type.ELECTRIQUE, Type.COMBAT) == 1
assert get_multiplicateur(Type.ELECTRIQUE, Type.ROCHE) == 1
assert get_multiplicateur(Type.ELECTRIQUE, Type.SOL) == 0
assert get_multiplicateur(Type.ELECTRIQUE, Type.FEE) == 1
assert get_multiplicateur(Type.ELECTRIQUE, Type.PSY) == 1
assert get_multiplicateur(Type.ELECTRIQUE, Type.TENEBRE) == 1
assert get_multiplicateur(Type.ELECTRIQUE, Type.SPECTRE) == 1
assert get_multiplicateur(Type.ELECTRIQUE, Type.POISON) == 1
assert get_multiplicateur(Type.ELECTRIQUE, Type.INSECTE) == 1
assert get_multiplicateur(Type.ELECTRIQUE, Type.VOL) == 2
assert get_multiplicateur(Type.ELECTRIQUE, Type.DRAGON) == 0.5
assert get_multiplicateur(Type.ELECTRIQUE, Type.ACIER) == 1
assert get_multiplicateur(Type.ELECTRIQUE, Type.GLACE) == 1

# Combat attack
assert get_multiplicateur(Type.COMBAT, Type.NORMAL) == 2
assert get_multiplicateur(Type.COMBAT, Type.FEU) == 1
assert get_multiplicateur(Type.COMBAT, Type.EAU) == 1
assert get_multiplicateur(Type.COMBAT, Type.PLANTE) == 1
assert get_multiplicateur(Type.COMBAT, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.COMBAT, Type.COMBAT) == 1
assert get_multiplicateur(Type.COMBAT, Type.ROCHE) == 2
assert get_multiplicateur(Type.COMBAT, Type.SOL) == 1
assert get_multiplicateur(Type.COMBAT, Type.FEE) == 0.5
assert get_multiplicateur(Type.COMBAT, Type.PSY) == 0.5
assert get_multiplicateur(Type.COMBAT, Type.TENEBRE) == 2
assert get_multiplicateur(Type.COMBAT, Type.SPECTRE) == 0
assert get_multiplicateur(Type.COMBAT, Type.POISON) == 0.5
assert get_multiplicateur(Type.COMBAT, Type.INSECTE) == 0.5
assert get_multiplicateur(Type.COMBAT, Type.VOL) == 0.5
assert get_multiplicateur(Type.COMBAT, Type.DRAGON) == 1
assert get_multiplicateur(Type.COMBAT, Type.ACIER) == 2
assert get_multiplicateur(Type.COMBAT, Type.GLACE) == 2

# Roche attack
assert get_multiplicateur(Type.ROCHE, Type.NORMAL) == 1
assert get_multiplicateur(Type.ROCHE, Type.FEU) == 2
assert get_multiplicateur(Type.ROCHE, Type.EAU) == 1
assert get_multiplicateur(Type.ROCHE, Type.PLANTE) == 1
assert get_multiplicateur(Type.ROCHE, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.ROCHE, Type.COMBAT) == 0.5
assert get_multiplicateur(Type.ROCHE, Type.ROCHE) == 1
assert get_multiplicateur(Type.ROCHE, Type.SOL) == 0.5
assert get_multiplicateur(Type.ROCHE, Type.FEE) == 1
assert get_multiplicateur(Type.ROCHE, Type.PSY) == 1
assert get_multiplicateur(Type.ROCHE, Type.TENEBRE) == 1
assert get_multiplicateur(Type.ROCHE, Type.SPECTRE) == 1
assert get_multiplicateur(Type.ROCHE, Type.POISON) == 1
assert get_multiplicateur(Type.ROCHE, Type.INSECTE) == 2
assert get_multiplicateur(Type.ROCHE, Type.VOL) == 2
assert get_multiplicateur(Type.ROCHE, Type.DRAGON) == 1
assert get_multiplicateur(Type.ROCHE, Type.ACIER) == 0.5
assert get_multiplicateur(Type.ROCHE, Type.GLACE) == 2

# Sol attack
assert get_multiplicateur(Type.SOL, Type.NORMAL) == 1
assert get_multiplicateur(Type.SOL, Type.FEU) == 2
assert get_multiplicateur(Type.SOL, Type.EAU) == 1
assert get_multiplicateur(Type.SOL, Type.PLANTE) == 0.5
assert get_multiplicateur(Type.SOL, Type.ELECTRIQUE) == 2
assert get_multiplicateur(Type.SOL, Type.COMBAT) == 1
assert get_multiplicateur(Type.SOL, Type.ROCHE) == 2
assert get_multiplicateur(Type.SOL, Type.SOL) == 1
assert get_multiplicateur(Type.SOL, Type.FEE) == 1
assert get_multiplicateur(Type.SOL, Type.PSY) == 1
assert get_multiplicateur(Type.SOL, Type.TENEBRE) == 1
assert get_multiplicateur(Type.SOL, Type.SPECTRE) == 1
assert get_multiplicateur(Type.SOL, Type.POISON) == 2
assert get_multiplicateur(Type.SOL, Type.INSECTE) == 0.5
assert get_multiplicateur(Type.SOL, Type.VOL) == 0
assert get_multiplicateur(Type.SOL, Type.DRAGON) == 1
assert get_multiplicateur(Type.SOL, Type.ACIER) == 2
assert get_multiplicateur(Type.SOL, Type.GLACE) == 1

# Fee attack
assert get_multiplicateur(Type.FEE, Type.NORMAL) == 1
assert get_multiplicateur(Type.FEE, Type.FEU) == 0.5
assert get_multiplicateur(Type.FEE, Type.EAU) == 1
assert get_multiplicateur(Type.FEE, Type.PLANTE) == 1
assert get_multiplicateur(Type.FEE, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.FEE, Type.COMBAT) == 2
assert get_multiplicateur(Type.FEE, Type.ROCHE) == 1
assert get_multiplicateur(Type.FEE, Type.SOL) == 1
assert get_multiplicateur(Type.FEE, Type.FEE) == 1
assert get_multiplicateur(Type.FEE, Type.PSY) == 1
assert get_multiplicateur(Type.FEE, Type.TENEBRE) == 2
assert get_multiplicateur(Type.FEE, Type.SPECTRE) == 1
assert get_multiplicateur(Type.FEE, Type.POISON) == 0.5
assert get_multiplicateur(Type.FEE, Type.INSECTE) == 1
assert get_multiplicateur(Type.FEE, Type.VOL) == 1
assert get_multiplicateur(Type.FEE, Type.DRAGON) == 2
assert get_multiplicateur(Type.FEE, Type.ACIER) == 0.5
assert get_multiplicateur(Type.FEE, Type.GLACE) == 1

# Psy attack
assert get_multiplicateur(Type.PSY, Type.NORMAL) == 1
assert get_multiplicateur(Type.PSY, Type.FEU) == 1
assert get_multiplicateur(Type.PSY, Type.EAU) == 1
assert get_multiplicateur(Type.PSY, Type.PLANTE) == 1
assert get_multiplicateur(Type.PSY, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.PSY, Type.COMBAT) == 2
assert get_multiplicateur(Type.PSY, Type.ROCHE) == 1
assert get_multiplicateur(Type.PSY, Type.SOL) == 1
assert get_multiplicateur(Type.PSY, Type.FEE) == 1
assert get_multiplicateur(Type.PSY, Type.PSY) == 0.5
assert get_multiplicateur(Type.PSY, Type.TENEBRE) == 0
assert get_multiplicateur(Type.PSY, Type.SPECTRE) == 1
assert get_multiplicateur(Type.PSY, Type.POISON) == 2
assert get_multiplicateur(Type.PSY, Type.INSECTE) == 1
assert get_multiplicateur(Type.PSY, Type.VOL) == 1
assert get_multiplicateur(Type.PSY, Type.DRAGON) == 1
assert get_multiplicateur(Type.PSY, Type.ACIER) == 0.5
assert get_multiplicateur(Type.PSY, Type.GLACE) == 1

# Tenebre attack
assert get_multiplicateur(Type.TENEBRE, Type.NORMAL) == 1
assert get_multiplicateur(Type.TENEBRE, Type.FEU) == 1
assert get_multiplicateur(Type.TENEBRE, Type.EAU) == 1
assert get_multiplicateur(Type.TENEBRE, Type.PLANTE) == 1
assert get_multiplicateur(Type.TENEBRE, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.TENEBRE, Type.COMBAT) == 0.5
assert get_multiplicateur(Type.TENEBRE, Type.ROCHE) == 1
assert get_multiplicateur(Type.TENEBRE, Type.SOL) == 1
assert get_multiplicateur(Type.TENEBRE, Type.FEE) == 0.5
assert get_multiplicateur(Type.TENEBRE, Type.PSY) == 2
assert get_multiplicateur(Type.TENEBRE, Type.TENEBRE) == 0.5
assert get_multiplicateur(Type.TENEBRE, Type.SPECTRE) == 2
assert get_multiplicateur(Type.TENEBRE, Type.POISON) == 1
assert get_multiplicateur(Type.TENEBRE, Type.INSECTE) == 1
assert get_multiplicateur(Type.TENEBRE, Type.VOL) == 1
assert get_multiplicateur(Type.TENEBRE, Type.DRAGON) == 1
assert get_multiplicateur(Type.TENEBRE, Type.ACIER) == 1
assert get_multiplicateur(Type.TENEBRE, Type.GLACE) == 1

# Spectre attack
assert get_multiplicateur(Type.SPECTRE, Type.NORMAL) == 0
assert get_multiplicateur(Type.SPECTRE, Type.FEU) == 1
assert get_multiplicateur(Type.SPECTRE, Type.EAU) == 1
assert get_multiplicateur(Type.SPECTRE, Type.PLANTE) == 1
assert get_multiplicateur(Type.SPECTRE, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.SPECTRE, Type.COMBAT) == 1
assert get_multiplicateur(Type.SPECTRE, Type.ROCHE) == 1
assert get_multiplicateur(Type.SPECTRE, Type.SOL) == 1
assert get_multiplicateur(Type.SPECTRE, Type.FEE) == 1
assert get_multiplicateur(Type.SPECTRE, Type.PSY) == 2
assert get_multiplicateur(Type.SPECTRE, Type.TENEBRE) == 0.5
assert get_multiplicateur(Type.SPECTRE, Type.SPECTRE) == 2
assert get_multiplicateur(Type.SPECTRE, Type.POISON) == 1
assert get_multiplicateur(Type.SPECTRE, Type.INSECTE) == 1
assert get_multiplicateur(Type.SPECTRE, Type.VOL) == 1
assert get_multiplicateur(Type.SPECTRE, Type.DRAGON) == 1
assert get_multiplicateur(Type.SPECTRE, Type.ACIER) == 1
assert get_multiplicateur(Type.SPECTRE, Type.GLACE) == 1

# Poison attack
assert get_multiplicateur(Type.POISON, Type.NORMAL) == 1
assert get_multiplicateur(Type.POISON, Type.FEU) == 1
assert get_multiplicateur(Type.POISON, Type.EAU) == 1
assert get_multiplicateur(Type.POISON, Type.PLANTE) == 2
assert get_multiplicateur(Type.POISON, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.POISON, Type.COMBAT) == 1
assert get_multiplicateur(Type.POISON, Type.ROCHE) == 0.5
assert get_multiplicateur(Type.POISON, Type.SOL) == 0.5
assert get_multiplicateur(Type.POISON, Type.FEE) == 2
assert get_multiplicateur(Type.POISON, Type.PSY) == 1
assert get_multiplicateur(Type.POISON, Type.TENEBRE) == 1
assert get_multiplicateur(Type.POISON, Type.SPECTRE) == 0.5
assert get_multiplicateur(Type.POISON, Type.POISON) == 0.5
assert get_multiplicateur(Type.POISON, Type.INSECTE) == 1
assert get_multiplicateur(Type.POISON, Type.VOL) == 1
assert get_multiplicateur(Type.POISON, Type.DRAGON) == 1
assert get_multiplicateur(Type.POISON, Type.ACIER) == 0
assert get_multiplicateur(Type.POISON, Type.GLACE) == 1

# Insecte attack
assert get_multiplicateur(Type.INSECTE, Type.NORMAL) == 1
assert get_multiplicateur(Type.INSECTE, Type.FEU) == 0.5
assert get_multiplicateur(Type.INSECTE, Type.EAU) == 1
assert get_multiplicateur(Type.INSECTE, Type.PLANTE) == 2
assert get_multiplicateur(Type.INSECTE, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.INSECTE, Type.COMBAT) == 0.5
assert get_multiplicateur(Type.INSECTE, Type.ROCHE) == 1
assert get_multiplicateur(Type.INSECTE, Type.SOL) == 1
assert get_multiplicateur(Type.INSECTE, Type.FEE) == 0.5
assert get_multiplicateur(Type.INSECTE, Type.PSY) == 2
assert get_multiplicateur(Type.INSECTE, Type.TENEBRE) == 2
assert get_multiplicateur(Type.INSECTE, Type.SPECTRE) == 0.5
assert get_multiplicateur(Type.INSECTE, Type.POISON) == 0.5
assert get_multiplicateur(Type.INSECTE, Type.INSECTE) == 1
assert get_multiplicateur(Type.INSECTE, Type.VOL) == 0.5
assert get_multiplicateur(Type.INSECTE, Type.DRAGON) == 1
assert get_multiplicateur(Type.INSECTE, Type.ACIER) == 0.5
assert get_multiplicateur(Type.INSECTE, Type.GLACE) == 1

# Vol attack
assert get_multiplicateur(Type.VOL, Type.NORMAL) == 1
assert get_multiplicateur(Type.VOL, Type.FEU) == 1
assert get_multiplicateur(Type.VOL, Type.EAU) == 1
assert get_multiplicateur(Type.VOL, Type.PLANTE) == 2
assert get_multiplicateur(Type.VOL, Type.ELECTRIQUE) == 0.5
assert get_multiplicateur(Type.VOL, Type.COMBAT) == 2
assert get_multiplicateur(Type.VOL, Type.ROCHE) == 0.5
assert get_multiplicateur(Type.VOL, Type.SOL) == 1
assert get_multiplicateur(Type.VOL, Type.FEE) == 1
assert get_multiplicateur(Type.VOL, Type.PSY) == 1
assert get_multiplicateur(Type.VOL, Type.TENEBRE) == 1
assert get_multiplicateur(Type.VOL, Type.SPECTRE) == 1
assert get_multiplicateur(Type.VOL, Type.POISON) == 1
assert get_multiplicateur(Type.VOL, Type.INSECTE) == 2
assert get_multiplicateur(Type.VOL, Type.VOL) == 1
assert get_multiplicateur(Type.VOL, Type.DRAGON) == 1
assert get_multiplicateur(Type.VOL, Type.ACIER) == 0.5
assert get_multiplicateur(Type.VOL, Type.GLACE) == 1

# Dragon attack
assert get_multiplicateur(Type.DRAGON, Type.NORMAL) == 1
assert get_multiplicateur(Type.DRAGON, Type.FEU) == 1
assert get_multiplicateur(Type.DRAGON, Type.EAU) == 1
assert get_multiplicateur(Type.DRAGON, Type.PLANTE) == 1
assert get_multiplicateur(Type.DRAGON, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.DRAGON, Type.COMBAT) == 1
assert get_multiplicateur(Type.DRAGON, Type.ROCHE) == 1
assert get_multiplicateur(Type.DRAGON, Type.SOL) == 1
assert get_multiplicateur(Type.DRAGON, Type.FEE) == 0
assert get_multiplicateur(Type.DRAGON, Type.PSY) == 1
assert get_multiplicateur(Type.DRAGON, Type.TENEBRE) == 1
assert get_multiplicateur(Type.DRAGON, Type.SPECTRE) == 1
assert get_multiplicateur(Type.DRAGON, Type.POISON) == 1
assert get_multiplicateur(Type.DRAGON, Type.INSECTE) == 1
assert get_multiplicateur(Type.DRAGON, Type.VOL) == 1
assert get_multiplicateur(Type.DRAGON, Type.DRAGON) == 2
assert get_multiplicateur(Type.DRAGON, Type.ACIER) == 0.5
assert get_multiplicateur(Type.DRAGON, Type.GLACE) == 1

# Acier attack
assert get_multiplicateur(Type.ACIER, Type.NORMAL) == 1
assert get_multiplicateur(Type.ACIER, Type.FEU) == 0.5
assert get_multiplicateur(Type.ACIER, Type.EAU) == 0.5
assert get_multiplicateur(Type.ACIER, Type.PLANTE) == 1
assert get_multiplicateur(Type.ACIER, Type.ELECTRIQUE) == 0.5
assert get_multiplicateur(Type.ACIER, Type.COMBAT) == 1
assert get_multiplicateur(Type.ACIER, Type.ROCHE) == 2
assert get_multiplicateur(Type.ACIER, Type.SOL) == 1
assert get_multiplicateur(Type.ACIER, Type.FEE) == 2
assert get_multiplicateur(Type.ACIER, Type.PSY) == 1
assert get_multiplicateur(Type.ACIER, Type.TENEBRE) == 1
assert get_multiplicateur(Type.ACIER, Type.SPECTRE) == 1
assert get_multiplicateur(Type.ACIER, Type.POISON) == 1
assert get_multiplicateur(Type.ACIER, Type.INSECTE) == 1
assert get_multiplicateur(Type.ACIER, Type.VOL) == 1
assert get_multiplicateur(Type.ACIER, Type.DRAGON) == 1
assert get_multiplicateur(Type.ACIER, Type.ACIER) == 0.5
assert get_multiplicateur(Type.ACIER, Type.GLACE) == 2

# Glace attack
assert get_multiplicateur(Type.GLACE, Type.NORMAL) == 1
assert get_multiplicateur(Type.GLACE, Type.FEU) == 0.5
assert get_multiplicateur(Type.GLACE, Type.EAU) == 0.5
assert get_multiplicateur(Type.GLACE, Type.PLANTE) == 2
assert get_multiplicateur(Type.GLACE, Type.ELECTRIQUE) == 1
assert get_multiplicateur(Type.GLACE, Type.COMBAT) == 1
assert get_multiplicateur(Type.GLACE, Type.ROCHE) == 1
assert get_multiplicateur(Type.GLACE, Type.SOL) == 2
assert get_multiplicateur(Type.GLACE, Type.FEE) == 1
assert get_multiplicateur(Type.GLACE, Type.PSY) == 1
assert get_multiplicateur(Type.GLACE, Type.TENEBRE) == 1
assert get_multiplicateur(Type.GLACE, Type.SPECTRE) == 1
assert get_multiplicateur(Type.GLACE, Type.POISON) == 1
assert get_multiplicateur(Type.GLACE, Type.INSECTE) == 1
assert get_multiplicateur(Type.GLACE, Type.VOL) == 2
assert get_multiplicateur(Type.GLACE, Type.DRAGON) == 2
assert get_multiplicateur(Type.GLACE, Type.ACIER) == 0.5
assert get_multiplicateur(Type.GLACE, Type.GLACE) == 0.5