import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory

FFXC = FFX_Xbox.FFXC

def arrival():
    FFX_memory.clickToControl()
    wakkaLateMenu = FFX_menu.mrrGrid1()
    FFX_Screen.mrrFormat()
    FFX_Xbox.menuA()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3.7)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0) #In position
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', -1) #Turning
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.035)
    FFXC.set_value('AxisLy', 0) #Positioned and turned
    FFXC.set_value('AxisLx', 0)
    claskoSkip = True
    if FFX_memory.userControl():
        print("Skip successful.")
        time.sleep(2)
        FFX_Xbox.menuB() #Engage skip
        cam = FFX_memory.getCamera()
        startTime = time.time()
        timeLimit = 60 #Max number of seconds that we will wait for the skip to occur.
        maxTime = startTime + timeLimit
        while cam[0] < 0.77:
            cam = FFX_memory.getCamera()
            currentTime = time.time()
            if currentTime > maxTime:
                print("Skip failed for some reason. Moving on without skip.")
                claskoSkip = False
                break
        FFX_memory.clickToControl()
        FFXC.set_value('AxisLy', 0) #Skip should have committed.
        FFXC.set_value('AxisLx', 0) #Otherwise, backup pathing will take over.
    
    else:
        print("We got in battle before attempting the skip. Going to try one more time.")
        FFX_Battle.fleeAll()
        FFX_memory.clickToControl()
        
        pos = FFX_memory.getCoords()
        while pos[1] < -630:
            FFXC.set_value('AxisLy', 1)
            FFXC.set_value('AxisLx', 0)
            pos = FFX_memory.getCoords()
        FFXC.set_value('AxisLy', 0)
        FFXC.set_value('AxisLx', -1)
        time.sleep(1.5)
        FFXC.set_value('AxisLy', 0) #In position
        FFXC.set_value('AxisLx', 0)
        time.sleep(0.3)
        FFXC.set_value('AxisLy', -1) #Turning
        FFXC.set_value('AxisLx', 1)
        time.sleep(0.035)
        FFXC.set_value('AxisLy', 0) #Positioned and turned
        FFXC.set_value('AxisLx', 0)
        time.sleep(3)
        if FFX_memory.userControl():
            print("Skip successful.")
            FFX_Xbox.menuB() #Engage skip
            cam = FFX_memory.getCamera()
            startTime = time.time()
            timeLimit = 30 #Max number of seconds that we will wait for the skip to occur.
            FFXC.set_value('AxisLy', 1) #Just in case we get stuck somehow.
            FFXC.set_value('AxisLx', 1)
            maxTime = startTime + timeLimit
            while cam[0] < 0.77:
                cam = FFX_memory.getCamera()
                currentTime = time.time()
                if currentTime > maxTime:
                    print("Skip failed for some reason. Moving on without skip.")
                    claskoSkip = False
                    break
            FFX_memory.clickToControl()
            FFXC.set_value('AxisLy', 0) #Skip should have committed.
            FFXC.set_value('AxisLx', 0) #Otherwise, backup pathing will take over.
        else:
            print("Failed the skip twice. Going old-school backup strats.")
    FFX_Logs.writeStats("Clasko Skip success:")
    FFX_Logs.writeStats(claskoSkip)
    checkpoint = 0
    lastCP = 0
    while checkpoint != 100:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            pos = FFX_memory.getCoords()
            cam = FFX_memory.getCamera()
            mapVal = FFX_memory.getMap()
            if mapVal == 92:
                checkpoint = 100
            elif checkpoint == 0:
                if pos[1] > -570:
                    checkpoint = 20
                    #print("Possible skip here, refactor later.")
                elif cam[0] > 1:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 1)
                elif cam[0] > 0.6:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20:
                if mapVal == 92:
                    checkpoint = 100
                elif cam[0] > 1.5:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((-0.55 * pos[0]) -529.64):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
                elif cam[0] > 1:
                    if pos[1] > -490 and pos[0] > -55:
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 1)
                elif cam[0] > 0.6:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > -490 and pos[0] > -55:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
                else:
                    if pos[1] > -490 and pos[0] > -55:
                        FFXC.set_value('AxisLy', 0)
                    else:
                        FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 30:
                if FFX_memory.getMap() == 92:
                    checkpoint = 100
                elif cam[0] > 1:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
                elif cam[0] > 0.6:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
        elif FFX_Screen.BattleScreen():
            print("Starting battle MRR (preload)")
            FFX_Battle.fleeAll()
            FFX_memory.clickToControl()
            hpCheck = FFX_memory.getHP()
            print(hpCheck)
            if hpCheck[0] != 520 or hpCheck[3] != 644 or hpCheck[2] != 1030:
                FFX_Battle.healUp(3)
            else:
                print("No need to heal up. Moving onward.")
        elif FFX_Screen.BattleComplete():
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            FFX_Xbox.menuB()
        else:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    return wakkaLateMenu

def mainPath(wakkaLateMenu):
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.7)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2.5)
    FFX_Xbox.SkipDialog(3) #Up the first lift
    FFXC.set_value('AxisLx', 0)
    
    status = [0, 0, 0, 1, 0]
    #Yuna complete, Kimahri complete, Valefor overdrive, Battle counter, Yuna level up complete]
    #kimahriComplete = 0
    #yunaComplete = 0
    #yunaEarlyLevels = 0
    #battleCounter = 0
    checkpoint = 0
    lastCP = 0
    #valeforDrive = 0
    
    while checkpoint != 1000:
        if lastCP != checkpoint:
            lastCP = checkpoint
            print("Checkpoint reached: ", checkpoint)
        if FFX_Screen.BattleScreen():
            print("Starting battle MRR (preload)")
            if status[0] == 1 and status[1] == 1 and status[2] == 2:
                FFX_Battle.fleeAll()
                FFX_memory.clickToControl()
            else:
                print("Starting battle MRR")
                status = FFX_Battle.MRRbattle(status)
                print("Status update: ", status)
                #print("Yuna Complete state: ", status[0])
                #print("Kimahri Complete state: ", status[1])
            status[3] += 1
            
            if wakkaLateMenu == True and FFX_memory.getSLVLWakka() >= 3:
                wakkaLateMenu = FFX_menu.mrrGrid2(wakkaLateMenu)
            elif FFX_memory.getYunaSlvl() >= 8 and status[4] == 0:
                print("Yuna has enough levels now. Going to do her grid.")
                FFX_menu.mrrGridYuna()
                print("Yuna's gridding is complete for now.")
                status[4] = 1
        else:
            #print("Checkpoint: ", checkpoint)
            pos = FFX_memory.getCoords()
            if pos == [0.0,0.0]: #This means we've lost control of the character for any reason.
                if checkpoint == 80 and FFX_Screen.PixelTestTol(676,444,(212, 212, 212),5):
                    print("1000 gil chest")
                    time.sleep(0.6)
                    FFX_Xbox.menuB()
                    checkpoint = 90
                else:
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', 0)
                    #if checkpoint == 0:
                    #    FFX_Xbox.menuB()
            elif checkpoint == 0:
                if pos[1] > -540:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10:
                if pos[1] > -460:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] > -108:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20:
                if pos[0] > -85:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 30:
                if pos[1] > -370:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLy', 1) #Overlook > rest of the path
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 40:
                if pos[0] > 50:
                    checkpoint = 50
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[0] > -50:
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 50:
                if pos[1] > -277:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 118:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60:
                if pos[1] > -140:
                    checkpoint = 70
                    # 70 - Get the chest
                    # 100 - Skip past the chest with the money
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 130:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 70:
                if pos[1] > -29:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] > 90:
                        FFXC.set_value('AxisLx', -1)
                    elif pos[0] < 85:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 80:
                FFX_Xbox.menuB()
            elif checkpoint == 90:
                if pos[1] < -115:
                    checkpoint = 100
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 100:
                if pos[0] < -40:
                    checkpoint = 110
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[0] > 90:
                        FFXC.set_value('AxisLy', 0)
                    elif pos[1] > -210:
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 110:
                if pos[1] > 60:
                    checkpoint = 120
                else:
                    FFXC.set_value('AxisLy', 1) #Long path north
                    if pos[0] > -100:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 120:
                if pos[0] > 30:
                    checkpoint = 130
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] < 130:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 130:
                if pos[1] > 230:
                    checkpoint = 140
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 140:
                if pos[0] < -87:
                    checkpoint = 150
                else:
                    FFXC.set_value('AxisLx', -1) #Chocobo before Shedinja
                    if pos[1] < 275:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 150:
                if pos[1] > 380:
                    checkpoint = 160
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 160:
                if pos[0] > 20:
                    checkpoint = 170
                else:
                    FFXC.set_value('AxisLx', 1) #Away from Shedinja.
                    if pos[1] < 440:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 170:
                if pos[1] > 515:
                    checkpoint = 180
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 180:
                if pos[0] < 55:
                    checkpoint = 190
                else:
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 190:
                if pos[0] < -70:
                    checkpoint = 200
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] > 580:
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 200:
                if pos[1] > 675:
                    checkpoint = 210
                else:
                    FFXC.set_value('AxisLy', 1) #Past the chest (near the end)
                    if pos[0] > -109:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 210:
                if pos[1] > 833:
                    checkpoint = 215
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < -60:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 215: #Delay based on statuses
                if status[0] == 1 and status[1] == 1 and status[2] == 2:
                    checkpoint = 220
                else:
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(0.8)
                    FFXC.set_value('AxisLy', -1)
                    time.sleep(0.8)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 220:
                if pos[0] > 1:
                    checkpoint = 230
                else:
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 230:
                if pos[0] > 35:
                    checkpoint = 240
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] > 815:
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 240:
                if pos[1] > 845:
                    checkpoint = 250
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 45:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 250: #Map to Map lift
                if pos[0] < 65 and pos[1] > 895:
                    FFX_Xbox.menuB() #We have hit the lift
                    time.sleep(0.5)
                    checkpoint = 260
                else:
                    if pos[0] > 65:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
                    if pos[1] < 895:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 260:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.7)
                FFXC.set_value('AxisLx', 0)
                time.sleep(4)
                FFXC.set_value('AxisLx', -1)
                time.sleep(1.5)
                checkpoint = 270
            elif checkpoint == 270:
                if pos[1] > 200:
                    checkpoint = 280
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 280:
                if pos[0] < 83:
                    checkpoint = 290
                else:
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 290:
                if pos[1] > 215:
                    FFX_Xbox.SkipDialog(0.5)
                    checkpoint = 300
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 300:
                if pos[0] > 150:
                    checkpoint = 320
                else:
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 320:
                if pos[0] > 222:
                    checkpoint = 330
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] > 255:
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 330:
                if pos[1] < 172:
                    checkpoint = 340
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 340:
                if pos[0] > 270:
                    checkpoint = 350
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] < 167 and pos[0] < 245:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 350:
                FFX_Xbox.SkipDialog(2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                FFX_memory.awaitControl()
                FFXC.set_value('AxisLy', -1)
                time.sleep(2.5)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                print("End of MRR pathing section.")
                checkpoint = 1000
    print("End of MRR section. Status:")
    print(status)

def battleSite():
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    print("Starting battle site section")
    FFX_menu.battleSiteGrid()
    FFXC.set_value('AxisLy', -1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    if FFX_memory.userControl():
        print("Clasko skip was successful earlier. Pathing appropriately.")
        FFXC.set_value('AxisLy', -1)
        FFXC.set_value('AxisLx', 1)
        time.sleep(2)
        FFXC.set_value('AxisLy', 0)
        time.sleep(6)
        FFXC.set_value('AxisLy', 1)
        FFXC.set_value('AxisLx', 1)
        FFX_Xbox.SkipDialog(10)
        FFXC.set_value('AxisLy', 0)
        FFXC.set_value('AxisLx', 0)
    else:
        print("Clasko skip was not successful. Slower method.")
        FFX_memory.clickToControl() #Scene where Wakka kicks a cannon
        FFXC.set_value('AxisLy', -1)
        FFXC.set_value('AxisLx', 1)
        time.sleep(4)
        FFXC.set_value('AxisLy', 0)
        time.sleep(6)
        FFXC.set_value('AxisLy', 1)
        FFXC.set_value('AxisLx', 1)
        FFX_Xbox.SkipDialog(10)
        FFXC.set_value('AxisLy', 0)
        FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToMap1() #The command center is that way.
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(7)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2.6)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.5)
    
    pos = FFX_memory.getCoords()
    while pos[1] < 3260: #Towards O'aka
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 1)
        pos = FFX_memory.getCoords()
    
    while FFX_memory.userControl(): #Talk to O'aka
        if pos[0] < -50:
            FFXC.set_value('AxisLx', 1)
        elif pos[0] > -45:
            FFXC.set_value('AxisLx', -1)
        else:
            FFXC.set_value('AxisLx', 0)
        if pos[1] < 3425:
            FFXC.set_value('AxisLy', 1)
            FFX_Xbox.menuB()
        else:
            FFXC.set_value('AxisLy', -1)
            FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_menu.battleSiteOaka()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.touchSaveSphere()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.6)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFX_Screen.clickToMap1()
    time.sleep(0.7)
    FFXC.set_value('AxisLy', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl() #Meeting Kinoc
    
    
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.2)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3.4)
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl(): #Are you ready? (that guy)
        if pos[0] < 218:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', -1)
        if pos[1] < 3127:
            FFXC.set_value('AxisLy', 1)
        else:
            FFXC.set_value('AxisLy', -1)
        FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
        
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.awaitPixel(680,804,(221,221,221)) ### Possible to replace this later?
    time.sleep(1.6)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    
    status = FFX_Battle.battleGui()
    FFX_Xbox.SkipDialog(10)
    FFX_Xbox.skipSceneSpec()
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLx', -1)
    time.sleep(7)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    FFX_Xbox.SkipDialog(8)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToMap1() #Skips a ton of monologuing and memories
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3.8)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.touchSaveSphere()
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToMap1() #Was it worth it scene
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToMap1() #Talking to Auron
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(6)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.5)
    pos = FFX_memory.getCoords()
    while pos[0] < ((0.05 * pos[1]) + 942.12):
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(5.5)
    FFXC.set_value('AxisLy', 0)
    
    return 1