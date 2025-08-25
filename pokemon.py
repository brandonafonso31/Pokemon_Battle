from sprite import *
from pokemon_type import *
from pokemon_move import *
from random import randint
from config import img_dir_path,cries_dir_path
from pokemon_nature import Nature
from math import floor
from pokemon_talent import Talent
from random import randint,choice
import os, pygame

LINE_PRINT = "-"*100

class Pokemon:
    def __init__(self,name: str,hp: int,atk: int,def_: int,atk_spe: int,def_spe: int,vit: int, \
        gen: int,type1: Type, nature:Nature= Nature.BIZARRE, EV={"hp":0,"atk":0,"def_":0,"atk_spe":0,"def_spe":0,"vit":0}, \
            type2=None,talent:Talent=None,num_on_sprite_sheet=None,item=None,id_num=0,nickname="",howl_path=""):
        
        # Infos
        self.name = name
        self.id = id_num
        self.nature = nature
        self.nickname = nickname
        
        # Stats Meilleurs avec dic_stat = {} ?
        self.EV = EV
        self.hp = real_hp(hp,EV["hp"])
        self.atk = real_stat("atk",atk,nature,EV["atk"])
        self.def_ = real_stat("def_",def_,nature,EV["def_"])
        self.atk_spe = real_stat("atk_spe",atk_spe,nature,EV["atk_spe"])
        self.def_spe = real_stat("def_sep",def_spe,nature,EV["def_spe"])
        self.vit = real_stat("vit",vit,nature,EV["vit"])
        self.hp_max = self.hp      
        
        self.legit = self.check_sum_EV() and self.check_each_EV()
        self.is_ko = False
        # Buff / Debuff
        self.stats_modifier = { 
            "hp": 0,
            "atk": 0,
            "def_": 0,
            "atk_spe": 0,
            "def_spe": 0,
            "vit": 0
        }
        
        # Types
        self.type1 = type1
        self.type2 = type2 
        
        # Sprite
        self.gen = gen
        self.num_on_sprite_sheet = num_on_sprite_sheet
        self.rect = None
        
        # Meilleurs avec juste self.moveset = [] ?
        self.move1 = None
        self.move2 = None
        self.move3 = None
        self.move4 = None
        
        # Talent
        self.talent = talent
        
        # Howl
        self.howl_path = howl_path
        
        # A implementer
        self.trainer = None         # Dresseur ? je sais plus pour quoi faire ... pour différencier 2 pokemons identiques ?
        self.shiny = False          # change uniquement les scripts
        self.item = item            # objet tenu par le pokémon
    
    def __str__(self):
        output = f"{LINE_PRINT}\n{self.name} | {self.show_type()} | Talent: {self.talent} | Nature: {self.nature}\n{LINE_PRINT}"
        return output + f"\nStats:\n{self.show_stats()}\n{LINE_PRINT}\nMoves:\n{self.show_moves()}\n{LINE_PRINT}\n"
    
    def __eq__(self, other):
        return self.id == other.id  and self.trainer == other.trainer # id sera implémenter dans la classe Team_Pokemon est sera de 1 à 6 unique et vérifié
        """return self.name == other.name and self.dresseur == other.dresseur \
            and self.EV == other.EV and self.get_moveset() == other.get_moveset() \
                and self.get_stats() == other.get_stats() and self.nickname == other.nickname \
                    and self.talent == other.talent and self.nature == other.nature \
                        and self.shiny == other.shiny and self.item == other.item"""
    
    
    def show_type(self):
        types = f"TYPE1: {self.type1.name}"
        if self.type2 != None:
            types += f", TYPE2: {self.type2.name}"
        return types
    def get_stats(self):
        return [self.hp,self.atk,self.def_,self.atk_spe,self.def_spe,self.vit]
    def show_stats(self):
        return f"hp: {self.hp},\nATK: {self.atk},\nDEF: {self.def_},\nATK_SPE: {self.atk_spe},\nDEF_SPE: {self.def_spe},\nVIT: {self.vit}"
    
    
    def show_moves(self):
        return f"Move1: {self.move1},\nMove2: {self.move2},\nMove3: {self.move3}, \nMove4: {self.move4}"
    def learn_move(self, new_move: Move):
        if new_move in [self.move1, self.move2, self.move3, self.move4]:
            print(f"L'attaque {new_move} est déjà apprise")
            return
        if self.move1 is None:
            self.move1 = new_move
        elif self.move2 is None:
            self.move2 = new_move 
        elif self.move3 is None:
            self.move3 = new_move 
        elif self.move4 is None:
            self.move4 = new_move 
        else:
            move_to_remove = "move" + str(input(f"Choisir un move à remplacer :  {self.show_moves()} → "))
            try:
                setattr(self, move_to_remove, new_move)
            except Exception:
                print(f"Erreur : move '{move_to_remove}' inexistant.")
                self.learn_move(new_move)
                return

        print(f"L'attaque {new_move} a été apprise\n")
        
    
    
    def sprites(self,front_or_back,save_to_filename):
        sprites = os.path.join(sprites_dir_path,f"sprites_gen{self.gen}")
        return recup_sprite_pokemon(sprites, self.num_on_sprite_sheet, front_or_back,self.id)
        
    
    
    def get_cm(self, opponent, move : Move, objects=None):
        """CM est une multiplication : (stab) x (efficacité) x (objets tenus) x (talents) x (climats) x (un nbre entre 0.85 et 1) x crit"""
        msg = ""
        rand = randint(85,100)
        
        if self.type1 is None and self.type2 is not None :
            self.type1, self.type2 = self.type2, None
            
        if self.type2 is None:
            eff = get_multiplicateur(move.type,self.type1)
        else:
            eff = get_double_multiplicateur(move.type,opponent.type1,opponent.type2)
            
        stab = (move.type == self.type1 or move.type == self.type2) + 1
        
        if eff == 4:
            msg+="C'est hyper efficace !"
        elif eff == 2:
            msg+="C'est super efficace !"
        elif eff ==1:
            msg+="C'est efficace"
        elif eff == 0.5:
            msg+="Ce n'est pas très efficace"
        elif eff == 0.25:
            msg+="Ce n'est vraiment pas efficace"
        elif eff == 0:
            msg+="Cela ne fait aucun dégat"
        print(msg)
        return stab * eff * rand/100    # a ajouter |---> * crit * objets * talents * climats
            
    def use_move(self, move_id: str, opponent, window):
        move = getattr(self, move_id) 
        # PP check
        if move.pp < 1:
            print(f"No PP left for {move.name}")
            return None  # Signal to request another move
        move.pp -= 1
        print(f"{self.name} uses {move.name}")
        # Calculate damage
        damage = 0
        if isinstance(move, SpecialMove):
            damage = get_damage(self.atk_spe, opponent.def_spe, move.power)
        elif isinstance(move, PhysicalMove):
            damage = get_damage(self.atk, opponent.def_, move.power)
        elif isinstance(move, StatusMove):
            # TODO: Implement status effects
            print(f"{move.name} has status effects!")
            return self, opponent
        # Apply type effectiveness
        damage *= self.get_cm(opponent, move)
        damage = max(0, floor(damage))
        # Apply damage
        old_hp = opponent.hp
        opponent.hp -= damage
        if opponent.hp <= 0:
            opponent.hp = 0
            print(f"{opponent.name} fainted!")
        return self, opponent, old_hp
    
            
    def heal(self):
        self.hp = self.hp_max
        self.is_ko = False
        print(f"{self.name} a été soigné")
        return self
    
    def get_moveset(self):
        return [move for move in [self.move1, self.move2, self.move3, self.move4] if move is not None]

    def is_dead(self):
        return self.hp <= 0
    
    def check_sum_EV(self):
        return sum([_ for _ in self.EV.values()]) <= 510
            
    def check_each_EV(self):
        return all([_ <= 252 for _ in self.EV.values()])

    def add_rect(self,coord,scale = 2):
        self.rect = pygame.Rect(coord[0], coord[1], 100*scale, 100*scale)
    
    
    def change_talent(self, talent: Talent):
        self.talent = talent
        print(f"{self.name} a désormais le talent {talent}")
        
    def change_stat_from_buff_debuff(self, stat_name):
        """Renvoie la stat modifiée par les stages."""
        scale = self.stats_modifier[stat_name]
        base_value = getattr(self, stat_name)
        if scale >= 0:
            ratio = (2 + scale) / 2
        else:
            ratio = 2 / (2 - scale)
        return int(base_value * ratio)
        
    def add_buff_debuff(self, stat_name, scale=1):
        boolean_change_stat = False
        stat = self.stats_modifier[stat_name]
        if stat >= 6 and scale > 0:
            print(f"{self.name} ne peut pas augmenter {stat_name} au delà de 6")
        elif stat <= -6 and scale < 0:
            print(f"{self.name} ne peut pas baisser {stat_name} en dessous de -6")
        else:
            stat += scale
            boolean_change_stat = True
        return boolean_change_stat
            
    def apply_buff_debuff(self, stat_name, scale=1):
        """Applique un buff ou un debuff à une stat."""
        if stat_name not in self.stats_modifier:
            print(f"Stat {stat_name} non reconnue.")
            return
        
        boolean_change_stat = self.add_buff_debuff(stat_name, scale)
        if boolean_change_stat:
            self.change_stat_from_buff_debuff(stat_name)
            if scale > 0 :
                print(f"{self.name} a augmenté {stat_name} de {scale} stages.")
            elif scale < 0 :
                print(f"{self.name} a diminué {stat_name} de {-scale} stages.")


    def play_howl(self):
        """Joue le cri du Pokémon KO"""
        sound = pygame.mixer.Sound(self.howl_path)
        sound.play()


    def animate_death(self, window, front_or_back, elapsed):
        """
        Anime la disparition du Pokémon KO (appelée à chaque frame par ko()).
        - elapsed : temps écoulé depuis le début de l’anim
        """
        with open("data/actual_battle.json") as f:
            json_data = json.load(f)

        background = pygame.image.load(json_data["background"]).convert()
        current_pokemon_id = json_data["current"]
        pokemon = "opponent" if front_or_back == "front" else "trainer"
        x, y = json_data[pokemon][str(current_pokemon_id[pokemon == "opponent"])]["x"], \
            json_data[pokemon][str(current_pokemon_id[pokemon == "opponent"])]["y"]

        scale = 2 + (front_or_back == "back")
        w = 100 * scale
        rect = pygame.Rect(x, y, w, w)

        # Exemple très simple : après 1s, efface le sprite
        if elapsed >= 1:
            window.blit(background, rect, rect)  # on efface le sprite
            return True  # animation terminée
        return False  # animation encore en cours

        
def get_scale_by_nature(stat_name: str, nature: Nature):
    return 1.1 if stat_name == nature.effect()["stat_boost"] else 0.9 if stat_name == nature.effect()["stat_neg"] else 1
     
def real_hp(hp:int, EV:int, IV=31, niv=50):
    hp = (2 * hp + IV + EV//4) * niv
    hp = hp// 100 + niv + 10
    return hp

def real_stat(stat_name:str, stat:int, nature:Nature, EV:int, IV=31, niv=50):
    stat = (2 * stat + IV + EV//4) * niv
    stat = stat//100 + 5
    return floor(stat*get_scale_by_nature(stat_name,nature))                                          

def get_damage(x,y,z,niv=50):
    damage = (niv * 0.4 +2) * z * x
    damage = damage//(y * niv) + 2
    return damage