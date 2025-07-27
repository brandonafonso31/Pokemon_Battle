from enum import Enum

class Type(Enum):
    NORMAL,FEU,EAU,PLANTE,ELECTRIQUE,COMBAT,ROCHE,SOL,FEE,PSY,TENEBRE,SPECTRE,POISON,INSECTE,VOL,DRAGON,ACIER,GLACE = range(18)
    
"""
print(Type.GLACE)           # Type.GLACE
print(Type.GLACE.name)      # "GLACE"
print(Type.GLACE.value)     # 17

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
    [0,2,0.5,0.5,1,1,2,2,1,1,1,1,1,1,1,0.5,1,1],            # eau
    [1,0.5,2,0.5,1,1,2,2,1,1,1,1,0.5,0.5,0.5,0.5,0.5,1],    # plante
    [1,1,2,0.5,0.5,1,1,0,1,1,1,1,1,1,2,0.5,1,1],            # electrique
    [2,1,1,1,1,1,2,1,0.5,0.5,2,0,0.5,0.5,0.5,1,2,2],        # combat
    [1,2,1,1,1,0.5,1,0.5,1,1,1,1,1,2,2,1,0.5,2],            # roche
    [0,2,1,0.5,2,1,2,1,1,1,1,1,2,0.5,0,1,2,1],              # sol
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