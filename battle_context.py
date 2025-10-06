import json
from config import battle_history_path


class BattleContext:
    """Représente un événement de combat (ex: GOT_HIT, START, END, etc.)."""

    def __init__(
        self,
        timing: str,
        attacker,
        defender,
        move=None,
        damage: int = 0,
    ):
        self.timing = timing
        self.attacker = attacker
        self.defender = defender
        self.move = move
        self.damage = damage
        self.cancel_attack = False
        self.extra = {}  # pour stocker des infos supplémentaires selon le contexte

    def to_dict(self) -> dict:
        """Retourne une version sérialisable du contexte."""
        return {
            "timing": self.timing,
            "attacker": str(self.attacker),
            "defender": str(self.defender),
            "move": str(self.move),
            "damage": self.damage,
            "cancel_attack": self.cancel_attack,
            "extra": self.extra,
        }

    def __repr__(self) -> str:
        return (
            f"<Context {self.timing}: {self.attacker} vs {self.defender}, "
            f"move={self.move}, dmg={self.damage}, cancel={self.cancel_attack}>"
        )


# === Fonctions utilitaires pour la gestion de l’historique === #

def init_context_history():
    """Réinitialise le fichier d'historique des contextes."""
    with open(battle_history_path, "w", encoding="utf-8") as f:
        f.write("")


def create_context(timing: str, attacker, defender, move=None, damage: int = 0):
    """Crée un nouveau contexte de combat."""
    return BattleContext(timing, attacker, defender, move, damage)


def add_context_to_history(context: BattleContext) -> None:
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


# === Exemple de test / démo === #
if __name__ == "__main__":
    init_context_history()

    test_context_1 = create_context("ABOUT_TO_GET_HIT", "Pikachu", "Bulbasaur", "Thunderbolt", 42)
    test_context_2 = create_context("GOT_HIT", "Charmander", "Squirtle", "Tackle", 12)

    add_context_to_history(test_context_1)
    add_context_to_history(test_context_2)

    print(test_context_1)
    print(test_context_2)
