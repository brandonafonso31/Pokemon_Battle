# Une class en plus pour pokemon_team ?
import sprite,pygame,json,os
from config import battle_json_path,resolution

class Pokemon_trainer:
    def __init__(self, name: str):
        self.name = name
        self.pokemon_team = []
        self.pc = []
    
    def __str__(self):
        string  = f"Dresseur: {self.name}\nPokémon:"
        if len(self.pokemon_team)>0:
            string += f"\n{self.pokemon_team[0]}"
        if len(self.pokemon_team)>1:
            string +=f"\n{self.pokemon_team[1]}"
        if len(self.pokemon_team)>2:
            string += f"\n{self.pokemon_team[2]}"
        if len(self.pokemon_team)>3:
            string += f"\n{self.pokemon_team[3]}"
        if len(self.pokemon_team)>4:
            string += f"\n{self.pokemon_team[4]}"
        if len(self.pokemon_team)>5:
            string += f"\n{self.pokemon_team[5]}"
        return string
    
    def catch_pokemon(self, pokemon, nickname=None):
        nb_pokemon = len(self.pokemon_team)
        pokemon.id = nb_pokemon
        if nb_pokemon >= 6:
            print(f"{self.name} a déjà 6 Pokémon dans son équipe.")
            self.pc.append(pokemon)
            print(f"{pokemon.name} a été envoyé dans la boîte PC.")
        else:
            pokemon.trainer = self
            pokemon.nickname = nickname if nickname is not None else pokemon.name
            pokemon.id = len(self.pokemon_team) + 1
            self.pokemon_team.append(pokemon)
            print(f"{self.name} a capturé {pokemon.name}")
            
    def send_next(self,front_or_back: str):
        with open(battle_json_path, "r") as f:
            data = json.load(f)
        team = self.pokemon_team
        for i in range(len(team)):
            pokemon = team[i]
            if pokemon.hp != 0:
                # afficher un texte poour annoncer l'arrive du suivant                
                with open(battle_json_path, "r") as f:
                    data = json.load(f)
                dic = data["current"]
                dic = {"current": [dic[0],i+1]} if front_or_back == "front" else {"current": [i+1,dic[1]]}
                sprite.update_battle_json(dic)
                pokemon.play_howl()
                return pokemon,True
        return None,False
    
    def set_team_into_json(self,trainer_or_opponent: str):      
        pokemon_team = {}
        for i in range(len(self.pokemon_team)):
            pokemon = self.pokemon_team[i]
            if trainer_or_opponent == "trainer":
                data = sprite.get_trainer_sprite(resolution, pokemon, i+1, f"pokemon_back_{i+1}.png")
            else:
                data = sprite.get_opponent_sprite(resolution, pokemon, i+1, f"pokemon_front_{i+1}.png")
            pokemon_team[str(i+1)] = data      
        
        sprite.update_battle_json({trainer_or_opponent: pokemon_team})   

def get_trainer():       
    from pokemon_init import leviator,dracaufeu,ectoplasma    
    trainer_ai = Pokemon_trainer("Ash")
    trainer_ai.catch_pokemon(dracaufeu)
    trainer_ai.catch_pokemon(ectoplasma)
    trainer = Pokemon_trainer("Brandon")
    trainer.catch_pokemon(leviator)
    print(trainer_ai,trainer,sep="\n")

    trainer.set_team_into_json("trainer")
    trainer_ai.set_team_into_json("opponent")
    sprite.update_battle_json({"current": [1,1]})
    return trainer,trainer_ai
