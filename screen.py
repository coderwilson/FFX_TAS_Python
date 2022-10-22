import memory.main
import vars

gameVars = vars.varsHandle()


def clear_mouse(counter):
    try:
        return
    except Exception:
        if counter > 10:
            return
        else:
            return


def battle_screen():
    if memory.main.turnReady():
        return True
    else:
        return False


def faint_check():
    faints = 0
    charHP = memory.main.getBattleHP()
    frontParty = memory.main.getActiveBattleFormation()
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
    if not memory.main.battleActive():
        return True
    else:
        return False


def await_turn():
    counter = 0
    print("Waiting for next turn in combat.")
    # Just to make sure there's no overlap from the previous character's turn

    # Now let's do this.
    while not battle_screen() or memory.main.userControl():
        if not memory.main.battleActive():
            pass
        counter += 1
        if counter % 100000 == 0:
            print("Waiting for player turn:", counter / 10000)
        if memory.main.gameOver():
            return False
    while not memory.main.mainBattleMenu():
        pass
    return True


def turn_rikku_red():
    return turn_rikku()


def turn_rikku():
    if memory.main.getBattleCharTurn() == 6:
        return True
    else:
        return False


def turn_tidus():
    if memory.main.getBattleCharTurn() == 0:
        return True
    else:
        return False


def turn_wakka():
    if memory.main.getBattleCharTurn() == 4:
        return True
    else:
        return False


def turn_lulu():
    if memory.main.getBattleCharTurn() == 5:
        return True
    else:
        return False


def turn_kimahri():
    if memory.main.getBattleCharTurn() == 3:
        return True
    else:
        return False


def turn_auron():
    if memory.main.getBattleCharTurn() == 2:
        return True
    else:
        return False


def turn_yuna():
    if memory.main.getBattleCharTurn() == 1:
        return True
    else:
        return False


def turn_seymour():
    if memory.main.getBattleCharTurn() == 7:
        return True
    else:
        return False


def turn_aeon():
    turn = memory.main.getBattleCharTurn()
    if turn > 7 and turn <= 19:
        print("Aeon's turn:")
        return True
    else:
        return False
