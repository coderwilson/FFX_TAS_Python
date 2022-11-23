import memory
from players.anima import Anima
from players.auron import Auron
from players.bahamut import Bahamut
from players.base import Player
from players.ifrit import Ifrit
from players.ixion import Ixion
from players.kimahri import Kimahri
from players.lulu import Lulu
from players.magus_sisters import Cindy, Mindy, Sandy
from players.rikku import Rikku
from players.shiva import Shiva
from players.tidus import Tidus
from players.valefor import Valefor
from players.wakka import Wakka
from players.yojimbo import Yojimbo
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
        case 7:
            raise NotImplementedError("This is Seymour")
        case 8:
            return Valefor
        case 9:
            return Ifrit
        case 10:
            return Ixion
        case 11:
            return Shiva
        case 12:
            return Bahamut
        case 13:
            return Anima
        case 14:
            return Yojimbo
        case 15:
            return Cindy
        case 16:
            return Sandy
        case 17:
            return Mindy
        case _:
            raise NotImplementedError(
                f"No player class implemented for {current_character}"
            )
