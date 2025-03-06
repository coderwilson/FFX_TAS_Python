import logging

from tqdm import tqdm

import memory.main
import vars

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()


def battle_screen():
    if memory.main.turn_ready():
        return True
    else:
        return False


def faint_check():
    faints = 0
    char_hp = memory.main.get_battle_hp()
    front_party = memory.main.get_active_battle_formation()
    logger.debug(f"faint_check() {front_party}")
    logger.debug(f"faint_check() {char_hp}")
    if turn_aeon():
        return 0
    if front_party[0] != 255 and char_hp[0] == 0:
        faints += 1
    if front_party[1] != 255 and char_hp[1] == 0:
        faints += 1
    if front_party[2] != 255 and char_hp[2] == 0:
        faints += 1
    logger.debug(f"faint_check() Fainted Characters: {faints}")
    return faints


def battle_complete():
    if not memory.main.battle_active():
        return True
    else:
        return False


def await_turn():
    logger.debug("Waiting for next turn in combat.")
    # Just to make sure there's no overlap from the previous character's turn

    # Now let's do this.
    fmt = "Waiting for player turn... elapsed {elapsed}"
    with tqdm(bar_format=fmt) as pbar:
        while not (battle_screen() or memory.main.user_control()):
            pbar.update()
            if memory.main.battle_wrap_up_active():
                return False
            if not memory.main.battle_active():
                pass
            if memory.main.game_over():
                return False
        while not memory.main.main_battle_menu():
            if memory.main.battle_wrap_up_active():
                return False
    return True


def turn_seymour():
    if memory.main.get_battle_char_turn() == 7:
        return True
    else:
        return False


def turn_aeon():
    turn = memory.main.get_battle_char_turn()
    if turn > 7 and turn <= 19:
        logger.debug(f"Aeon's turn: {turn}")
        return True
    else:
        return False
