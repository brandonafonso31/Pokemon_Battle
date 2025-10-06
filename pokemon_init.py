from pokemon_type import Type
from pokemon_move import *
from pokemon_nature import Nature
from pokemon_ability import abilities
from pokedex import create_pokemon

#--------------------------------------| Dracaufeu |--------------------------------------#
dracaufeu_EV = {"hp":0,"atk":0,"def_":0,"atk_spe":252,"def_spe":6,"vit":252}
dracaufeu = create_pokemon(6,nature=Nature.MODESTE,EV=dracaufeu_EV,num_on_sprite_sheet=7)

lance_flamme = SpecialMove("Lance-Flammes",Type.FEU,power=90,accuracy=100,pp=15, effect = dico_effect_move["Lance-Flammes"], prio = 0)
crocs_eclair = SpecialMove("Croc-éclair",Type.ELECTRIQUE,power=90,accuracy=100,pp=15, effect = dico_effect_move["Croc-éclair"], prio = 0)
lance_soleil = SpecialMove("Lance-Soleil",Type.PLANTE,power=90,accuracy=100,pp=15, effect = dico_effect_move["Lance-Soleil"], prio = 0)
atterisage = StatusMove("Atterisage",Type.VOL,accuracy=100,pp=15, effect = dico_effect_move["Atterissage"], prio = 0)

dracaufeu.learn_move(lance_flamme)
dracaufeu.learn_move(crocs_eclair)
dracaufeu.learn_move(lance_soleil)
#dracaufeu.learn_move(atterisage)
dracaufeu.change_ability(abilities["Intimidation"]())
#print(dracaufeu)
#--------------------------------------| Léviator |---------------------------------------#
leviator_EV = {"hp":6,"atk":252,"def_":0,"atk_spe":0,"def_spe":0,"vit":252}
leviator = create_pokemon(130, EV=leviator_EV, nature=Nature.RIGIDE, num_on_sprite_sheet=151)


crocgivre = PhysicalMove("Crocs Givre",Type.GLACE,power=65,accuracy=95,pp=15, effect = dico_effect_move["Crocs Givre"], prio = 0)
cascade = PhysicalMove("Cascade",Type.EAU,power=80,accuracy=100,pp=15, effect = dico_effect_move["Cascade"], prio = 0)
danse_draco = StatusMove("Danse Draco",Type.DRAGON,accuracy=100,pp=20, effect = dico_effect_move["Danse Draco"], prio = 0)
seisme = PhysicalMove("Séisme",Type.SOL,power=100,accuracy=100,pp=10, effect = dico_effect_move["Séisme"], prio = 0)
aquajet = PhysicalMove("Aqua-Jet",Type.EAU,power=40,accuracy=100,pp=20, effect = dico_effect_move["Aqua-Jet"], prio = 1)

leviator.learn_move(crocgivre)
leviator.learn_move(cascade)
leviator.learn_move(aquajet)
leviator.learn_move(seisme)
leviator.change_ability(abilities["Intimidation"]())
#print(leviator)
#--------------------------------------| Pikachu |----------------------------------------#
pikachu_EV = {"hp":252,"atk":252,"def_":252,"atk_spe":252,"def_spe":252,"vit":252}
pikachu = create_pokemon(25,nature=Nature.BRAVE,EV=dracaufeu_EV,num_on_sprite_sheet=30)

cage_eclair = StatusMove("Cage-Éclair",Type.ELECTRIQUE,accuracy=90,pp=20, effect = dico_effect_move["Cage-Éclair"], prio = 0)

pikachu.learn_move(cage_eclair)
"""pikachu.learn_move("fatal-foudre")
pikachu.learn_move("chargeur")
pikachu.learn_move("électacle")"""
#print(pikachu)
#--------------------------------------| Ectoplasma |----------------------------------------#

gengar_Ev = {"hp":6,"atk":0,"def_":0,"atk_spe":252,"def_spe":0,"vit":252}
gengar = create_pokemon(94,nature=Nature.MODESTE,EV=gengar_Ev,num_on_sprite_sheet=108)
gengar.change_ability(abilities["Intimidation"]())

tonnerre = SpecialMove("Tonnerre",Type.ELECTRIQUE,power=90,accuracy=100,pp=15, effect = dico_effect_move["Tonnerre"], prio = 0)
balle_ombre = SpecialMove("Balle'Ombre",Type.SPECTRE,power=80,accuracy=100,pp=10, effect = dico_effect_move["Balle'Ombre"], prio = 0)
gengar.learn_move(tonnerre)
gengar.learn_move(balle_ombre)
print(gengar)