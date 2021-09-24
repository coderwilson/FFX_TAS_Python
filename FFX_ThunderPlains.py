import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory

FFXC = FFX_Xbox.FFXC
 
def southPathing(blitzwin):
    FFX_memory.clickToControl()
    print("Start of the Thunder Plains section")
    checkpoint = 0
    stepCount = 0
    stepMax = 500
    complete = 0
    status = [False,False,False,False] #Rikku charged, Light Curtain, Lunar Curtain, Grenade Thrown
    status[2] = blitzwin
    speedcount = FFX_memory.getSpeed()
    if speedcount >= 14:
        status[3] = True
    FFX_memory.fullPartyFormat_New('postbunyip', 11)
    while complete == 0:
        if FFX_Screen.dodgeLightning():
            print("Dodge")
        if FFX_memory.userControl():
            pos = FFX_memory.getCoords()
            stepCount += 1
            if checkpoint == 0:
                if pos[1] > -800:
                    checkpoint = 1
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] > 15:
                        FFXC.set_value('AxisLx', 0)
                    else:
                        FFXC.set_value('AxisLx', 1)
            elif checkpoint == 1:
                if pos[1] > -600:
                    checkpoint = 2
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] > 0:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 2:
                if pos[1] > 700:
                    checkpoint = 3
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < -30:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 12:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 3:
                if FFX_memory.getMap() == 256:
                    checkpoint = 4
                    print("End of the southern section.")
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 70:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 4:
                FFXC.set_value('AxisLy', 1)
                FFX_Xbox.SkipDialog(0.5)
                FFXC.set_value('AxisLx', -1)
                FFX_Xbox.SkipDialog(10)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                complete = 1
            
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()
            if FFX_Screen.BattleScreen():
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                print("Starting battle")
                status = FFX_Battle.thunderPlains(status, 1)
            elif FFX_Screen.BattleComplete():
                FFX_Xbox.menuB()
    return status
    
def agency(blitzWin):
    #Arrive at the travel agency
    FFX_memory.clickToControl3()
    speedCount = FFX_memory.getSpeed()
    
    #Talk to the lady
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.SkipDialog(0.15)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    time.sleep(0.6)
    FFX_Xbox.menuB()
    FFX_Screen.awaitPixel(888,470,(191, 191, 191))
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(1.6)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuRight()
    speedNeeded = 14 - speedCount #15 plus two (Spherimorph, Flux), minus 1 because it starts on 1
    if speedNeeded > 1:
        speedNeeded = 1 #Limit so we don't over-spend and run out of money.
    if speedNeeded > 0:
        while speedNeeded > 0:
            FFX_Xbox.menuRight()
            speedNeeded -= 1
    
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.SkipDialog(0.3)
    
    #Next, Grab Auron's weapon
    time.sleep(0.5)
    FFX_Xbox.menuB()
    FFX_Screen.awaitPixel(888,470,(191, 191, 191))
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Got any weapons?
    time.sleep(1.6)
    FFX_Xbox.menuRight()
    time.sleep(0.4)
    FFX_Xbox.menuB() #Sell
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Sell Tidus' longsword
    time.sleep(0.1)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Sell Auron Katana
    time.sleep(0.1)
    time.sleep(0.1)
    FFX_Xbox.menuA()
    FFX_Xbox.menuLeft()
    time.sleep(0.4)
    FFX_Xbox.menuB() #Buy
    time.sleep(0.8)
    #time.sleep(30) #Testing only
    
    if blitzWin == False:
        FFX_Xbox.menuB()
        time.sleep(0.8)
        FFX_Xbox.menuUp() #Baroque sword
        #time.sleep(10) #Testing only
        time.sleep(0.1)
        FFX_Xbox.menuB() #Weapon for Tidus (for Evrae fight)
        time.sleep(0.1)
        FFX_Xbox.menuB() #Do not equip
        time.sleep(0.1)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Shimmering Blade
    time.sleep(0.1)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuB() #Do not equip
    time.sleep(0.1)
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    
    #Now for Yuna's scene
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    time.sleep(2) #Scene in Yuna's room. Not as exciting as it sounds.
    
    FFX_memory.clickToControl3()
    print("Yuna's done talking. Let's keep going.")
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB() #Talk to Rikku
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.1)
    
    FFX_Xbox.SkipDialog(3) #Pick up lightning shield
    time.sleep(2)
    
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.awaitMap1()
    
def northPathing(status):
    #Start of northern section
    checkpoint = 0
    stepCount = 0
    stepMax = 500
    while checkpoint < 1000:
        if FFX_Screen.dodgeLightning():
            print("Dodge")
        if FFX_memory.userControl():
            pos = FFX_memory.getCoords()
            stepCount += 1
            
            if pos == [0.0,0.0]: #This means we've lost control of the character for any reason.
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFX_Xbox.menuB()
            elif checkpoint == 0:
                if pos[1] > -900:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
            elif checkpoint == 10:
                if pos[1] > -700:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 10:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 50:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20:
                if pos[1] > -20:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 50:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 85:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if pos[1] > -100:
                    checkpoint = 40
                    #complete = 1
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] > 50:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 40:
                if pos[1] > 190:
                    checkpoint = 50
                    #complete = 1
                else:
                    if pos[0] > 90:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLy', 1)
            elif checkpoint == 50:
                if status[2] == True:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 1)
                    time.sleep(1)
                    FFXC.set_value('AxisLx', -1)
                    time.sleep(1)
            elif checkpoint == 60:
                if pos[1] > 1 and pos[1] < 150:
                    checkpoint = 1000
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 70:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 90:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            
            
        elif FFX_Screen.BattleScreen():
            print("Starting battle")
            status = FFX_Battle.thunderPlains(status, 2)
        elif FFX_memory.menuOpen():
            FFX_Xbox.menuB()
        elif FFX_memory.getMap() == 110:
            print("Thunder Plains North complete")
            checkpoint = 1000
        else:
            FFX_Xbox.menuB()
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
    
    FFX_memory.awaitControl()
    print("Thunder Plains North complete. Moving up to the Macalania save sphere.")
    FFXC.set_value('AxisLy', 1)
    FFX_Xbox.SkipDialog(6)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl3() # Conversation with Auron about Yuna being hard to guard.
    
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.SkipDialog(6)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0) #Approaching the party

    return status