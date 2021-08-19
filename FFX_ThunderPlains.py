import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory

FFXC = FFX_Xbox.FFXC
 
def southPathing():
    
    print("Start of the Thunder Plains section")
    checkpoint = 0
    stepCount = 0
    stepMax = 500
    complete = 0
    status = [False,False,False] #Rikku charged, Light Curtain, Lunar Curtain
    FFX_memory.fullPartyFormat('kimahri')
    while complete == 0:
        if FFX_Screen.dodgeLightning():
            print("Dodge")
        if FFX_memory.userControl() == False:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
        if FFX_Screen.BattleScreen():
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            print("Starting battle")
            status = FFX_Battle.thunderPlains(status, 1)
        elif FFX_Screen.BattleComplete():
            FFX_Xbox.menuB()
        elif FFX_Screen.PixelTest(293,127,(64, 193, 64)):
            print("Thunder Plains south complete")
            FFXC.set_value('AxisLy', 1)
            FFXC.set_value('AxisLx', -1)
            FFX_Xbox.SkipDialog(8)
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            complete = 1
        elif FFX_Screen.PixelTest(267,254,(64, 193, 64)):
            print("Thunder Plains south complete")
            complete = 1
        elif FFX_Screen.Minimap1():
            pos = FFX_memory.getCoords()
            stepCount += 1
            if pos == [0.0,0.0]: #This means we've lost control of the character for any reason.
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFX_Xbox.menuB()
            elif checkpoint == 0:
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
                if pos[1] < 600:
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
                FFXC.set_value('AxisLx', 1)
                FFX_Xbox.SkipDialog(3)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                complete = 1
            
            
            #if stepCount < 20:
            #    FFXC.set_value('AxisLy', 1)
            #    time.sleep(0.02)
            #elif stepCount < 30:
            #    FFXC.set_value('AxisLy', 1)
            #    FFXC.set_value('AxisLx', -1)
            #    time.sleep(0.02)
            #elif stepCount < 95:
            #    FFXC.set_value('AxisLy', 1)
            #    if stepCount % 20 > 18:
            #        FFXC.set_value('AxisLx', -1)
            #    else :
            #        FFXC.set_value('AxisLx', 0)
            #    time.sleep(0.02)
            #elif stepCount < 140:
            #    FFXC.set_value('AxisLx', 1)
            #    if stepCount % 10 < 2:
            #        FFXC.set_value('AxisLy', 0)
            #    else:
            #        FFXC.set_value('AxisLy', 1)
            #    time.sleep(0.02)
            #elif stepCount < 205:
            #    FFXC.set_value('AxisLy', 1)
            #    FFXC.set_value('AxisLx', 0)
            #    time.sleep(0.02)
            #elif stepCount < 215:
            #    FFXC.set_value('AxisLy', 1)
            #    FFXC.set_value('AxisLx', 1)
            #    time.sleep(0.02)
            #elif stepCount < 225:
            #    FFXC.set_value('AxisLy', 1)
            #    FFXC.set_value('AxisLx', 0)
            #    time.sleep(0.02)
            #elif stepCount < 235:
            #    FFXC.set_value('AxisLy', 1)
            #    FFXC.set_value('AxisLx', 1)
            #    time.sleep(0.02)
            #elif stepCount < 370:
            #    FFXC.set_value('AxisLy', 1)
            #    if stepCount % 30 > 27:
            #        FFXC.set_value('AxisLx', 1)
            #    else :
            #        FFXC.set_value('AxisLx', 0)
            #    time.sleep(0.02)
            #elif stepCount < 375:
            #    FFXC.set_value('AxisLy', -1)
            #    FFXC.set_value('AxisLx', -1)
            #    time.sleep(0.02)
            #elif stepCount < 396:
            #    FFXC.set_value('AxisLy', 1)
            #    FFXC.set_value('AxisLx', -1)
            #    time.sleep(0.02)
            #elif stepCount > 470:
            #    FFXC.set_value('AxisLy', 1)
            #    FFXC.set_value('AxisLx', 1)
            #    time.sleep(0.02)
            #elif stepCount < stepMax:
            #    FFXC.set_value('AxisLy', 1)
            #    FFXC.set_value('AxisLx', 0)
            #    time.sleep(0.02)
            #else:
            #    print("Problem with pathing. Resetting.")
            #    stepCount = 369
        else:
            FFX_Xbox.menuB()
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
    return status
    
def agency():
    #Arrive at the travel agency
    FFX_Screen.clickToPixel(266,251,(64, 193, 64))
    speedCount = FFX_memory.getSpeed()
    
    #Sort into a free slot.
    FFX_Screen.openMenu()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.6)
    FFX_Xbox.menuA()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    
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
    
    speedNeeded = 15 - speedCount #15 plus one extra grenade for Flux, minus 1 because it starts on 1
    if speedNeeded > 2:
        speedNeeded = 2 #Limit so we don't over-spend and run out of money.
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
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuA()
    FFX_Xbox.menuLeft()
    time.sleep(0.4)
    
    FFX_Xbox.menuB() #Buy
    time.sleep(0.8)
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
    #time.sleep(300)
    time.sleep(0.1)
    FFX_Xbox.menuUp()
    #time.sleep(10) #Testing only
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
    
    FFX_Screen.clickToPixel(266,251,(64, 193, 64))
    print("Yuna's done talking. Let's keep going.")
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB() #Talk to Rikku
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.1)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB() #Lightning shield
    time.sleep(1)
    FFX_Xbox.menuB() #Lightning shield
    time.sleep(0.5)
    FFX_menu.plainsArmor()
    FFXC.set_value('AxisLy', 1)
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
        if FFX_Screen.BattleScreen():
            print("Starting battle")
            status = FFX_Battle.thunderPlains(status, 2)
        elif FFX_Screen.BattleComplete():
            FFX_Xbox.menuB()
        elif FFX_Screen.PixelTest(295,235,(64, 193, 64)):
            print("Thunder Plains North complete")
            checkpoint = 1000
        elif FFX_Screen.Minimap1():
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
            
            
            #if stepCount < 180:
            #    FFXC.set_value('AxisLy', 1)
            #    if stepCount % 30 > 26:
            #        FFXC.set_value('AxisLx', 1)
            #    else :
            #        FFXC.set_value('AxisLx', 0)
            #    time.sleep(0.02)
            #elif stepCount < 190:
            #    FFXC.set_value('AxisLy', 1)
            #    FFXC.set_value('AxisLx', -1)
            #    time.sleep(0.02)
            #elif stepCount < 400:
            #    FFXC.set_value('AxisLy', 1)
            #    if stepCount % 10 > 7:
            #        FFXC.set_value('AxisLx', 1)
            #    else :
            #        FFXC.set_value('AxisLx', 0)
            #    time.sleep(0.02)
            #elif stepCount < 450:
            #    FFXC.set_value('AxisLy', 1)
            #    if stepCount % 5 > 2:
            #        FFXC.set_value('AxisLx', 1)
            #    else :
            #        FFXC.set_value('AxisLx', 0)
            #    time.sleep(0.02)
            #elif stepCount < 470:
            #    FFXC.set_value('AxisLy', 1)
            #    FFXC.set_value('AxisLx', 1)
            #    time.sleep(0.02)
            #elif stepCount < 500:
            #    FFXC.set_value('AxisLy', 1)
            #    FFXC.set_value('AxisLx', -1)
            #    time.sleep(0.02)
            #else:
            #    FFXC.set_value('AxisLx', 0)
            #    FFXC.set_value('AxisLy', 0)
            #    time.sleep(0.02)
            #    print("Problem with pathing. Awaiting manual intervention.")
            #    stepCount = 1
        else:
            FFX_Xbox.menuB()
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
    
    print("Thunder Plains North complete. Moving up to the Macalania save sphere.")
    FFXC.set_value('AxisLy', 1)
    FFX_Xbox.SkipDialog(6)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToMap1() # Conversation with Auron about Yuna being hard to guard.
    
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.SkipDialog(6)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0) #Approaching the party