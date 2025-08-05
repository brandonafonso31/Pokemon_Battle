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
        nb_pokemon = len(self.pokemon_team)
        pokemon.id = nb_pokemon
        if nb_pokemon >= 6:
            print(f"{self.name} a déjà 6 Pokémon dans son équipe.")
            self.pc.append(pokemon)
            print(f"{pokemon.name} a été envoyé dans la boîte PC.")
        else:
            pokemon.trainer = self
            pokemon.nickname = nickname if nickname is not None else pokemon.name
            self.pokemon_team.append(pokemon)
            print(f"{self.name} a capturé {pokemon.name}")
            
    def send_next(self):
        team = self.pokemon_team
        for i in range(len(team)):
            if team[i].pv != 0:
                #afficher un texte poour annoncer l'arrive du suivant
                return team[i],True
        return None,False
 
from pokemon_init import leviator,dracaufeu,ectoplasma    
trainer_ai = Trainer("Ash")
trainer_ai.catch_pokemon(dracaufeu)
trainer_ai.catch_pokemon(ectoplasma)
trainer = Trainer("Brandon")
trainer.catch_pokemon(leviator)
print(trainer_ai,trainer,sep="\n")