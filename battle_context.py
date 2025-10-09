import json
from config import battle_history_path,last_context_path


class BattleContext:

    def __init__(self, timing: str,attacker, defender, move=None, damage: int = 0):
        self.timing = timing
        self.attacker = attacker
        self.defender = defender
        self.move = move
        self.damage = damage
        self.cancel_attack = False

    def to_dict(self):
        """Retourne une version sérialisable du contexte."""
        return {
            "timing": self.timing.name,
            "attacker": self.attacker.name,
            "defender": self.defender.name,
            "move": str(self.move),
            "damage": self.damage,
            "cancel_attack": self.cancel_attack
        }

    def __repr__(self):
        return (
            f"<Context {self.timing}: {self.attacker} vs {self.defender}, "
            f"move={self.move}, dmg={self.damage}, cancel={self.cancel_attack}>"
        )


def init_context_history():
    """Réinitialise le fichier d'historique des contextes."""
    with open(battle_history_path, "w", encoding="utf-8") as f:
        f.write("")


def create_context(timing: str, attacker, defender, move=None, damage: int = 0):
    """Crée un nouveau contexte de combat."""
    context = BattleContext(timing, attacker, defender, move, damage)
    add_context_to_history(context)
    set_last_context(context)
    return context


def add_context_to_history(context: BattleContext):
    """Ajoute le contexte au fichier JSON sous forme d'objet indexé."""
    try:
        with open(battle_history_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    index = str(len(data))
    data[index] = context.to_dict()

    with open(battle_history_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
def set_last_context(context: BattleContext):
    with open(last_context_path, "w", encoding="utf-8") as f:
        json.dump(context.to_dict(), f, ensure_ascii=False, indent=2)


"""from battle_timing import Timing
from pokemon_init import dracaufeu,leviator

init_context_history()
test_context_1 = create_context(Timing.ABOUT_TO_GET_HIT, dracaufeu, leviator, dracaufeu.move1, 84)
test_context_2 = create_context(Timing.GOT_HIT, leviator, dracaufeu, leviator.move2, 130)
add_context_to_history(test_context_1)
add_context_to_history(test_context_2)

set_last_context(test_context_1)
set_last_context(test_context_2)"""