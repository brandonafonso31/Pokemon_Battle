class Talent:
    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.effect = effect    # fonction callable that applies the effect

    def __str__(self):
        return f"{self.name}: {self.description}"