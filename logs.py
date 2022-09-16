import datetime
import memory
try:
    from memory import baseValue
except Exception:
    baseValue = 0x0
game = "FFX_"
ext = ".txt"
fileName = "none"
fileStats = "none"
filePlot = "none"
fileMemChange = "none"
fileRNG = "none"


def writeStats(message):
    global statsFile
    global fileStats

    statsFile = open(fileStats, "a")
    statsFile.write(str(message))
    statsFile.write("\n")
    statsFile.close()


def nextStats(rngSeedNum):
    global fileStats
    global game
    global ext
    if fileStats == "none":
        timeNow = datetime.datetime.now()
        fileStats = "Logs/" + game + "Stats_ " + str(rngSeedNum) + "_" + str(timeNow.year) + str(timeNow.month) + str(
            timeNow.day) + "_" + str(timeNow.hour) + "_" + str(timeNow.minute) + "_" + str(timeNow.second) + ext

        global statsFile
        statsFile = open(fileStats, "x")
        statsFile.close()

        statsFile = open(fileStats, "a")
        statsFile.write("Stats file is ready for writing!\n")
        statsFile.write("\n")
        statsFile.close()
    print("Stats file is ready for writing!\n")


def resetStatsLog():
    global fileStats
    fileStats = "none"


def writePlot(message):
    global plotFile
    global filePlot

    plotFile = open(filePlot, "a")
    plotFile.write(str(message))
    plotFile.write("\n")
    plotFile.close()


def nextPlot():
    global filePlot
    global game
    global ext
    if filePlot == "none":
        timeNow = datetime.datetime.now()
        filePlot = "Logs/" + game + "Plot_ " + str(timeNow.year) + str(timeNow.month) + str(
            timeNow.day) + "_" + str(timeNow.hour) + "_" + str(timeNow.minute) + "_" + str(timeNow.second) + ext

        global plotFile
        plotFile = open(filePlot, "x")
        plotFile.close()

        plotFile = open(filePlot, "a")
        plotFile.write("plotting file is ready for writing!\n")
        plotFile.write("\n")
        plotFile.close()
        print("X/Y plotting file is ready for writing!\n")


def writeMemChange(message):
    global memChangeFile
    global fileMemChange

    memChangeFile = open(fileMemChange, "a")
    memChangeFile.write(str(message))
    memChangeFile.write("\n")
    memChangeFile.close()


def openRNGTrack():
    global fileRNG
    global game
    global ext
    timeNow = datetime.datetime.now()
    fileRNG = "Logs/" + game + "RNG_ " + str(timeNow.year) + str(timeNow.month) + str(
        timeNow.day) + "_" + str(timeNow.hour) + "_" + str(timeNow.minute) + "_" + str(timeNow.second) + ext

    global RNGFile
    try:
        RNGFile = open(fileRNG, "a")
    except Exception:
        RNGFile = open(fileRNG, "x")
    RNGFile.close()

    RNGFile = open(fileRNG, "a")
    RNGFile.write("RNG log is ready for writing!\n")
    RNGFile.write("\n")
    RNGFile.close()
    print("RNG log is ready for writing!\n")


def writeRNGTrack(message):
    global RNGFile
    global fileRNG

    RNGFile = open(fileRNG, "a")
    RNGFile.write(str(message))
    RNGFile.write("\n")
    RNGFile.close()


class memChangeMonitor:
    def __init__(self, baseOffsetRef, isPointerRef=False, ptrOffsetRef=0x0, typeRef='4byte', childReport: int = 0):
        self.isPointer = isPointerRef
        self.baseOffset = baseOffsetRef
        if self.isPointer:
            self.ptrOffset = ptrOffsetRef
        self.varType = typeRef
        self.key = baseValue + 0x003988a5

        self.setLastValue()

        if childReport != 0:
            self.reportOnChild = False
        else:
            self.reportOnChild = True
            self.childHandle = memChangeMonitor(
                self.baseOffset, True, self.ptrOffset, self.typeRef, 0)

    def setLastValue(self):
        if self.isPointer:
            ptrRef = memory.readBytes(key, 4)

            if self.varType == 'byte':
                self.lastValue = memory.readBytes(
                    ptrRef + self.ptrOffset, 1)
            elif self.varType == '2byte':
                self.lastValue = memory.readBytes(
                    ptrRef + self.ptrOffset, 2)
            elif self.varType == '4byte':
                self.lastValue = memory.readBytes(
                    ptrRef + self.ptrOffset, 4)
            elif self.varType == 'float':
                self.lastValue = memory.float_from_integer(
                    memory.readBytes(ptrRef + self.ptrOffset, 4))
        else:
            if self.varType == 'byte':
                self.lastValue = memory.readBytes(key, 1)
            elif self.varType == '2byte':
                self.lastValue = memory.readBytes(key, 2)
            elif self.varType == '4byte':
                self.lastValue = memory.readBytes(key, 4)
            elif self.varType == 'float':
                self.lastValue = memory.float_from_integer(
                    memory.readBytes(key, 4))

    def reportIfChange(self):
        if self.checkChange():
            if self.reportOnChild:
                writeMemChange("Value changed (parent)")
            else:
                writeMemChange("Value changed")
            writeMemChange("Base offset: " + str(self.baseOffset))
            writeMemChange("Pointer value: " + str(self.isPointer))
            if self.isPointer:
                writeMemChange("Pointer offset: " + str(self.pointerOffset))
            writeMemChange("Type of variable: " + str(self.varType))
            writeMemChange("Previous value: " + self. lastValue)
            writeMemChange("Updated value: " + self.getNewValue())
            writeMemChange("Time of change: " + timeStamp())
            writeMemChange("?? Game state ??")
            writeMemChange("Story progress: " + str(memory.getStoryProgress()))
            writeMemChange("Current map: " + str(memory.getMap()))
            writeMemChange("Battle Active: " + str(memory.battleActive()))

            writeMemChange("----------------------------")
            if self.reportOnChild:
                self.childHandle.forceReportChild()
            self.setLastValue()

    def forceReportChild(self):
        writeMemChange("Value changed (child)")
        writeMemChange("Base offset: " + str(self.baseOffset))
        writeMemChange("Pointer value: " + str(self.isPointer))
        if self.isPointer:
            writeMemChange("Pointer offset: " + str(self.pointerOffset))
        writeMemChange("Type of variable: " + str(self.varType))
        writeMemChange("Previous value: " + self. lastValue)
        writeMemChange("Updated value: " + self.getNewValue())
        writeMemChange("Time of change: " + timeStamp())
        writeMemChange("?? Game state ??")
        writeMemChange("Story progress: " + str(memory.getStoryProgress()))
        writeMemChange("Current map: " + str(memory.getMap()))
        writeMemChange("Battle Active: " + str(memory.battleActive()))
        writeMemChange("----------------------------")
        self.setLastValue()

    def forceReport(self):
        writeMemChange("Value force-reported")
        writeMemChange("Base offset: " + str(self.baseOffset))
        writeMemChange("Pointer value: " + str(self.isPointer))
        if self.isPointer:
            writeMemChange("Pointer offset: " + str(self.pointerOffset))
        writeMemChange("Type of variable: " + str(self.varType))
        writeMemChange("Previous value: " + self. lastValue)
        writeMemChange("Updated value: " + self.getNewValue())
        writeMemChange("Time of change: " + timeStamp())
        writeMemChange("?? Game state ??")
        writeMemChange("Story progress: " + str(memory.getStoryProgress()))
        writeMemChange("Current map: " + str(memory.getMap()))
        writeMemChange("Battle Active: " + str(memory.battleActive()))
        writeMemChange("----------------------------")
        self.setLastValue()

    def checkChange(self):
        if self.isPointer:
            ptrRef = memory.readBytes(key, 4)

            if self.varType == 'byte':
                if self.lastValue != memory.readBytes(ptrRef + self.ptrOffset, 1):
                    return True
            elif self.varType == '2byte':
                if self.lastValue != memory.readBytes(ptrRef + self.ptrOffset, 2):
                    return True
            elif self.varType == '4byte':
                if self.lastValue != memory.readBytes(ptrRef + self.ptrOffset, 4):
                    return True
            elif self.varType == 'float':
                if self.lastValue != memory.float_from_integer(memory.readBytes(ptrRef + self.ptrOffset, 4)):
                    return True
            return False
        else:
            if self.varType == 'byte':
                if self.lastValue != memory.readBytes(key, 1):
                    return True
            elif self.varType == '2byte':
                if self.lastValue != memory.readBytes(key, 2):
                    return True
            elif self.varType == '4byte':
                if self.lastValue != memory.readBytes(key, 4):
                    return True
            elif self.varType == 'float':
                if self.lastValue != memory.float_from_integer(memory.readBytes(key, 4)):
                    return True
            return False


def memChangeList():
    # Base offset, pointer (True/False), pointer offset, type to be returned
    # Fifth element is to report on another offset, only works for pointers.
    # Types can be '1byte', '2byte', '4byte', or 'float'
    fullList = [
        [0x8E9004, True, 0x1c, '4byte', 0x8],
        [0x8E9004, True, 0x1c, '4byte', 0xc]
    ]

    return fullList


def memChangeHandle():
    retArray = [0]
    firstEle = True
    memRefList = memChangeList()

    while len(baseArray) != 0:
        if firstEle:
            firstEle = False
            variables = memRefList.pop()
            retArray[0] = memChangeMonitor(baseOffsetRef=variables[0], isPointerRef=variables[1],
                                           ptrOffsetRef=variables[2], typeRef=variables[3], childReport=variables[4])
        else:
            variables = memRefList.pop()
            retArray.append(memChangeMonitor(baseOffsetRef=variables[0], isPointerRef=variables[1],
                                             ptrOffsetRef=variables[2], typeRef=variables[3], childReport=variables[4]))
    return retArray


def timeStamp():
    return datetime.datetime.now()
