import datetime

import memory.main

try:
    from memory.main import baseValue
except Exception:
    baseValue = 0x0
game = "FFX_"
ext = ".txt"
fileName = "none"
fileStats = "none"
filePlot = "none"
fileMemChange = "none"
fileRNG = "none"


def write_stats(message):
    global statsFile
    global fileStats

    statsFile = open(fileStats, "a")
    statsFile.write(str(message))
    statsFile.write("\n")
    statsFile.close()


def next_stats(rng_seed_num):
    global fileStats
    global game
    global ext
    if fileStats == "none":
        timeNow = datetime.datetime.now()
        fileStats = (
            "logs/"
            + game
            + "Stats_ "
            + str(rng_seed_num)
            + "_"
            + str(timeNow.year)
            + str(timeNow.month)
            + str(timeNow.day)
            + "_"
            + str(timeNow.hour)
            + "_"
            + str(timeNow.minute)
            + "_"
            + str(timeNow.second)
            + ext
        )

        global statsFile
        statsFile = open(fileStats, "x")
        statsFile.close()

        statsFile = open(fileStats, "a")
        statsFile.write("Stats file is ready for writing!\n")
        statsFile.write("\n")
        statsFile.close()
    print("Stats file is ready for writing!\n")


def reset_stats_log():
    global fileStats
    fileStats = "none"


def write_plot(message):
    global plotFile
    global filePlot

    plotFile = open(filePlot, "a")
    plotFile.write(str(message))
    plotFile.write("\n")
    plotFile.close()


def next_plot():
    global filePlot
    global game
    global ext
    if filePlot == "none":
        timeNow = datetime.datetime.now()
        filePlot = (
            "logs/"
            + game
            + "Plot_ "
            + str(timeNow.year)
            + str(timeNow.month)
            + str(timeNow.day)
            + "_"
            + str(timeNow.hour)
            + "_"
            + str(timeNow.minute)
            + "_"
            + str(timeNow.second)
            + ext
        )

        global plotFile
        plotFile = open(filePlot, "x")
        plotFile.close()

        plotFile = open(filePlot, "a")
        plotFile.write("plotting file is ready for writing!\n")
        plotFile.write("\n")
        plotFile.close()
        print("X/Y plotting file is ready for writing!\n")


def write_mem_change(message):
    global memChangeFile
    global fileMemChange

    memChangeFile = open(fileMemChange, "a")
    memChangeFile.write(str(message))
    memChangeFile.write("\n")
    memChangeFile.close()


def open_rng_track():
    global fileRNG
    global game
    global ext
    timeNow = datetime.datetime.now()
    fileRNG = (
        "logs/"
        + game
        + "RNG_ "
        + str(timeNow.year)
        + str(timeNow.month)
        + str(timeNow.day)
        + "_"
        + str(timeNow.hour)
        + "_"
        + str(timeNow.minute)
        + "_"
        + str(timeNow.second)
        + ext
    )

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


def write_rng_track(message):
    global RNGFile
    global fileRNG

    RNGFile = open(fileRNG, "a")
    RNGFile.write(str(message))
    RNGFile.write("\n")
    RNGFile.close()


class MemChangeMonitor:
    def __init__(
        self,
        baseOffsetRef,
        isPointerRef=False,
        ptrOffsetRef=0x0,
        typeRef="4byte",
        childReport: int = 0,
    ):
        self.isPointer = isPointerRef
        self.baseOffset = baseOffsetRef
        if self.isPointer:
            self.ptrOffset = ptrOffsetRef
        self.varType = typeRef
        self.key = baseValue + 0x003988A5

        self.set_last_value()

        if childReport != 0:
            self.reportOnChild = False
        else:
            self.reportOnChild = True
            self.childHandle = MemChangeMonitor(
                self.baseOffset, True, self.ptrOffset, self.typeRef, 0
            )

    def set_last_value(self):
        if self.isPointer:
            ptrRef = memory.main.read_bytes(key, 4)

            if self.varType == "byte":
                self.lastValue = memory.main.read_bytes(ptrRef + self.ptrOffset, 1)
            elif self.varType == "2byte":
                self.lastValue = memory.main.read_bytes(ptrRef + self.ptrOffset, 2)
            elif self.varType == "4byte":
                self.lastValue = memory.main.read_bytes(ptrRef + self.ptrOffset, 4)
            elif self.varType == "float":
                self.lastValue = memory.main.float_from_integer(
                    memory.main.read_bytes(ptrRef + self.ptrOffset, 4)
                )
        else:
            if self.varType == "byte":
                self.lastValue = memory.main.read_bytes(key, 1)
            elif self.varType == "2byte":
                self.lastValue = memory.main.read_bytes(key, 2)
            elif self.varType == "4byte":
                self.lastValue = memory.main.read_bytes(key, 4)
            elif self.varType == "float":
                self.lastValue = memory.main.float_from_integer(
                    memory.main.read_bytes(key, 4)
                )

    def report_if_change(self):
        if self.check_change():
            if self.reportOnChild:
                write_mem_change("Value changed (parent)")
            else:
                write_mem_change("Value changed")
            write_mem_change("Base offset: " + str(self.baseOffset))
            write_mem_change("Pointer value: " + str(self.isPointer))
            if self.isPointer:
                write_mem_change("Pointer offset: " + str(self.pointerOffset))
            write_mem_change("Type of variable: " + str(self.varType))
            write_mem_change("Previous value: " + self.lastValue)
            write_mem_change("Updated value: " + self.getNewValue())
            write_mem_change("Time of change: " + time_stamp())
            write_mem_change("?? Game state ??")
            write_mem_change("Story progress: " + str(memory.main.get_story_progress()))
            write_mem_change("Current map: " + str(memory.main.get_map()))
            write_mem_change("Battle Active: " + str(memory.main.battle_active()))

            write_mem_change("----------------------------")
            if self.reportOnChild:
                self.childHandle.force_report_child()
            self.set_last_value()

    def force_report_child(self):
        write_mem_change("Value changed (child)")
        write_mem_change("Base offset: " + str(self.baseOffset))
        write_mem_change("Pointer value: " + str(self.isPointer))
        if self.isPointer:
            write_mem_change("Pointer offset: " + str(self.pointerOffset))
        write_mem_change("Type of variable: " + str(self.varType))
        write_mem_change("Previous value: " + self.lastValue)
        write_mem_change("Updated value: " + self.getNewValue())
        write_mem_change("Time of change: " + time_stamp())
        write_mem_change("?? Game state ??")
        write_mem_change("Story progress: " + str(memory.main.get_story_progress()))
        write_mem_change("Current map: " + str(memory.main.get_map()))
        write_mem_change("Battle Active: " + str(memory.main.battle_active()))
        write_mem_change("----------------------------")
        self.set_last_value()

    def force_report(self):
        write_mem_change("Value force-reported")
        write_mem_change("Base offset: " + str(self.baseOffset))
        write_mem_change("Pointer value: " + str(self.isPointer))
        if self.isPointer:
            write_mem_change("Pointer offset: " + str(self.pointerOffset))
        write_mem_change("Type of variable: " + str(self.varType))
        write_mem_change("Previous value: " + self.lastValue)
        write_mem_change("Updated value: " + self.getNewValue())
        write_mem_change("Time of change: " + time_stamp())
        write_mem_change("?? Game state ??")
        write_mem_change("Story progress: " + str(memory.main.get_story_progress()))
        write_mem_change("Current map: " + str(memory.main.get_map()))
        write_mem_change("Battle Active: " + str(memory.main.battle_active()))
        write_mem_change("----------------------------")
        self.set_last_value()

    def check_change(self):
        if self.isPointer:
            ptrRef = memory.main.read_bytes(key, 4)

            if self.varType == "byte":
                if self.lastValue != memory.main.read_bytes(ptrRef + self.ptrOffset, 1):
                    return True
            elif self.varType == "2byte":
                if self.lastValue != memory.main.read_bytes(ptrRef + self.ptrOffset, 2):
                    return True
            elif self.varType == "4byte":
                if self.lastValue != memory.main.read_bytes(ptrRef + self.ptrOffset, 4):
                    return True
            elif self.varType == "float":
                if self.lastValue != memory.main.float_from_integer(
                    memory.main.read_bytes(ptrRef + self.ptrOffset, 4)
                ):
                    return True
            return False
        else:
            if self.varType == "byte":
                if self.lastValue != memory.main.read_bytes(key, 1):
                    return True
            elif self.varType == "2byte":
                if self.lastValue != memory.main.read_bytes(key, 2):
                    return True
            elif self.varType == "4byte":
                if self.lastValue != memory.main.read_bytes(key, 4):
                    return True
            elif self.varType == "float":
                if self.lastValue != memory.main.float_from_integer(
                    memory.main.read_bytes(key, 4)
                ):
                    return True
            return False


def mem_change_list():
    # Base offset, pointer (True/False), pointer offset, type to be returned
    # Fifth element is to report on another offset, only works for pointers.
    # Types can be '1byte', '2byte', '4byte', or 'float'
    fullList = [
        [0x8E9004, True, 0x1C, "4byte", 0x8],
        [0x8E9004, True, 0x1C, "4byte", 0xC],
    ]

    return fullList


def mem_change_handle():
    retArray = [0]
    firstEle = True
    memRefList = mem_change_list()

    while len(baseArray) != 0:
        if firstEle:
            firstEle = False
            variables = memRefList.pop()
            retArray[0] = MemChangeMonitor(
                baseOffsetRef=variables[0],
                isPointerRef=variables[1],
                ptrOffsetRef=variables[2],
                typeRef=variables[3],
                childReport=variables[4],
            )
        else:
            variables = memRefList.pop()
            retArray.append(
                MemChangeMonitor(
                    baseOffsetRef=variables[0],
                    isPointerRef=variables[1],
                    ptrOffsetRef=variables[2],
                    typeRef=variables[3],
                    childReport=variables[4],
                )
            )
    return retArray


def time_stamp():
    return datetime.datetime.now()
