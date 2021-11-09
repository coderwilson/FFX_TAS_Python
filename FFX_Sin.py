import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory

FFXC = FFX_Xbox.FFXC
 
def makingPlans():
    FFX_memory.clickToControl3()
    print("Final Push! Let's get this show on the road!!! (Highbridge)")
    
    #Start by touching the save sphere
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB()
    time.sleep(1)
    FFX_Xbox.menuB()
    time.sleep(1)
    FFX_Xbox.menuA()
    FFX_Xbox.menuB()
    
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.8)
    FFXC.set_value('AxisLx', 0)
    time.sleep(4.5)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.awaitControl()
    
    FFX_Xbox.airShipPath(2) #Talk to Yuna/Kimahri
    
    FFX_memory.clickToControl()
    
    FFX_Xbox.airShipReturn()
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(2.5)
    FFXC.set_value('AxisLy', 0)
    
    print("The hymn is the key")
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.25)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.5)
    FFX_Xbox.SkipDialog(2)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.awaitPixel(984,788,(247, 162, 74)) #To the Highbridge
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    
def Shedinja():
    FFX_memory.awaitControl()
    print("Moving to Shedinja")
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.25)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToStoryProgress(2945) #Click until we're in Bahamut's room.
    FFX_Xbox.SkipDialog(12) #Skip dialog before "We fight Yu Yevon".
    
    while not FFX_Screen.PixelTestTol(610,483,(156, 157, 156),5):
        if FFX_Screen.PixelTestTol(704,466,(154, 154, 154),5):
            FFX_Xbox.menuB()
        elif FFX_Screen.PixelTestTol(612,449,(152, 152, 152),5):
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #We fight Yu Yevon.
    FFX_memory.clickToStoryProgress(2970)

def economy():
    FFX_Screen.awaitPixel(597,407,(157, 159, 157))
    time.sleep(0.05)
    FFX_Xbox.menuB()
    time.sleep(1.2)
    FFX_Xbox.menuRight()
    time.sleep(0.05)
    FFX_Xbox.menuB()
    
    time.sleep(0.05)
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    
    equipSaleCount = 2
    while not FFX_Screen.PixelTestTol(800,830,(132, 131, 167),5):
        if FFX_Screen.PixelTestTol(287,786,(151, 4, 238),5):
            print("Equipped item, no sale.")
        else:
            print("Sell this item.")
            equipSaleCount += 1
            FFX_Xbox.menuB()
            FFX_Xbox.menuUp()
            FFX_Xbox.menuB()
            FFX_Xbox.menuRight()
        FFX_Xbox.menuDown()
        time.sleep(0.05)
        
    time.sleep(0.05)
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    print("Sold number of equipments: ", equipSaleCount)
    FFX_Xbox.SkipDialog(3) #Adjust to whichever vendor we're talking to.
    time.sleep(10)

def facingSin():
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', -1)
    FFX_Xbox.SkipDialog(0.3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    #time.sleep(1.5)
    #FFX_Xbox.menuB() #Open the airship travelling menu
    
    #FFX_Screen.awaitPixel(984,789,(250, 163, 79))
    FFX_Xbox.SkipDialog(10)
    
    FFX_memory.clickToControl()
    FFX_Xbox.airShipPath(3)
    FFX_Battle.SinArms()
    
    FFX_memory.clickToControl()
    while FFX_memory.userControl(): #Back into the hallway
        FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    
    FFX_Xbox.airShipPath(4)
    FFX_Xbox.airShipPath(5)
    FFX_Battle.SinFace()
    print("End of battle with Sin's face.")

def insideSin(length, autoEggHunt, seed):
    print("Sea of Sorrow section")
    if autoEggHunt == True:
        import zz_eggHuntAuto
    FFXC.set_value('AxisLy', -1)
    FFX_memory.clickToControl()
    while FFX_memory.userControl():
        FFX_Xbox.menuB()
    
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    if length == 'short':
        print("Short game, no menuing.")
    else:
        FFX_memory.fullPartyFormat('kimahri')
        #FFX_menu.endGameSwap() #Just re-using the same party format patterns.
    

    
    checkpoint = 0
    lastCP = 0
    while checkpoint < 1000:
        pos = FFX_memory.getCoords()
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            if pos == [0.0,0.0]:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                if checkpoint == 280:
                    FFX_Xbox.menuB()
            elif checkpoint == 0:
                if pos[1] > ((0.81 * pos[0]) -885.74):
                    checkpoint = 5
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((-1.24 * pos[0]) -683.96):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 5:
                if pos[1] > -650:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] < ((0.81 * pos[0]) -885.74):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 10:
                cam = FFX_memory.getCamera()
                if cam[0] > 1.4:
                    checkpoint = 15
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 15:
                if pos[1] > ((-0.22 * pos[0]) -295.87):
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] < ((1.13 * pos[0]) -844.54):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 20:
                if pos[1] > -300:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30: #Left through the jagged area
                if pos[0] < 9:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] < ((-0.10 * pos[0]) -257.09):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 40:
                cam = FFX_memory.getCamera()
                if cam[0] < 0.4:
                    checkpoint = 50
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < -10:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 50: #Up to the waterfall
                if pos[1] > 20:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((5.69 * pos[0]) -140.53):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60: #Past the waterfall on the right
                if pos[0] < -275:
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] < 55:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 70:
                cam = FFX_memory.getCamera()
                if cam[0] < -0.3:
                    checkpoint = 90
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 90: #The dumb corner with the terrible camera angle
                if pos[1] > 175:
                    checkpoint = 100
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] > ((1.55 * pos[0]) + 688.48):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 100:
                if pos[1] > 322:
                    checkpoint = 110
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((0.62 * pos[0]) + 440.00):
                        FFXC.set_value('AxisLx', 0)
                    else:
                        FFXC.set_value('AxisLx', -1)
            elif checkpoint == 110: #Up and over the hump
                if pos[0] > 185:
                    checkpoint = 120
                else:
                    if pos[1] < ((0.38 * pos[0]) + 449):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
                    if pos[1] > ((0.38 * pos[0]) + 429):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 120: #And down the other side
                cam = FFX_memory.getCamera()
                if cam[0] > 0.4:
                    checkpoint = 125
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 125: #Sliding around the corner
                if pos[1] < ((0.80 * pos[00]) + 9.40):
                    checkpoint = 130
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] < ((-0.43 * pos[0]) + 469.71):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 130: #Back up towards Seymour
                if pos[1] > 710:
                    checkpoint = 140
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 390:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 140: #Shift left
                if pos[0] < 220:
                    checkpoint = 150
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] < 750:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 150: #Shift left
                if FFX_memory.getMap() == 204:
                    #Fast game, nothing to see here.
                    checkpoint = 170
                elif pos[1] < 600:
                    checkpoint = 160
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < 850:
                        if pos[0] < 230:
                            FFXC.set_value('AxisLx', 1)
                        else:
                            FFXC.set_value('AxisLx', 0)
                    else:
                        if pos[0] < 190:
                            FFXC.set_value('AxisLx', 1)
                        else:
                            FFXC.set_value('AxisLx', 0)
            elif checkpoint == 160: #Seymour
                print("We've reached the Seymour screen.")
                FFX_memory.fullPartyFormat('yuna')
                #FFX_menu.endGameSwap2()
                FFXC.set_value('AxisLy', 1)
                time.sleep(5)
                FFXC.set_value('AxisLy', 0)
                FFX_Battle.omnis(seed)
                FFX_memory.clickToControl()
                FFX_menu.endGameSwap()
                checkpoint = 170
            elif checkpoint == 170: #Start, City of Dying Dreams
                if pos[1] > -220:
                    checkpoint = 180
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((-0.78 * float(pos[0])) - 107.5):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 180: #Towards the tiny bridge
                if pos[1] < ((-0.97 * pos[0]) - 162.5):
                    checkpoint = 190
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 190: #Across the tiny bridge
                if pos[1] > ((0.95 * pos[0]) -220.09):
                    checkpoint = 200
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < ((-0.97 * pos[0]) - 164):
                        FFXC.set_value('AxisLx', 1)
                    elif pos[1] < ((-0.97 * pos[0]) - 162.5):
                        FFXC.set_value('AxisLx', 0)
                    else:
                        FFXC.set_value('AxisLx', -1)
            elif checkpoint == 200: #First corner and past the pit
                if pos[1] > 160 :
                    checkpoint = 210
                else:
                    if pos[1] < -60:
                        FFXC.set_value('AxisLy', 1)
                        if pos[0] < -5:
                            FFXC.set_value('AxisLx', 1)
                        else:
                            FFXC.set_value('AxisLx', 0)
                    else:
                        if pos[0] < 10:
                            FFXC.set_value('AxisLy', 0)
                            FFXC.set_value('AxisLx', 1)
                        else:
                            FFXC.set_value('AxisLy', 1)
                            FFXC.set_value('AxisLx', 0)
            elif checkpoint == 210:
                if pos[0] > 210:
                    checkpoint = 220
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > 175:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 220: #Into the last open area
                if pos[0] > 265:
                    checkpoint = 230
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
                    time.sleep(0.25)
                    FFXC.set_value('AxisLx', 0)
                    time.sleep(0.25)
            elif checkpoint == 230:
                if pos[1] > 230:
                    checkpoint = 240
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] > 290:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 240:
                if pos[1] > 320:
                    checkpoint = 250
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 250: #After one-way ramp, up the next ramp.
                if pos[1] > 360:
                    checkpoint = 260
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] < ((-15.14 * float(pos[0])) + 5271.57):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 260:
                if pos[1] < -1:
                    checkpoint = 270
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
                    time.sleep(1.2)
                    FFXC.set_value('AxisLx', 1)
                    time.sleep(0.25)
            elif checkpoint == 270:
                print("Made it to the final save sphere and point of no return.")
                FFXC.set_value('AxisLx', 1)
                time.sleep(1)
                FFXC.set_value('AxisLx', 0)
                while FFX_memory.userControl(): #Up to the giant egg thing
                    FFXC.set_value('AxisLy', 1)
                FFX_memory.awaitControl()
                while FFX_memory.userControl(): #Approach
                    FFXC.set_value('AxisLy', 1)
                FFX_memory.awaitControl()
                while FFX_memory.userControl(): #Approach again, engages egg hunt.
                    FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.5)
                print("Start of egg hunt section.")
                checkpoint = 280
                eggStart = FFX_Logs.timeStamp()
                while not FFX_memory.userControl():
                    FFXC.set_value('AxisLx', 1)
                time.sleep(0.5) #Just to get us out of position 0,0
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                
            elif checkpoint == 280:
                if FFX_memory.getStoryProgress() >= 3270:
                    eggEnd = FFX_Logs.timeStamp()
                    eggDuration = eggEnd - eggStart
                    FFX_Logs.writeStats("Egg hunt duration:")
                    FFX_Logs.writeStats(str(eggDuration))
                    print("Done with the egg hunt. Final prep for BFA.")
                    checkpoint = 290
                elif autoEggHunt == True:
                    zz_eggHuntAuto.engage()
                else:
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 0)
                    #Still in the egg hunt screen
            else:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                checkpoint = 1000
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeLateGame()
            elif FFX_Screen.BattleComplete():
                FFX_Xbox.menuB()

    if length == 'short':
        print("Short game, no menuing.")
    else:
        FFX_memory.fullPartyFormat('yuna')
        FFX_menu.BFA()
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
