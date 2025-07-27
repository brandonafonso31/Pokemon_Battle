from pokemon import *


class Dresseur:
    def __init__(self, name: str, pokemon_team: list):
        self.name = name
        self.pokemon_team = []
    
    def __str__(self):
        return self.name
    
    def capturer(self, pokemon: Pokemon):
        pokemon.dresseur = self
        self.pokemon_team.append(pokemon)
        
    