import memory.main
import vars

gameVars = vars.varsHandle()


def clearMouse(counter):
    try:
        return
    except Exception:
        if counter > 10:
            return
        else:
            return


def BattleScreen():
    if memory.main.turnReady():
        return True
    else:
        return False


def faintCheck():
    faints = 0
    charHP = memory.main.getBattleHP()
    frontParty = memory.main.getActiveBattleFormation()
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
    if not memory.main.battleActive():
        return True
    else:
        return False


def awaitTurn():
    counter = 0
    print("Waiting for next turn in combat.")
    # Just to make sure there's no overlap from the previous character's turn

    # Now let's do this.
    while not BattleScreen() or memory.main.userControl():
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


def turnRikkuRed():
    return turnRikku()


def turnRikku():
    if memory.main.getBattleCharTurn() == 6:
        return True
    else:
        return False


def turnTidus():
    if memory.main.getBattleCharTurn() == 0:
        return True
    else:
        return False


def turnWakka():
    if memory.main.getBattleCharTurn() == 4:
        return True
    else:
        return False


def turnLulu():
    if memory.main.getBattleCharTurn() == 5:
        return True
    else:
        return False


def turnKimahri():
    if memory.main.getBattleCharTurn() == 3:
        return True
    else:
        return False


def turnAuron():
    if memory.main.getBattleCharTurn() == 2:
        return True
    else:
        return False


def turnYuna():
    if memory.main.getBattleCharTurn() == 1:
        return True
    else:
        return False


def turnSeymour():
    if memory.main.getBattleCharTurn() == 7:
        return True
    else:
        return False


def turnAeon():
    turn = memory.main.getBattleCharTurn()
    if turn > 7 and turn <= 19:
        print("Aeon's turn:")
        return True
    else:
        return False
