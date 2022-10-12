from math import cos, sin
from collections import Counter
import logs
import struct
import xbox
import targetPathing
import vars
import os.path
import ctypes
import ctypes.wintypes
from ReadWriteMemory import ReadWriteMemory
from ReadWriteMemory import Process
import time
gameVars = vars.varsHandle()

# Process Permissions
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020

MAX_PATH = 260

baseValue = 0


class LocProcess(Process):
    def __init__(self, *args, **kwargs):
        super(LocProcess, self).__init__(*args, **kwargs)

    def readBytes(self, lp_base_address: int, size: int = 4):
        """
        See the original ReadWriteMemory values for details on how this works. This version allows us to pass
        the number of bytes to be retrieved instead of a static 4-byte size. Default is 4 for reverse-compatibility
        """
        try:
            read_buffer = ctypes.c_uint()
            lp_buffer = ctypes.byref(read_buffer)
            n_size = ctypes.sizeof(read_buffer)
            lp_number_of_bytes_read = ctypes.c_ulong(0)
            ctypes.windll.kernel32.ReadProcessMemory(self.handle, lp_base_address, lp_buffer,
                                                     size, lp_number_of_bytes_read)
            return read_buffer.value
        except (BufferError, ValueError, TypeError) as error:
            if self.handle:
                self.close()
            self.error_code = self.get_last_error()
            error = {'msg': str(error), 'Handle': self.handle, 'PID': self.pid,
                     'Name': self.name, 'ErrorCode': self.error_code}
            ReadWriteMemoryError(error)

    def writeBytes(self, lp_base_address: int, value: int, size: int = 4) -> bool:
        """
        Same as above, write a passed number of bytes instead of static 4 bytes. Default is 4 for reverse-compatibility
        """
        try:
            write_buffer = ctypes.c_uint(value)
            lp_buffer = ctypes.byref(write_buffer)
            n_size = ctypes.sizeof(write_buffer)
            lp_number_of_bytes_written = ctypes.c_ulong(0)
            ctypes.windll.kernel32.WriteProcessMemory(self.handle, lp_base_address, lp_buffer,
                                                      size, lp_number_of_bytes_written)
            return True
        except (BufferError, ValueError, TypeError) as error:
            if self.handle:
                self.close()
            self.error_code = self.get_last_error()
            error = {'msg': str(error), 'Handle': self.handle, 'PID': self.pid,
                     'Name': self.name, 'ErrorCode': self.error_code}
            ReadWriteMemoryError(error)


class FFXMemory(ReadWriteMemory):
    def __init__(self, *args, **kwargs):
        super(FFXMemory, self).__init__(*args, **kwargs)
        self.process = LocProcess()

    def get_process_by_name(self, process_name: str | bytes) -> "Process":
        """
        :description: Get the process by the process executabe\'s name and return a Process object.

        :param process_name: The name of the executable file for the specified process for example, my_program.exe.

        :return: A Process object containing the information from the requested Process.
        """
        if not process_name.endswith('.exe'):
            self.process.name = process_name + '.exe'

        process_ids = self.enumerate_processes()

        for process_id in process_ids:
            self.process.handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, process_id)
            if self.process.handle:
                image_file_name = (ctypes.c_char * MAX_PATH)()
                if ctypes.windll.psapi.GetProcessImageFileNameA(self.process.handle, image_file_name, MAX_PATH) > 0:
                    filename = os.path.basename(image_file_name.value)
                    if filename.decode('utf-8') == process_name:
                        self.process.pid = process_id
                        self.process.name = process_name
                        return self.process
                self.process.close()

        raise ReadWriteMemoryError(f'Process "{self.process.name}" not found!')


def start():
    global process
    global xPtr
    global yPtr
    global coordsCounter
    coordsCounter = 0
    success = False

    # rwm = ReadWriteMemory()
    rwm = FFXMemory()
    print("#############")
    print(type(rwm))
    process = rwm.get_process_by_name('FFX.exe')
    print("#############")
    print(type(process))
    print("#############")
    process.open()

    global baseValue
    try:
        import zz_rootMem
        print("Process Modules:")
        baseValue = zz_rootMem.ListProcessModules(process.pid)
        print("Process Modules complete")
        print("Dynamically determined memory address:", hex(baseValue))
        success = True
    except Exception as errCode:
        print("Could not get memory address dynamically. ", errCode)
        baseValue = 0x00FF0000
        time.sleep(10)
    return success


def float_from_integer(integer):
    return struct.unpack('!f', struct.pack('!I', integer))[0]


def getCutsceneID():
    global baseValue
    key = baseValue + 0xD27C88
    cutscene_alt = process.readBytes(key, 4)
    storyline_prog = getStoryProgress()
    dialogue = diagProgressFlag()
    return (cutscene_alt, storyline_prog, dialogue)


def waitFrames(frames: int):
    frames = max(round(frames), 1)
    global baseValue
    key = baseValue + 0x0088FDD8
    current = process.readBytes(key, 4)
    final = current + frames
    previous = current - 1
    while current < final:
        if not (current == previous or current == previous + 1):
            final = final - previous
        previous = current
        current = process.readBytes(key, 4)
    return


def rngSeed():
    if int(gameVars.confirmedSeed()) == 999:
        global baseValue
        key = baseValue + 0x003988a5
        return process.readBytes(key, 1)
    return int(gameVars.confirmedSeed())


def setRngSeed(value):
    global baseValue
    key = baseValue + 0x003988a5
    print("+++++++++++++++++")
    print(type(process))
    print("+++++++++++++++++")
    return process.writeBytes(key, value, 1)


def gameOver():
    global baseValue
    key = baseValue + 0x00D2C9F1
    if process.readBytes(key, 1) == 1:
        return True
    else:
        return False


def battleComplete():
    global baseValue
    key = baseValue + 0x00D2C9F1
    if process.readBytes(key, 1) == 2:
        return True
    elif process.readBytes(key, 1) == 3:
        return True
    else:
        return False


def battleArenaResults():
    global baseValue
    if process.readBytes(baseValue + 0x00D2C9F1, 1) == 2:
        return True
    return False


def gameOverReset():
    global baseValue
    key = baseValue + 0x00D2C9F1
    process.writeBytes(key, 0, 1)


def battleActive():
    global baseValue
    key = baseValue + 0x00D2C9F1
    return process.readBytes(key, 1) == 0


def getCurrentTurn():
    global baseValue
    key = baseValue + 0x00D2AA00
    return process.readBytes(key, 1)


def getNextTurn():
    global baseValue
    key = baseValue + 0x00D2AA04
    return process.readBytes(key, 1)


def battleMenuCursor():
    global baseValue
    if not turnReady():
        return 255
    key2 = baseValue + 0x00F3C926
    return process.readBytes(key2, 1)


def battleScreen():
    if mainBattleMenu():
        global baseValue
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
    if process.readBytes(key, 1) == 0:
        return False
    else:
        while not mainBattleMenu():
            pass
        waitFrames(1)
        if gameVars.usePause():
            waitFrames(2)
        return True


def battleCursor2():
    global baseValue
    key = baseValue + 0x00F3CA01
    if process.readBytes(key, 1) != 0:
        key = baseValue + 0x00F3CA0E
        return process.readBytes(key, 1)
    else:
        return 255


def battleCursor3():
    global baseValue
    key = baseValue + 0x00F3CAFE
    return process.readBytes(key, 1)


def overdriveMenuActive():
    global baseValue
    key = baseValue + 0x00F3D6F4
    return process.readBytes(key, 1) == 4


def overdriveMenuActiveWakka():
    global baseValue
    key = baseValue + 0x00DA0BD0
    return process.readBytes(key, 1)


def auronOverdriveActive():
    global baseValue
    key = baseValue + 0x00F3D6B4
    return process.readBytes(key, 1) == 4


def mainBattleMenu():
    global baseValue
    key = baseValue + 0x00F3C911
    if process.readBytes(key, 1) > 0:
        return True
    else:
        return False


def otherBattleMenu():
    global baseValue
    key = baseValue + 0x00F3CA01
    if process.readBytes(key, 1) > 0:
        return True
    else:
        return False


def interiorBattleMenu():
    global baseValue
    key = baseValue + 0x00F3CAF1
    return process.readBytes(key, 1)


def superInteriorBattleMenu():
    global baseValue
    key = baseValue + 0x00F3CBE1
    return process.readBytes(key, 1)


def battleTargetId():
    global baseValue
    key = baseValue + 0x00F3D1B4
    retVal = process.readBytes(key, 1)
    print("Battle Target ID:", retVal)
    return retVal


def battleLineTarget():
    return readVal(0x00F3CA42)


def enemyTargetted():
    return readVal(0x00F3D1C0)


def battleTargetActive():
    global baseValue
    key = baseValue + 0x00F3D1B4
    retVal = process.readBytes(key, 1)
    print("Battle Target ID:", retVal)
    return retVal != 255


def userControl():
    global baseValue
    # Auto updating via reference to the baseValue above
    controlStruct = baseValue + 0x00f00740
    inControl = process.read(controlStruct)

    if inControl == 0:
        return False
    else:
        return True


def awaitControl():
    waitCounter = 0
    print("Awaiting control (no clicking)")
    while not userControl():
        waitCounter += 1
        if waitCounter % 10000000 == 0:
            print("Awaiting control -", waitCounter / 100000)
    waitFrames(1)
    return True


def clickToControl():
    waitCounter = 0
    print("Awaiting control (clicking)")
    while not userControl():
        xbox.tapB()
        waitCounter += 1
        if waitCounter % 1000 == 0:
            print("Awaiting control -", waitCounter / 1000)
    print("Control restored.")
    return True


def clickToControl2():
    waitCounter = 0
    print("Awaiting control (clicking)")
    while not userControl():
        xbox.tapB()
        waitCounter += 1
        if waitCounter % 1000 == 0:
            print("Awaiting control -", waitCounter / 1000)
    return True


def clickToControl3():
    waitCounter = 0
    print("Awaiting control (clicking only when appropriate - dialog)")
    waitFrames(6)
    while not userControl():
        if battleActive():
            while battleActive():
                xbox.tapB()
        if diagSkipPossible():
            xbox.tapB()
        elif menuOpen():
            print("Post-battle menu open")
            xbox.tapB()
        else:
            pass
        waitCounter += 1
        if waitCounter % 10000 == 0:
            print("Awaiting control -", waitCounter / 10000)
    print("User control restored.")
    return True


def clickToControlSpecial():
    FFXC = xbox.controllerHandle()
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
        if waitCounter % 10000 == 0:
            print("Awaiting control -", waitCounter / 10000)
    waitFrames(30 * 0.05)
    return True


def clickToEvent():
    FFXC = xbox.controllerHandle()
    while userControl():
        FFXC.set_value('BtnB', 1)
        if gameVars.usePause():
            waitFrames(2)
        else:
            waitFrames(1)
        FFXC.set_value('BtnB', 0)
        if gameVars.usePause():
            waitFrames(3)
        else:
            waitFrames(1)
    waitFrames(6)


def clickToEventTemple(direction):
    FFXC = xbox.controllerHandle()
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
        xbox.tapB()
    FFXC.set_neutral()
    waitFrames(30 * 0.2)
    while not userControl():
        clickToControl3()
        waitFrames(30 * 0.035)


def awaitEvent():
    waitFrames(1)
    while userControl():
        pass


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

    return [x, y]


def ammesFix(actorIndex: int = 0):
    global process
    global baseValue
    basePtr = baseValue + 0x1fc44e4
    baseAddr = process.read(basePtr)
    #xCoord = 749, yCoord = -71
    process.write(baseAddr + (0x880 * actorIndex) + 0x0c, 0x443B4000)
    process.write(baseAddr + (0x880 * actorIndex) + 0x14, 0xC28E0000)

def chocoEaterFun(actorIndex: int = 0):
    global process
    global baseValue
    basePtr = baseValue + 0x1fc44e4
    baseAddr = process.read(basePtr)
    process.write(baseAddr + (0x880 * actorIndex) + 0x14, 0xc4bb8000)

def extractorHeight():
    global process
    global baseValue
    height = getActorCoords(3)[2]
    print("^^Extractor Height:", height)
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
    angleVal = round(float_from_integer(process.read(key)), 2)
    key = process.get_pointer(x)
    xVal = round(float_from_integer(process.read(key)), 2)
    key = process.get_pointer(y)
    yVal = round(float_from_integer(process.read(key)), 2)
    key = process.get_pointer(z)
    zVal = round(float_from_integer(process.read(key)), 2)
    key = process.get_pointer(angle2)
    angleVal2 = round(float_from_integer(process.read(key)), 2)

    retVal = [angleVal, xVal, yVal, zVal, angleVal2]
    return retVal


def getHP():
    global baseValue
    # Out of combat HP only

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
    # Out of combat HP only

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


def getTidusMP():
    global baseValue
    retVal = process.read(baseValue + 0xD3207C)
    return retVal


def getYunaMP():
    global baseValue
    retVal = process.read(baseValue + 0xD32110)
    return retVal


def getOrder():
    global baseValue
    # Out of combat HP only

    coord = baseValue + 0x00D307E8
    pos1 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307E9
    pos2 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EA
    pos3 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EB
    pos4 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EC
    pos5 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307ED
    pos6 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EE
    pos7 = process.readBytes(coord, 1)

    formation = [255, pos1, pos2, pos3, pos4, pos5, pos6, pos7]
    print("Party formation:", formation)
    return formation


def getOrderSix():
    global baseValue
    # Out of combat HP only

    coord = baseValue + 0x00D307E8
    pos1 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307E9
    pos2 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EA
    pos3 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EB
    pos4 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EC
    pos5 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307ED
    pos6 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EE
    pos7 = process.readBytes(coord, 1)

    formation = [pos1, pos2, pos3, pos4, pos5, pos6, pos7]
    print(formation)
    while 255 in formation:
        formation.remove(255)
    return formation


def getOrderSeven():
    global baseValue
    # Out of combat HP only

    coord = baseValue + 0x00D307E8
    pos1 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307E9
    pos2 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EA
    pos3 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EB
    pos4 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EC
    pos5 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307ED
    pos6 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EE
    pos7 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EF
    pos8 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307F0
    pos9 = process.readBytes(coord, 1)

    formation = [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9]
    while 255 in formation:
        formation.remove(255)
    return formation


def getCharFormationSlot(charNum):
    allSlots = getOrderSeven()
    x = 0
    while x < len(allSlots):
        if allSlots[x] == charNum:
            return x
        else:
            x += 1
    return 255  # Character is not in the party


def getPhoenix():
    global baseValue

    key = getItemSlot(6)
    pDowns = getItemCountSlot(key)
    print("Phoenix Down count:", pDowns)
    return pDowns


def getPower():
    global baseValue

    key = getItemSlot(70)
    power = getItemCountSlot(key)
    print("Power spheres:", power)
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
    print("Speed spheres:", speed)
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
    hpArray = [hp1, hp2, hp3]
    return hpArray


def getEncounterID():
    global baseValue

    key = baseValue + 0x00D2A8EC
    formation = process.read(key)

    return formation


def clearEncounterID():
    global baseValue

    key = baseValue + 0x00D2A8EC
    process.write(key, 0)


def getActiveBattleFormation():
    global baseValue

    key = baseValue + 0x00F3F76C
    char1 = process.readBytes(key, 1)
    key = baseValue + 0x00F3F76E
    char2 = process.readBytes(key, 1)
    key = baseValue + 0x00F3F770
    char3 = process.readBytes(key, 1)

    battleForm = [char1, char2, char3]
    return battleForm


def getBattleFormation():
    global baseValue

    key = baseValue + 0x00F3F76C
    char1 = process.readBytes(key, 1)
    key = baseValue + 0x00F3F76E
    char2 = process.readBytes(key, 1)
    key = baseValue + 0x00F3F770
    char3 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A3
    char4 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A4
    char5 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A5
    char6 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A6
    char7 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A7
    char8 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A8
    char9 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A9
    char10 = process.readBytes(key, 1)

    battleForm = [char4, char5, char6, char7, char8, char9, char10]
    print(battleForm)
    if 255 in battleForm:
        while 255 in battleForm:
            battleForm.remove(255)
    battleForm.insert(0, char3)
    battleForm.insert(0, char2)
    battleForm.insert(0, char1)
    print(battleForm)
    return battleForm


def getBattleCharSlot(charNum) -> int:
    battleForm = getBattleFormation()
    if charNum not in battleForm:
        return 255
    try:
        if battleForm[0] == charNum:
            return 0
        if battleForm[1] == charNum:
            return 1
        if battleForm[2] == charNum:
            return 2
        if battleForm[3] == charNum:
            return 3
        if battleForm[4] == charNum:
            return 4
        if battleForm[5] == charNum:
            return 5
        if battleForm[6] == charNum:
            return 6
    except Exception:
        return 255


def getBattleCharTurn():
    global baseValue

    key = baseValue + 0x00D36A68
    battleCharacter = process.read(key)
    return battleCharacter


def getSLVLYuna():
    global baseValue
    # Out of combat HP only

    coord = baseValue + 0x00D32104
    return process.read(coord)


def getSLVLKim():
    global baseValue
    # Out of combat HP only

    coord = baseValue + 0x00D3222C
    return process.read(coord)


def getSLVLWakka():
    global baseValue
    # Out of combat HP only

    key = baseValue + 0x00D322E7
    sLvl = process.readBytes(key, 1)
    print("Wakka current Slvl", sLvl)
    return sLvl


def itemAddress(num):
    global baseValue
    return baseValue + 0x00D3095C + (num * 0x2)


def getItemsOrder():
    items = []
    for x in range(100):
        items.append(process.readBytes(itemAddress(x), 1))
    return items


def getUseItemsOrder():
    itemArray = getItemsOrder()
    x = 0
    while x < len(itemArray):
        try:
            if itemArray[x] == 20:
                ignoreThisValue = True
                x += 1
            elif itemArray[x] < 23:
                del itemArray[x]
            elif itemArray[x] > 69:
                del itemArray[x]
            else:
                x += 1
        except Exception as y:
            print(y)
            retryThisValue = True
            print("Retrying value")
    return itemArray


def getUseItemsSlot(itemNum):
    items = getUseItemsOrder()
    x = 0
    for x in range(len(items)):
        print(items[x], "|", itemNum, "|", x)
        if items[x] == itemNum:
            return x
        x += 1
    return 255


def getThrowItemsOrder():
    itemArray = getItemsOrder()
    print(itemArray)
    x = 0
    while x < len(itemArray):
        try:
            if itemArray[x] > 18:
                itemArray.remove(itemArray[x])
            else:
                x += 1
        except Exception as y:
            print(y)
            retryThisValue = True
            print("Retrying value")
    print(itemArray)
    return itemArray


def getThrowItemsSlot(itemNum):
    items = getThrowItemsOrder()
    x = 0
    while x < len(items):
        if items[x] == itemNum:
            print("Desired item", itemNum, "is in slot", x)
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
        except Exception as y:
            print(y)
            retryThisValue = True
            print("Retrying value")
    return itemArray


def getGridItemsSlot(itemNum) -> int:
    items = getGridItemsOrder()
    x = 0
    while x < len(items):
        if items[x] == itemNum:
            print("Desired item", itemNum, "is in slot", x)
            return x
        x += 1
    return 255


def getGridCursorPos():
    global baseValue
    key = baseValue + 0x012ACB78
    return process.readBytes(key, 1)


def getGridMoveUsePos():
    global baseValue
    key = baseValue + 0x012AC838
    return process.readBytes(key, 1)


def getGridMoveActive():
    global baseValue
    key = baseValue + 0x012AC82B
    if process.readBytes(key, 1):
        return True
    else:
        return False


def getGridUseActive():
    global baseValue
    key = baseValue + 0x012ACB6B
    if process.readBytes(key, 1):
        return True
    else:
        return False


def getItemSlot(itemNum):
    items = getItemsOrder()
    for x in range(len(items)):
        if items[x] == itemNum:
            return (x)
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

    # Set MaxSpot to one more than the last undesirable item
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
    print("Returning values:", retVal)
    return retVal


def itemCountAddr(num):
    return 0x00D30B5C + num


def getItemsCount():
    global baseValue
    itemCounts = []
    for x in range(60):
        itemCounts.append(process.readBytes(baseValue + 0x00D30B5C + x, 1))
    return itemCounts


def getItemCountSlot(itemSlot) -> int:
    global baseValue
    return process.readBytes(baseValue + 0x00D30B5C + itemSlot, 1)


def getMenuDisplayCharacters():
    base = 0x01441BD4
    characters = []
    for cur in range(7):
        char = readVal(base + cur)
        print(cur, char)
        characters.append(char)
    print(characters)
    return characters


def getGilvalue():
    global baseValue
    key = baseValue + 0x00D307D8
    return process.read(key)


def setGilvalue(newValue):
    global baseValue
    key = baseValue + 0x00D307D8
    return process.write(key, newValue)


def setStory(newValue):
    global baseValue
    key = baseValue + 0x00D2D67C
    return process.writeBytes(key, newValue, 2)


def RikkuODCursor1():
    global baseValue
    key = baseValue + 0x00F3CB32
    return process.readBytes(key, 1)


def RikkuODCursor2():
    return RikkuODCursor1()


def getOverdriveBattle(character):
    global process
    global baseValue

    basePointer = baseValue + 0x00d334cc
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x5bc
    retVal = process.readBytes(basePointerAddress + offset, 1)
    print("In-Battle Overdrive values:\n", retVal)
    return retVal


def getCharWeakness(character):
    global process
    global baseValue

    basePointer = baseValue + 0x00d334cc
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x5dd
    retVal = process.readBytes(basePointerAddress + offset, 1)
    print("In-Battle Overdrive values:\n", retVal)
    return retVal


def tidusEscapedState():
    global baseValue

    basePointer = baseValue + 0x00D334CC
    basePointerAddress = process.read(basePointer)
    offset = 0xDC8
    retVal = not process.readBytes(basePointerAddress + offset, 1)
    print("Tidus Escaped State:", retVal)
    return retVal


def deadstate(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x606

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 2 == 1:
        return True
    else:
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
        return True
    else:
        return False


def petrifiedstate(character):
    if character not in getActiveBattleFormation():
        return False

    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x606

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 8 >= 4:
        return True
    else:
        return False


def confusedState(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x607

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 2 == 1:
        print("Character %d is confused" % character)
        return True
    else:
        print("Character %d is not confused" % character)
        return False

def sleepState(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x608

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal == 3:
        print("Character %d is asleep" % character)
        return True
    else:
        print("Character %d is not asleep" % character)
        return False

def autoLifeState(character: int = 0):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x617

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 4 >= 2:
        print("Character autolife is active", character)
        return True
    else:
        print("Character autolife is not active", character)
        return False


def confusedStateByPos(position):
    posArray = getBattleFormation()
    x = 0
    if position in posArray:
        if posArray[x] == position:
            return confusedState(posArray[x])
        else:
            x += 1


def battleType():
    # 0 is normal, 1 is pre-empt, 2 is ambushed
    return readVal(0x00D2C9DC)


def getEnemyCurrentHP():
    global process
    global baseValue
    enemyNum = 20
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)

    while enemyNum < 27:
        offset1 = (0xf90 * enemyNum) + 0x594
        key1 = basePointerAddress + offset1
        offset2 = (0xf90 * enemyNum) + 0x5D0
        key2 = basePointerAddress + offset2
        if enemyNum == 20:
            maxHP = [process.readBytes(key1, 4)]
            currentHP = [process.readBytes(key2, 4)]
        else:
            nextHP = process.readBytes(key1, 4)
            if nextHP != 0:
                maxHP.append(nextHP)
                currentHP.append(process.readBytes(key2, 4))
        enemyNum += 1
    print("Enemy HP current values:", currentHP)
    return currentHP


def getEnemyMaxHP():
    global process
    global baseValue
    enemyNum = 20
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)

    while enemyNum < 25:
        offset1 = (0xf90 * enemyNum) + 0x594
        key1 = basePointerAddress + offset1
        offset2 = (0xf90 * enemyNum) + 0x5D0
        key2 = basePointerAddress + offset2
        if enemyNum == 20:
            maxHP = [process.readBytes(key1, 4)]
            currentHP = [process.readBytes(key2, 4)]
        else:
            if maxHP != 0:
                maxHP.append(process.readBytes(key1, 4))
                currentHP.append(process.readBytes(key2, 4))
        enemyNum += 1
    print("Enemy HP max values:")
    print(maxHP)
    print("Enemy HP current values:")
    print(currentHP)
    return maxHP


def menuOpen():
    global baseValue

    key = baseValue + 0x00F407E4
    menuOpen = process.readBytes(key, 1)
    if menuOpen == 0:
        return False
    else:
        return True


def closeMenu():
    while menuOpen():
        xbox.tapA()


def saveMenuOpen():
    global baseValue

    key = baseValue + 0x008E7300
    menuOpen = process.readBytes(key, 1)
    if menuOpen == 1:
        return True
    else:
        return False


def backToMainMenu():
    gameVars = vars.varsHandle()
    while menuNumber() not in [1, 2, 3, 4, 5]:
        if menuOpen():
            xbox.tapA()
        else:
            xbox.tapY()
        if gameVars.usePause():
            waitFrames(6)


def openMenu():
    FFXC = xbox.controllerHandle()
    menuCounter = 0
    while not (userControl() and menuOpen() and menuNumber() == 5):
        if menuOpen() and not userControl():
            print("Post-Battle summary screen is open. Attempting close.", menuCounter)
            xbox.menuB()
        elif userControl() and not menuOpen():
            print("Menu is not open, attempting to open.", menuCounter)
            xbox.tapY()
            menuCounter += 1
        elif menuOpen() and userControl() and menuNumber() > 5:
            print("The wrong menu is open.", menuCounter)
            xbox.tapA()
            menuCounter += 1
        elif battleActive():
            print("Can't open menu during battle.", menuCounter)
            return False
        else:
            pass
    FFXC.set_neutral()
    print("Menu open returning")
    return True


def menuNumber():
    global baseValue
    return process.readBytes(baseValue + 0x85B2CC, 1)


def sGridActive():
    global baseValue

    key = baseValue + 0x0085B30C
    menuOpen = process.readBytes(key, 1)
    if menuOpen == 1:
        return True
    else:
        return False


def sGridMenu():
    global baseValue

    key = baseValue + 0x0012AD860
    menuOpen = process.readBytes(key, 1)
    return menuOpen


def sGridChar():
    global baseValue

    key = baseValue + 0x0012BEE2C
    character = process.readBytes(key, 1)
    return character


def sGridNodeSelected():
    global baseValue

    key = baseValue + 0x0012BEB7E
    nodeNumber = process.readBytes(key, 1)
    key = baseValue + 0x0012BEB7F
    nodeRegion = process.readBytes(key, 1)
    return [nodeNumber, nodeRegion]


def cursorLocation():
    global baseValue

    key = baseValue + 0x0021D09A4
    menu1 = process.readBytes(key, 1)
    key = baseValue + 0x0021D09A6
    menu2 = process.readBytes(key, 1)

    return [menu1, menu2]


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
    progress = process.readBytes(key, 2)
    return progress


def getMap():
    global baseValue

    key = baseValue + 0x00D2CA90
    progress = process.readBytes(key, 2)
    return progress


def touchingSaveSphere():
    global baseValue

    key = baseValue + 0x0021D09A6
    value = process.readBytes(key, 1)
    if value != 0:
        return True
    else:
        return False


def saveMenuCursor():
    global baseValue

    key = baseValue + 0x001467942
    return process.readBytes(key, 1)


def mapCursor():
    global baseValue
    basePointer = baseValue + 0x00F2FF14
    basePointerAddress = process.read(basePointer)
    print(basePointerAddress)
    ret = process.readBytes(basePointerAddress + 272, 1)
    print(ret)
    return ret


def clearSaveMenuCursor():
    global baseValue

    key = baseValue + 0x001467942
    return process.writeBytes(key, 0, 1)


def clearSaveMenuCursor2():
    global baseValue

    key = baseValue + 0x001468302
    return process.writeBytes(key, 0, 1)


def saveMenuCursor2():
    global baseValue

    key = baseValue + 0x001468302
    return process.readBytes(key, 1)


def NewGameCursor():
    global baseValue

    key = baseValue + 0x001467942
    value = process.readBytes(key, 1)
    return value


def targetingAlly():
    return readVal(0x00F3D1C0) == 0


def targetingEnemy():
    return not targetingAlly()


def getYunaSlvl():
    global baseValue

    key = baseValue + 0x00D3212B
    sLvl = process.readBytes(key, 1)
    return sLvl


def getTidusSlvl():
    global baseValue

    key = baseValue + 0x00D32097
    sLvl = process.readBytes(key, 1)
    return sLvl


def getKimahriSlvl():
    global baseValue

    key = baseValue + 0x00D32253
    sLvl = process.readBytes(key, 1)
    return sLvl


def getLuluSlvl():
    return readVal(0x00D3237B)


def getTidusXP():
    global baseValue

    key = baseValue + 0x00D32070
    Lvl = process.read(key)
    return Lvl


def setTidusSlvl(levels):
    global baseValue

    key = baseValue + 0x00D32097
    sLvl = process.writeBytes(key, levels, 1)
    return sLvl


def menuControl():
    global baseValue

    key = baseValue + 0x0085A03C
    control = process.readBytes(key, 1)
    if control == 1:
        return True
    else:
        return False


def diagSkipPossible_old():
    global baseValue

    key = baseValue + 0x0085A03C
    control = process.readBytes(key, 1)
    if control == 1:
        waitFrames(1)
        return True
    else:
        return False


def diagSkipPossible():
    global baseValue

    key = baseValue + 0x00F2FED0
    control = process.readBytes(key, 1)
    if control == 1:
        return True
    else:
        key = baseValue + 0x0085A03C
        control = process.readBytes(key, 1)
        if control == 1:
            return True
        else:
            return False


def cutsceneSkipPossible():
    global baseValue

    key = baseValue + 0x00D2A008
    control = process.readBytes(key, 1)
    if control == 1:
        return True
    else:
        return False


def specialTextOpen():
    global baseValue

    key = baseValue + 0x01466D30
    control = process.readBytes(key, 1)
    if control == 1:
        return True
    else:
        key = baseValue + 0x01476988
        control = process.readBytes(key, 1)
        if control == 1:
            return True
        else:
            return False


def awaitMenuControl():
    counter = 0
    while not menuControl():
        counter += 1
        if counter % 100000 == 0:
            print("Waiting for menu control.", counter)


def clickToStoryProgress(destination):
    FFXC = xbox.controllerHandle()
    counter = 0
    currentState = getStoryProgress()
    print("Story goal:", destination, "| Awaiting progress state:", currentState)
    while currentState < destination:
        if menuControl():
            FFXC.set_value('BtnB', 1)
            FFXC.set_value('BtnA', 1)
            waitFrames(1)
            FFXC.set_value('BtnB', 0)
            FFXC.set_value('BtnA', 0)
            waitFrames(1)
        if counter % 100000 == 0:
            print("Story goal:", destination, "| Awaiting progress state:",
                  currentState, "| counter:", counter / 100000)
        counter += 1
        currentState = getStoryProgress()
    print("Story progress has reached destination. Value:", destination)


def desertFormat(rikkuCharge):
    order = getOrderSix()
    if order == [0, 3, 2, 4, 6, 5]:
        print("Formation is fine, moving on.")
    elif not rikkuCharge:
        fullPartyFormat('desert1')
    else:
        fullPartyFormat('desert2')


def partySize():
    battleForm = getBattleFormation()
    if 255 in battleForm:
        while 255 in battleForm:
            battleForm.remove(255)
    return len(battleForm)


def activepartySize():
    battleForm = getActiveBattleFormation()
    if 255 in battleForm:
        while 255 in battleForm:
            battleForm.remove(255)
    return len(battleForm)


def getCharacterIndexInMainMenu(character):
    res = getMenuDisplayCharacters().index(character)
    print("Char is in position", res)
    return res


def fullPartyFormat(frontLine, *, fullMenuClose=True):
    gameVars = vars.varsHandle()
    order = getOrderSeven()
    partyMembers = len(order)
    frontLine = frontLine.lower()
    orderFinal = getPartyFormatFromText(frontLine)
    orderFinal.extend(x for x in order if x not in orderFinal)
    if Counter(order[:3]) == Counter(orderFinal[:3]):
        print("Good to go, no action taken.")
    else:
        print("Converting from formation:")
        print(order)
        print("Into formation:")
        print(orderFinal)
        print("Manipulating final formation to minimize movements")
        replacement_dict = {}
        new_characters = [x for x in orderFinal[:3] if x not in order[:3]]
        for i in range(3):
            if order[i] in orderFinal[:3]:
                replacement_dict[i] = order[i]
            else:
                replacement_dict[i] = new_characters.pop()
        for i in range(3):
            orderFinal[i] = replacement_dict[i]
        print("New Final Order:")
        print(orderFinal)
        while not menuOpen():
            if not openMenu():
                return
        FFXC = xbox.controllerHandle()
        FFXC.set_neutral()
        while getMenuCursorPos() != 7:
            menuDirection(getMenuCursorPos(), 7, 11)
            if gameVars.usePause():
                waitFrames(1)
        while menuNumber() != 14:
            xbox.tapB()
        startPos = 0
        while Counter(order[:3]) != Counter(orderFinal[:3]):
            print("==Full Party Format function, original")
            # Select target in the wrong spot.
            print("Selecting start position")
            if order[startPos] == orderFinal[startPos]:
                while order[startPos] == orderFinal[startPos] and order != orderFinal:
                    startPos += 1
                    if startPos == partyMembers:
                        startPos = 0
            print("Character", nameFromNumber(
                orderFinal[startPos]), "should be in position", startPos)

            # Set target, end position
            print("Selecting destination position.")
            endPos = 0
            if orderFinal[startPos] != order[endPos]:
                while orderFinal[startPos] != order[endPos] and order != orderFinal:
                    endPos += 1

            print("Character", nameFromNumber(
                order[endPos]), "found in position", endPos)

            print("Looking for character.")
            if startPos < 3 and endPos < 3:
                startPos += 1
                if startPos == partyMembers:
                    startPos = 0
                continue

            # Move cursor to start position
            print("Moving to start position")
            if partyFormatCursor1() != startPos:
                # print("Cursor not in right spot")
                while partyFormatCursor1() != startPos:
                    menuDirection(partyFormatCursor1(), startPos, partyMembers)
                    if gameVars.usePause():
                        waitFrames(1)

            while menuNumber() != 20:
                xbox.menuB()  # Click on Start location

            # Move cursor to end position
            print("Moving to destination position.")
            while partyFormatCursor2() != endPos:
                menuDirection(partyFormatCursor2(), endPos, partyMembers)
                if gameVars.usePause():
                    waitFrames(1)
            while menuNumber() != 14:
                xbox.menuB()  # Click on End location, performs swap.
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
        print("Party format is good now.")
        if fullMenuClose:
            closeMenu()
        else:
            backToMainMenu()


def menuDirection(currentmenuposition, targetmenuposition, menusize):
    distance = abs(currentmenuposition - targetmenuposition)
    distanceUnsigned = currentmenuposition - targetmenuposition
    halfmenusize = menusize / 2
    if distance == halfmenusize:
        xbox.tapUp()
    elif distance < halfmenusize:
        if distanceUnsigned > 0:
            xbox.tapUp()
        else:
            xbox.tapDown()
    else:
        if distanceUnsigned > 0:
            xbox.tapDown()
        else:
            xbox.tapUp()


def sideToSideDirection(currentmenuposition, targetmenuposition, menusize):
    distance = abs(currentmenuposition - targetmenuposition)
    distanceUnsigned = currentmenuposition - targetmenuposition
    print("Menu Size:", menusize)
    halfmenusize = menusize / 2
    if distance == halfmenusize:
        print("Marker 1")
        xbox.tapLeft()
    elif distance < halfmenusize:
        if distanceUnsigned > 0:
            print("Marker 2")
            xbox.tapRight()
        else:
            print("Marker 3")
            xbox.tapLeft()
    else:
        if distanceUnsigned > 0:
            print("Marker 4")
            xbox.tapLeft()
        else:
            print("Marker 5")
            xbox.tapRight()


def partyFormatCursor1():
    global baseValue

    coord = baseValue + 0x0147151C
    retVal = process.readBytes(coord, 1)
    return retVal


def partyFormatCursor2():
    global baseValue

    coord = baseValue + 0x01471520
    retVal = process.readBytes(coord, 1)
    return retVal


def getPartyFormatFromText(frontLine):
    print("||| FRONT LINE VARIABLE:", frontLine)
    if frontLine == 'kimahri':
        orderFinal = [0, 3, 2, 6, 4, 5, 1]
    elif frontLine == 'rikku':
        orderFinal = [0, 6, 2, 3, 4, 5, 1]
    elif frontLine == 'yuna':
        orderFinal = [0, 1, 2, 6, 4, 5, 3]
    elif frontLine == 'kilikawoods1':
        orderFinal = [0, 1, 4, 3, 5, 2]
    elif frontLine == 'kilikawoodsbackup':
        orderFinal = [3, 1, 4, 0, 5]
    elif frontLine == 'gauntlet':
        orderFinal = [0, 1, 3, 2, 4, 5, 6]
    elif frontLine == 'miihen':
        orderFinal = [0, 4, 2, 3, 5, 1]
    elif frontLine == 'macalaniaescape':
        orderFinal = [0, 1, 6, 2, 4, 3, 5]
    elif frontLine == 'desert1':
        orderFinal = [0, 6, 2, 3, 4, 5]
    elif frontLine == 'desert2':
        orderFinal = [0, 3, 2, 6, 4, 5]
    elif frontLine == 'desert3':
        orderFinal = [0, 5, 2, 6, 4, 3]
    elif frontLine == 'desert9':
        orderFinal = [0, 4, 2, 3, 5]
    elif frontLine == 'guards':
        orderFinal = [0, 2, 3, 6, 4, 5]
    elif frontLine == 'evrae':
        orderFinal = [0, 6, 3, 2, 4, 5]
    elif frontLine == 'djose':
        orderFinal = [0, 4, 2, 3, 1, 5]
    elif frontLine == 'spheri':
        orderFinal = [0, 3, 1, 4, 2, 6, 5]
    elif frontLine == 'crawler':
        orderFinal = [0, 3, 5, 4, 2, 6, 1]
    elif frontLine == 'besaid1':
        orderFinal = [0, 1, 5, 3, 4]
    elif frontLine == 'besaid2':
        orderFinal = [0, 4, 5, 3, 5]
    elif frontLine == 'kilika':
        orderFinal = [0, 1, 4, 3, 5]
    elif frontLine == 'mrr1':
        orderFinal = [0, 4, 2, 3, 5, 1]
    elif frontLine == 'mrr2':
        orderFinal = [1, 4, 3, 5, 2, 0]
    elif frontLine == 'battlesite':
        orderFinal = [0, 1, 4, 5, 2, 3]
    elif frontLine == 'postbunyip':
        orderFinal = [0, 4, 2, 6, 1, 3, 5]
    elif frontLine == 'mwoodsneedcharge':
        orderFinal = [0, 6, 2, 4, 1, 3, 5]
    elif frontLine == 'mwoodsgotcharge':
        orderFinal = [0, 4, 2, 6, 1, 3, 5]
    elif frontLine == 'mwoodsdone':
        orderFinal = [0, 3, 2, 4, 1, 6, 5]
    elif frontLine == 'besaid':
        orderFinal = [5, 1, 0, 4]
    elif frontLine == 'highbridge':
        orderFinal = [0, 1, 2, 6, 4, 5]
    elif frontLine == 'guards_no_lulu':
        orderFinal = [0, 3, 6]
    elif frontLine == 'guards_lulu':
        orderFinal = [0, 5, 6]
    elif frontLine == 'tidkimwak':
        orderFinal = [0, 4, 3, 6, 1, 2, 5]
    elif frontLine == 'nemlulu':
        orderFinal = [0, 1, 5, 2, 3, 4, 6]
    elif frontLine == 'initiative':
        orderFinal = [0, 4, 6, 1, 2, 3, 5]
    else:
        orderFinal = [6, 5, 4, 3, 2, 1, 0]
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


def getActorArraySize():
    global baseValue
    return process.read(baseValue + 0x01fc44e0)


def getActorID(actorNum):
    global baseValue
    basePointer = baseValue + 0x01fc44e4
    basePointerAddress = process.read(basePointer)
    offsetX = (0x880 * actorNum)
    return process.readBytes(basePointerAddress + offsetX, 2)


def getActorCoords(actorNumber):
    global process
    global baseValue
    retVal = [0, 0, 0]
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
        keyZ = basePointerAddress + offsetZ
        retVal[2] = float_from_integer(process.read(keyZ))

        return retVal
    except Exception:
        pass


def getActorAngle(actorNumber):
    global process
    global baseValue
    try:
        basePointer = baseValue + 0x01fc44e4
        basePointerAddress = process.read(basePointer)
        offset = (0x880 * actorNumber) + 0x158
        retVal = float_from_integer(process.read(basePointerAddress + offset))
        return retVal
    except Exception:
        pass


def miihenGuyCoords():
    spearGuy = 255
    for x in range(getActorArraySize()):
        actorNum = getActorID(x)
        if actorNum == 0x202D:
            spearGuy = x
    return getActorCoords(spearGuy)


def actorIndex(actorNum: int = 41):
    actorIndex = 255
    for x in range(getActorArraySize()):
        actorMem = getActorID(x)
        if actorNum == actorMem:
            actorIndex = x
    return actorIndex


def mrrGuyCoords():
    print("+++Searching for MRR guy")
    mrrGuy = 255
    for x in range(getActorArraySize()):
        actorNum = getActorID(x)
        # print("Actor", x, ":", hex(actorNum))
        if actorNum == 0x2083:
            mrrGuy = x
    print("+++MRR guy in position:", mrrGuy)
    mrrGuyPos = getActorCoords(mrrGuy)
    return [mrrGuyPos[0], mrrGuyPos[1]]


def lucilleMiihenCoords():
    return getActorCoords(8)


def lucilleDjoseCoords():
    return getActorCoords(11)


def lucilleDjoseAngle():
    global process
    global baseValue
    retVal = [0, 0]

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
    retVal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x = 0

    basePointer = baseValue + 0x00386DD4
    basePointerAddress = process.read(basePointer)
    for x in range(20):
        offset = (0x94 * x) + 0x39
        retVal[x] = process.readBytes(basePointerAddress + offset, 1)
    print("Overdrive values:\n", retVal)
    return retVal


def overdriveState2():
    global process
    global baseValue
    retVal = [0, 0, 0, 0, 0, 0, 0]
    x = 0
    basePointer = baseValue + 0x003AB9B0
    basePointerAddress = process.read(basePointer)
    for x in range(7):
        offset = (0x94 * x) + 0x39
        retVal[x] = process.readBytes(basePointerAddress + offset, 1)
    print("Overdrive values:\n", retVal)
    return retVal


def charLuck(character: int = 0):
    global process
    global baseValue
    basePointer = baseValue + 0x003AB9B0
    basePointerAddress = process.read(basePointer)
    offset = (0x94 * character) + 0x34
    retVal = process.readBytes(basePointerAddress + offset, 1)
    return retVal


def charAccuracy(character: int = 0):
    global process
    global baseValue
    basePointer = baseValue + 0x003AB9B0
    basePointerAddress = process.read(basePointer)
    offset = (0x94 * character) + 0x36
    retVal = process.readBytes(basePointerAddress + offset, 1)
    return retVal


def dodgeLightning(lDodgeNum):
    global baseValue

    if lStrikeCount() != lDodgeNum or (lStrikeCount() == 1 and lDodgeNum == 0):
        waitFrames(3)
        xbox.tapB()
        waitFrames(5)
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
    print("Clicking to dialog progress:", num)
    lastNum = diagProgressFlag()
    while diagProgressFlag() != num:
        if userControl():
            return False
        else:
            xbox.tapB()
            if diagProgressFlag() != lastNum:
                lastNum = diagProgressFlag()
                print("Dialog change:", diagProgressFlag(), "- clicking to", num)
    return True


def setEncounterRate(setVal):
    global baseValue

    key = baseValue + 0x008421C8
    process.writeBytes(key, setVal, 1)


def setGameSpeed(setVal):
    global baseValue

    key = baseValue + 0x008E82A4
    process.writeBytes(key, setVal, 1)


def printRNG36():
    global baseValue

    coord = baseValue + 0x00D35F68
    retVal = process.readBytes(coord, 1)
    print("------------------------------")
    print("RNG36 value:", retVal)
    print("------------------------------")


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
    key = baseValue + 0x01440A30
    return process.readBytes(key, 1)


# Naming
def getNamingMenu():
    return readVal(0x0146A22C)


def getNamingIndex():
    return readVal(0x0146A228)


def nameHasCharacters():
    return readVal(0x0146A240)


# ------------------------------
# Egg hunt section
def eggX(eggNum):
    global process
    global baseValue
    eggNum += 23
    basePointer = baseValue + 0x1FC44E4
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + (0x880 * eggNum) + 0x0C
    retVal = float_from_integer(process.read(key))
    return retVal


def eggY(eggNum):
    global process
    global baseValue
    eggNum += 23
    basePointer = baseValue + 0x1FC44E4
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + (0x880 * eggNum) + 0x14
    retVal = float_from_integer(process.read(key))
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
    retVal = process.readBytes(key, 1)
    return retVal


def getEggPicked(eggNum):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C4CC + (0x40 * eggNum) + 5
    retVal = process.readBytes(key, 1)
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
        varArray = [self.num, self.isActive, self.x, self.y,
                    150 - self.eggLife, self.eggPicked, self.distance]
        print("Egg_num, Is_Active, X, Y, Egg Life, Picked up, distance")
        print(varArray)


def buildEggs():
    retArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(10):
        retArray[x] = egg(x)
    return retArray


def iceX(actor):
    global process
    global baseValue
    # Icicle 0 is actor 7 in the array, incremented for each additional icicle.
    offset = actor + 7

    basePointer = baseValue + 0x1fc44e4
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + (0x880 * offset) + 0x0C
    retVal = float_from_integer(process.read(key))
    return retVal


def iceY(actor):
    global process
    global baseValue
    # Icicle 0 is actor 7 in the array, incremented for each additional icicle.
    offset = actor + 7

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
    retVal = process.readBytes(key, 1)
    return retVal


class icicle:
    def __init__(self, icenum):
        self.num = icenum
        self.x = iceX(self.num)
        self.y = iceY(self.num)
        self.isActive = True

    def reportVars(self):
        varArray = [self.num, self.x, self.y]
        print("Ice_num, X, Y")
        print(varArray)


def buildIcicles():
    retArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(16):
        retArray[x] = icicle(x)
    return retArray


# ------------------------------
# Soft reset section

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
    process.writeBytes(key, 1, 1)


def setRNG2():
    global baseValue
    global process
    key = baseValue + 0x00D35EE0
    process.writeBytes(key, 0x7E9F20D2, 4)


# ------------------------------
# Blitzball!

class blitzActor:
    def __init__(self, playerNum: int):
        self.num = playerNum
        self.position = getActorCoords(self.num)
        self.distance = 0

    def updateCoords(self, activePlayer=12):
        self.position = getActorCoords(self.num + 2)
        self.distance = 100

    def getCoords(self):
        coords = getActorCoords(self.num)
        return coords

    def currentHP(self):
        return blitzHP(self.num)

    def aggro(self):
        return getBlitzAggro(self.num)


def getBlitzAggro(playerIndex: int = 99):
    global baseValue
    ptrKey = process.read(baseValue + 0x00F2FF14)
    if playerIndex == 6:
        offset = 0x2DC35
    elif playerIndex == 7:
        offset = 0x343E5
    elif playerIndex == 8:
        offset = 0x3AB95
    elif playerIndex == 9:
        offset = 0x41345
    elif playerIndex == 10:
        offset = 0x47AF5

    if playerIndex in [6, 7, 8, 9, 10]:
        if process.readBytes(ptrKey + offset, 1) == 255:
            return False
        else:
            return True
    else:
        return False


def blitzHP(playerIndex=99):
    global baseValue
    if playerIndex == 99:
        return 9999
    else:
        ptrKey = process.read(baseValue + 0x00F2FF14)
        offset = 0x1c8 + (0x4 * playerIndex)
        hpValue = process.read(ptrKey + offset)
        return hpValue


def blitzOwnScore():
    global baseValue
    key = baseValue + 0x00D2E0CE
    score = process.readBytes(key, 1)
    return score


def blitzOppScore():
    global baseValue
    key = baseValue + 0x00D2E0CF
    score = process.readBytes(key, 1)
    return score


def blitzballPatriotsStyle():
    global baseValue

    key = baseValue + 0x00D2E0CE


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
    # 20 = Movement menu (auto, type A, or type B)
    # 29 = Formation menu
    # 38 = Breakthrough
    # 24 = Pass To menu (other variations are set to 24)
    # Unsure about other variations, would take more testing.

    key = baseValue + 0x014765DA
    status = process.readBytes(key, 1)
    if status == 17 or status == 27:
        status = 24
    return status


def resetBlitzMenuNum():
    global baseValue
    key = baseValue + 0x014765DA
    process.writeBytes(key, 1, 1)


def blitzCurrentPlayer():
    global baseValue

    key = baseValue + 0x00F25B6A
    player = process.readBytes(key, 1)
    return player


def blitzTargetPlayer():
    global baseValue

    key = baseValue + 0x00D3761C
    player = process.readBytes(key, 1)
    return player


def blitzCoords():
    global baseValue

    key = baseValue + 0x00D37698
    xVal = process.readBytes(key, 1)
    xVal = xVal * -1
    key = baseValue + 0x00D37690
    yVal = process.readBytes(key, 1)
    return [xVal, yVal]


def blitzGameActive():
    if getMap() == 62:
        return True
    else:
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

# ------------------------------
# Function for logging


def readBytes(key, size):
    return process.readBytes(key, size)


# ------------------------------
# Equipment array

# 0x0 - ushort - name/group (?)
# 0x3 - byte - wpn./arm. state
# 0x4 - byte - owner char (basis for field below)
# 0x5 - byte - equip type idx. (0 = cur. chara wpn., 1 = cur. chara arm., 2 = next chara wpn., etc.)
# 0x6 - byte - equip icon shown? (purely visual- a character will still keep it equipped if his stat struct says so)
# 0x8 - byte - atk. type
# 0x9 - byte - dmg. constant
# 0xA - byte - base crit rate (armor has one too!!!)
# 0xB - byte - slot count (cannot be < abi count, game won't let you)
# 0xC - ushort - wpn./arm. model (?)
# 0xE - ushort - auto-ability 1
# 0x10 - ushort - auto-ability 2
# 0x12 - ushort - auto-ability 3
# 0x14 - ushort - auto-ability 4

def getEquipType(equipNum):
    global baseValue

    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) + 0x05
    retVal = process.readBytes(key, 1)
    return retVal


def getEquipLegit(equipNum):
    global baseValue

    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) + 0x03
    retVal = process.readBytes(key, 1)
    if retVal in [0, 8, 9]:
        return True
    else:
        return False


def isEquipBrotherhood(equipNum):
    if getEquipOwner(equipNum) == 0:
        global baseValue
        basePointer = baseValue + 0x00d30f2c
        key = basePointer + (0x16 * equipNum) + 0x03
        retVal = process.readBytes(key, 1)
        if retVal == 9:
            return True
    return False


def getEquipOwner(equipNum):
    global baseValue

    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) + 0x04
    retVal = process.readBytes(key, 1)
    return retVal


def getEquipSlotCount(equipNum):
    global baseValue

    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) + 0x0B
    retVal = process.readBytes(key, 1)
    return retVal


def getEquipCurrentlyEquipped(equipNum):
    global baseValue

    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) + 0x06
    retVal = process.readBytes(key, 1)
    return retVal


def getEquipAbilities(equipNum):
    global baseValue
    retVal = [255, 255, 255, 255]

    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) + 0x0E
    retVal[0] = process.readBytes(key, 2)
    key = basePointer + (0x16 * equipNum) + 0x10
    retVal[1] = process.readBytes(key, 2)
    key = basePointer + (0x16 * equipNum) + 0x12
    retVal[2] = process.readBytes(key, 2)
    key = basePointer + (0x16 * equipNum) + 0x14
    retVal[3] = process.readBytes(key, 2)
    return retVal


def getEquipExists(equipNum):
    global baseValue

    basePointer = baseValue + 0x00d30f2c
    key = basePointer + (0x16 * equipNum) + 0x02
    retVal = process.readBytes(key, 1)

    return retVal


class equipment:
    def __init__(self, equipNum):
        self.num = equipNum
        self.equipType = getEquipType(equipNum)
        self.equipOwner = getEquipOwner(equipNum)
        self.equipOwnerAlt = getEquipOwner(equipNum)
        self.equipAbilities = getEquipAbilities(equipNum)
        self.equipStatus = getEquipCurrentlyEquipped(equipNum)
        self.slots = getEquipSlotCount(equipNum)
        self.exists = getEquipExists(equipNum)
        self.brotherhood = isEquipBrotherhood(equipNum)

    def createCustom(self, eType: int, eOwner1: int, eOwner2: int, eSlots: int, eAbilities):
        self.equipType = eType
        self.equipOwner = eOwner1
        self.equipOwnerAlt = eOwner2
        self.equipAbilities = eAbilities
        self.equipStatus = 0
        self.slots = eSlots
        self.exists = 1
        self.brotherhood = False

    def equipmentType(self):
        return self.equipType

    def owner(self):
        return self.equipOwner

    def abilities(self):
        return self.equipAbilities

    def hasAbility(self, abilityNum):
        if abilityNum in self.equipAbilities:
            return True
        return False

    def isEquipped(self):
        return self.equipStatus

    def slotCount(self):
        return self.slots

    def equipExists(self):
        return self.exists

    def isBrotherhood(self):
        return self.brotherhood


def allEquipment():
    firstEquipment = True
    for i in range(200):
        currentHandle = equipment(i)
        if getEquipLegit(i) and currentHandle.equipExists():
            if firstEquipment:
                equipHandleArray = [equipment(i)]
                firstEquipment = False
            else:
                equipHandleArray.append(equipment(i))
    return equipHandleArray


def weaponArrayCharacter(charNum):
    equipHandles = allEquipment()
    firstEquipment = True
    while len(equipHandles) > 0:
        currentHandle = equipHandles.pop(0)
        if currentHandle.owner() == charNum and currentHandle.equipmentType() == 0:
            if firstEquipment:
                charWeaps = [currentHandle]
                firstEquipment = False
            else:
                charWeaps.append(currentHandle)
    return charWeaps


def equippedWeaponHasAbility(charNum: int = 1, abilityNum: int = 32769):
    equipHandles = weaponArrayCharacter(charNum)
    while len(equipHandles) > 0:
        currentHandle = equipHandles.pop(0)
        if currentHandle.isEquipped() == charNum:
            print("## Owner:", currentHandle.owner())
            print("## Equipped:", currentHandle.isEquipped())
            print("## Has Ability:", currentHandle.hasAbility(abilityNum))
            if currentHandle.hasAbility(abilityNum):
                return True
            else:
                return False


def checkThunderStrike() -> int:
    results = 0
    tidusWeaps = weaponArrayCharacter(0)
    while len(tidusWeaps) > 0:
        currentHandle = tidusWeaps.pop(0)
        if currentHandle.hasAbility(0x8026):
            results += 1
            break

    wakkaWeaps = weaponArrayCharacter(4)
    while len(wakkaWeaps) > 0:
        currentHandle = wakkaWeaps.pop(0)
        if currentHandle.hasAbility(0x8026):
            results += 2
            break
    return results


def checkZombieStrike():
    ability = 0x8032
    gameVars = vars.varsHandle()

    charWeaps = weaponArrayCharacter(0)  # Tidus
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setZombie(0)
            return True

    charWeaps = weaponArrayCharacter(1)  # Yuna
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setZombie(1)
            return True

    charWeaps = weaponArrayCharacter(2)  # Auron
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setZombie(2)
            return True

    charWeaps = weaponArrayCharacter(3)  # Kimahri
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setZombie(3)
            return True

    charWeaps = weaponArrayCharacter(4)  # Wakka
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setZombie(4)
            return True

    charWeaps = weaponArrayCharacter(5)  # Lulu
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setZombie(5)
            return True

    charWeaps = weaponArrayCharacter(6)  # Rikku
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setZombie(6)
            return True

    return False


def checkAbility(ability=0x8032):
    results = [False, False, False, False, False, False, False]

    charWeaps = weaponArrayCharacter(0)  # Tidus
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            results[0] = True

    charWeaps = weaponArrayCharacter(1)  # Yuna
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            results[1] = True

    charWeaps = weaponArrayCharacter(2)  # Auron
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            results[2] = True

    charWeaps = weaponArrayCharacter(3)  # Kimahri
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            results[3] = True

    charWeaps = weaponArrayCharacter(4)  # Wakka
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            results[4] = True

    charWeaps = weaponArrayCharacter(5)  # Lulu
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            results[5] = True

    charWeaps = weaponArrayCharacter(6)  # Rikku
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            results[6] = True

    return results


def checkAbilityArmor(ability=0x8032, slotCount: int = 99):
    results = [False, False, False, False, False, False, False]

    charWeaps = armorArrayCharacter(0)  # Tidus
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            if slotCount != 99:
                if currentHandle.slotCount() != slotCount:
                    results[0] = False
                else:
                    results[0] = True
            else:
                results[0] = True

    charWeaps = armorArrayCharacter(1)  # Yuna
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            if slotCount != 99:
                if currentHandle.slotCount() != slotCount:
                    results[1] = False
                else:
                    results[1] = True
            else:
                results[1] = True

    charWeaps = armorArrayCharacter(2)  # Auron
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            if slotCount != 99:
                if currentHandle.slotCount() != slotCount:
                    results[2] = False
                else:
                    results[2] = True
            else:
                results[2] = True

    charWeaps = armorArrayCharacter(3)  # Kimahri
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            if slotCount != 99:
                if currentHandle.slotCount() != slotCount:
                    results[3] = False
                else:
                    results[3] = True
            else:
                results[3] = True

    charWeaps = armorArrayCharacter(4)  # Wakka
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            if slotCount != 99:
                if currentHandle.slotCount() != slotCount:
                    results[4] = False
                else:
                    results[4] = True
            else:
                results[4] = True

    charWeaps = armorArrayCharacter(5)  # Lulu
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            if slotCount != 99:
                if currentHandle.slotCount() != slotCount:
                    results[5] = False
                else:
                    results[5] = True
            else:
                results[5] = True

    charWeaps = armorArrayCharacter(6)  # Rikku
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            if slotCount != 99:
                if currentHandle.slotCount() != slotCount:
                    results[6] = False
                else:
                    results[6] = True
            else:
                results[6] = True

    return results


def weapon_armor_cursor():
    global baseValue
    return process.readBytes(baseValue + 0x0146A5E4, 1)


def customizeMenuArray():
    retArray = []
    global baseValue
    for x in range(60):
        offset = 0x1197730 + (x * 4)
        retArray.append(process.readBytes(baseValue + offset, 2))
    print("Customize menu: ")
    print(retArray)
    return retArray


def checkNEArmor():
    ability = 0x801D
    gameVars = vars.varsHandle()

    charWeaps = armorArrayCharacter(0)  # Tidus
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setneArmor(0)
            return True

    charWeaps = armorArrayCharacter(1)  # Yuna
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setneArmor(1)
            return True

    charWeaps = armorArrayCharacter(2)  # Auron
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setneArmor(2)
            return True

    charWeaps = armorArrayCharacter(3)  # Kimahri
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setneArmor(3)
            return True

    charWeaps = armorArrayCharacter(4)  # Wakka
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setneArmor(4)
            return True

    charWeaps = armorArrayCharacter(5)  # Lulu
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setneArmor(5)
            return True

    charWeaps = armorArrayCharacter(6)  # Rikku
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.hasAbility(ability):
            gameVars.setneArmor(6)
            return True

    return False


def shopMenuDialogueRow():
    return readVal(0x0146780A)


def airshipShopDialogueRow():
    return readVal(0x014676D2)


def hunterSpear():
    kimWeapHandles = weaponArrayCharacter(3)
    if len(kimWeapHandles) == 1:
        return False
    else:
        while len(kimWeapHandles) > 0:
            currentHandle = kimWeapHandles.pop(0)
            if currentHandle.abilities() == [0x800b, 0x8000, 0x8064, 0x00ff]:
                return True
    return False


def armorArrayCharacter(charNum):
    equipHandles = allEquipment()
    firstEquipment = True
    charWeaps = []
    while len(equipHandles) > 0:
        currentHandle = equipHandles.pop(0)
        if currentHandle.owner() == charNum and currentHandle.equipmentType() == 1:
            if firstEquipment:
                charWeaps = [currentHandle]
                firstEquipment = False
            else:
                charWeaps.append(currentHandle)
    try:
        return charWeaps
    except Exception:
        return []


def equippedArmorHasAbility(charNum: int, abilityNum: int = 0x801D):
    equipHandles = armorArrayCharacter(charNum)
    while len(equipHandles) > 0:
        currentHandle = equipHandles.pop(0)
        if currentHandle.isEquipped() == charNum:
            print("## Owner:", currentHandle.owner())
            print("## Equipped:", currentHandle.isEquipped())
            print("## Has Ability:", currentHandle.hasAbility(abilityNum))
            if currentHandle.hasAbility(abilityNum):
                return True
            else:
                return False


def equipWeapCursor():
    global baseValue

    key = baseValue + 0x01440A38
    retVal = process.readBytes(key, 1)
    return retVal


def assignAbilityToEquipCursor():
    global baseValue
    key = baseValue + 0x01440AD0
    retVal = process.readBytes(key, 1)
    return retVal

# ------------------------------
# Shopping related stuff


def itemShopMenu():
    global baseValue
    key = baseValue + 0x0085A860
    retVal = process.readBytes(key, 1)
    return retVal


def equipShopMenu():
    global baseValue
    key = baseValue + 0x0085A83C
    retVal = process.readBytes(key, 1)
    return retVal


def cureMenuOpen():
    global baseValue
    key = baseValue + 0x01440A35
    retVal = process.readBytes(key, 1)
    return retVal


def itemMenuNumber():
    global baseValue
    key = baseValue + 0x0085A318
    retVal = process.readBytes(key, 1)
    return retVal


def itemMenuColumn():
    global baseValue
    key = baseValue + 0x01440A48
    retVal = process.readBytes(key, 1)
    return retVal


def informationActive():
    global baseValue
    key = baseValue + 0x0146AA28
    retVal = process.readBytes(key, 1)
    return retVal == 7


def itemMenuRow():
    global baseValue
    key = baseValue + 0x01440A38
    retVal = process.readBytes(key, 1)
    return retVal


def equipSellRow():
    global baseValue
    key = baseValue + 0x01440C00
    retVal = process.readBytes(key, 1)
    return retVal


def nameConfirmOpen():
    return readVal(0x014408E8) == 8


def equipBuyRow():
    global baseValue
    key = baseValue + 0x01440B68
    retVal = process.readBytes(key, 1)
    return retVal


def cursorEnabledInEquip():
    global baseValue
    key = baseValue + 0x008CC7EC
    retVal = process.readBytes(key, 1)
    return retVal == 12


def equipConfirmationRow():
    global baseValue
    key = baseValue + 0x01440C98
    retVal = process.readBytes(key, 1)
    return retVal


def equipMenuOpenFromChar():
    global baseValue
    key = baseValue + 0x01440A2A
    retVal = process.readBytes(key, 1)
    return retVal == 5


def configCursor():
    global baseValue
    key = baseValue + 0x0146A404
    retVal = process.readBytes(key, 1)
    return retVal


def readVal(address, bytes=1):
    global baseValue
    key = baseValue + address
    retVal = process.readBytes(key, bytes)
    return retVal


def spareChangeAmount():
    return readVal(0x00F40424, 4)


def oakaGilAmount():
    return readVal(0x01467A84, 4)


def oakaGilCursor():
    return readVal(0x014663A8)


def oakaInterface():
    return readVal(0x00F26D30)


def spareChangeCursor():
    return readVal(0x00F40418)


def spareChangeOpen():
    return readVal(0x00F3CAF1) == 4


def configCursorColumn():
    global baseValue
    key = baseValue + 0x0085A3FC
    retVal = process.readBytes(key, 1)
    return retVal


def purchasingAmountItems():
    return readVal(0x01440C00)


def configAeonCursorColumn():
    global baseValue
    key = baseValue + 0x0085A454
    retVal = process.readBytes(key, 1)
    return retVal


def loadMenuCursor():
    global baseValue
    key = baseValue + 0x008E72E0
    retVal = process.readBytes(key, 1)
    return retVal


def rikkuOverdriveItemSelectedNumber():
    global baseValue
    key = baseValue + 0x00D2C948
    retVal = process.readBytes(key, 1)
    return retVal


def sphereGridPlacementOpen():
    global baseValue
    key = baseValue + 0x012ACB6B
    retVal = process.readBytes(key, 1)
    return retVal


def movingPromptOpen():
    global baseValue
    key = baseValue + 0x012AD543
    retVal = process.readBytes(key, 1)
    return retVal

# ------------------------------
# Bevelle Trials indicators


def btBiDirection():
    key = baseValue + 0x0092DEED
    return process.readBytes(key, 1)


def btTriDirectionMain():
    key = baseValue + 0x0092E1ED
    return process.readBytes(key, 1)

# ------------------------------
# Gagazet trials


def GTouterRing():
    global baseValue
    key = baseValue + 0x014DFC34
    height = float_from_integer(process.read(key))
    return height


def GTinnerRing():
    global baseValue
    key = baseValue + 0x014DFDA0
    height = float_from_integer(process.read(key))
    return height

# ------------------------------
# Save spheres


def getSaveSphereDetails():
    mapVal = getMap()
    storyVal = getStoryProgress()
    print("Map:", mapVal, "| Story:", storyVal)
    x = 0
    y = 0
    diag = 0
    if mapVal == 389:
        # Ammes
        x = 994
        y = -263
        diag = 9
    if mapVal == 49:
        # Baaj
        x = 230
        y = -215
        diag = 17
    if mapVal == 63:
        # Before Klikk
        x = -100
        y = 143
        diag = 29
    if mapVal == 64:
        # Before Tros
        x = 5
        y = -170
        diag = 3
    if mapVal == 19:
        # Besaid beach
        x = -310
        y = -475
        diag = 48
    if mapVal == 65:
        # Kilika - before Geneaux
        x = -3
        y = 175
        diag = 46
    if mapVal == 88:
        # Luca before Oblitzerator
        x = 175
        y = -310
        diag = 62
    if mapVal == 123:
        # Luca after Oblitzerator
        x = -270
        y = -45
        diag = 90
    if mapVal == 171:
        # Mi'ihen agency
        x = 35
        y = -10
        diag = 85
    if mapVal == 115:
        # Old Road
        x = 48
        y = -910
        diag = 40
    if mapVal == 59 and getStoryProgress() > 1000:
        # Miihen last screen, late game
        x = 15
        y = 125
        diag = 121
    if mapVal == 92:
        # MRR
        x = 5
        y = -740
        if getStoryProgress() < 1000:
            diag = 39
        else:
            diag = 43  # Nemesis run
    if mapVal == 119:
        # Battle Site
        x = -55
        y = 3335
        diag = 115
    if mapVal == 110:
        # Mac woods start
        x = 255
        y = -15
        diag = 84
    if mapVal == 221:
        # Mac woods before Spherimorph
        x = 195
        y = -123
        if getStoryProgress() < 4000:
            diag = 19
        else:
            diag = 23
    if mapVal == 106:
        # Mac Temple entrance
        x = -22
        y = -127
        diag = 68
    if mapVal == 153:
        # Mac Temple exit
        x = 820
        y = -235
        diag = 44
    if mapVal == 129:
        # Bikanel start
        x = 19
        y = -60
        diag = 35
    if mapVal == 136:
        # Bikanel Rikku tent
        x = 205
        y = 30
        diag = 59
    if mapVal == 130:
        # Home entrance screen
        x = 61
        y = 92
        diag = 25
    if mapVal == 208:
        # Highbridge before Natus
        x = 33
        y = 1251
        diag = 124
    if mapVal == 194:
        # Airship while rescuing Yuna, cockpit
        x = -275
        y = 344
        if getStoryProgress() < 2700:  # During Yuna rescue
            diag = 217
        else:  # Before Shedinja/Highbridge
            diag = 220
    if mapVal == 266:
        x = -305
        y = 185
        if getStoryProgress() < 3000:  # NEA trip
            diag = 39
        else:
            diag = 43
    if mapVal == 285:
        # After Flux
        x = 140
        y = -640
        diag = 84
    if mapVal == 316:
        # Just before Zan trials
        x = -20
        y = 358
        diag = 25
    if mapVal == 318:
        # Before Yunalesca
        x = -5
        y = -170
        diag = 26
    if mapVal == 140:
        # Thunder plains
        x = -45
        y = -870
        diag = 77
    if mapVal == 322:  # Nemesis run
        # Inside Sin, next to airship
        x = 225
        y = -250
        diag = 15
    if mapVal == 19:  # Nemesis run
        # Besaid beach
        x = -310
        y = -475
        diag = 55
    if mapVal == 263:  # Nemesis run
        # Thunder Plains agency
        x = -30
        y = -10
        diag = 114
    if mapVal == 307:  # Nemesis run
        # Monster Arena
        x = 4
        y = 5
        diag = 166
    if mapVal == 98:  # Nemesis run
        # Kilika docks
        x = 46
        y = -252
        diag = 34
    if mapVal == 82:  # Nemesis run
        # Djose temple
        x = 100
        y = -240
        diag = 89
    if mapVal == 137:  # Nemesis run
        # Bikanel Desert
        x = -15
        y = 240
        diag = 31
    if mapVal == 313:  # Nemesis run
        # Zanarkand campfire
        x = 135
        y = -1
        diag = 4
    if mapVal == 327:  # Nemesis run
        # Sin, end zone
        x = -37
        y = -508
        diag = 10
    if mapVal == 258:  # Nemesis run
        # Omega (only used in Nemesis)
        x = -112
        y = -1066
        diag = 23
    if mapVal == 307:
        # Monster Arena (only used in Nemesis)
        x = 2
        y = 5
        diag = 166
    if mapVal == 259:  # Nemesis run
        # Gagazet (only used in Nemesis)
        x = -59
        y = 99
        diag = 219
    if mapVal == 82:
        # Djose temple (only used in Nemesis)
        x = 97
        y = -241
        diag = 89
    if mapVal == 128:  # Nemesis run
        # MRR upper lift (only used in Nemesis)
        x = 230
        y = 140
        diag = 68
    print("Values: [", x, ",", y, "] -", diag)
    return [x, y, diag]


def touchSaveSphere(saveCursorNum: int = 0):
    print("MEM - Touch Save Sphere")
    clearSaveMenuCursor()
    clearSaveMenuCursor2()

    ssDetails = getSaveSphereDetails()
    FFXC = xbox.controllerHandle()
    while userControl():
        targetPathing.setMovement([ssDetails[0], ssDetails[1]])
        xbox.tapB()
        waitFrames(1)
    FFXC.set_neutral()
    print("Waiting for cursor to reset before we do things - Mark 1")
    while menuControl() == 0:
        pass
    waitFrames(1)
    print("Mark 2")
    #waitFrames(300)
    inc = 0

    while not (saveMenuCursor() == 0 and saveMenuCursor2() == 0 and diagProgressFlag() == ssDetails[2]):
        print("Cursor test: A", getStoryProgress(), "|", diagProgressFlag(), "|", getMap(), "|", inc)
        inc += 1
        if saveMenuOpen():
            xbox.tapA()
        elif diagSkipPossible() and diagProgressFlag() != ssDetails[2]:
            xbox.tapB()
    while not (saveMenuCursor() == 0 and saveMenuCursor2() == 0):
        print("Cursor test: B", saveMenuCursor(), "|", saveMenuCursor2(), "|", diagSkipPossible(), "|", inc)
        inc += 1
        if saveMenuOpen():
            xbox.tapA()
        elif diagSkipPossible():
            xbox.tapA()
    while saveMenuCursor() == 0 and saveMenuCursor2() == 0:
        print("Cursor test: C", saveMenuCursor(), "|", saveMenuCursor2(), "|", diagSkipPossible(), "|", inc)
        inc += 1
        if saveMenuOpen():
            xbox.tapA()
        elif diagSkipPossible():
            if diagProgressFlag() != ssDetails[2]:
                xbox.tapB()
            else:
                xbox.tapA()
    while not userControl():
        print("Cursor test: D", saveMenuCursor(), "|", saveMenuCursor2(), "|", inc)
        inc += 1
        if saveMenuOpen():
            xbox.tapA()
        else:
            xbox.tapB()
    print("Cursor test: E", saveMenuCursor(), "|", saveMenuCursor2(), "|", inc)
    inc += 1


def touchSaveSphere_notWorking(saveCursorNum: int = 0):
    print("MEM - Touch Save Sphere")

    ssDetails = getSaveSphereDetails()
    FFXC = xbox.controllerHandle()
    while userControl():
        targetPathing.setMovement([ssDetails[0], ssDetails[1]])
        xbox.tapB()
        waitFrames(1)
    FFXC.set_neutral()
    print("Waiting for cursor to reset before we do things - Mark 1")
    while menuControl() == 0:
        pass
    waitFrames(1)
    print("Mark 2")
    #waitFrames(300)

    xbox.tapA()
    #while saveMenuCursor() == 0:
    #    if saveMenuOpen():
    #        xbox.tapA()
    #    elif diagProgressFlag() != ssDetails[2] and diagSkipPossible():
    #        xbox.tapB()
    #    else:
    #        xbox.tapA()

    while not userControl():
        if saveMenuOpen():
            xbox.tapA()
        elif diagProgressFlag() == ssDetails[2]:
            print("Cursor test:", saveMenuCursor())
            print("Cursor test2:", saveMenuCursor2())
            if saveCursorNum == 0 and saveMenuCursor() == 0:
                xbox.tapA()
            elif saveCursorNum == 1 and saveMenuCursor2() == 0:
                xbox.tapA()
            else:
                xbox.menuB()
        else:
            xbox.tapB()
    clearSaveMenuCursor()
    clearSaveMenuCursor2()


def csrBaajSaveClear():
    if userControl():
        print("No need to clear. User is in control.")
    else:
        print("Save dialog has popped up for some reason. Attempting clear.")
        FFXC = xbox.controllerHandle()
        try:
            FFXC.set_neutral()
        except Exception:
            FFXC.set_neutral()
        while not userControl():
            if saveMenuOpen():
                xbox.tapA()
            elif diagProgressFlag() == 109:
                if saveMenuCursor() == 0 and saveMenuCursor2() == 0:
                    xbox.tapA()
                else:
                    xbox.tapB()
                waitFrames(4)

    clearSaveMenuCursor()
    clearSaveMenuCursor2()

# ------------------------------
# Testing


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

# ------------------------------


def printMemoryLog():
    pass


def printMemoryLog_backup():
    global baseValue
    global process
    # (Pointer) [[ffx.exe + 8DED2C] + 0x6D0]
    ptrVal = process.read(baseValue + 0x008DED2C)
    finalCoords = ptrVal + 0x6D0
    coord1 = process.read(finalCoords)
    logs.writeStats("Temp Value 1: " + str(coord1))

    # (Pointer) [[ffx.exe + 8DED2C] + 0x704]
    ptrVal = process.read(baseValue + 0x008DED2C)
    finalCoords = ptrVal + 0x704
    logs.writeStats("Temp Value 2: " + str(coord1))

    # (Pointer) [[ffx.exe + 8CB9D8] + 0x10D2E]
    ptrVal = process.read(baseValue + 0x008CB9D8)
    finalCoords = ptrVal + 0x10D2E
    logs.writeStats("Temp Value 3: " + str(coord1))

    # ffx.exe + D2A00C
    logs.writeStats("Temp Value 4: " + str(coord1))

# ------------------------------
# Load game functions


def loadGamePage():
    global baseValue
    key = baseValue + 0x008E72DC
    retVal = process.readBytes(key, 1)
    return retVal


def loadGameCursor():
    global baseValue
    key = baseValue + 0x008E72E0
    retVal = process.readBytes(key, 1)
    return retVal


def loadGamePos():
    return loadGamePage() + loadGameCursor()


def lucaWorkersBattleID():
    return readVal(0x01466DCC)

# ------------------------------
# RNG tracking based on the first six hits


def lastHitInit():
    global baseValue
    print("Initializing values")
    key = baseValue + 0xd334cc
    ptrVal = process.read(key)
    lastHitVals = [0] * 8
    try:
        for x in range(8):
            lastHitVals[x] = process.read(ptrVal + ((x + 20) * 0xF90) + 0x7AC)
            # print("Val:", lastHitVals[x])
        # print(lastHitVals)
        gameVars.firstHitsSet(lastHitVals)
        return True
    except Exception:
        return False


def lastHitCheckChange() -> int:
    global baseValue
    key = baseValue + 0xd334cc
    ptrVal = process.read(key)
    changeFound = False
    changeValue = 9999
    for x in range(8):
        memVal = process.read(ptrVal + ((x + 20) * 0xF90) + 0x7AC)
        if memVal != gameVars.firstHitsValue(x) and not changeFound:
            changeFound = True
            changeValue = memVal
            print("**Registered hit:", changeValue)
            # logs.writeStats(changeValue)
            lastHitInit()
            print("Mark 1")
            return int(changeValue)
            print("Mark 2")
    return 9999


# ------------------------------
# NE armor manip
RNG_CONSTANTS_1 = (
    2100005341, 1700015771, 247163863, 891644838, 1352476256, 1563244181,
    1528068162, 511705468, 1739927914, 398147329, 1278224951, 20980264,
    1178761637, 802909981, 1130639188, 1599606659, 952700148, -898770777,
    -1097979074, -2013480859, -338768120, -625456464, -2049746478, -550389733,
    -5384772, -128808769, -1756029551, 1379661854, 904938180, -1209494558,
    -1676357703, -1287910319, 1653802906, 393811311, -824919740, 1837641861,
    946029195, 1248183957, -1684075875, -2108396259, -681826312, 1003979812,
    1607786269, -585334321, 1285195346, 1997056081, -106688232, 1881479866,
    476193932, 307456100, 1290745818, 162507240, -213809065, -1135977230,
    -1272305475, 1484222417, -1559875058, 1407627502, 1206176750, -1537348094,
    638891383, 581678511, 1164589165, -1436620514, 1412081670, -1538191350,
    -284976976, 706005400,
)

RNG_CONSTANTS_2 = (
    10259, 24563, 11177, 56952, 46197, 49826, 27077, 1257, 44164, 56565, 31009,
    46618, 64397, 46089, 58119, 13090, 19496, 47700, 21163, 16247, 574, 18658,
    60495, 42058, 40532, 13649, 8049, 25369, 9373, 48949, 23157, 32735, 29605,
    44013, 16623, 15090, 43767, 51346, 28485, 39192, 40085, 32893, 41400, 1267,
    15436, 33645, 37189, 58137, 16264, 59665, 53663, 11528, 37584, 18427,
    59827, 49457, 22922, 24212, 62787, 56241, 55318, 9625, 57622, 7580, 56469,
    49208, 41671, 36458,
)


def buildRNGarray(index: int, arraySize: int = 255):
    global baseValue
    offset = baseValue + 0xD35ED8 + (index * 4)
    arrayVal = [process.read(offset)]
    for x in range(arraySize):
        arrayVal.append(rollNextRNG(arrayVal[x], index))
    return arrayVal


def nextCrit(character: int, charLuck: int, enemyLuck: int) -> int:
    # Returns the next time the character will critically strike, counting number of advances from present.
    # If 255 is returned, there will not be a next crit in the foreseeable future.
    rngIndex = min(20 + character, 27)
    rngArray = rngArrayFromIndex(index=rngIndex, arrayLen=200)
    del rngArray[0]
    del rngArray[0]
    for x in range(len(rngArray)):
        crit_roll = s32(rngArray[x]) % 101
        crit_chance = charLuck - enemyLuck
        if crit_roll < crit_chance:
            if x == 0:
                pass
            else:
                return x
    return 255


def futureAttackWillCrit(character: int, charLuck: int, enemyLuck: int, attackIndex: int = 0) -> bool:
    # Returns if a specific attack in the future will crit.
    # Attack Index 0 represents the next attack.
    # Assumes no escape attempts, primarily this is used for Aeons anyway.
    rngIndex = min(20 + character, 27)
    rngArray = rngArrayFromIndex(index=rngIndex, arrayLen=200)
    del rngArray[0]
    del rngArray[0]
    if attackIndex > 90:
        return False
    crit_roll = s32(rngArray[attackIndex * 2]) % 101
    crit_chance = charLuck - enemyLuck
    if crit_roll < crit_chance:
        return True
    return False


def rng01():
    global baseValue
    return process.read(baseValue + 0xD35EDC)


def rng01Array(arrayLen: int = 600):
    retVal = [rng01()]  # First value is the current value
    for x in range(arrayLen):  # Subsequent values are based on first value.
        retVal.append(rollNextRNG(retVal[x], 1))
    return retVal


def rng01Advances(advanceCount: int = 50):
    testArray = rng01Array()
    rangeVal = advanceCount
    for i in range(rangeVal):
        testArray.append(testArray[i] & 0x7fffffff)
    return testArray


def nextChanceRNG01(version='white'):
    testArray = rng01Array()
    evenArray = []
    oddArray = []
    rangeVal = int((len(testArray) - 1) / 2) - 2
    if version == 'white':
        modulo = 13
        battleIndex = 8
    else:
        modulo = 10
        battleIndex = 0
    for i in range(rangeVal):
        if (testArray[((i + 1) * 2) - 1] & 0x7fffffff) % modulo == battleIndex:
            oddArray.append(i)
        if (testArray[(i + 1) * 2] & 0x7fffffff) % modulo == battleIndex:
            evenArray.append(i)

    #print("------------------------------")
    #print("Next event will appear on the odd array without manip. Area:", version)
    #print("oddArray:", oddArray[0])
    #print("evenArray:", evenArray[0])
    #print("------------------------------")
    return ([oddArray, evenArray])


def advanceRNG01():
    global baseValue
    key = baseValue + 0xD35EDC
    process.write(key, rng01Array()[2])


def rng02():
    global baseValue
    return process.read(baseValue + 0xD35EE0)


def rng02Array(arrayLen: int = 200000):
    retVal = [rng02()]  # First value is the current value
    for x in range(arrayLen):  # Subsequent values are based on first value.
        retVal.append(rollNextRNG(retVal[x], 2))
    return retVal


def setTestRNG02():
    global baseValue
    key = baseValue + 0xD35EE0
    process.write(key, 3777588919)


def rng10():
    global baseValue
    return process.read(baseValue + 0xD35F00)


def rng10Array(arrayLen: int = 256):
    retVal = [rng10()]  # First value is the current value
    for x in range(arrayLen):  # Subsequent values are based on first value.
        retVal.append(rollNextRNG(lastRNG=retVal[x], index=10))
    return retVal


def nextChanceRNG10(dropChanceVal: int = 60) -> int:
    testArray = rng10Array()
    for i in range(len(testArray)):
        if i < 3:
            pass
        elif (testArray[i] & 0x7fffffff) % 255 < dropChanceVal:
            return (i - 3)


def nextChanceRNG10Full(dropChanceVal: int = 60) -> int:
    testArray = rng10Array()
    resultsArray = [False, False, False]
    for i in range(len(testArray)):
        if i < 3:
            pass
        elif (testArray[i] & 0x7fffffff) % 255 < dropChanceVal:
            resultsArray.append(True)
        else:
            resultsArray.append(False)
    return resultsArray


def nextChanceRNG10Calm() -> int:
    testArray = rng10Array()
    for i in range(len(testArray)):
        if i < 3:
            pass
        elif (testArray[i] & 0x7fffffff) % 255 >= 60 and (testArray[i + 3] & 0x7fffffff) % 255 < 60:
            return (i - 3)


def noChanceX3RNG10Highbridge() -> int:
    testArray = rng10Array()
    for i in range(len(testArray)):
        if i < 3:
            pass
        elif (testArray[i] & 0x7fffffff) % 255 < 30 and (testArray[i + 3] & 0x7fffffff) % 255 < 30 \
                and (testArray[i] & 0x7fffffff) % 255 < 30:
            return (i - 3)


def advanceRNG10():
    global baseValue
    key = baseValue + 0xD35F00
    process.write(key, rng10Array()[1])


def rng12():
    global baseValue
    return process.read(baseValue + 0xD35F08)


def rng12Array(advances: int = 255):
    retVal = [rng12()]  # First value is the current value
    for x in range(advances):  # Subsequent values are based on first value.
        retVal.append(rollNextRNG(retVal[x], 12))
    return retVal


def nextChanceRNG12(beforeNatus: bool = False) -> int:
    abilityMod = 13

    nextChance = 256
    if beforeNatus:
        ptr = 5
    else:
        ptr = 1
    testArray = rng12Array()
    while nextChance == 256:
        # Assume killer is aeon
        if ptr > 250:
            return 256
        elif (testArray[ptr + 1] & 0x7fffffff) % 2 == 1:  # equipment
            #print("RNG12 ptr: ", ptr)
            baseMod = (abilityMod + ((testArray[ptr + 3] & 0x7fffffff) & 7)) - 4
            abilities = (baseMod + ((baseMod >> 31) & 7)) >> 3

            if ptr == 1:
                if nextDropRNG13(abilities, beforeNatus):
                    print("Mark1")
                    nextChance = 0
                else:
                    print("Mark2")
                    nextChance = 1
                if beforeNatus:
                    nextChance += 1
            else:
                nextChance = int((ptr - 1) / 4)
        else:
            ptr += 4
    if beforeNatus:
        nextChance -= 1
    return int(nextChance)


def advanceRNG12():
    global baseValue
    key = baseValue + 0xD35F08
    process.write(key, rng12Array()[4])


def rng13():
    global baseValue
    return process.read(baseValue + 0xD35F0C)


def rng13Array(arrayLen: int = 20):
    retVal = [rng13()]  # First value is the current value
    for x in range(arrayLen):  # Subsequent values are based on first value.
        retVal.append(rollNextRNG(retVal[x], 13))
    return retVal


def nextDropRNG13(aSlots: int, beforeNatus: bool = False) -> int:
    outcomes = [4, 1, 1, 1, 2, 2, 3, 3]
    filledSlots = [9] * aSlots
    if beforeNatus:
        ptr = 2
    else:
        ptr = 1
    testArray = rng13Array()
    while 9 in filledSlots and ptr < 20:
        try:
            if outcomes[(((testArray[ptr] & 0x7fffffff) % 7) + 1)] in filledSlots:
                pass
            else:
                filledSlots.remove(9)
                filledSlots.append(
                    outcomes[(((testArray[ptr] & 0x7fffffff) % 7) + 1)])
        except Exception:
            pass
        ptr += 1

    #print("RNG13: ", filledSlots)

    if 1 in filledSlots:
        return True
    else:
        return False


def nextChanceRNG13() -> int:
    nextChance = 256
    outcomes = [4, 1, 1, 1, 2, 2, 3, 3]
    ptr = 1
    nextChance = 0
    testArray = rng13Array()
    while nextChance == 0:
        #print("RNG13 outcome: ", outcomes[(((testArray[ptr] & 0x7fffffff) % 7) + 1)])
        if outcomes[(((testArray[ptr] & 0x7fffffff) % 7) + 1)] == 1:
            nextChance = ptr
        else:
            ptr += 1
    print("Value found. ", ptr)
    return int(nextChance)


def advanceRNG13():
    global baseValue
    key = baseValue + 0xD35F0C
    process.write(key, rng13Array()[4])


def rng23():
    global baseValue
    return process.read(baseValue + 0xD35F16)


def rng23Array(arrayLen: int = 200):
    retVal = [rng23()]  # First value is the current value
    for x in range(arrayLen):  # Subsequent values are based on first value.
        retVal.append(rollNextRNG(retVal[x], 13))
    return retVal


def advanceRNG23():
    global baseValue
    key = baseValue + 0xD35F16
    process.write(key, rng23Array()[1])


def s32(integer: int) -> int:
    return ((integer & 0xffffffff) ^ 0x80000000) - 0x80000000


def rollNextRNG(lastRNG: int, index: int) -> int:
    """Returns a generator object that yields rng values
    for a given rng index.
    """
    rng_value = s32(lastRNG)
    rng_constant_1 = RNG_CONSTANTS_1[index]
    rng_constant_2 = RNG_CONSTANTS_2[index]

    new_value = s32(rng_value * rng_constant_1 ^ rng_constant_2)
    new_value = s32((new_value >> 0x10) + (new_value << 0x10))
    return new_value


def arenaArray():
    global baseValue
    retArray = []
    for i in range(104):
        key = baseValue + 0xD30C9C + i
        retArray.append(process.readBytes(key, 1))
    return retArray


def arenaFarmCheck(zone: str = "besaid", endGoal: int = 10, report=False, returnArray=False):
    import nemesis.menu as menu
    complete = True
    zone = zone.lower()
    if zone == "besaid":
        zoneIndexes = [8, 15, 27]
    if zone == "kilika":
        zoneIndexes = [21, 30, 38, 61]
    if zone == "miihen":
        zoneIndexes = [0, 9, 16, 22, 34, 47, 50, 62, 85]
    if zone == "mrr":
        zoneIndexes = [5, 23, 40, 51, 63, 91]
    if zone == "djose":
        zoneIndexes = [1, 10, 17, 28, 31, 79, 83]
    if zone == "tplains":
        zoneIndexes = [6, 24, 35, 52, 64, 76, 89, 87]
    if zone == "maclake":
        zoneIndexes = [3, 11, 18, 36]
    if zone == "macwoods":
        zoneIndexes = [2, 25, 32, 65, 71, 94]
    if zone == "bikanel":
        zoneIndexes = [12, 29, 41, 42, 53, 88]
    if zone == "calm":
        zoneIndexes = [4, 13, 19, 33, 55, 57, 72, 73, 80]
    if zone == "gagazet":
        zoneIndexes = [14, 20, 37, 39, 45, 46, 49, 58, 60, 69, 84, 86]
    if zone == "stolenfayth":
        zoneIndexes = [7, 26, 44, 48, 54, 66, 68, 92, 98]
    if zone == "justtonberry":
        zoneIndexes = [98]
    if zone == "sin1":
        zoneIndexes = [37]
    if zone == "sin2":
        zoneIndexes = [56, 70, 77, 78, 81, 93, 90, 97]
    if zone == "omega":
        zoneIndexes = [67, 74, 75, 82, 95, 96, 99, 100, 101, 102, 103]

    testArray = arenaArray()
    resultArray = []

    for i in range(len(zoneIndexes)):
        resultArray.append(testArray[zoneIndexes[i]])
        if testArray[zoneIndexes[i]] < endGoal:
            complete = False
    if report:
        print("############")
        print("Next Sphere Grid checkpoint:", gameVars.nemCheckpointAP())
        print("Tidus S.levels:", getTidusSlvl(), "- need levels:",
              menu.nextAPneeded(gameVars.nemCheckpointAP()))
        print("Number of captures in this zone:")
        print(resultArray)
        print("End goal is", endGoal,
              "minimum before leaving this zone for each index.")
        print("############")
    if returnArray:
        return resultArray
    else:
        return complete


def arenaCursor():
    global baseValue

    key = baseValue + 0x00D2A084
    status = process.readBytes(key, 2)
    return status


# Escape logic, and used for others

def rngFromIndex(index: int = 20):
    memTarget = 0xD35ED8 + (index * 0x4)
    global baseValue
    return process.read(baseValue + memTarget)


def rngArrayFromIndex(index: int = 20, arrayLen: int = 20):
    retVal = [rngFromIndex(index)]  # First value is the current value
    for x in range(arrayLen):  # Subsequent values are based on first value.
        retVal.append(rollNextRNG(retVal[x], index))
    retVal = [x & 0x7fffffff for x in retVal]  # Anding it because that's the value that's actually used
    return retVal


def advanceRNGindex(index: int = 43):
    global baseValue
    key = 0xD35ED8 + (index * 0x4)
    process.write(baseValue + key, rngArrayFromIndex(index=index)[1])


def nextSteal(stealCount:int=0, preAdvance:int=0):
    useArray = rngArrayFromIndex(index=10, arrayLen=1+preAdvance)
    stealRNG = useArray[1+preAdvance] % 255
    stealChance = 2 ** stealCount
    print("=== ", useArray[1], " === ", stealRNG, " < ", 255 // stealChance, " = ", stealRNG < (255 // stealChance))
    return stealRNG < (255 // stealChance)

def nextStealRare(preAdvance:int=0):
    useArray = rngArrayFromIndex(index=11, arrayLen=1+preAdvance)
    stealCritRNG = useArray[1+preAdvance] % 255
    return stealCritRNG < 32
