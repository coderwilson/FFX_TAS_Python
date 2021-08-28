import FFX_Xbox
import FFX_Screen
import time
import FFX_Logs
import FFX_memory

FFXC = FFX_Xbox.FFXC

def breakthrough(action):
    #Action == 1, pass.
    #Action == 2, shoot. Always attempt the first special kind of shot.
    print("Breakthrough")
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(1.5)
    if action == 2:
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(1.5)
    if action == 2:
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()

def halfOver():
    print("End of half")
    time.sleep(2)
    FFX_Xbox.menuB()
    time.sleep(2)
    FFX_Xbox.menuB()
    time.sleep(2)
    FFX_Xbox.menuB()
    time.sleep(2)
    FFX_Xbox.menuB()
    time.sleep(2)
    FFX_Xbox.menuB()

def checkResults():
    complete = 0
    while complete == 0:
        if FFX_Screen.PixelTest(961,423,(72, 54, 125)):
            complete = 1
        elif FFX_Screen.PixelTest(841,379,(221, 221, 221)) and FFX_Screen.PixelTest(723,383,(22, 22, 22)):
            complete = 2
        else:
            FFX_Xbox.menuA()
    return complete

def startHalf():
    print("Start of half")
    complete = 0
    while not FFX_Screen.PixelTest(1204,764,(0, 95, 134)): # Waiting for game to start
        if FFX_Screen.PixelTest(945,610,(234, 145, 0)): #Set techniques
            time.sleep(0.2)
            FFX_Xbox.menuA()
            time.sleep(0.2)
            FFX_Xbox.menuB()
        elif FFX_Screen.PixelTest(784,587,(234, 199, 0)): #Set Mark
            time.sleep(0.2)
            FFX_Xbox.menuA()
            time.sleep(0.2)
            FFX_Xbox.menuB()
        elif FFX_Screen.PixelTest(709,448,(164, 166, 164)):
            time.sleep(0.2)
            FFX_Xbox.menuB()
        elif FFX_Screen.PixelTest(729,611,(234, 143, 0)): #Assign roles (overtime)
            time.sleep(0.2)
            FFX_Xbox.menuA()
            time.sleep(0.2)
            FFX_Xbox.menuB()
        elif FFX_Screen.PixelTestTol(858,407,(217, 217, 217),5):
            FFX_Xbox.menuA()
            time.sleep(0.15)
            FFX_Xbox.menuDown()
            time.sleep(0.15)
            FFX_Xbox.menuB()
        else:
            FFX_Xbox.menuA()
        time.sleep(0.5)

def blitzMain():
    half = 1
    print("Clicking until Blitzball game starts")
    FFX_Screen.clickToPixel(1204,764,(0, 95, 134))
    
    
    #First half
    while not FFX_Screen.PixelTest(1235,154,(36, 220, 153)):
        #Check for breakthrough
        if FFX_Screen.PixelTest(345,99,(234, 192, 0)):
            breakthrough(1)
        elif FFX_Screen.PixelTest(1204,764,(0, 95, 134)):
            FFX_Xbox.menuB()
    
    half = 2
    halfOver()
    print("Skipping dialog, Wakka pumping up the team")
    FFX_Xbox.SkipDialog(10)
    FFX_Screen.clickToPixel(730,590,(0, 0, 0))
    
    #Second half (and overtime if needed)
    while not half == 0:
        startHalf()
        while not FFX_Screen.PixelTest(1235,154,(36, 220, 153)):
            #Check for breakthrough
            if FFX_Screen.PixelTest(345,99,(234, 192, 0)):
                if FFX_memory.blitzOppScore() == 0:
                    breakthrough(2)
                else:
                    breakthrough(1)
            elif FFX_Screen.PixelTest(1204,764,(0, 95, 134)):
                FFX_Xbox.menuB()
        halfOver()
        counter = 0
        while checkResults() == 0:
            counter += 1
            if counter % 100 == 0:
                print(checkResults)
            time.sleep(0.1)
        if checkResults() == 1:
            print("Game complete in ", half, "periods")
            FFX_Logs.writeStats("Blitz complete in number of periods:")
            FFX_Logs.writeStats(str(half))
            half = 0
            FFX_Xbox.menuA()
            FFX_Xbox.skipSave()
        elif checkResults() == 2 :
            half += 1
            FFX_Xbox.menuB()