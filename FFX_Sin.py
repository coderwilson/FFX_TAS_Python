import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_zzairShipPath
import FFX_targetPathing
import zz_eggHuntAuto

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC
 
def makingPlans():
    FFX_memory.clickToControl3()
    print("Final Push! Let's get this show on the road!!! (Highbridge)")
    
    #Start by touching the save sphere
    FFXC.set_movement(-1, -1)
    time.sleep(1)
    FFXC.set_neutral()
    FFX_Xbox.menuB()
    time.sleep(1)
    FFX_Xbox.menuB()
    time.sleep(1)
    FFX_Xbox.menuA()
    FFX_Xbox.menuB()
    
    FFXC.set_movement(1, -1)
    time.sleep(0.8)
    FFXC.set_movement(0, -1)
    time.sleep(4.5)
    FFXC.set_neutral()
    
    FFX_memory.awaitControl()
    
    FFX_zzairShipPath.airShipPath(2) #Talk to Yuna/Kimahri
    
    FFX_memory.awaitControl()
    FFXC.set_movement(0, 1)
    time.sleep(2.5)
    FFXC.set_neutral()
    
    print("The hymn is the key")
    FFX_memory.clickToControl()
    FFXC.set_movement(1, 1)
    time.sleep(0.25)
    FFXC.set_movement(0, 1)
    time.sleep(0.5)
    FFX_Xbox.SkipDialog(2)
    FFXC.set_neutral()
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
    FFXC.set_movement(1, 1)
    time.sleep(0.25)
    FFXC.set_movement(0, 1)
    time.sleep(3)
    FFXC.set_neutral()
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
    FFXC.set_movement(0, 1)
    time.sleep(3)
    FFXC.set_movement(-1, 1)
    FFX_Xbox.SkipDialog(0.3)
    FFXC.set_neutral()
    #time.sleep(1.5)
    #FFX_Xbox.menuB() #Open the airship travelling menu
    
    #FFX_Screen.awaitPixel(984,789,(250, 163, 79))
    FFX_Xbox.SkipDialog(10)
    
    while not FFX_memory.userControl():
        if FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        elif FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.tapB()
    
    FFX_zzairShipPath.airShipPath(3)
    FFX_Battle.SinArms()
    
    FFX_memory.clickToControl()
    while FFX_memory.userControl(): #Back into the hallway
        FFXC.set_movement(0, -1)
    FFXC.set_neutral()
    time.sleep(0.2)
    
    FFX_zzairShipPath.airShipPath(4)
    FFX_zzairShipPath.airShipPath(5)
    FFX_Battle.SinFace()
    print("End of battle with Sin's face.")

def insideSin():
    FFXC.set_movement(0, -1)
    while FFX_memory.getMap() != 203: #Skip dialog and run to the sea of sorrows map
        FFX_Xbox.menuB()
    FFXC.set_neutral()
    
    FFX_memory.fullPartyFormat('kimahri')
    checkpoint = 0
    while FFX_memory.getMap() != 324: #All the way to the egg hunt.
        if FFX_memory.userControl():
            #Events
            if FFX_memory.getMap() == 296: #Seymour battle
                print("We've reached the Seymour screen.")
                FFX_memory.fullPartyFormat('yuna')
                #FFX_menu.endGameSwap2()
                FFXC.set_movement(0, 1)
                time.sleep(5)
                FFXC.set_neutral()
                FFX_Battle.omnis()
                FFX_memory.clickToControl()
                FFX_menu.endGameSwap()
            elif checkpoint < 41 and FFX_memory.getMap() == 204:
                checkpoint = 41
            elif checkpoint < 68 and FFX_memory.getMap() == 327:
                checkpoint = 68
            
            #General Pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.insideSin(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    
def eggHunt(autoEggHunt):
    #Done with pathing, now for egg hunt.
    eggStart = FFX_Logs.timeStamp()
    while not FFX_memory.userControl():
        FFXC.set_movement(-1, -1)
    time.sleep(0.5)
    if autoEggHunt == True:
        zz_eggHuntAuto.engage()
    else:
        print("Start of egg hunt. User control expected.")
        waitCount = 0
        while FFX_memory.getMap() != 325:
            time.sleep(1)
            waitCount += 1
            if waitCount % 10 == 0:
                print("Still waiting on user to do this section. ", waitCount / 10)
    eggEnd = FFX_Logs.timeStamp()
    eggDuration = eggEnd - eggStart
    FFX_Logs.writeStats("Egg hunt duration:")
    FFX_Logs.writeStats(str(eggDuration))
    
    print("Done with the egg hunt. Final prep for BFA.")
    FFX_memory.fullPartyFormat('yuna')
    FFX_menu.BFA()
