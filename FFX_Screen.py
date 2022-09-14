import FFX_memory
import FFX_vars
gameVars = FFX_vars.varsHandle()


def clearMouse(counter):
    try:
        return
    except Exception:
        if counter > 10:
            return
        else:
            return


def BattleScreen():
    if FFX_memory.turnReady():
        return True
    else:
        return False


def faintCheck():
    faints = 0
    charHP = FFX_memory.getBattleHP()
    frontParty = FFX_memory.getActiveBattleFormation()
    print("##", frontParty, "##")
    print("##", charHP, "##")
    if turnAeon():
        return 0
    if frontParty[0] != 255 and charHP[0] == 0:
        faints += 1
    if frontParty[1] != 255 and charHP[1] == 0:
        faints += 1
    if frontParty[2] != 255 and charHP[2] == 0:
        faints += 1
    print("## Fainted Characters:", faints, "##")
    return faints


def BattleComplete():
    if not FFX_memory.battleActive():
        return True
    else:
        return False


def awaitTurn():
    counter = 0
    print("Waiting for next turn in combat.")
    # Just to make sure there's no overlap from the previous character's turn

    # Now let's do this.
    while not BattleScreen() or FFX_memory.userControl():
        if not FFX_memory.battleActive():
            pass
        counter += 1
        if counter % 100000 == 0:
            print("Waiting for player turn:", counter / 10000)
        if FFX_memory.gameOver():
            return False
    while not FFX_memory.mainBattleMenu():
        pass
    return True


def turnRikkuRed():
    return turnRikku()


def turnRikku():
    if FFX_memory.getBattleCharTurn() == 6:
        return True
    else:
        return False


def turnTidus():
    if FFX_memory.getBattleCharTurn() == 0:
        return True
    else:
        return False


def turnWakka():
    if FFX_memory.getBattleCharTurn() == 4:
        return True
    else:
        return False


def turnLulu():
    if FFX_memory.getBattleCharTurn() == 5:
        return True
    else:
        return False


def turnKimahri():
    if FFX_memory.getBattleCharTurn() == 3:
        return True
    else:
        return False


def turnAuron():
    if FFX_memory.getBattleCharTurn() == 2:
        return True
    else:
        return False


def turnYuna():
    if FFX_memory.getBattleCharTurn() == 1:
        return True
    else:
        return False


def turnSeymour():
    if FFX_memory.getBattleCharTurn() == 7:
        return True
    else:
        return False


def turnAeon():
    turn = FFX_memory.getBattleCharTurn()
    if turn > 7 and turn <= 19:
        print("Aeon's turn:")
        return True
    else:
        return False
