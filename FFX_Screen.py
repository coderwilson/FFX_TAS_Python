import time
import pyautogui
#import FFX_Xbox
import FFX_Logs
import FFX_memory
#from playsound import playsound
import FFX_vars
gameVars = FFX_vars.varsHandle()


def clearMouse(counter):
    try:
        # pyautogui.moveTo(1598,898)
        return
    except:
        if counter > 10:
            return
        else:
            #clearMouse(counter + 1)
            return


def BattleScreen():
    if FFX_memory.turnReady():
        # if gameVars.usePause():
        #    FFX_memory.waitFrames(12)
        # else:
        #    FFX_memory.waitFrames(6)
        return True
    else:
        return False


def faintCheck():
    faints = 0
    charHP = FFX_memory.getBattleHP()
    frontParty = FFX_memory.getActiveBattleFormation()
    partySize = FFX_memory.activepartySize()
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
    print("## Num of characters have fainted:", faints, "##")
    return faints


def BattleComplete():
    if FFX_memory.battleActive() == False:
        return True
    else:
        return False


def awaitTurn():
    counter = 0
    print("Waiting for next turn in combat.")
    # Just to make sure there's no overlap from the previous character's turn

    # Now let's do this.
    while not BattleScreen() or FFX_memory.userControl():
        if FFX_memory.battleActive() == False:
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
        FFX_Logs.writeLog("Seymour's turn:")
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


def MRRbattle():
    bNum = FFX_memory.getBattleNum()
    if bNum == 96:
        return 3
    if bNum == 97:
        return 4
    if bNum == 98:
        return 5
    if bNum == 100:
        return 2
    if bNum == 101:
        return 7
    if bNum == 102:
        return 1
    if bNum == 109:
        return 8
    if bNum == 110:
        return 9
    if bNum == 111:
        return 6
    if bNum == 112:
        return 1
    if bNum == 113:
        return 1
    # If none of the pre-determined screens show up, just return the Flee option.
    return 1


def mrrCompletion(status):
    FFX_memory.openMenu()
    if status[0] == 0:
        if FFX_memory.getSLVLYuna() > 573:
            status[0] = 1
    if status[1] == 0:
        if FFX_memory.getSLVLKim() > 495:
            status[1] = 1

    return status


def desertCharge():
    chargeState = [False, False]
    chargeState[0] = checkCharge(1)
    chargeState[1] = checkCharge(2)
    return chargeState
