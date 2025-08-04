from pokemon import Pokemon

# Une class en plus poour pokemon_team ?

class Dresseur:
    def __init__(self, name: str):
        self.name = name
        self.pokemon_team = []
    
    def __str__(self):
        string  = f"Dresseur: {self.name}\nPokémon:\n"
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
    
    def capturer(self, pokemon: Pokemon):
        pokemon.dresseur = self
        self.pokemon_team.append(pokemon)
 
from pokemon_init import leviator,dracaufeu,pikachu     
dresseur_test = Dresseur("Ash")
dresseur_test.capturer(leviator)
dresseur_test.capturer(dracaufeu)
dresseur_test.capturer(pikachu)
print(dresseur_test)