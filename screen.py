import memory.main
import vars

game_vars = vars.vars_handle()


def battle_screen():
    if memory.main.turn_ready():
        return True
    else:
        return False


def faint_check():
    faints = 0
    charHP = memory.main.get_battle_hp()
    frontParty = memory.main.get_active_battle_formation()
    print("##", frontParty, "##")
    print("##", charHP, "##")
    if turn_aeon():
        return 0
    if frontParty[0] != 255 and charHP[0] == 0:
        faints += 1
    if frontParty[1] != 255 and charHP[1] == 0:
        faints += 1
    if frontParty[2] != 255 and charHP[2] == 0:
        faints += 1
    print("## Fainted Characters:", faints, "##")
    return faints


def battle_complete():
    if not memory.main.battle_active():
        return True
    else:
        return False


def await_turn():
    counter = 0
    print("Waiting for next turn in combat.")
    # Just to make sure there's no overlap from the previous character's turn

    # Now let's do this.
    while not battle_screen() or memory.main.user_control():
        if not memory.main.battle_active():
            pass
        counter += 1
        if counter % 100000 == 0:
            print("Waiting for player turn:", counter / 10000)
        if memory.main.game_over():
            return False
    while not memory.main.main_battle_menu():
        pass
    return True


def turn_rikku_red():
    return turn_rikku()


def turn_rikku():
    if memory.main.get_battle_char_turn() == 6:
        return True
    else:
        return False


def turn_tidus():
    if memory.main.get_battle_char_turn() == 0:
        return True
    else:
        return False


def turn_wakka():
    if memory.main.get_battle_char_turn() == 4:
        return True
    else:
        return False


def turn_lulu():
    if memory.main.get_battle_char_turn() == 5:
        return True
    else:
        return False


def turn_kimahri():
    if memory.main.get_battle_char_turn() == 3:
        return True
    else:
        return False


def turn_auron():
    if memory.main.get_battle_char_turn() == 2:
        return True
    else:
        return False


def turn_yuna():
    if memory.main.get_battle_char_turn() == 1:
        return True
    else:
        return False


def turn_seymour():
    if memory.main.get_battle_char_turn() == 7:
        return True
    else:
        return False


def turn_aeon():
    turn = memory.main.get_battle_char_turn()
    if turn > 7 and turn <= 19:
        print("Aeon's turn:")
        return True
    else:
        return False
