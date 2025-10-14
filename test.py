
import battle_context as bc
from pokemon_init import dracaufeu,leviator
from battle_timing import Timing

bc.init_context_history()
test_context_1 = bc.create_context(Timing.ABOUT_TO_GET_HIT, dracaufeu, leviator, dracaufeu.move1, 84)
test_context_2 = bc.create_context(Timing.GOT_HIT, leviator, dracaufeu, leviator.move2, 130)