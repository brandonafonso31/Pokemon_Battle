from enum import Enum

class Nature(Enum):
    SOLO, RIGIDE,MAUVAIS, BRAVE, ASSURE, MALIN, LACHE, RELAX, MODESTE, DOUX, FOUFOU, DISCRET, CALME, PRUDENT, GENTIL, \
        MALPOLI, TIMIDE, PRESSE, JOVIAL, NAIF, HARDI, BIZARRE, PUDIQUE, DOCILE, SERIEUX = range(25)
        
    def __str__(self):
        return self.name
    
    def effect(self):
        stat_change = {"stat_boost": None,"stat_neg": None}
        # boost atk
        if self == Nature.SOLO:
            stat_change["stat_boost"] = "atk"
            stat_change["stat_neg"] = "def"
        elif self == Nature.RIGIDE:
            stat_change["stat_boost"] = "atk"
            stat_change["stat_neg"] = "atk_spe"
        elif self == Nature.MAUVAIS:
            stat_change["stat_boost"] = "atk"
            stat_change["stat_neg"] = "def_spe"
        elif self == Nature.BRAVE:
            stat_change["stat_boost"] = "atk"
            stat_change["stat_neg"] = "vit"
        
        #boost def
        elif self == Nature.ASSURE:
            stat_change["stat_boost"] = "def"
            stat_change["stat_neg"] = "atk"
        elif self == Nature.MALIN:
            stat_change["stat_boost"] = "def"
            stat_change["stat_neg"] = "atk_spe"
        elif self == Nature.LACHE:
            stat_change["stat_boost"] = "def"
            stat_change["stat_neg"] = "def_spe"
        elif self == Nature.RELAX:
            stat_change["stat_boost"] = "def"
            stat_change["stat_neg"] = "vit"
            
        # boost atk_spe
        elif self == Nature.MODESTE:
            stat_change["stat_boost"] = "atk_spe"
            stat_change["stat_neg"] = "atk"
        elif self == Nature.DOUX:
            stat_change["stat_boost"] = "atk_spe"
            stat_change["stat_neg"] = "def"
        elif self == Nature.FOUFOU:
            stat_change["stat_boost"] = "atk_spe"
            stat_change["stat_neg"] = "def_spe"
        elif self == Nature.DISCRET:
            stat_change["stat_boost"] = "atk_spe"
            stat_change["stat_neg"] = "vit"
            
        # boost def_spe
        elif self == Nature.CALME:
            stat_change["stat_boost"] = "def_spe"
            stat_change["stat_neg"] = "atk"
        elif self == Nature.PRUDENT:
            stat_change["stat_boost"] = "def_spe"
            stat_change["stat_neg"] = "atk_spe"
        elif self == Nature.GENTIL:
            stat_change["stat_boost"] = "def_spe"
            stat_change["stat_neg"] = "def"
        elif self == Nature.MALPOLI:
            stat_change["stat_boost"] = "def_spe"
            stat_change["stat_neg"] = "vit"
        
        # boost vit
        elif stat_change == Nature.TIMIDE:
            stat_change["stat_boost"] = "vit"
            stat_change["stat_neg"] = "atk"
        elif self == Nature.PRESSE:
            stat_change["stat_boost"] = "vit"
            stat_change["stat_neg"] = "def"
        elif self == Nature.JOVIAL:
            stat_change["stat_boost"] = "vit"
            stat_change["stat_neg"] = "atk_spe"
        elif self == Nature.NAIF:
            stat_change["stat_boost"] = "vit"
            stat_change["stat_neg"] = "def_spe"
        
        # les 5 talents qui: baisse et boost la même stat "dit neutre"
        else:
            stat_change["stat_boost"] = None
            stat_change["stat_neg"] = None
        return stat_change
    
"""pb=0
l_pb = []
for n in Nature:
    for n2 in Nature:
        if n!=n2 and n.effect() == n2.effect():
            if (n2,n) not in l_pb:
                l_pb.append((n,n2))
                pb +=1
    
print(f"{pb} ont le meme dico !")
for a,b in l_pb:
    if a == Nature.HARDI or b == Nature.HARDI or a == Nature.PUDIQUE or b == Nature.PUDIQUE or\
        a == Nature.DOCILE or b == Nature.DOCILE or a == Nature.SERIEUX or b == Nature.SERIEUX or\
            a == Nature.BIZARRE or b == Nature.BIZARRE:
                pass
    else:
        print(a,b)"""