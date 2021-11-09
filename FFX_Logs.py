import datetime
import time
game = "FFX_"
ext = ".txt"
fileName = "none"
fileStats = "none"
filePlot = "none"


def writeLog(message):
    print("Function no longer used")
    #global logFile
    #global fileName
    
    #logFile = open(fileName, "a")
    #logFile.write(message)
    #logFile.write("\n")
    #logFile.close()

def nextFile():
    print("Function no longer used")
    #global fileName
    #global game
    #global ext
    #if fileName == "none":
    #    timeNow = datetime.datetime.now()
    #    fileName = "Logs/" + game + str(timeNow.year) + str(timeNow.month) + str(timeNow.day) + "_" + str(timeNow.hour) + "_" + str(timeNow.minute) + "_" + str(timeNow.second) + ext
    #    
    #    global logFile
    #    logFile = open(fileName, "x")
    #    logFile.close()
    #    
    #    logFile = open(fileName, "a")
    #    logFile.write("New file is ready for writing!\n")
    #    logFile.write("\n")
    #    logFile.close()
    #    print("New file is ready for writing!\n")

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
    timeNow = datetime.datetime.now()
    fileStats = "Logs/" + game + "Stats_ " + str(rngSeedNum) + "_" + str(timeNow.year) + str(timeNow.month) + str(timeNow.day) + "_" + str(timeNow.hour) + "_" + str(timeNow.minute) + "_" + str(timeNow.second) + ext
    
    global statsFile
    statsFile = open(fileStats, "x")
    statsFile.close()
    
    statsFile = open(fileStats, "a")
    statsFile.write("Stats file is ready for writing!\n")
    statsFile.write("\n")
    statsFile.close()
    print("Stats file is ready for writing!\n")

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
        filePlot = "Logs/" + game + "Plot_ " + str(timeNow.year) + str(timeNow.month) + str(timeNow.day) + "_" + str(timeNow.hour) + "_" + str(timeNow.minute) + "_" + str(timeNow.second) + ext
        
        global plotFile
        plotFile = open(filePlot, "x")
        plotFile.close()
        
        plotFile = open(filePlot, "a")
        plotFile.write("plotting file is ready for writing!\n")
        plotFile.write("\n")
        plotFile.close()
        print("X/Y plotting file is ready for writing!\n")

def timeStamp():
    return datetime.datetime.now()