from pokemon import Pokemon
from typing import override

class Item:
    def __init__(self,name:str,effect:str = ""):
        self.name = name
        self.effect = effect
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __str__(self):
        return self.name
    
    def use(self,pokemon:Pokemon):
        pass
    
class Balls(Item):
    def __init__(self,name:str,effect:str = ""):
        super().__init__(name, effect)
        
    @override    
    def use(self,pokemon:Pokemon):
        pass

class Heals(Item):
    def __init__(self,name:str,effect:str = ""):
        super().__init__(name, effect)
        
class Heal_Status(Item):
    def __init__(self,name:str,effect:str = ""):
        super().__init__(name, effect)
        
class Fight_object(Item):
    def __init__(self,name:str,effect:str = ""):
        super().__init__(name, effect)