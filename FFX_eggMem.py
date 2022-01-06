import FFX_memory
global process
global baseValue

def float_from_integer(integer):
    return struct.unpack('!f', struct.pack('!I', integer))[0]

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

def clickToControl():
    waitCounter = 0
    print("Awaiting control (clicking)")
    while not userControl():
        FFXC.set_value('BtnB', 1)
        time.sleep(0.04)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.04)
        waitCounter += 1
        if waitCounter % 100 == 0:
            print("Awaiting control - ", waitCounter / 100)
    time.sleep(0.05)
    return True

def getCoords():
    global process
    global baseValue
    #Auto updating via reference to the baseValue above
    global xPtr
    global yPtr
    global coordsCounter
    coordsCounter += 1
    xPtr = baseValue + 0x0084DED0
    yPtr = baseValue + 0x0084DED8
    #xPtr = 0x012DDED0
    #yPtr = 0x012DDED8
    coord1 = process.get_pointer(xPtr)
    x = float_from_integer(process.read(coord1))
    coord2 = process.get_pointer(yPtr)
    y = float_from_integer(process.read(coord2))
    #if [x,y] != [0.0,0.0]:
        #if coordsCounter % 1000 == 99:
            #print("Coordinates check: ")
            #print(str(x).format(24), " | ",str(y).format(24))
            #xPtr = baseValue + 0x0084DED0
    
    return [x,y]

def getCamera():
    global baseValue
    angle = baseValue + 0x008A86B8
    z = baseValue + 0x008A86FC
    x = baseValue + 0x008A86F8
    y = baseValue + 0x008A8700
    
    key = process.get_pointer(angle)
    angleVal = round(float_from_integer(process.read(key)),2)
    key = process.get_pointer(x)
    xVal = round(float_from_integer(process.read(key)),2)
    key = process.get_pointer(y)
    yVal = round(float_from_integer(process.read(key)),2)
    key = process.get_pointer(z)
    zVal = round(float_from_integer(process.read(key)),2)
    
    retVal = [angleVal,xVal,yVal,zVal]
    #print("Camera details: ", retVal)
    return retVal

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
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    while not userControl(): #Get out of combat or whatever
        FFX_Xbox.menuB()
    while userControl() and not menuOpen():
        FFXC.set_value('BtnY',1)
        time.sleep(0.035)
        FFXC.set_value('BtnY',0)
        time.sleep(0.035)
    time.sleep(0.7)