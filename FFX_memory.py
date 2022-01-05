import struct
import FFX_Xbox
import time
import FFX_Screen

from math import cos, sin
baseValue = 0

def float_from_integer(integer):
    return struct.unpack('!f', struct.pack('!I', integer))[0]

def waitFrames(frames: int):
    frames = max(round(frames), 1)
    global baseValue
    key = baseValue + 0x0088FDD8
    current = process.readBytes(key, 4)
    final = current + frames
    previous = current-1
    while current < final:
        if not (current == previous or current == previous + 1): 
            final = final - previous
        previous = current
        current = process.readBytes(key, 4)
    return

def start():
    global process
    global xPtr
    global yPtr
    global coordsCounter
    coordsCounter = 0
    from ReadWriteMemory import ReadWriteMemory

    rwm = ReadWriteMemory()
    print("Memory module opened:")
    print(rwm)
    process = rwm.get_process_by_name('FFX.exe')

    print("Process now captured for FFX (reading memory)")
    print(process)
    process.open()
    print(process.__dict__)
    print(process.pid)

    global baseValue
    try:
        import FFX_zz_rootMem
        print("Process Modules:")
        baseValue = FFX_zz_rootMem.ListProcessModules(process.pid)
        print("Process Modules complete")
        #testValue = FFX_zz_rootMem.GetBaseAddr(process.pid,b'FFX.exe')
        print("Dynamically determined memory address: ",hex(baseValue))
    except Exception as errCode:
        print("Could not get memory address dynamically. ", errCode)
        baseValue = 0x00FF0000

def rngSeed():
    global baseValue
    key = baseValue + 0x003988a5
    return process.readBytes(key,1)

def setRngSeed(value):
    global baseValue
    key = baseValue + 0x003988a5
    return process.writeBytes(key,value,1)

def gameOver():
    global baseValue
    key = baseValue + 0x00D2C9F1
    if process.readBytes(key,1) == 1:
        return True
    else:
        return False

def battleComplete():
    global baseValue
    key = baseValue + 0x00D2C9F1
    if process.readBytes(key,1) == 2:
        return True
    elif process.readBytes(key,1) == 3:
        return True
    else:
        return False

def gameOverReset():
    global baseValue
    key = baseValue + 0x00D2C9F1
    process.writeBytes(key,0,1)

def battleActive():
    global baseValue
    key = baseValue + 0x00D2C9F1
    if process.readBytes(key,1) == 0:
        return True
    else:
        return False

def getNextTurn():
    global baseValue
    key = baseValue + 0x00D2AA04
    return process.readBytes(key,1)

def battleMenuCursor():
    global baseValue
    key = baseValue + 0x00F3F77B
    while process.readBytes(key,1) == 0:
        waitFrames(1)
    key2 = baseValue + 0x00F3C926
    return process.readBytes(key2,1)

def battleScreen():
    if mainBattleMenu():
        global baseValue
        #key = baseValue + 0x00F3C9EF
        #if process.readBytes(key,1) == 0:
        #    return False
        if battleMenuCursor() == 255:
            return False
        else:
            waitFrames(10)
            return True
    else:
        return False

def turnReady():
    global baseValue
    key = baseValue + 0x00F3F77B
    if process.readBytes(key,1) == 0:
        return False
    else:
        waitFrames(4) #Can be dialed in from 15
        return True

def battleCursor2():
    global baseValue
    key = baseValue + 0x00F3CA01
    if process.readBytes(key,1) != 0:
        key = baseValue + 0x00F3CA0E
        return process.readBytes(key,1)
    else:
        return 255

def battleCursor3():
    global baseValue
    key = baseValue + 0x00F3CAFE
    return process.readBytes(key,1)

def mainBattleMenu():
    global baseValue
    key = baseValue + 0x00F3C911
    if process.readBytes(key,1) > 0:
        return True
    else:
        return False

def otherBattleMenu():
    global baseValue
    key = baseValue + 0x00F3CA01
    if process.readBytes(key,1) > 0:
        return True
    else:
        return False

def battleTargetId():
    global baseValue
    key = baseValue + 0x00F3D1B4
    retVal = process.readBytes(key,1)
    print("Battle Target ID: ", retVal)
    return retVal

def userControl():
    global baseValue
    #Auto updating via reference to the baseValue above
    global xPtr
    global yPtr
    xPtr = baseValue + 0x0084DED0
    yPtr = baseValue + 0x0084DED8
    coord1 = process.get_pointer(xPtr)
    x = float_from_integer(process.read(coord1))
    coord2 = process.get_pointer(yPtr)
    y = float_from_integer(process.read(coord2))

    if [x,y] == [0.0,0.0]:
        return False
    else:
        return True

def awaitControl():
    waitCounter = 0
    print("Awaiting control (no clicking)")
    while not userControl():
        waitCounter += 1
        if waitCounter % 10000000 == 0:
            print("Awaiting control - ", waitCounter / 100000)
    waitFrames(30 * 0.05)
    return True

def clickToControl():
    FFXC = FFX_Xbox.controllerHandle()
    waitCounter = 0
    print("Awaiting control (clicking)")
    while not userControl():
        FFX_Xbox.tapB()
        waitCounter += 1
        if waitCounter % 1000 == 0:
            print("Awaiting control - ", waitCounter / 1000)
    waitFrames(30 * 0.05)
    return True

def clickToControl2():
    waitCounter = 0
    print("Awaiting control (clicking)")
    while not userControl():
        FFXC.set_value('BtnB', 1)
        waitFrames(30 * 0.04)
        FFXC.set_value('BtnB', 0)
        waitFrames(30 * 0.04)
        waitCounter += 1
        if waitCounter % 1000 == 0:
            print("Awaiting control - ", waitCounter / 1000)
    waitFrames(30 * 0.05)
    return True

def clickToControl3():
    waitCounter = 0
    print("Awaiting control (clicking only when appropriate - dialog)")
    waitFrames(6)
    while not userControl():
        if battleActive():
            while battleActive():
                FFX_Xbox.tapB()
        if diagSkipPossible():
            print("Skip dialog")
            FFX_Xbox.tapB()
        elif menuOpen():
            print("Menu open (after battle)")
            FFX_Xbox.tapB()
        else:
            waitFrames(30 * 0.035)
        waitCounter += 1
        if waitCounter % 1000 == 0:
            print("Awaiting control - ", waitCounter / 1000)
    waitFrames(30 * 0.05)
    print("User control restored.")
    return True

def clickToControlSpecial():
    FFXC = FFX_Xbox.controllerHandle()
    waitCounter = 0
    print("Awaiting control (clicking)")
    while not userControl():
        FFXC.set_value('BtnB', 1)
        FFXC.set_value('BtnY', 1)
        waitFrames(30 * 0.035)
        FFXC.set_value('BtnB', 0)
        FFXC.set_value('BtnY', 0)
        waitFrames(30 * 0.035)
        waitCounter += 1
        if waitCounter % 100 == 0:
            print("Awaiting control - ", waitCounter / 100)
    waitFrames(30 * 0.05)
    return True

def clickToEvent():
    while userControl():
        FFX_Xbox.tapB()
    waitFrames(30 * 0.2)

def clickToEventTemple(direction):
    FFXC = FFX_Xbox.controllerHandle()
    if direction == 0:
        FFXC.set_movement(0, 1)
    if direction == 1:
        FFXC.set_movement(1, 1)
    if direction == 2:
        FFXC.set_movement(1, 0)
    if direction == 3:
        FFXC.set_movement(1, -1)
    if direction == 4:
        FFXC.set_movement(0, -1)
    if direction == 5:
        FFXC.set_movement(-1, -1)
    if direction == 6:
        FFXC.set_movement(-1, 0)
    if direction == 7:
        FFXC.set_movement(-1, 1)
    while userControl():
        FFX_Xbox.tapB()
    FFXC.set_neutral()
    waitFrames(30 * 0.2)
    while not userControl():
        clickToControl3()
        waitFrames(30 * 0.035)

def awaitEvent():
    waitFrames(1)
    while userControl():
        waitFrames(1)

def getCoords():
    global process
    global baseValue
    global xPtr
    global yPtr
    global coordsCounter
    coordsCounter += 1
    xPtr = baseValue + 0x0084DED0
    yPtr = baseValue + 0x0084DED8
    coord1 = process.get_pointer(xPtr)
    x = float_from_integer(process.read(coord1))
    coord2 = process.get_pointer(yPtr)
    y = float_from_integer(process.read(coord2))

    return [x,y]

def extractorHeight():
    global process
    global baseValue
    global zPtr
    key = baseValue + 0x01fc44e4
    height = float_from_integer(process.read(key + 0x1990))
    print("^^Extractor Height: ", height)
    return height

def getHeight():
    global process
    global baseValue
    global zPtr
    
    zPtr = baseValue + 0x0084DED0
    coord1 = process.get_pointer(zPtr)
    return float_from_integer(process.read(coord1))

def getMovementVectors():
    global process
    global baseValue
    addr = baseValue + 0x00F00754
    ptr = process.get_pointer(addr)
    angle = float_from_integer(process.read(ptr))
    forward = [cos(angle), sin(angle)]
    right = [sin(angle), -cos(angle)]
    return (forward, right)

def getCamera():
    global baseValue
    angle = baseValue + 0x008A86B8
    x = baseValue + 0x008A86F8
    y = baseValue + 0x008A8700
    z = baseValue + 0x008A86FC
    angle2 = baseValue + 0x008A86C0

    key = process.get_pointer(angle)
    angleVal = round(float_from_integer(process.read(key)),2)
    key = process.get_pointer(x)
    xVal = round(float_from_integer(process.read(key)),2)
    key = process.get_pointer(y)
    yVal = round(float_from_integer(process.read(key)),2)
    key = process.get_pointer(z)
    zVal = round(float_from_integer(process.read(key)),2)
    key = process.get_pointer(angle2)
    angleVal2 = round(float_from_integer(process.read(key)),2)

    retVal = [angleVal,xVal,yVal,zVal, angleVal2]
    #print("Camera details: ", retVal)
    return retVal

def getHP():
    global baseValue
    #Out of combat HP only

    coord = baseValue + 0x00D32078
    HP_Tidus = process.read(coord)

    coord = baseValue + 0x00D3210C
    HP_Yuna = process.read(coord)

    coord = baseValue + 0x00D321A0
    HP_Auron = process.read(coord)

    coord = baseValue + 0x00D32234
    HP_Kimahri = process.read(coord)

    coord = baseValue + 0x00D322C8
    HP_Wakka = process.read(coord)

    coord = baseValue + 0x00D3235C
    HP_Lulu = process.read(coord)

    coord = baseValue + 0x00D323F0
    HP_Rikku = process.read(coord)

    return [HP_Tidus, HP_Yuna, HP_Auron, HP_Kimahri, HP_Wakka, HP_Lulu, HP_Rikku]

def getMaxHP():
    global baseValue
    #Out of combat HP only

    coord = baseValue + 0x00D32080
    HP_Tidus = process.read(coord)

    coord = baseValue + 0x00D32114
    HP_Yuna = process.read(coord)

    coord = baseValue + 0x00D321A8
    HP_Auron = process.read(coord)

    coord = baseValue + 0x00D3223C
    HP_Kimahri = process.read(coord)

    coord = baseValue + 0x00D322D0
    HP_Wakka = process.read(coord)

    coord = baseValue + 0x00D32364
    HP_Lulu = process.read(coord)

    coord = baseValue + 0x00D323F8
    HP_Rikku = process.read(coord)

    return [HP_Tidus, HP_Yuna, HP_Auron, HP_Kimahri, HP_Wakka, HP_Lulu, HP_Rikku]

def getOrder():
    global baseValue
    #Out of combat HP only

    coord = baseValue + 0x00D307E8
    pos1 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307E9
    pos2 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EA
    pos3 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EB
    pos4 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EC
    pos5 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307ED
    pos6 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EE
    pos7 = process.readBytes(coord,1)

    formation = [255, pos1, pos2, pos3, pos4, pos5, pos6, pos7]
    print("Party formation: ", formation)
    return formation

def getOrderSix():
    global baseValue
    #Out of combat HP only

    coord = baseValue + 0x00D307E8
    pos1 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307E9
    pos2 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EA
    pos3 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EB
    pos4 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EC
    pos5 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307ED
    pos6 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EE
    pos7 = process.readBytes(coord,1)

    formation = [pos1, pos2, pos3, pos4, pos5, pos6, pos7]
    print(formation)
    while 255 in formation:
        formation.remove(255)
    #print("Party formation: ", formation)
    return formation

def getOrderSeven():
    global baseValue
    #Out of combat HP only

    coord = baseValue + 0x00D307E8
    pos1 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307E9
    pos2 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EA
    pos3 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EB
    pos4 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EC
    pos5 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307ED
    pos6 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EE
    pos7 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EF
    pos8 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307F0
    pos9 = process.readBytes(coord,1)

    formation = [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9]
    #print("Party formation, non-clean:", formation)
    while 255 in formation:
        formation.remove(255)
    #print("Party formation, cleaned: ", formation)
    return formation

def getCharFormationSlot(charNum):
    allSlots = getOrderSeven()
    x = 0
    while x < len(allSlots):
        if allSlots[x] == charNum:
            return x
        else:
            x += 1
    return 255 #Character is not in the party

def getPhoenix():
    global baseValue

    key = getItemSlot(6)
    pDowns = getItemCountSlot(key)
    print("Phoenix Down count: ", pDowns)
    return pDowns

def getPower():
    global baseValue

    key = getItemSlot(70)
    power = getItemCountSlot(key)
    print("Power spheres: ", power)
    return power

def setPower(qty):
    global baseValue

    slot = getItemSlot(70)
    key = baseValue + itemCountAddr(slot)
    process.writeBytes(key, qty, 1)
    power = getPower()
    return power

def getSpeed():
    global baseValue

    key = getItemSlot(72)
    speed = getItemCountSlot(key)
    print("Speed spheres: ", speed)
    return speed

def setSpeed(qty):
    global baseValue

    slot = getItemSlot(72)
    key = baseValue + itemCountAddr(slot)
    process.writeBytes(key, qty, 1)
    speed = getSpeed()
    return speed

def getBattleHP():
    global baseValue

    key = baseValue + 0x00F3F7A4
    hp1 = process.read(key)
    key = baseValue + 0x00F3F834
    hp2 = process.read(key)
    key = baseValue + 0x00F3F8C4
    hp3 = process.read(key)
    hpArray = [0, hp1, hp2, hp3]
    print("HP values: ", hpArray)
    return hpArray

def getBattleNum():
    global baseValue

    key = baseValue + 0x00D2A8EC
    formation = process.read(key)

    #print("Battle Number: ", formation)
    return formation

def getActiveBattleFormation():
    global baseValue

    key = baseValue + 0x00F3F76C
    char1 = process.readBytes(key, 1)
    key = baseValue + 0x00F3F76E
    char2 = process.readBytes(key, 1)
    key = baseValue + 0x00F3F770
    char3 = process.readBytes(key, 1)

    battleForm = [char1, char2, char3]
    if 255 in battleForm:
        while 255 in battleForm:
            battleForm.remove(255)
    return battleForm

def getBattleFormation():
    global baseValue

    key = baseValue + 0x00F3F76C
    char1 = process.readBytes(key,1)
    key = baseValue + 0x00F3F76E
    char2 = process.readBytes(key,1)
    key = baseValue + 0x00F3F770
    char3 = process.readBytes(key,1)
    key = baseValue + 0x00D2C8A3
    char4 = process.readBytes(key,1)
    key = baseValue + 0x00D2C8A4
    char5 = process.readBytes(key,1)
    key = baseValue + 0x00D2C8A5
    char6 = process.readBytes(key,1)
    key = baseValue + 0x00D2C8A6
    char7 = process.readBytes(key,1)
    key = baseValue + 0x00D2C8A7
    char8 = process.readBytes(key,1)

    battleForm = [char1, char2, char3, char4, char5, char6, char7, char8]
    print(battleForm)
    if 255 in battleForm:
        while 255 in battleForm:
            battleForm.remove(255)
    print(battleForm)
    return battleForm

def getBattleCharSlot(charNum):
    battleForm = getBattleFormation()
    try:
        if battleForm[0] == charNum:
            return 1
        if battleForm[1] == charNum:
            return 2
        if battleForm[2] == charNum:
            return 3
        if battleForm[3] == charNum:
            return 4
        if battleForm[4] == charNum:
            return 5
        if battleForm[5] == charNum:
            return 6
        if battleForm[6] == charNum:
            return 7
    except:
        return 0

def getBattleCharTurn():
    global baseValue

    key = baseValue + 0x00D36A68
    battleCharacter = process.read(key)
    return battleCharacter

def getSLVLYuna():
    global baseValue
    #Out of combat HP only

    coord = baseValue + 0x00D32104
    return process.read(coord)

def getSLVLKim():
    global baseValue
    #Out of combat HP only

    coord = baseValue + 0x00D3222C
    return process.read(coord)

def getSLVLWakka():
    global baseValue
    #Out of combat HP only

    key = baseValue + 0x00D322E7
    sLvl = process.readBytes(key,1)
    print("Wakka current Slvl", sLvl)
    return sLvl

def itemAddress(num):
    if num == 1:
        return 0x00D3095C
    if num == 2:
        return 0x00D3095E
    if num == 3:
        return 0x00D30960
    if num == 4:
        return 0x00D30962
    if num == 5:
        return 0x00D30964
    if num == 6:
        return 0x00D30966
    if num == 7:
        return 0x00D30968
    if num == 8:
        return 0x00D3096A
    if num == 9:
        return 0x00D3096C
    if num == 10:
        return 0x00D3096E
    if num == 11:
        return 0x00D30970
    if num == 12:
        return 0x00D30972
    if num == 13:
        return 0x00D30974
    if num == 14:
        return 0x00D30976
    if num == 15:
        return 0x00D30978
    if num == 16:
        return 0x00D3097A
    if num == 17:
        return 0x00D3097C
    if num == 18:
        return 0x00D3097E
    if num == 19:
        return 0x00D30980
    if num == 20:
        return 0x00D30982
    if num == 21:
        return 0x00D30984
    if num == 22:
        return 0x00D30986
    if num == 23:
        return 0x00D30988
    if num == 24:
        return 0x00D3098A
    if num == 25:
        return 0x00D3098C
    if num == 26:
        return 0x00D3098E
    if num == 27:
        return 0x00D30990
    if num == 28:
        return 0x00D30992
    if num == 29:
        return 0x00D30994
    if num == 30:
        return 0x00D30996

def getItemsOrder():
    global baseValue
    items = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for x in range(30):
        address = itemAddress(x + 1)
        key = baseValue + address
        item = process.readBytes(key,1)
        items[x + 1] = item

    #print(items)
    return items

def getUseItemsOrder():
    itemArray = getItemsOrder()
    x = 1
    while x < len(itemArray):
        #print("x = %d" % x)
        try:
            if itemArray[x] == 20:
                print("Al Bhed pots, disregard.")
                x += 1
            elif itemArray[x] < 23:
                del itemArray[x]
            elif itemArray[x] > 69:
                del itemArray[x]
            else:
                x += 1
        except:
            x += 1
        #print(itemArray)
    print("Use command, item order:")
    print(itemArray)
    return itemArray

def getUseItemsSlot(itemNum):
    items = getUseItemsOrder()
    x = 1
    while x < len(items):
        #print(items[x + 1], " | ", itemNum)
        if items[x] == itemNum:
            return x
        x += 1
    return 255

def getThrowItemsOrder():
    itemArray = getItemsOrder()
    x = 1
    while x < len(itemArray):
        try:
            if itemArray[x] > 15:
                itemArray.remove(itemArray[x])
            else:
                x += 1
        except:
            x += 1
    print("Throw Item command, item order:")
    print(itemArray)
    return itemArray

def getThrowItemsSlot(itemNum):
    items = getThrowItemsOrder()
    x = 1
    while x < len(items):
        #print(items[x + 1], " | ", itemNum)
        if items[x] == itemNum:
            print("Desired item ", itemNum, " is in slot ", x)
            return x
        x += 1
    return 255

def getGridItemsOrder():
    itemArray = getItemsOrder()
    x = 0
    while x < len(itemArray):
        try:
            if itemArray[x] < 70 or itemArray[x] > 99:
                itemArray.remove(itemArray[x])
            else:
                x += 1
        except:
            x += 1
    print("Sphere grid, item order:")
    print(itemArray)
    return itemArray

def getGridItemsSlot(itemNum) -> int:
    items = getGridItemsOrder()
    x = 0
    while x < len(items):
        #print(items[x + 1], " | ", itemNum)
        if items[x] == itemNum:
            print("Desired item ", itemNum, " is in slot ", x)
            return x
        x += 1
    return 255

def getGridCursorPos():
    global baseValue
    key = baseValue + 0x012ACB78
    return process.readBytes(key,1)

def getGridMoveUsePos():
    global baseValue
    key = baseValue + 0x012AC838
    return process.readBytes(key,1)

def getGridMoveActive():
    global baseValue
    key = baseValue + 0x012AC82B
    if process.readBytes(key,1):
        return True
    else:
        return False

def getGridUseActive():
    global baseValue
    key = baseValue + 0x012ACB6B
    if process.readBytes(key,1):
        return True
    else:
        return False

def getItemSlot(itemNum):
    items = getItemsOrder()
    for x in range(30):
        #print(items[x + 1], " | ", itemNum)
        if items[x + 1] == itemNum:
            return (x + 1)
    return 255

def checkItemsMacalania():
    bombCore = 0
    lMarble = 0
    fScale = 0
    aWind = 0
    grenade = 0
    lunar = 0
    light = 0

    bombCore = getItemSlot(27)
    lMarble = getItemSlot(30)
    fScale = getItemSlot(32)
    aWind = getItemSlot(24)
    grenade = getItemSlot(35)
    lunar = getItemSlot(56)
    light = getItemSlot(57)

    #Set MaxSpot to one more than the last undesirable item
    if light - lunar != 1:
        maxSpot = light
    elif lunar - grenade != 1:
        maxSpot = lunar
    elif grenade - aWind != 1:
        maxSpot = grenade
    elif aWind - fScale != 1:
        maxSpot = aWind
    elif fScale - lMarble != 1:
        maxSpot = fScale
    elif lMarble - bombCore != 1:
        maxSpot = lMarble
    else:
        maxSpot = bombCore

    retVal = [bombCore, lMarble, fScale, aWind, grenade, lunar, light, maxSpot]
    print("Returning values: ", retVal)
    return retVal

def itemCountAddr(num):
    if num == 1:
        return 0x00D30B5C
    if num == 2:
        return 0x00D30B5D
    if num == 3:
        return 0x00D30B5E
    if num == 4:
        return 0x00D30B5F
    if num == 5:
        return 0x00D30B60
    if num == 6:
        return 0x00D30B61
    if num == 7:
        return 0x00D30B62
    if num == 8:
        return 0x00D30B63
    if num == 9:
        return 0x00D30B64
    if num == 10:
        return 0x00D30B65
    if num == 11:
        return 0x00D30B66
    if num == 12:
        return 0x00D30B67
    if num == 13:
        return 0x00D30B68
    if num == 14:
        return 0x00D30B69
    if num == 15:
        return 0x00D30B6A
    if num == 16:
        return 0x00D30B6B
    if num == 17:
        return 0x00D30B6C
    if num == 18:
        return 0x00D30B6D
    if num == 19:
        return 0x00D30B6E
    if num == 20:
        return 0x00D30B6F
    if num == 21:
        return 0x00D30B70
    if num == 22:
        return 0x00D30B71
    if num == 23:
        return 0x00D30B72
    if num == 24:
        return 0x00D30B73
    if num == 25:
        return 0x00D30B74
    if num == 26:
        return 0x00D30B75
    if num == 27:
        return 0x00D30B76
    if num == 28:
        return 0x00D30B77
    if num == 29:
        return 0x00D30B78
    if num == 30:
        return 0x00D30B79

def getItemsCount():
    global baseValue
    itemCounts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for x in range(30):
        address = itemCountAddr(x + 1)
        key = baseValue + address
        itemCount = process.readBytes(key,1)
        itemCounts[x + 1] = itemCount

    #print(itemCounts)
    return itemCounts

def getItemCountSlot(itemSlot) -> int:
    items = getItemsCount()
    for x in range(30):
        if itemSlot == x + 1:
            print("Number of this item: ", items[x + 1])
            return items[x + 1]
    return 0

def getGilvalue():
    global baseValue
    key = baseValue + 0x00D307D8
    return process.read(key)

def setGilvalue(newValue):
    global baseValue
    key = baseValue + 0x00D307D8
    return process.write(key, newValue)

def rikkuODItems(slot):
    #This function gets the item slots for each item, swaps if they're backwards,
    # and then moves the cursor to each item and presses B when we reach it.
    
    if slot == 0:
        while RikkuODCursor1() >= 1:
            print("Cursor1: ", RikkuODCursor1(), " || Moving to slot: ", slot)
            if RikkuODCursor1() % 2 != slot % 2:
                FFX_Xbox.tapRight()
            elif RikkuODCursor1() > slot:
                FFX_Xbox.tapUp()
            else:
                FFX_Xbox.tapDown()
            waitFrames(2)
    else:
        while RikkuODCursor1() != slot:
            print("Cursor1: ", RikkuODCursor1(), " || Moving to slot: ", slot)
            if RikkuODCursor1() % 2 != slot % 2:
                FFX_Xbox.tapRight()
            elif RikkuODCursor1() > slot:
                FFX_Xbox.tapUp()
            else:
                FFX_Xbox.tapDown()
            waitFrames(2)
    waitFrames(2)
    FFX_Xbox.tapB()
    waitFrames(2)

def oldODLogic():
    if item1 % 2 == 0: #First item is in the right-hand column
        FFX_Xbox.menuRight()
        cursor += 1

    while cursor < item1:
        FFX_Xbox.menuDown()
        cursor += 2

    FFX_Xbox.menuB() #We should now have selected the first item.

    if item1 % 2 != item2 % 2: #First and second items are on different columns
        print("Items are in opposing columns. Switching columns.")
        if item1 % 2 == 0:
            FFX_Xbox.menuLeft()
            FFX_Xbox.menuDown()
        else:
            FFX_Xbox.menuRight()
        cursor += 1

    if cursor == item2:
        FFX_Xbox.menuB() #Cursor starts on item 2. Only occurs if opposite columns.
    else:
        while cursor < item2:
            FFX_Xbox.menuDown()
            cursor += 2
        FFX_Xbox.menuB() #Cursor is now on item 2.

def RikkuODCursor1():
    global baseValue
    key = baseValue + 0x00F3CB32
    return process.readBytes(key,1)


def RikkuODCursor2():
    return RikkuODCursor1()


def getOverdriveBattle(character):
    global process
    global baseValue
    
    basePointer = baseValue + 0x00d334cc
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x5bc
    retVal = process.readBytes(basePointerAddress + offset, 1)
    print("In-Battle Overdrive values: ", retVal)
    return retVal

def getCharWeakness(character):
    global process
    global baseValue
    
    basePointer = baseValue + 0x00d334cc
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x5dd
    retVal = process.readBytes(basePointerAddress + offset, 1)
    print("In-Battle Overdrive values: ", retVal)
    return retVal

def getOverdriveValue(character): #Older function, I think Crimson wrote this one.
    return getOverdriveBattle(character)

def deadstate(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x606

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 2 == 1:
        #print("Character %d is dead" % character)
        return True
    else:
        #print("Character %d is not dead" % character)
        return False
        
def berserkstate(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x607

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 4 >= 2:
        #print("Character %d is berserked" % character)
        return True
    else:
        #print("Character %d is not berserked" % character)
        return False

def petrifiedstate(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x606

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 8 >= 4:
        #print("Character %d is petrified" % character)
        return True
    else:
        #print("Character %d is not petrified" % character)
        return False

def confusedState(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character)+0x607

    key = basePointerAddress + offset
    retVal = process.readBytes(key,1)

    if retVal % 2 == 1:
        print("Character %d is confused" % character)
        return True
    else:
        print("Character %d is not confused" % character)
        return False

def confusedStateByPos(position):
    posArray = getBattleFormation()
    x = 0
    if position in posArray:
        if posArray[x] == position:
            return confusedState(posArray[x])
        else:
            x += 1

def getEnemyCurrentHP():
    global process
    global baseValue
    enemyNum = 20
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)

    while enemyNum < 27:
        offset1 = (0xf90 * enemyNum)+0x594
        key1 = basePointerAddress + offset1
        offset2 = (0xf90 * enemyNum)+0x5D0
        key2 = basePointerAddress + offset2
        if enemyNum == 20:
            maxHP = [process.readBytes(key1,4)]
            currentHP = [process.readBytes(key2,4)]
        else:
            nextHP = process.readBytes(key1,4)
            if nextHP != 0:
                maxHP.append(nextHP)
                currentHP.append(process.readBytes(key2,4))
        enemyNum += 1
    print("Enemy HP max values:")
    print(maxHP)
    print("Enemy HP current values:")
    print(currentHP)
    return currentHP

def setEnemyCurrentHP(numToSet, newHP):
    getEnemyCurrentHP()
    global process
    global baseValue
    numToSet = numToSet + 20
    enemyNum = 20
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)

    while enemyNum < 25:
        offset1 = (0xf90 * enemyNum)+0x594
        key1 = basePointerAddress + offset1
        offset2 = (0xf90 * enemyNum)+0x5D0
        key2 = basePointerAddress + offset2
        if enemyNum == numToSet:
            currentHP = [process.writeBytes(key2, newHP,4)]
            print("HP value has been changed.")
        enemyNum += 1
    getEnemyCurrentHP()

def getEnemyMaxHP():
    global process
    global baseValue
    enemyNum = 20
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)

    while enemyNum < 25:
        offset1 = (0xf90 * enemyNum)+0x594
        key1 = basePointerAddress + offset1
        offset2 = (0xf90 * enemyNum)+0x5D0
        key2 = basePointerAddress + offset2
        if enemyNum == 20:
            maxHP = [process.readBytes(key1,4)]
            currentHP = [process.readBytes(key2,4)]
        else:
            if maxHP != 0:
                maxHP.append(process.readBytes(key1,4))
                currentHP.append(process.readBytes(key2,4))
        enemyNum += 1
    print("Enemy HP max values:")
    print(maxHP)
    print("Enemy HP current values:")
    print(currentHP)
    return maxHP

def menuOpen():
    global baseValue

    key = baseValue + 0x00F407E4
    menuOpen = process.readBytes(key,1)
    if menuOpen == 1:
        return True
    else:
        return False

def closeMenu():
    while menuOpen():
        FFX_Xbox.menuA()

def openMenu():
    FFXC = FFX_Xbox.controllerHandle()
    FFXC.set_neutral()
    while not userControl(): #Get out of combat or whatever
        FFX_Xbox.menuB()
    while userControl() and not menuOpen():
        FFXC.set_value('BtnY',1)
        waitFrames(1)
        FFXC.set_value('BtnY',0)
        waitFrames(1)
    waitFrames(15)

def menuNumber():
    global baseValue
    return process.readBytes(baseValue + 0x85B2CC, 1)

def sGridActive():
    global baseValue

    key = baseValue + 0x0085B30C
    menuOpen = process.readBytes(key,1)
    print(menuOpen)
    if menuOpen == 1:
        return True
    else:
        return False

def sGridMenu():
    global baseValue

    key = baseValue + 0x0012AD860
    menuOpen = process.readBytes(key,1)
    return menuOpen

def sGridChar():
    global baseValue

    key = baseValue + 0x0012BEE2C
    character = process.readBytes(key,1)
    return character

def sGridNodeSelected():
    global baseValue
    
    key = baseValue + 0x0012BEB7E
    nodeNumber = process.readBytes(key,1)
    key = baseValue + 0x0012BEB7F
    nodeRegion = process.readBytes(key,1)
    return [nodeNumber, nodeRegion]

def cursorLocation():
    global baseValue

    key = baseValue + 0x0021D09A4
    menu1 = process.readBytes(key,1)
    key = baseValue + 0x0021D09A6
    menu2 = process.readBytes(key,1)

    return [menu1,menu2]

def getMenuCursorPos():
    global baseValue

    key = baseValue + 0x01471508
    pos = process.readBytes(key, 1)

    return pos

def getMenu2CharNum():
    global baseValue

    key = baseValue + 0x0147150C
    pos = process.readBytes(key, 1)

    return pos

def getCharCursorPos():
    global baseValue

    key = baseValue + 0x01441BE8
    pos = process.readBytes(key, 1)

    return pos

def getStoryProgress():
    global baseValue

    key = baseValue + 0x00D2D67C
    progress = process.readBytes(key,2)
    #print("Story progress: ", progress)
    return progress

def getMap():
    global baseValue

    key = baseValue + 0x00D2CA90
    progress = process.readBytes(key,2)
    return progress

def touchingSaveSphere():
    global baseValue

    key = baseValue + 0x0021D09A6
    value = process.readBytes(key,1)
    if value != 0:
        return True
    else:
        return False

def saveMenuCursor():
    global baseValue

    key = baseValue + 0x001467942
    value = process.readBytes(key,1)
    if value != 0:
        return True
    else:
        return False

def NewGameCursor():
    global baseValue

    key = baseValue + 0x001467942
    value = process.readBytes(key,1)
    return value

def getYunaSlvl():
    global baseValue

    key = baseValue + 0x00D3212B
    sLvl = process.readBytes(key,1)
    return sLvl

def getTidusSlvl():
    global baseValue

    key = baseValue + 0x00D32097
    sLvl = process.readBytes(key,1)
    return sLvl

def getTidusXP():
    global baseValue

    key = baseValue + 0x00D32070
    Lvl = process.read(key)
    return Lvl

def setTidusSlvl(levels):
    global baseValue

    key = baseValue + 0x00D32097
    sLvl = process.writeBytes(key,levels,1)
    return sLvl

def menuControl():
    global baseValue

    key = baseValue + 0x0085A03C
    control = process.readBytes(key,1)
    if control == 1:
        waitFrames(1)
        return True
    else:
        return False

def diagSkipPossible_old():
    global baseValue

    key = baseValue + 0x0085A03C
    control = process.readBytes(key,1)
    if control == 1:
        waitFrames(1)
        return True
    else:
        return False

def diagSkipPossible():
    global baseValue

    key = baseValue + 0x00F2FED0
    control = process.readBytes(key,1)
    if control == 1:
        waitFrames(1)
        return True
    else:
        key = baseValue + 0x0085A03C
        control = process.readBytes(key,1)
        if control == 1:
            waitFrames(1)
            return True
        else:
            return False

def cutsceneSkipPossible():
    global baseValue

    key = baseValue + 0x00D2A008
    control = process.readBytes(key,1)
    if control == 1:
        return True
    else:
        return False

def specialTextOpen():
    global baseValue

    key = baseValue + 0x01466D30
    control = process.readBytes(key,1)
    if control == 1:
        waitFrames(30 * 0.035)
        return True
    else:
        key = baseValue + 0x01476988
        control = process.readBytes(key,1)
        if control == 1:
            waitFrames(30 * 0.035)
            return True
        else:
            return False

def awaitMenuControl():
    counter = 0
    while not menuControl():
        counter += 1
        if counter % 100000 == 0:
            print("Waiting for menu control. ", counter)

def clickToStoryProgress(destination):
    FFXC = FFX_Xbox.controllerHandle()
    counter = 0
    currentState = getStoryProgress()
    print("Story goal: ", destination," | Awaiting progress state: ", currentState)
    while currentState < destination:
        if menuControl():
            FFXC.set_value('BtnB',1)
            FFXC.set_value('BtnA',1)
            waitFrames(30 * 0.035)
            FFXC.set_value('BtnB',0)
            FFXC.set_value('BtnA',0)
            waitFrames(30 * 0.035)
        if counter % 100000 == 0:
            print("Story goal: ", destination," | Awaiting progress state: ", currentState, " | counter: ", counter / 100000)
        counter += 1
        currentState = getStoryProgress()
    print("Story progress has reached destination. Value: ", destination)

def desertFormat(rikkuCharge):
    order = getOrderSix()
    if order == [0,3,2,4,6,5]:
        print("Formation is fine, moving on.")
    elif rikkuCharge == False:
        fullPartyFormat('desert1')
    else:
        fullPartyFormat('desert2')

def partySize():
    return len(getBattleFormation())

def activepartySize():
    return len(getActiveBattleFormation())

def fullPartyFormat_New(frontLine, menusize):
    print("==Full Party Format function, revamped 1")
    frontLine = frontLine.lower()
    order = getOrderSeven()
    partyMembers = len(order)
    
    orderFinal = getPartyFormatFromText(frontLine)
    
    if order == orderFinal:
        print("Good to go, no action taken.")
    else:
        print("Converting from formation:")
        print(order)
        print("Into formation:")
        print(orderFinal)
        while not menuOpen():
            openMenu()

        currentmenuposition = getMenuCursorPos()

        targetmenuposition = 7
        menudistance = abs(targetmenuposition - currentmenuposition)

        if menudistance < (menusize / 2 - 1):
            for i in range(menudistance):
                if targetmenuposition > currentmenuposition:
                    FFX_Xbox.menuDown()
                else:
                    FFX_Xbox.menuUp()
        else:
            for i in range(menusize - menudistance):
                if targetmenuposition > currentmenuposition:
                    FFX_Xbox.menuUp()
                else:
                    FFX_Xbox.menuDown()

        FFX_Xbox.menuB()

        if order[0] != orderFinal[0]:
            print("Looking for ", nameFromNumber(orderFinal[0]))
            if order[1] == orderFinal[0]:
                print("Tidus in Second slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[1] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif order[2] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0]), " in Third slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                order[2] = order[0]
                order[0] = orderFinal[0]
                FFX_Xbox.menuUp()
            elif order[3] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0]), " in Fourth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[3] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            elif order[4] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0]), " in Fifth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                order[4] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
            elif partyMembers > 5 and order[5] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0]), " in Sixth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                order[5] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
            elif partyMembers == 7 and order[6] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0]), " in seventh slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                order[6] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
        else:
            print(nameFromNumber(order[0]), " seems fine.")
            FFX_Xbox.menuDown()
        if order[1] != orderFinal[1]:
            print("Looking for ", nameFromNumber(orderFinal[1]))
            if order[2] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1]), " in Third slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[2] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif order[3] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1]), " in Fourth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[3] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
            elif order[4] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1]), " in Fifth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[4] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            elif partyMembers > 5 and order[5] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1]), " in Sixth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[5] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            elif partyMembers == 7 and order[6] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1]), " in Seventh slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[6] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
        else:
            print(nameFromNumber(order[1]), " seems fine.")
            FFX_Xbox.menuDown()
        if order[2] != orderFinal[2]:
            print("Looking for ", nameFromNumber(orderFinal[2]))
            if order[3] == orderFinal[2]:
                print(nameFromNumber(orderFinal[2]), " in fourth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[3] = order[2]
                order[2] = orderFinal[2]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif order[4] == orderFinal[2]:
                print(nameFromNumber(orderFinal[2]), " in fifth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[4] = order[2]
                order[2] = orderFinal[2]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
            elif partyMembers > 5 and order[5] == orderFinal[2]:
                print(nameFromNumber(orderFinal[2]), " in sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[5] = order[2]
                order[2] = orderFinal[2]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            elif partyMembers == 7 and order[6] == orderFinal[2]:
                print(nameFromNumber(orderFinal[2]), " in seventh slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[6] = order[2]
                order[2] = orderFinal[2]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
        else:
            print(nameFromNumber(order[2]), " seems fine.")
            FFX_Xbox.menuDown()
        if order[3] != orderFinal[3]:
            print("Looking for ", nameFromNumber(orderFinal[3]))
            if order[4] == orderFinal[3]:
                print(nameFromNumber(orderFinal[3]), " in fifth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[4] = order[3]
                order[3] = orderFinal[3]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif partyMembers > 5 and order[5] == orderFinal[3]:
                print(nameFromNumber(orderFinal[3]), " in sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[5] = order[3]
                order[3] = orderFinal[3]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
            elif partyMembers == 7 and order[6] == orderFinal[3]:
                print(nameFromNumber(orderFinal[3]), " in seventh slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[6] = order[3]
                order[3] = orderFinal[3]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
        else:
            print(nameFromNumber(order[3]), " seems fine.")
            FFX_Xbox.menuDown()
        if partyMembers > 5 and order[4] != orderFinal[4]:
            print("Looking for ", nameFromNumber(orderFinal[4]))
            if order[5] == orderFinal[4]:
                print(nameFromNumber(orderFinal[4]), " in Sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[5] = order[4]
                order[4] = orderFinal[4]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif partyMembers == 7 and order[6] == orderFinal[4]:
                print(nameFromNumber(orderFinal[4]), " in Seventh slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[6] = order[4]
                order[4] = orderFinal[4]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
        else:
            print(nameFromNumber(order[4]), " seems fine.")
            FFX_Xbox.menuDown()
        if partyMembers == 7 and order[5] != orderFinal[5]:
            print(nameFromNumber(order[5]), " and ", nameFromNumber(order[6]),
                  "are swapped. Flipping them back.")
            print("Expected order: ", orderFinal[5], " | ", orderFinal[6])
            FFX_Xbox.menuB()
            FFX_Xbox.menuDown()
            FFX_Xbox.menuB()
        elif partyMembers == 7:
            print(nameFromNumber(orderFinal[5]), " and ", nameFromNumber(orderFinal[6]), " seem fine.")

        # waitFrames(30 * 120) #For testing only. Allows us to see what's going on.
        FFX_Xbox.menuA()
        #closeMenu()

def fullPartyFormat(frontLine):
    order = getOrderSeven()
    partyMembers = len(order)
    frontLine = frontLine.lower()
    orderFinal = getPartyFormatFromText(frontLine)
    if order == orderFinal:
        print("Good to go, no action taken.")
    else:
        print("Converting from formation:")
        print(order)
        print("Into formation:")
        print(orderFinal)
        if menuOpen() == False:
            while menuOpen() == False:
                openMenu()
        else:
            #Sometimes needs delay if menu was opened via other means.
            waitFrames(12)
        waitFrames(10)
        #if getStoryProgress() >= 1120: #Before vs after the Customize option is on the menu
        #    while getMenuCursorPos() != 8:
        #    print(getMenuCursorPos())
        #    FFX_Xbox.menuUp()
        #else:
        while getMenuCursorPos() != 7:
            print(getMenuCursorPos())
            FFX_Xbox.menuUp()
        FFX_Xbox.menuB()
        waitFrames(1)
        
        startPos = 0
        targetPos = 1
        while order != orderFinal:
            print("==Full Party Format function, original")
            #Select target in the wrong spot.
            print("Selecting start position")
            if order[startPos] == orderFinal[startPos]:
                while order[startPos] == orderFinal[startPos] and order != orderFinal:
                    startPos += 1
                    if startPos == partyMembers:
                        startPos = 0
            print("Character ", nameFromNumber(orderFinal[startPos]), " should be in position ", startPos)
            print("Looking for character.")
            
            #Move cursor to start position
            print("Moving to start position")
            if partyFormatCursor1() != startPos:
                #print("Cursor not in right spot")
                while partyFormatCursor1() != startPos:
                    menuDirection(partyFormatCursor1(), startPos, partyMembers)
            waitFrames(2)
            FFX_Xbox.menuB() #Click on Start location
            waitFrames(2)
            
            #Set target, end position
            print("Selecting destination position.")
            endPos = 0
            if orderFinal[startPos] != order[endPos]:
                while orderFinal[startPos] != order[endPos] and order != orderFinal:
                    endPos += 1
            
            print("Character ", nameFromNumber(order[endPos]), " found in position ", endPos)
            
            #Move cursor to end position
            print("Moving to destination position.")
            while partyFormatCursor2() != endPos:
                menuDirection(partyFormatCursor2(), endPos, partyMembers)
            waitFrames(2)
            FFX_Xbox.menuB() #Click on End location, performs swap.
            waitFrames(2)
            print("Start and destination positions have been swapped.")
            startPos += 1
            if startPos == partyMembers:
                startPos = 0
            
            print("Reporting results")
            print("Converting from formation:")
            print(order)
            print("Into formation:")
            print(orderFinal)
            order = getOrderSeven()
            #waitFrames(30 * 30)
    print("Party format is good now.")
    #if frontLine != 'miihen':
    closeMenu()

def menuDirection_oldAttempt(currentmenuposition, targetmenuposition, menusize):
    print("Menu move") #could be improved further, for now this is good.
    
    if targetmenuposition > currentmenuposition:
        distanceDown = targetmenuposition - currentmenuposition
        print("Distance Down: ", distanceDown)
        distanceUp = currentmenuposition + menusize - targetmenuposition
        print("Distance Up: ", distanceUp)
        if distanceUp < distanceDown:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    else:
        distanceUp = currentmenuposition - targetmenuposition
        print("Distance Up: ", distanceUp)
        distanceDown = targetmenuposition + menusize - currentmenuposition
        print("Distance Down: ", distanceDown)
        if distanceUp < distanceDown:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
            
def menuDirection(currentmenuposition, targetmenuposition, menusize):
    #print("Menu move (new)")
    distance = abs(currentmenuposition - targetmenuposition)
    distanceUnsigned = currentmenuposition - targetmenuposition
    #print("Menu Size: ", menusize)
    halfmenusize = menusize / 2
    if distance == halfmenusize:
        #print("Marker 1")
        FFX_Xbox.menuUp()
    elif distance < halfmenusize:
        if distanceUnsigned > 0:
            #print("Marker 2")
            FFX_Xbox.menuUp()
        else:
            #print("Marker 3")
            FFX_Xbox.menuDown()
    else:
        if distanceUnsigned > 0:
            #print("Marker 4")
            FFX_Xbox.menuDown()
        else:
            FFX_Xbox.menuUp()
            #print("Marker 5")

def partyFormatCursor1():
    global baseValue

    coord = baseValue + 0x0147151C
    retVal = process.readBytes(coord, 1)
    #print("cursor identify: ", retVal)
    return retVal

def partyFormatCursor2():
    global baseValue

    coord = baseValue + 0x01471520
    retVal = process.readBytes(coord, 1)
    #print("cursor identify: ", retVal)
    return retVal

def getPartyFormatFromText(frontLine):
    print("||||||||||||| FRONT LINE VARIABLE: ", frontLine)
    if frontLine == 'kimahri':
        orderFinal = [0,3,2,6,4,5,1]
    elif frontLine == 'rikku':
        orderFinal = [0,6,2,3,4,5,1]
    elif frontLine == 'yuna':
        orderFinal = [0,1,2,6,4,5,3]
    elif frontLine == 'gauntlet':
        orderFinal = [0,1,3,2,4,5,6]
    elif frontLine == 'miihen':
        orderFinal = [0,4,2,3,5,1]
    elif frontLine == 'macalaniaescape':
        orderFinal = [0,1,6,2,4,3,5]
    elif frontLine == 'desert1':
        orderFinal = [0,6,2,3,4,5]
    elif frontLine == 'desert2':
        orderFinal = [0,3,2,6,4,5]
    elif frontLine == 'desert9':
        orderFinal = [0,4,2,3,5]
    elif frontLine == 'guards':
        orderFinal = [0,2,3,6,4,5]
    elif frontLine == 'evrae':
        orderFinal = [0,6,3,2,4,5]
    elif frontLine == 'djose':
        orderFinal = [0,4,2,3,1,5]
    elif frontLine == 'spheri':
        orderFinal = [0,3,1,4,2,6,5]
    elif frontLine == 'crawler':
        orderFinal = [0,3,5,4,2,6,1]
    elif frontLine == 'besaid1':
        orderFinal = [0,1,5,3,4]
    elif frontLine == 'kilika':
        orderFinal = [0,1,4,3,5]
    elif frontLine == 'mrr1':
        orderFinal = [0,4,2,3,5,1]
    elif frontLine == 'mrr2':
        orderFinal = [1,4,3,5,2,0]
    elif frontLine == 'battlesite':
        orderFinal = [0,1,4,5,2,3]
    elif frontLine == 'postbunyip':
        orderFinal = [0, 4, 2, 6, 1, 3, 5]
    elif frontLine == 'mwoodsneedcharge':
        orderFinal = [0, 6, 2, 4, 1, 3, 5]
    elif frontLine == 'mwoodsgotcharge':
        orderFinal = [0, 4, 2, 6, 1, 3, 5]
    elif frontLine == 'mwoodsdone':
        orderFinal = [0, 3, 2, 4, 1, 6, 5]
    elif frontLine == 'besaid':
        orderFinal = [5,1,0,4]
    else:
        orderFinal = [6,5,4,3,2,1,0]
    return orderFinal

def nameFromNumber(charNum):
    if charNum == 0:
        return "Tidus"
    if charNum == 1:
        return "Yuna"
    if charNum == 2:
        return "Auron"
    if charNum == 3:
        return "Kimahri"
    if charNum == 4:
        return "Wakka"
    if charNum == 5:
        return "Lulu"
    if charNum == 6:
        return "Rikku"

def getActorCoords(actorNumber):
    global process
    global baseValue
    retVal = [0,0,0]
    try:
        basePointer = baseValue + 0x01fc44e4
        basePointerAddress = process.read(basePointer)
        offsetX = (0x880 * actorNumber) + 0x0c
        offsetY = (0x880 * actorNumber) + 0x14
        offsetZ = (0x880 * actorNumber) + 0x10

        keyX = basePointerAddress + offsetX
        retVal[0] = float_from_integer(process.read(keyX))
        keyY = basePointerAddress + offsetY
        retVal[1] = float_from_integer(process.read(keyY))
        keyZ = basePointerAddress + offsetY
        retVal[2] = float_from_integer(process.read(keyZ))

        return retVal
    except:
        doNothing = True

def miihenGuyCoords():
    global process
    global baseValue
    retVal = [0,0]
    
    basePointer = baseValue + 0x01fc44e4
    basePointerAddress = process.read(basePointer)
    offsetX = 0x330c
    offsetY = 0x3314

    keyX = basePointerAddress + offsetX
    retVal[0] = float_from_integer(process.read(keyX))
    keyY = basePointerAddress + offsetY
    retVal[1] = float_from_integer(process.read(keyY))

    return retVal

def lucilleMiihenCoords():
    return getActorCoords(8)

def lucilleDjoseCoords():
    return getActorCoords(11)

def lucilleDjoseAngle():
    global process
    global baseValue
    retVal = [0,0]
    
    basePointer = baseValue + 0x01fc44e4
    basePointerAddress = process.read(basePointer)
    offsetX = 0x91D8
    offsetY = 0x91E8

    keyX = basePointerAddress + offsetX
    retVal[0] = float_from_integer(process.read(keyX))
    keyY = basePointerAddress + offsetY
    retVal[1] = float_from_integer(process.read(keyY))

    return retVal

def affectionArray():
    global process
    global baseValue
    
    tidus = 255
    key = baseValue + 0x00D2CAC0
    yuna = process.readBytes(key, 1)
    key = baseValue + 0x00D2CAC4
    auron = process.readBytes(key, 1)
    key = baseValue + 0x00D2CAC8
    kimahri = process.readBytes(key, 1)
    key = baseValue + 0x00D2CACC
    wakka = process.readBytes(key, 1)
    key = baseValue + 0x00D2CAD0
    lulu = process.readBytes(key, 1)
    key = baseValue + 0x00D2CAD4
    rikku = process.readBytes(key, 1)
    
    return [tidus, yuna, auron, kimahri, wakka, lulu, rikku]

def overdriveState():
    global process
    global baseValue
    retVal = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    x = 0
    
    basePointer = baseValue + 0x00386DD4
    basePointerAddress = process.read(basePointer)
    for x in range(20):
        offset = (0x94 * x) + 0x39
        retVal[x] = process.readBytes(basePointerAddress + offset, 1)
    print("Overdrive values: ", retVal)
    return retVal

def overdriveState2():
    global process
    global baseValue
    retVal = [0,0,0,0,0,0,0]
    x = 0
    
    basePointer = baseValue + 0x003AB9B0
    basePointerAddress = process.read(basePointer)
    for x in range(7):
        offset = (0x94 * x) + 0x39
        retVal[x] = process.readBytes(basePointerAddress + offset, 1)
    print("Overdrive values: ", retVal)
    return retVal

def dodgeLightning(lDodgeNum): #Not working yet
    global baseValue
    
    if lStrikeCount() != lDodgeNum:
        waitFrames(30 * 0.07)
        FFX_Xbox.menuB()
        waitFrames(30 * 0.07)
        return True
    else:
        return False

def lStrikeCount():
    global baseValue

    key = baseValue + 0x00D2CE8C
    return process.readBytes(key, 2)

def lDodgeCount():
    global baseValue

    key = baseValue + 0x00D2CE8E
    return process.readBytes(key, 2)

def savePopupCursor():
    global baseValue

    key = baseValue + 0x0146780A
    return process.readBytes(key, 1)

def diagProgressFlag():
    global baseValue

    key = baseValue + 0x00F25A80
    return process.readBytes(key, 4)

def clickToDiagProgress(num):
    print("Clicking to dialog progress: ", num)
    lastNum = diagProgressFlag()
    while diagProgressFlag() != num:
        if userControl():
            return False
        else:
            FFX_Xbox.tapB()
            if diagProgressFlag() != lastNum:
                lastNum = diagProgressFlag()
                print("Dialog change: ", diagProgressFlag(), " - clicking to ", num)
    return True

def setEncounterRate(setVal):
    global baseValue

    key = baseValue + 0x008421C8
    process.writeBytes(key, setVal, 1)

def printRNG36():
    global baseValue

    coord = baseValue + 0x00D35F68
    retVal = process.readBytes(coord, 1)
    print("--------------------------------------------")
    print("--------------------------------------------")
    print("RNG36 value: ",retVal)
    print("--------------------------------------------")
    print("--------------------------------------------")

def end():
    global process
    process.close()
    print("Memory reading process is now closed.")

def getFrameCount():
    global baseValue
    key = baseValue + 0x0088FDD8
    return process.readBytes(key, 4)

def nameAeonReady():
    global baseValue
    key = baseValue + 0x0146A22C
    return process.readBytes(key, 1)

def clearNameAeonReady():
    global baseValue
    key = baseValue + 0x0146A22C
    process.writeBytes(key, 0, 1)
    

#-------------------------------------------------------
#Egg hunt section


def eggX(eggNum):
    global process
    global baseValue
    eggNum += 23
    basePointer = baseValue + 0x1FC44E4
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + (0x880 * eggNum) + 0x0C
    retVal = float_from_integer(process.read(key))
    #print("Egg ", eggNum," X value: ", retVal)
    return retVal

def eggY(eggNum):
    global process
    global baseValue
    eggNum += 23
    basePointer = baseValue + 0x1FC44E4
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + (0x880 * eggNum) + 0x14
    retVal = float_from_integer(process.read(key))
    #print("Egg ", eggNum," Y value: ", retVal)
    return retVal

def getEggDistance(eggNum):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C4CC + (0x40 * eggNum)
    retVal = float_from_integer(process.read(key))
    return retVal

def getEggLife(eggNum):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C4CC + (0x40 * eggNum) + 4
    retVal = process.readBytes(key,1)
    return retVal

def getEggPicked(eggNum):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C4CC + (0x40 * eggNum) + 5
    retVal = process.readBytes(key,1)
    return retVal

class egg:
    def __init__(self, eggnum):
        self.num = eggnum
        self.x = eggX(self.num)
        self.y = eggY(self.num)
        self.distance = getEggDistance(self.num)
        self.eggLife = getEggLife(eggnum)
        self.eggPicked = getEggPicked(eggnum)

        if self.distance != 0 and self.eggPicked == 0:
            self.isActive = True
        else:
            self.isActive = False

        if self.eggPicked == 1:
            self.goForEgg = False
        elif self.eggLife > 100 and self.distance > 100:
            self.goForEgg = False
        elif self.distance > 250:
            self.goForEgg = False
        elif self.distance == 0:
            self.goForEgg = False
        else:
            self.goForEgg = True

    def reportVars(self):
        varArray = [self.num, self.isActive, self.x, self.y, 150 - self.eggLife, self.eggPicked, self.distance]
        print("Egg_num, Is_Active, X, Y, Egg Life, Picked up, distance")
        print(varArray)

def buildEggs():
    retArray = [0,0,0,0,0,0,0,0,0,0]
    for x in range(10):
        retArray[x] = egg(x)
    return retArray

def iceX(actor):
    global process
    global baseValue
    offset = actor + 7 #Icicle 0 is actor 7 in the array, incremented for each additional icicle.
    
    basePointer = baseValue + 0x1fc44e4
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + (0x880 * offset) + 0x0C
    retVal = float_from_integer(process.read(key))
    return retVal


def iceY(actor):
    global process
    global baseValue
    offset = actor + 7 #Icicle 0 is actor 7 in the array, incremented for each additional icicle.
    
    basePointer = baseValue + 0x1fc44e4
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + (0x880 * offset) + 0x14
    retVal = float_from_integer(process.read(key))
    return retVal

def getIceDistance(iceNum):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C0CC + (0x40 * iceNum)
    retVal = float_from_integer(process.read(key))
    return retVal

def getIceLife(iceNum):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C0CC + (0x40 * iceNum) + 4
    retVal = process.readBytes(key,1)
    return retVal


class icicle:
    def __init__(self, icenum):
        self.num = icenum
        self.x = iceX(self.num)
        self.y = iceY(self.num)
        #self.distance = getIceDistance(self.num)
        #self.iceLife = getEggLife(icenum)
        #self.eggPicked = getEggPicked(icenum)
        
        #if self.distance != 0: #Either we're in battle or the icicle is not active.
        #    self.isActive = True
        #else:
        #    self.isActive = False
        self.isActive = True

    def reportVars(self):
        varArray = [self.num, self.x, self.y]
        print("Ice_num, X, Y")
        print(varArray)

def buildIcicles():
    retArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for x in range(16):
        retArray[x] = icicle(x)
    return retArray


#-------------------------------------------------------
#Soft reset section

def setMapReset():
    global baseValue

    key = baseValue + 0x00D2CA90
    process.writeBytes(key, 23, 2)

def forceMapLoad():
    global baseValue

    key = baseValue + 0x00F3080C
    process.writeBytes(key, 1, 1)

def resetBattleEnd():
    global baseValue
    key = baseValue + 0x00D2C9F1
    process.writeBytes(key,3,1)

#---------------------------------------------
#Blitzball!

class blitzActor:
    def __init__(self, playerNum):
        self.num = playerNum + 2
        self.position = getActorCoords(self.num - 2)
        #print(self.position)
        self.distance = 0
    
    def updateCoords(self, activePlayer=12):
        self.position = getActorCoords(self.num)
        #if activePlayer != 12 and activePlayer != self.num:
            #actPos = getActorCoords(activePlayer-2)
            #self.distance = abs(self.position[0] - actPos[0]) + abs(self.position[1] - actPos[1])
        #else:
        self.distance = 100
    
    def getCoords(self):
        #print(self.num - 2)
        coords = getActorCoords(self.num - 2)
        #print(coords)
        return coords

def blitzOwnScore():
    global baseValue

    key = baseValue + 0x0151728C
    score = process.readBytes(key, 1)
    return score

def blitzOppScore():
    global baseValue

    key = baseValue + 0x0151644C
    score = process.readBytes(key, 1)
    return score

def blitzballPatriotsStyle():
    global baseValue

    key = baseValue + 0x00D2E0CE
    progress = process.writeBytes(key,50,1)

def blitzClockMenu():
    global baseValue

    key = baseValue + 0x014765FA
    status = process.readBytes(key, 1)
    return status

def blitzClockPause():
    global baseValue

    key = baseValue + 0x014663B0
    status = process.readBytes(key, 1)
    return status

def blitzMenuNum():
    global baseValue
    #20 = Movement menu (auto, type A, or type B)
    #29 = Formation menu
    #38 = Breakthrough
    #24 = Pass To menu (other variations are set to 24)
    #Unsure about other variations, would take more testing.

    key = baseValue + 0x014765DA
    status = process.readBytes(key, 1)
    if status == 17 or status == 27:
        status = 24
    return status

def blitzCurrentPlayer():
    global baseValue

    key = baseValue + 0x00F25B6A
    player = process.readBytes(key, 1)
    #print("Target Player number: ", player)
    #print("12 = Opposing team")
    #print("18 = non-controlled ball (shot or pass)")
    return player

def blitzTargetPlayer():
    global baseValue

    key = baseValue + 0x00D3761C
    player = process.readBytes(key, 1)
    #print("Target Player number: ", player)
    #print("12 = Opposing team")
    #print("18 = non-controlled ball (shot or pass)")
    return player

def blitzCoords():
    global baseValue

    key = baseValue + 0x00D37698
    xVal = process.readBytes(key, 1)
    xVal = xVal * -1
    key = baseValue + 0x00D37690
    yVal = process.readBytes(key, 1)
    return [xVal,yVal]

def blitzGameActive():
    if getMap() == 62:
        return True
    else:
        return False

def blitzBallControl():
    try:
        if blitzClockMenu() == 24:
            if blitzCurrPlayer() >= 2 and blitzCurrPlayer <= 6:
                return True
            else:
                return False
        else:
            return False
    except:
        return False

def blitzClock():
    global baseValue
    
    basePointer = baseValue + 0x00F2FF14
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x24C
    clockValue = process.read(key)
    return clockValue

def blitzCharSelectCursor():
    global baseValue

    key = baseValue + 0x0146780A
    cursor = process.readBytes(key, 1)
    return cursor

def blitzProceedCursor():
    global baseValue

    key = baseValue + 0x01467CEA
    cursor = process.readBytes(key, 1)
    return cursor

def blitzCursor():
    global baseValue

    key = baseValue + 0x014676D2
    cursor = process.readBytes(key, 1)
    return cursor

#-------------------------------------------------------
#Function for logging
def readBytes(key,size):
    return process.readBytes(key,size)
    

#-------------------------------------------------------
#Equipment array

#0x0 - ushort - name/group (?)
#0x3 - byte - wpn./arm. state
#0x4 - byte - owner char (basis for field below)
#0x5 - byte - equip type idx. (0 = cur. chara wpn., 1 = cur. chara arm., 2 = next chara wpn., etc.)
#0x6 - byte - equip icon shown? (purely visual- a character will still keep it equipped if his stat struct says so)
#0x8 - byte - atk. type
#0x9 - byte - dmg. constant
#0xA - byte - base crit rate (armor has one too!!!)
#0xB - byte - slot count (cannot be < abi count, game won't let you)
#0xC - ushort - wpn./arm. model (?)
#0xE - ushort - auto-ability 1
#0x10 - ushort - auto-ability 2
#0x12 - ushort - auto-ability 3
#0x14 - ushort - auto-ability 4

def getEquipType(equipNum):
    global baseValue
    
    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) +0x05
    retVal = process.readBytes(key,1)
    return retVal

def getEquipOwner(equipNum):
    global baseValue
    
    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) +0x04
    retVal = process.readBytes(key,1)
    return retVal

def getEquipSlotCount(equipNum):
    global baseValue
    
    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) +0x0B
    retVal = process.readBytes(key,1)
    return retVal

def getEquipCurrentlyEquipped(equipNum):
    global baseValue
    
    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) +0x06
    retVal = process.readBytes(key,1)
    return retVal

def getEquipAbilities(equipNum):
    global baseValue
    retVal = [255,255,255,255]
    
    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) +0x0E
    retVal[0] = process.readBytes(key,2)
    key = basePointer + (0x16 * equipNum) +0x10
    retVal[1] = process.readBytes(key,2)
    key = basePointer + (0x16 * equipNum) +0x12
    retVal[2] = process.readBytes(key,2)
    key = basePointer + (0x16 * equipNum) +0x14
    retVal[3] = process.readBytes(key,2)
    return retVal

def getEquipExists(equipNum):
    global baseValue
    
    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) +0x0B
    retVal = process.readBytes(key,1)
    return retVal
    
class equipment:
    def __init__(self, equipNum):
        self.num = equipNum
        self.equipType = getEquipType(equipNum)
        self.equipOwner = getEquipOwner(equipNum)
        self.equipAbilities = getEquipAbilities(equipNum)
        self.isEquipped = getEquipCurrentlyEquipped(equipNum)
    
    def equipmentType(self):
        return self.equipType
    
    def owner(self):
        return self.equipOwner
    
    def abilities(self):
        return self.equipAbilities
    
    def hasAbility(self, abilityNum):
        for i in range(4):
            if self.equipAbilities[i] == abilityNum:
                return True
        return False
        
    def isEquipped(self):
        return self.isEquipped

def allEquipment():
    firstEquipment = True
    for i in range(200):
        if getEquipExists(i):
            if firstEquipment:
                equipHandleArray = [equipment(i)]
                firstEquipment = False
            else:
                equipHandleArray.append(equipment(i))
    
    return equipHandleArray

def weaponArrayCharacter(charNum):
    equipHandles = allEquipment()
    print("####")
    print(equipHandles)
    print("####")
    firstEquipment = True
    while len(equipHandles) > 0:
        print(len(equipHandles))
        currentHandle = equipHandles.pop(0)
        print("Owner: ", currentHandle.owner())
        if currentHandle.owner() == charNum and currentHandle.equipmentType() == 0:
            if firstEquipment:
                charWeaps = [currentHandle]
            else:
                charWeaps.append(currentHandle)
    return charWeaps

def armorArrayCharacter(charNum):
    equipHandles = allEquipment()
    firstEquipment = True
    for i in len(equipHandles):
        if equipHandles[i].owner() == charNum and equipHandles[i].equipmentType() == 1:
            if firstEquipment:
                charWeaps = [equipHandles[i]]
            else:
                charWeaps.append(equipHandles[i])
    return charWeaps

def equipWeapCursor():
    global baseValue
    
    key = baseValue + 0x01440A38
    retVal = process.readBytes(key,1)
    return retVal

#-------------------------------------------------------
#Testing

def memTestVal0():
    key = baseValue + 0x00D35EE0
    return process.readBytes(key, 1)
def memTestVal1():
    key = baseValue + 0x00D35EE1
    return process.readBytes(key, 1)
def memTestVal2():
    key = baseValue + 0x00D35EE2
    return process.readBytes(key, 1)
def memTestVal3():
    key = baseValue + 0x00D35EE3
    return process.readBytes(key, 1)