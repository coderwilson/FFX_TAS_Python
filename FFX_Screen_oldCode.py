
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
        if FFX_memory.menuOpen() and not FFX_memory.userControl():
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
