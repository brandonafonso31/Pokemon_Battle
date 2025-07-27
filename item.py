from pokemon import Pokemon

class Item:
    def __init__(self,name:str,effect:str = ""):
        self.name = name
        self.effect = effect
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __str__(self):
        return self.name
    
class Balls(Item):
    def __init__(self,name:str,effect:str = ""):
        super(Item)
        
    def throw(self,pokemon:Pokemon):
        pass

class Heals(Item):
    def __init__(self,name:str,effect:str = ""):
        super(Item)

class Heal_Status(Item):
    def __init__(self,name:str,effect:str = ""):
        super(Item)
        
class Fight_object(Item):
    def __init__(self,name:str,effect:str = ""):
        super(Item)