import time
import pyautogui
#import FFX_Xbox
import FFX_Logs
import FFX_memory

#FFXC = FFX_Xbox.FFXC
#FFXC = FFX_Xbox.FFXC

def clearMouse(counter):
    try:
        pyautogui.moveTo(1598,898)
    except:
        if counter > 10:
            return
        else:
            clearMouse(counter + 1)

def BattleScreen():
    if FFX_memory.turnReady():
        time.sleep(0.2)
        return True
    else:
        return False

    
def BattleScreen_old():
    if PixelTest(1464, 181, (229, 189, 96)) :
        if not PixelTestTol(131,693,(153, 155, 153),5):
            print("It is now someone's turn in battle.")
            time.sleep(0.735) #This delay is paramount.
        return True
    else :
        return False

def clickToBattle():
    print("Fix this later.")

def faintCheck():
    faints = 0
    if PixelTest(1347,701,(223, 55, 27)):
        faints += 1
    if PixelTest(1347,745,(221, 54, 26)):
        faints += 1
    if PixelTest(1347,788,(222, 54, 27)):
        faints += 1
    if faints > 0:
        FFX_Logs.writeLog("Num of characters have fainted: " + str(faints))
    return faints

def faintCheckTwo():
    faints = 0
    if PixelTest(1347,701,(223, 55, 27)):
        faints += 1
    elif PixelTest(1347,745,(221, 54, 26)):
        faints += 1
    if faints > 0:
        FFX_Logs.writeLog("Num of characters have fainted: " + str(faints))
    return faints

def BattleComplete():
    if FFX_memory.battleActive() == False:
        return True
    else :
        return False

def PixelValue(x, y):
    try:
        value = pyautogui.pixel(x, y)
    except:
        value = PixelValue(x, y)
    return value

def PixelTest( x, y, rgb ):
    try:
        return pyautogui.pixelMatchesColor(x, y, rgb)
    except:
        return False

def PixelTestTol( x, y, rgb, tol ):
    try:
        return pyautogui.pixelMatchesColor(x, y, rgb, tolerance = tol)
    except:
        return False

def awaitPixel(x,y,rgb):
    counter = 0
    print("Awaiting pixel: (", x, ", ", y, ") color: ", rgb)
    while not PixelTestTol(x,y,rgb,5):
        counter += 1;
        if counter % 100 == 0:
            print("awaiting pixel: ", counter / 100)
            print("Pixel being tested: (",x,",",y,")")
            print("Test state: ",rgb)
            try:
                print("Current State: ", pyautogui.pixel(x, y))
            except:
                print("Cannot get current state.")
        time.sleep(0.05)
    print("Trigger pixel achieved. Waiting is complete.")

def clickToPixel(x,y,rgb):
    print("Fix this later.")

def clickToPixelTol(x,y,rgb,tol):
    print("Fix this later.")

def awaitTurn() :
    counter = 0
    print("Waiting for next turn in combat.")
    #Just to make sure there's no overlap from the previous character's turn
    
    #Now let's do this.
    while not BattleScreen() or FFX_memory.userControl():
        if FFX_memory.battleActive() == False:
            time.sleep(0.01)
        counter += 1;
        if counter % 10000 == 0:
            print("Waiting for player turn: ", counter / 100)
        if FFX_memory.gameOver():
            return False
    return True

def awaitSave() :
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - FFX_Xbox.awaitSave")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")

def Minimap1() :
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - FFX_Screen.Minimap1")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")

def awaitMap1() :
    print("Fix this later.")

def clickToMap1() :
    print("Fix this later.")

def Minimap2() :
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - FFX_Screen.Minimap2")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")

def awaitMap2() :
    print("Fix this later.")

def clickToMap2() :
    print("Fix this later.")

def Minimap3() :
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - FFX_Screen.Minimap3")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")

def awaitMap3() :
    print("Fix this later.")

def clickToMap3() :
    print("Fix this later.")

def Minimap4() :
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - FFX_Screen.Minimap4")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")

def awaitMap4() :
    print("Fix this later.")

def clickToMap4() :
    print("Fix this later.")
    
def MinimapAny():
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - FFX_Screen.MinimapAny")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")
    print("ERROR - OLD MOVEMENT COMMAND FOUND")

def turnRikkuRed() :
    return turnRikku()
    
def turnRikku() :
    if FFX_memory.getBattleCharTurn() == 6:
        return True
    else:
        return False

def turnTidus() :
    if FFX_memory.getBattleCharTurn() == 0:
        return True
    else:
        return False

def turnWakka() :
    if FFX_memory.getBattleCharTurn() == 4:
        return True
    else:
        return False

def turnLulu() :
    if FFX_memory.getBattleCharTurn() == 5:
        return True
    else:
        return False

def turnKimahri() :
    if FFX_memory.getBattleCharTurn() == 3:
        return True
    else:
        return False

def turnAuron() :
    if FFX_memory.getBattleCharTurn() == 2:
        return True
    else:
        return False

def turnYuna() :
    if FFX_memory.getBattleCharTurn() == 1:
        return True
    else:
        return False

def turnSeymour() :
    if FFX_memory.getBattleCharTurn() == 7:
        FFX_Logs.writeLog("Seymour's turn:")
        return True
    else :
        return False

def turnAeon():
    turn = FFX_memory.getBattleCharTurn()
    if turn > 7 and turn <= 12:
        print("Aeon's turn:")
        return True
    else :
        return False

def awaitSwimToJecht():
    counter = 0
    while not ( PixelTest(1217,803,(222,222,222)) and PixelTest(1092,813,(64,64,64)) ):
        counter += 1
        if counter % 100 == 0:
            print("Waiting for the Jecht screen: ", counter / 100)
        time.sleep(0.1)
    print("Ready to go swimming")

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
    #If none of the pre-determined screens show up, just return the Flee option.
    return 1

def mrrCompletion(status):
    openMenu()
    if status[0] == 0:
        if FFX_memory.getSLVLYuna() > 573:
            status[0] = 1
    if status[1] == 0:
        if FFX_memory.getSLVLKim() > 495:
            status[1] = 1
    
    return status

def checkCharge(pos):
    if pos == 1:
        if PixelTest(1471,728,(255, 83, 0)) == True:
            FFX_Logs.writeLog("Character in position 1 is charged.")
            return True
        else:
            FFX_Logs.writeLog("Character in position 1 is NOT charged.")
            return False
    if pos == 2:
        if PixelTest(1471,770,(255, 83, 0)) == True:
            FFX_Logs.writeLog("Character in position 2 is charged.")
            return True
        else:
            FFX_Logs.writeLog("Character in position 2 is NOT charged.")
            return False

def spherimorphSpell():
    complete = 0
    spell = 0
    while complete == 0:
        if PixelTestTol(793,93,(221,221,221), 5):
            FFX_Logs.writeLog("Spherimorph cast Fire")
            complete = 1
            spell = 1 #Fire
        elif PixelTestTol(749,94,(219,219,219), 5):
            FFX_Logs.writeLog("Spherimorph cast Thunder")
            complete = 1
            spell = 2 #Thunder
        elif PixelTestTol(848,92,(223, 223, 223), 5):
            FFX_Logs.writeLog("Spherimorph cast Blizzard")
            complete = 1
            spell = 4 #Ice
        elif PixelTestTol(807,93,(221, 221, 221), 5):
            FFX_Logs.writeLog("Spherimorph cast Water")
            complete = 1
            spell = 3 #Water
    return spell

def imgSearch(img, conf):
    img = 'img\\' + str(img)
    try:
        imgTest = pyautogui.locateOnScreen(img, confidence=conf)
        print("Results for searching '",img,": ", imgTest)
        if imgTest[1] > 1:
            return True
    except Exception as errorMsg:
        print("Something went wrong. Could not find image.")
        print(errorMsg)
        return False

def imgSearch2(img, conf):
    try:
        imgTest = pyautogui.locateOnScreen(str(img), confidence=conf)
        print("Results for searching '",img,": ", imgTest)
        if imgTest[1] > 1:
            return True
    except Exception as errorMsg:
        print("Something went wrong. Could not find image.")
        print(errorMsg)
        return False

def desertCharge():
    chargeState = [False,False]
    chargeState[0] = checkCharge(1)
    chargeState[1] = checkCharge(2)
    return chargeState
