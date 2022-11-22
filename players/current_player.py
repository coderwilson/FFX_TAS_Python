import memory
from players.auron import Auron
from players.base import Player
from players.kimahri import Kimahri
from players.lulu import Lulu
from players.rikku import Rikku
from players.tidus import Tidus
from players.wakka import Wakka
from players.yuna import Yuna


def CurrentPlayer():
    current_character = memory.main.get_current_turn()
    match current_character:
        case 0:
            return Tidus
        case 1:
            return Yuna
        case 2:
            return Auron
        case 3:
            return Kimahri
        case 4:
            return Wakka
        case 5:
            return Lulu
        case 6:
            return Rikku
        case _:
            raise NotImplementedError(
                f"No player class implemented for {current_character}"
            )
