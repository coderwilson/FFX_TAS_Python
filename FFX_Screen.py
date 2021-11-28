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
        #FFX_Logs.writeLog("Battle is complete.")
        #print("Battle Complete")
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
        #return pixelTestTol(x, y, rgb, 5)
    except:
        return False

def PixelTestTol( x, y, rgb, tol ):
    try:
        #print(x, ", ", y, ", (", rgb, ")")
        #print(x, ", ", y, ", (", pyautogui.pixel(x, y), ")")
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

#def clickToPixel(x,y,rgb):
#    counter = 0
#    print("Clicking to pixel: (", x, ", ", y, ") color: ", rgb)
#    while not PixelTestTol(x,y,rgb,5):
#        counter += 1;
#        if counter % 100 == 0:
#            print("awaiting pixel (clicking): ", counter)
#            print("Pixel being tested: (",x,",",y,")")
#            print("Test state: ",rgb)
#            try:
#                print("Current State: ", pyautogui.pixel(x, y))
#            except:
#                print("Cannot get current state.")
#        FFX_Xbox.menuB()
#    print("Trigger pixel achieved. Waiting is complete.")

def clickToPixel(x,y,rgb):
    print("Fix this later.")

def clickToPixelTol(x,y,rgb,tol):
    print("Fix this later.")

#def clickToPixelTol(x,y,rgb,tol):
#    counter = 0
#    print("Clicking to pixel: (", x, ", ", y, ") color: ", rgb)
#    while not PixelTestTol(x,y,rgb, tol):
#        counter += 1;
#        if counter % 100 == 0:
#            print("awaiting pixel (clicking): ", counter)
#            print("Pixel being tested: (",x,",",y,")")
#            print("Test state: ",rgb)
#            try:
#                print("Current State: ", pyautogui.pixel(x, y))
#            except:
#                print("Cannot get current state.")
#        FFX_Xbox.menuB()
#    print("Trigger pixel achieved. Waiting is complete.")

def awaitTurn() :
    counter = 0
    print("Waiting for next turn in combat.")
    #Just to make sure there's no overlap from the previous character's turn
    
    #Now let's do this.
    while not BattleScreen() or FFX_memory.userControl():
        if FFX_memory.battleActive() == False:
            time.sleep(0.01)
        counter += 1;
        if counter % 100 == 0:
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
    if FFX_memory.getBattleCharTurn() == 6:
        return True
    else:
        return False
        
    #Old logic.
    #if PixelTest(1394, 166, (157,60,33)) :
    #    FFX_Logs.writeLog("Rikku's turn:")
    #    return True
    #else :
    #    return False
    
def turnRikku() :
    if FFX_memory.getBattleCharTurn() == 6:
        return True
    else:
        return False
        
    #Old logic.
    #if PixelTest(1379, 172, (174, 118, 57)) :
    #    FFX_Logs.writeLog("Rikku's turn:")
    #    return True
    #else :
    #    return False

def turnTidus() :
    if FFX_memory.getBattleCharTurn() == 0:
        return True
    else:
        return False
        
    #Old logic.
    #if PixelTest(1394, 166, (246, 203, 146)):
    #    FFX_Logs.writeLog("Tidus's turn:")
    #    return True
    #else :
    #    return False

def turnWakka() :
    if FFX_memory.getBattleCharTurn() == 4:
        return True
    else:
        return False
        
    #Old logic.
    #if PixelTest(1394, 166, (182, 135, 83)):
    #    FFX_Logs.writeLog("Wakka's turn:")
    #    return True
    #else :
    #    return False

def turnLulu() :
    if FFX_memory.getBattleCharTurn() == 5:
        return True
    else:
        return False
        
    #Old logic.
    #if PixelTest(1432, 193, (255, 36, 100)):
    #    FFX_Logs.writeLog("Lulu's turn:")
    #    return True
    #else :
    #    return False

def turnKimahri() :
    if FFX_memory.getBattleCharTurn() == 3:
        return True
    else:
        return False
        
    #Old logic.
    #if PixelTest(1427, 179, (157, 0, 16)):
    #    FFX_Logs.writeLog("Kimahri's turn:")
    #    return True
    #else :
    #    return False

def turnAuron() :
    if FFX_memory.getBattleCharTurn() == 2:
        return True
    else:
        return False
        
    #Old logic.
    #if PixelTest(1427, 179, (130, 80, 46)):
    #    FFX_Logs.writeLog("Auron's turn:")
    #    return True
    #else :
    #    return False

def turnYuna() :
    if FFX_memory.getBattleCharTurn() == 1:
        return True
    else:
        return False
        
    #Old logic.
    #if PixelTest(1407, 182, (255, 226, 205)):
    #    FFX_Logs.writeLog("Yuna's turn:")
    #    return True
    #else :
    #    return False

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

def besaidBattle():
    awaitTurn()
    time.sleep(0.6)
    if PixelTestTol(1373,4,(101, 123, 78),5): #Reverse, flier dingo flan
        return 1
    if PixelTestTol(372,316,(36, 45, 60),5): #Reverse, Dingo Flan Flier
        return 2
    if PixelTestTol(1530,7,(101, 127, 76),5): #Side, Dingo and Flan
        return 3
    if PixelTestTol(951,400,(49, 61, 84),5): # Dingo and Flier
        return 4
    if PixelTestTol(478,14,(114, 146, 77),5): #Front, Flan and Flier
        return 5
    return 0

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

def MRRbattle_old():
    awaitTurn()
    time.sleep(0.8)
    if PixelTest(1249,4,(15, 19, 14)): #Garuda, use flee.
        return 1
    elif PixelTest(1578,306,(169, 150, 89)): #Red, Funguar, Raptor.
        return 2
    elif PixelTest(177,27,(184, 168, 100)): #Lamashtu, Raptor, Red.
        return 3
    elif PixelTest(180,18,(178, 164, 103)): #Red, Gandyboy, Lamashtu.
        return 4
    elif PixelTest(827,350,(92, 86, 53)): #Gandboy, Red, Raptor (camera sideways)
        return 5
    elif PixelTest(1541,133,(40, 40, 16)): #Gandboy, Red, Funguar
        return 6
    elif PixelTest(1097,5,(19, 23, 24)): #Gandboy, Red, Funguar (reverse)
        return 7
    return 0

def mrrCompletion(status):
    openMenu()
    if status[0] == 0:
        if FFX_memory.getSLVLYuna() > 573:
            status[0] = 1
    if status[1] == 0:
        if FFX_memory.getSLVLKim() > 495:
            status[1] = 1
    
    #print("Extra pause during testing")
    #time.sleep(10) #Temporary during testing
    #print("End - Extra pause during testing")
    return status

def checkItemsMRR():
    pDown = 0
    grenade = 0
    power = 0
    target = 3
    while power == 0:
        if pDown == 0:
            if target == 4:
                if PixelTest(982,295,(254, 98, 0)):           
                    pDown = 4
            elif target == 5:
                if PixelTest(341,359,(254, 99, 0)):
                    pDown = 5
            elif target == 6:
                if PixelTest(982,359,(255, 99, 0)):
                    pDown = 6
            elif target == 7:
                if PixelTest(341,422,(255, 104, 6)):
                    pDown = 7
        elif power == 0:
            if target == 4:
                if PixelTest(982,295,(225, 3, 4)):
                    power = 4
            elif target == 5:
                if PixelTest(341,359,(204, 0, 0)):
                    power = 5
            elif target == 6:
                if PixelTest(982,359,(227, 2, 3)):
                    power = 6
            elif target == 7:
                if PixelTest(341,422,(185, 0, 1)):
                    power = 7
            elif target == 8:
                if PixelTest(982,422,(155, 0, 0)):
                    power = 8
            elif target == 9:
                if PixelTest(341,487,(208, 0, 1)):
                    power = 9
        target += 1
    print(pDown, " | ", power)
    return [pDown, power]

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

def partySize_Old():
    if PixelTest(1401,791,(199, 162, 255)):
        return 3
    elif PixelTest(1401,747,(199, 162, 255)):
        return 2
    elif PixelTest(1401,704,(199, 162, 255)):
        return 1
    else: return 0

def checkItemsMacalania():
    bombCore = 0
    lMarble = 0
    fScale = 0
    aWind = 0
    lunar = 0
    light = 0
    target = 3
    while light == 0:
        print("Checking item in position: ",target)
        if bombCore == 0:
            if target == 3:
                if PixelTestTol(351,276,(217, 233, 246), 5):
                    #confirmed
                    bombCore = 3
                    print("Bomb Core, position ", target)
            if target == 4:
                if PixelTestTol(991,276,(217, 233, 246), 5):
                    #Confirmed
                    bombCore = 4
                    print("Bomb Core, position ", target)
            if target == 5:
                if PixelTestTol(351,340,(226, 239, 249), 5):           
                    bombCore = 5
                    print("Bomb Core, position ", target)
                print("Test")
            if target == 6:
                if PixelTestTol(991,340,(226, 239, 249), 5):           
                    bombCore = 6
                    print("Bomb Core, position ", target)
        elif lMarble == 0:
            if target == 4:
                if PixelTestTol(991,276,(217, 233, 246), 0.98) and PixelTestTol(1211,280,(221, 221, 221), 0.98):           
                    lMarble = 4
                    print("Lightning marble, position ", target)
            if target == 5:
                if PixelTestTol(351,340,(226, 239, 249), 5) and PixelTestTol(571,344,(221, 221, 221), 5):           
                    lMarble = 5
                    print("Lightning marble, position ", target)
            if target == 6:
                if PixelTestTol(991,340,(226, 239, 249), 5) and PixelTestTol(1211,344,(221, 221, 221), 5):           
                    lMarble = 6
                    print("Lightning marble, position ", target)
            if target == 7:
                if PixelTestTol(351,404,(234, 245, 252), 5) and PixelTestTol(571,408,(221, 221, 221), 5):           
                    lMarble = 7
                    print("Lightning marble, position ", target)
            if target == 8:
                if PixelTestTol(991,404,(234, 245, 252), 5) and PixelTestTol(1211,408,(221, 221, 221), 5):           
                    lMarble = 8
                    print("Lightning marble, position ", target)
        elif fScale == 0:
            if target == 5:
                if PixelTestTol(351,340,(226, 239, 249), 5) and PixelTestTol(412,344,(221, 221, 221), 5):           
                    fScale = 5
                    print("Fish Scale, position ", target)
            if target == 6:
                if PixelTestTol(991,340,(226, 239, 249), 5) and PixelTestTol(1052,344,(221, 221, 221), 5):           
                    fScale = 6
                    print("Fish Scale, position ", target)
            if target == 7:
                if PixelTestTol(351,404,(234, 245, 252), 5) and PixelTestTol(412,408,(221, 221, 221), 5):           
                    fScale = 7
                    print("Fish Scale, position ", target)
            if target == 8:
                if PixelTestTol(991,404,(234, 245, 252), 5) and PixelTestTol(1052,408,(221, 221, 221), 5):           
                    fScale = 8
                    print("Fish Scale, position ", target)
            if target == 9:
                if PixelTestTol(351,468,(237, 246, 252), 5) and PixelTestTol(412,472,(222, 222, 222), 5):           
                    fScale = 9
                    print("Fish Scale, position ", target)
        elif aWind == 0:
            if target == 6:
                if PixelTestTol(991,340,(226, 239, 249), 5) and PixelTestTol(1168,344,(221, 221, 221), 5):           
                    aWind = 6
                    print("Arctic Wind, position ", target)
            if target == 7:
                if PixelTestTol(351,404,(234, 245, 252), 5) and PixelTestTol(528,408,(221, 221, 221), 5):           
                    aWind = 7
                    print("Arctic Wind, position ", target)
            if target == 8:
                if PixelTestTol(991,404,(234, 245, 252), 5) and PixelTestTol(1168,409,(221, 221, 221), 5):           
                    aWind = 8
                    print("Arctic Wind, position ", target)
            if target == 9:
                if PixelTestTol(351,468,(237, 246, 252), 5) and PixelTestTol(527,471,(222, 222, 222), 5):           
                    aWind = 9
                    print("Arctic Wind, position ", target)
            if target == 10:
                if PixelTestTol(991,468,(237, 246, 252), 5) and PixelTestTol(1168,472,(222, 222, 222), 5):           
                    aWind = 10
                    print("Arctic Wind, position ", target)
        elif lunar == 0:
            if target == 7:
                if PixelTest(331,408,(168, 164, 221)):           
                    lunar = 7
                    print("Lunar Curtain, position ", target)
            if target == 8:
                if PixelTest(971,408,(168, 164, 221)):         
                    lunar = 8
                    print("Lunar Curtain, position ", target)
            if target == 9:
                if PixelTest(331,472,(168, 164, 221)):           
                    lunar = 9
                    print("Lunar Curtain, position ", target)
            if target == 10:
                if PixelTest(971,472,(168, 164, 221)):           
                    lunar = 10
                    print("Lunar Curtain, position ", target)
            if target == 11:
                if PixelTest(331,536,(168, 164, 221)):           
                    lunar = 11
                    print("Lunar Curtain, position ", target)
        elif light == 0:
            if target == 8:
                if PixelTest(971,408,(168, 164, 221)):         
                    light = 8
                    print("Light Curtain, position ", target)
            if target == 9:
                if PixelTest(331,472,(168, 164, 221)):           
                    light = 9
                    print("Light Curtain, position ", target)
            if target == 10:
                if PixelTest(971,472,(168, 164, 221)):           
                    light = 10
                    print("Light Curtain, position ", target)
            if target == 11:
                if PixelTest(331,536,(168, 164, 221)):           
                    light = 11
                    print("Light Curtain, position ", target)
            if target == 12:
                if PixelTest(971,536,(168, 164, 221)):           
                    light = 12
                    print("Light Curtain, position ", target)
        if target > 12:
            break
        print("Increment target from ", target)
        target += 1
        print("Increment target, now ", target)
        
    #Set MaxSpot to one more than the last undesirable item
    if light - lunar != 1:
        maxSpot = light
    elif lunar - aWind != 1:
        maxSpot = lunar
    elif aWind - fScale != 1:
        maxSpot = aWind
    elif fScale - lMarble != 1:
        maxSpot = fScale
    elif lMarble - bombCore != 1:
        maxSpot = lMarble
    else:
        maxSpot = bombCore
    print(bombCore, " | ", lMarble, " | ", fScale, " | ", aWind, " | ", lunar, " | ", light)
    #time.sleep(10)
    return [bombCore, lMarble, fScale, aWind, lunar, light, grenade, maxSpot]

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

def abPotPos(count):
    print("Fix this later.")

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

def clickImage(img):
    search = pyautogui.center(pyautogui.locateOnScreenCenter(img,0.85))
    print('Search values: ', search)
    if search != [0,0]:
        pyautogui.click(search[0], search[1])
        time.sleep(1)
        return True
    else:
        return False
