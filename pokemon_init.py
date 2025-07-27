from pokemon import Pokemon
from pokemon_type import *
from move import *

#--------------------------------------| Dracaufeu |--------------------------------------#
dracaufeu = Pokemon("Dracaufeu",pv=78,atk=84,def_=78,atk_spe=109,def_spe=85,vit=100,gen=1,
                    type1=Type.FEU,type2=Type.VOL,talent="brasier",num_on_sprite_sheet=7)

lance_flamme = SpecialMove("Lance-Flammes",Type.FEU,power=90,precision=100,pp=15, effect = dico_effect_move["Lance-Flammes"], prio = 0)
crocs_eclair = SpecialMove("Croc-éclair",Type.ELECTRIQUE,power=90,precision=100,pp=15, effect = dico_effect_move["Croc-éclair"], prio = 0)
lance_soleil = SpecialMove("Lance-Soleil",Type.PLANTE,power=90,precision=100,pp=15, effect = dico_effect_move["Lance-Soleil"], prio = 0)
atterisage = StatusMove("Atterisage",Type.VOL,precision=100,pp=15, effect = dico_effect_move["Atterissage"], prio = 0)

dracaufeu.learn_move(lance_flamme)
dracaufeu.learn_move(crocs_eclair)
dracaufeu.learn_move(lance_soleil)
dracaufeu.learn_move(atterisage)
#print(dracaufeu)
#--------------------------------------| Léviator |---------------------------------------#
leviator = Pokemon("Léviator",pv=95,atk=125,def_=79,atk_spe=60,def_spe=100,vit=81,gen=1,
                   type1=Type.EAU,type2=Type.VOL,talent="intimidation",num_on_sprite_sheet=151)

crocgivre = PhysicalMove("Crocs Givre",Type.GLACE,power=65,precision=95,pp=15, effect = dico_effect_move["Crocs Givre"], prio = 0)

leviator.learn_move(crocgivre)
leviator.learn_move("cascade")
leviator.learn_move("danse draco")
leviator.learn_move("séïsme")
#print(leviator)
#--------------------------------------| Pikachu |----------------------------------------#
pikachu = Pokemon("Pikachu",pv=35,atk=55,def_=40,atk_spe=50,def_spe=50,vit=90,gen=1,
                   type1=Type.ELECTRIQUE,talent="paratonerre",num_on_sprite_sheet=30)

cageeclair = StatusMove("Cage-Éclair",Type.ELECTRIQUE,precision=90,pp=20, effect = dico_effect_move["Cage-Éclair"], prio = 0)

pikachu.learn_move(cageeclair)
"""pikachu.learn_move("fatal-foudre")
pikachu.learn_move("chargeur")
pikachu.learn_move("électacle")"""
#print(pikachu)