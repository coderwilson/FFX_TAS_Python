import time
import pyautogui
import FFX_Xbox
import FFX_Logs
import FFX_memory

FFXC = FFX_Xbox.FFXC

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
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 0)
        FFX_memory.getEnemyCurrentHP()
        if not PixelTestTol(131,693,(153, 155, 153),5):
            print("It is now someone's turn in battle.")
            time.sleep(0.735) #This delay is paramount.
        return True
    else :
        return False
    
def clickToBattle():
    FFX_Logs.writeLog("Clicking until it's someone's turn in battle")
    print("Clicking until it's someone's turn in battle")
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('Dpad', 0)
    complete = 0
    while complete == 0 :
        if BattleScreen():
            complete = 1
        elif BattleComplete():
            complete = 1
        else:
            FFX_Xbox.menuB()
    
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
    if PixelTest(1464, 151, (91, 94, 141)) :
        FFX_Logs.writeLog("Battle is complete.")
        print("Battle Complete")
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

def clickToPixel(x,y,rgb):
    counter = 0
    print("Clicking to pixel: (", x, ", ", y, ") color: ", rgb)
    while not PixelTestTol(x,y,rgb,5):
        counter += 1;
        if counter % 100 == 0:
            print("awaiting pixel (clicking): ", counter)
            print("Pixel being tested: (",x,",",y,")")
            print("Test state: ",rgb)
            try:
                print("Current State: ", pyautogui.pixel(x, y))
            except:
                print("Cannot get current state.")
        FFX_Xbox.menuB()
    print("Trigger pixel achieved. Waiting is complete.")

def clickToPixelTol(x,y,rgb,tol):
    counter = 0
    print("Clicking to pixel: (", x, ", ", y, ") color: ", rgb)
    while not PixelTestTol(x,y,rgb, tol):
        counter += 1;
        if counter % 100 == 0:
            print("awaiting pixel (clicking): ", counter)
            print("Pixel being tested: (",x,",",y,")")
            print("Test state: ",rgb)
            try:
                print("Current State: ", pyautogui.pixel(x, y))
            except:
                print("Cannot get current state.")
        FFX_Xbox.menuB()
    print("Trigger pixel achieved. Waiting is complete.")

def dodgeLightning():
    try:
        pix = pyautogui.pixel(1500,800)
        if pix[0] > 200 or pix[1] > 200 or pix[2] > 200 :
            FFX_Xbox.menuB()
            return 1
        else :
            return 0
    except:
        return False

def awaitTurn() :
    counter = 0
    print("Waiting for next turn in combat.")
    #Just to make sure there's no overlap from the previous character's turn
    time.sleep(0.5) 
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('Dpad', 0)
    
    #Now let's do this.
    while not BattleScreen():
        if BattleComplete():
            return True
        counter += 1;
        if counter % 100 == 0:
            print("Waiting for player turn: ", counter / 100)
    return True

def awaitSave() :
    FFX_Logs.writeLog("Awaiting save dialog to pop up")
    counter = 0
    complete = 0
    while complete == 0:
        counter += 1;
        if counter % 100 == 0:
            print("Waiting for Save dialog: ", counter / 100)
        savePopup = PixelTest(630,422,(70,53,124))
        saveScreen = PixelTest(1,1,(87, 85, 122))
        if PixelTestTol(591,769,(221, 221, 221),5): #Skips specific dialog, SS Winno
            FFX_Xbox.menuB()
        elif PixelTestTol(580,768,(222, 222, 222),5): #Skips specific dialog, SS Winno
            FFX_Xbox.menuB()
        elif PixelTestTol(493,735,(220, 220, 220),5): #Skips specific dialog, SS Winno
            FFX_Xbox.menuB()
        elif PixelTestTol(482,738,(215, 215, 215),5): #Skips specific dialog, SS Winno
            FFX_Xbox.menuB()
        elif savePopup == True:
            FFX_Xbox.menuA()
            complete = 1
        elif saveScreen == True:
            FFX_Xbox.menuA()
            FFX_Xbox.menuA()
            FFX_Xbox.menuA()
            FFX_Xbox.menuB()
            complete = 1
        else:
            if not PixelTestTol(1,1,(0,0,0),5):
                FFX_Xbox.menuB()
    print("Save dialog achieved")
    FFX_Logs.writeLog("Save dialog on screen.")
    complete = 0
    while complete == 0:
        savePopup = PixelTestTol(630,422,(0,0,0),5)
        if savePopup == True:
            complete = 1
        elif PixelTestTol(752,484,(149, 149, 149),5):
            FFX_Xbox.menuA()
        elif PixelTestTol(752,518,(149, 149, 149),5):
            FFX_Xbox.menuB()
    print("Save dialog cleared. Moving on.")
    FFX_Logs.writeLog("Save dialog cleared. Moving on.")
        
def Minimap1() :
    try:
        return pyautogui.pixelMatchesColor(271, 181, (158,158,53), tolerance=5)
    except:
        return False

def awaitMap1() :
    print("Waiting for the minimap to come up in the top left corner")
    counter = 0
    while not Minimap1() :
        counter += 1;
        if counter % 100 == 0:
            print("Waiting | ", counter / 100)
        if BattleComplete():
            FFX_Xbox.menuB()
        if BattleScreen():
            break
        time.sleep(0.05)
    print("Resuming control")

def clickToMap1() :
    print("Clicking until top-left map appears")
    while not Minimap1() :
        FFXC.set_value('BtnB', 1)
        time.sleep(0.04)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.04)
    print("Map trigger achieved")

def Minimap2() :
    try:
        return pyautogui.pixelMatchesColor(1328, 181, (158,158,53), tolerance=5)
    except:
        return False

def awaitMap2() :
    print("Waiting for the minimap to come up in the top right corner")
    counter = 0
    while not Minimap2() :
        counter += 1;
        if counter % 100 == 0:
            print("Waiting | ", counter / 100)
        if BattleComplete():
            FFX_Xbox.menuB()
        if BattleScreen():
            break
        time.sleep(0.05)
    print("Resuming control")

def clickToMap2() :
    print("Clicking until top-right map appears")
    while not Minimap2() :
        FFXC.set_value('BtnB', 1)
        time.sleep(0.04)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.04)
    print("Map trigger achieved")

def Minimap3() :
    try:
        return pyautogui.pixelMatchesColor(271, 718, (158,158,53), tolerance=5)
    except:
        return False

def awaitMap3() :
    print("Waiting for the minimap to come up in the bottom left corner")
    counter = 0
    while not Minimap3() :
        counter += 1;
        if counter % 100 == 0:
            print("Waiting | ", counter / 100)
        if BattleComplete():
            FFX_Xbox.menuB()
        if BattleScreen():
            break
        time.sleep(0.05)
    print("Resuming control")

def clickToMap3() :
    print("Clicking until bottom-left map appears")
    while not Minimap3() :
        FFXC.set_value('BtnB', 1)
        time.sleep(0.04)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.04)
    print("Map trigger achieved")

def Minimap4() :
    try:
        return pyautogui.pixelMatchesColor(1328, 718, (160, 160, 53), tolerance=5)
    except:
        return False

def awaitMap4() :
    print("Waiting for the minimap to come up in the bottom right corner")
    counter = 0
    while not Minimap4() :
        counter += 1;
        if counter % 100 == 0:
            print("Waiting | ", counter / 100)
        if BattleComplete():
            FFX_Xbox.menuB()
        if BattleScreen():
            break
        time.sleep(0.05)
    print("Resuming control")

def clickToMap4() :
    print("Clicking until bottom-right map appears")
    while not Minimap4() :
        FFXC.set_value('BtnB', 1)
        time.sleep(0.04)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.04)
    print("Map trigger achieved")
    
def MinimapAny():
    if Minimap1(): #Top left is the most common minimap.
        return True
    if Minimap2():
        return True
    if Minimap3():
        return True
    if Minimap4():
        return True
    return False
    
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
    if PixelTest(1432, 166, (65, 140, 190)):
        FFX_Logs.writeLog("Seymour's turn:")
        return True
    else :
        return False

def turnAeon():
    if PixelTest(1392, 183, (33, 8, 183)):
        FFX_Logs.writeLog("Aeon's turn:")
        time.sleep(0.4)
        return True
    else :
        return False

def countItems(slot) :
    width = 70
    height = 70
    x = 667
    if slot == 1:
        y = 223
    elif slot == 2:
        y = 295
    elif slot == 3:
        y = 365
    
    print("Checking for number of items")
    try :
        
        loc = pyautogui.locateOnScreen('Images\count1.PNG', region=(x,y,width,height))
        print("1 - ",loc)
        time.sleep(10)
        return 1
    except :
        try :
            loc = pyautogui.locateOnScreen('Images\count1.PNG', region=(x,y,width,height))
            print("2 - ",loc)
            time.sleep(10)
            return 2
        except :
            try :
                loc = pyautogui.locateOnScreen('Images\count1.PNG', region=(x,y,width,height))
                print("3 - ",loc)
                time.sleep(10)
                return 3
            except :
                print("0 - no item found")
                return 0

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

def mrrFormat():
    FFX_Logs.writeLog("Reformatting party")
    openMenu()
    time.sleep(0.2)
    if checkMRRForm() == 0:
        order = FFX_memory.getOrderSix()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuB()
        
        if order[0] != 0: #Tidus is not in the first slot
            print("Looking for Tidus")
            if order[1] == 0:
                print("Tidus in Second slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[1] = order[0]
                order[0] = 0
            elif order[2] == 0:
                print("Tidus in Third slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                order[2] = order[0]
                order[0] = 0
            elif order[3] == 0:
                print("Tidus in Fourth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                order[3] = order[0]
                order[0] = 0
            elif order[4] == 0:
                print("Tidus in Fifth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                order[4] = order[0]
                order[0] = 0
            elif order[5] == 0:
                print("Tidus in Sixth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                order[5] = order[0]
                order[0] = 0
        else:
            print("Tidus seems fine.")
            FFX_Xbox.menuDown()
        if order[1] != 4: #Wakka is not in the second slot
            print("Looking for Wakka")
            if order[2] == 4:
                print("Wakka in Third slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[2] = order[1]
                order[1] = 4
            elif order[3] == 4:
                print("Wakkain Fourth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                order[3] = order[1]
                order[1] = 4
            elif order[4] == 4:
                print("Wakka in Fifth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                order[4] = order[1]
                order[1] = 4
            elif order[5] == 4:
                print("Wakka in Sixth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                order[5] = order[1]
                order[1] = 4
        else:
            print("Wakka seems fine.")
            FFX_Xbox.menuDown()
        if order[2] != 2: #Auron, 3rd slot
            print("Looking for Auron")
            if order[3] == 2:
                print("Auron in fourth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[3] = order[2]
                order[2] = 2
            elif order[4] == 2:
                print("Auron in fifth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                order[4] = order[2]
                order[2] = 2
            elif order[5] == 2:
                print("Auron in sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                order[5] = order[2]
                order[2] = 2
            else:
                print("Something's wrong, can't find Lulu.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
        else:
            print("Auron seems fine.")
            FFX_Xbox.menuDown()
        if order[3] != 5: #Lulu, 4th slot
            print("Looking for Lulu")
            if order[4] == 5:
                print("Lulu in fifth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[4] = order[3]
                order[3] = 5
            elif order[5] == 5:
                print("Lulu in sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                order[5] = order[3]
                order[3] = 5
        else:
            print("Lulu seems fine.")
            FFX_Xbox.menuDown()
        if order[4] != 3: #Kimahri, 5th slot
            print("Swapping 5th and 6th slots")
            FFX_Xbox.menuB()
            FFX_Xbox.menuDown()
            FFX_Xbox.menuB()
            order[5] = order[4]
            order[4] = 3
        else:
            print("Lulu and Yuna seem fine.")
            
        
        FFX_Xbox.menuA()
        FFX_Xbox.menuDown()
        FFX_Xbox.menuDown()
        FFX_Xbox.menuDown()
    return checkMRRForm()

def checkMRRForm():
    success = 1
    order = FFX_memory.getOrderSix()
    if order[0] != 0:
        print("Tidus is NOT first")
        success = 0
    else:
        print("Tidus is first")
    if order[1] != 4:
        print("Wakka is NOT second")
        success = 0
    else:
        print("Wakka is second")
    if order[2] != 2:
        print("Auron is not third.")
        success = 0
    else:
        print("Auron is third")
    if order[3] != 5:
        print("Lulu is not fourth.")
        success = 0
    else:
        print("Lulu is fourth")
    if order[4] != 3:
        print("Kimahri is not fifth.")
        success = 0
    else:
        print("Kimahri is fifth")
    if order[5] != 1:
        print("Yuna is not last.")
        success = 0
    else:
        print("Yuna is last")
    return success
    
def checkMMRForm_old():
    success = 1
    if PixelTest(307,181,(22,22,22)):
        print("Tidus is first")
    else:
        print("Tidus is NOT first")
        success = 0
    if PixelTest(311,255,(22,22,22)):
        print("Kimahri is second")
    else:
        print("Kimahri is NOT second")
        success = 0
    if PixelTest(348,480,(22,22,22)):
        print("Wakka is fifth")
    else:
        print("Wakka is NOT fifth")
        success = 0
    if PixelTest(288,405,(22,22,22)):
        print("Lulu is fourth")
    else:
        print("Lulu is NOT fourth")
        success = 0
    if success == 0:
        print("Doesn't matter between Auron and Yuna")
    elif PixelTest(270,556,(22,22,22)):
        print("Yuna is sixth, we're good.")
    else:
        print("Yuna/Auron backwards")
        success = 0
    return success

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
    position = 1
    count += 1
    if count > 100: #Prevent infinite loop
        return 0
    try:
        potTest = pyautogui.locateOnScreen('img\\ABpotion.JPG', confidence=0.8)
        print("Details for Al Bhed potion: ", potTest)
        if potTest[0] > 467:
            position += 1
            FFX_Xbox.menuRight()
        if potTest[1] > 734:
            position += 2
            FFX_Xbox.menuDown()
        if potTest[1] > 779:
            position += 2
            FFX_Xbox.menuDown()
        print("Now hovering position: ", position)
        #time.sleep(20)
        return position
    except Exception as errorMsg:
        print("Something went wrong. Could not find item.")
        print(errorMsg)
        return abPotPos(count)

def RikkuODMap():
    position = 1
    try:
        mapTest = pyautogui.locateOnScreen('img\\Map_R_OD.JPG', confidence=0.75)
        print("Details for Map: ", mapTest)
        print("mapTest[1]: ", mapTest[1])
        if mapTest[1] > 785:
            if mapTest[0] > 467:
                print("Map on right side.")
                FFX_Xbox.menuRight()
                FFX_Xbox.menuB()
                FFX_Xbox.menuLeft()
                return True
            elif mapTest[0] > 50:
                print("Map on left side.")
                FFX_Xbox.menuB()
                return True
    except Exception as errorMsg:
        print("Something went wrong. Could not find item.")
        print(errorMsg)
        return False

def RikkuODLuck():
    if PixelTestTol(174,802,(100, 16, 190),5) and PixelTestTol(279,812,(172, 172, 172),5):
        FFX_Xbox.menuB()
        return True
    if PixelTestTol(524,801,(60, 3, 141),5) and PixelTestTol(629,812,(172, 172, 172),5):
        FFX_Xbox.menuRight()
        FFX_Xbox.menuB()
        FFX_Xbox.menuLeft()
        return True

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

def openMenu():
    print("Opening menu")
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    complete = 0
    while complete == 0:
        if PixelTestTol(1583,32,(79, 86, 133),5):
            if PixelTestTol(1466,735,(32, 43, 81),5):
                if PixelTestTol(1155,184,(153, 153, 153),5):
                    time.sleep(0.2)
                    complete = 1
                else:
                    FFX_Xbox.menuA()
            else:
                FFX_Xbox.menuA()
        else:
            FFXC.set_value('BtnY', 1)
            time.sleep(0.35)
            FFXC.set_value('BtnY', 0)
            time.sleep(0.35)
    return 1

def desertCharge():
    chargeState = [False,False]
    chargeState[0] = checkCharge(1)
    chargeState[1] = checkCharge(2)
    return chargeState