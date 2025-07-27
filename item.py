class Item:
    def __init__(self,name:str,effect:str = ""):
        self.name = name
        self.effect = effect
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __str__(self):
        return self.name
    