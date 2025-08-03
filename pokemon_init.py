from pokemon import Pokemon
from pokemon_type import Type
from pokemon_move import *
from pokemon_nature import Nature
from pokemon_talent import Talent,talents

#--------------------------------------| Dracaufeu |--------------------------------------#
dracaufeu_EV = {"hp":0,"atk":0,"def_":0,"atk_spe":252,"def_spe":6,"vit":252}
dracaufeu = Pokemon("Dracaufeu",hp=78,atk=84,def_=78,atk_spe=109,def_spe=85,vit=100,gen=1,
                    type1=Type.FEU,type2=Type.VOL,num_on_sprite_sheet=7,EV=dracaufeu_EV,nature=Nature.MODESTE)

lance_flamme = SpecialMove("Lance-Flammes",Type.FEU,power=90,precision=100,pp=15, effect = dico_effect_move["Lance-Flammes"], prio = 0)
crocs_eclair = SpecialMove("Croc-éclair",Type.ELECTRIQUE,power=90,precision=100,pp=15, effect = dico_effect_move["Croc-éclair"], prio = 0)
lance_soleil = SpecialMove("Lance-Soleil",Type.PLANTE,power=90,precision=100,pp=15, effect = dico_effect_move["Lance-Soleil"], prio = 0)
atterisage = StatusMove("Atterisage",Type.VOL,precision=100,pp=15, effect = dico_effect_move["Atterissage"], prio = 0)

dracaufeu.learn_move(lance_flamme)
#dracaufeu.learn_move(crocs_eclair)
dracaufeu.learn_move(lance_soleil)
#dracaufeu.learn_move(atterisage)
dracaufeu.change_talent(talents["Intimidation"]())
print(dracaufeu)
#--------------------------------------| Léviator |---------------------------------------#
leviator_EV = {"hp":6,"atk":252,"def_":0,"atk_spe":0,"def_spe":0,"vit":252}
leviator = Pokemon("Léviator",hp=95,atk=125,def_=79,atk_spe=60,def_spe=100,vit=81,gen=1,
                   type1=Type.EAU,type2=Type.VOL,num_on_sprite_sheet=151,EV=leviator_EV, nature=Nature.RIGIDE)

crocgivre = PhysicalMove("Crocs Givre",Type.GLACE,power=65,precision=95,pp=15, effect = dico_effect_move["Crocs Givre"], prio = 0)
cascade = PhysicalMove("Cascade",Type.EAU,power=80,precision=100,pp=15, effect = dico_effect_move["Cascade"], prio = 0)
danse_draco = StatusMove("Danse Draco",Type.DRAGON,precision=100,pp=20, effect = dico_effect_move["Danse Draco"], prio = 0)
seisme = PhysicalMove("Séisme",Type.SOL,power=100,precision=100,pp=10, effect = dico_effect_move["Séisme"], prio = 0)
aquajet = PhysicalMove("Aqua-Jet",Type.EAU,power=40,precision=100,pp=20, effect = dico_effect_move["Aqua-Jet"], prio = 1)

leviator.learn_move(crocgivre)
leviator.learn_move(cascade)
leviator.learn_move(aquajet)
leviator.learn_move(seisme)
leviator.change_talent(talents["Intimidation"]())
print(leviator)
#--------------------------------------| Pikachu |----------------------------------------#
pikachu_EV = {"hp":252,"atk":252,"def_":252,"atk_spe":252,"def_spe":252,"vit":252}
pikachu = Pokemon("Pikachu",hp=35,atk=55,def_=40,atk_spe=50,def_spe=50,vit=90,gen=1,
                   type1=Type.ELECTRIQUE,num_on_sprite_sheet=30,EV=pikachu_EV, nature=Nature.BRAVE)

cage_eclair = StatusMove("Cage-Éclair",Type.ELECTRIQUE,precision=90,pp=20, effect = dico_effect_move["Cage-Éclair"], prio = 0)

pikachu.learn_move(cage_eclair)
"""pikachu.learn_move("fatal-foudre")
pikachu.learn_move("chargeur")
pikachu.learn_move("électacle")"""
print(pikachu)