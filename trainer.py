# Une class en plus pour pokemon_team ?

class Trainer:
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
        nb_pokmeon = len(self.pokemon_team)
        pokemon.id = nb_pokmeon
        if nb_pokmeon >= 6:
            print(f"{self.name} a déjà 6 Pokémon dans son équipe.")
            self.pc.append(pokemon)
            print(f"{pokemon.name} a été envoyé dans la boîte PC.")
        else:
            pokemon.trainer = self
            pokemon.nickname = nickname if nickname is not None else pokemon.name
            self.pokemon_team.append(pokemon)
            print(f"{self.name} a capturé {pokemon.name}")
        
    def change_pokemon(self, pokemon_id, new_pokemon):
        if 0 <= pokemon_id < len(self.pokemon_team):
            old_pokemon = self.pokemon_team[pokemon_id]
            self.pokemon_team[pokemon_id] = new_pokemon
            print(f"{self.name} a remplacé {old_pokemon.name} par {new_pokemon.name}")
        else:
            print(f"ID de Pokémon invalide: {pokemon_id}.")
 
from pokemon_init import leviator,dracaufeu,pikachu     
trainer_ai = Trainer("Ash")
trainer_ai.catch_pokemon(dracaufeu)
trainer = Trainer("Brandon")
trainer.catch_pokemon(leviator)
print(trainer_ai,trainer,sep="\n")