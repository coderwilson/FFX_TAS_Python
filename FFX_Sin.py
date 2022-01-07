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
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_neutral()
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 1)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 1)
    FFX_Xbox.menuA()
    FFX_Xbox.menuB()
    
    FFXC.set_movement(1, -1)
    FFX_memory.waitFrames(30 * 0.8)
    FFXC.set_movement(0, -1)
    FFX_memory.waitFrames(30 * 4.5)
    FFXC.set_neutral()
    
    FFX_memory.awaitControl()
    
    FFX_zzairShipPath.airShipPath(2) #Talk to Yuna/Kimahri
    
    FFX_memory.awaitControl()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 2.5)
    FFXC.set_neutral()
    
    print("The hymn is the key")
    FFX_memory.clickToControl()
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 0.25)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 0.5)
    FFX_Xbox.SkipDialog(2)
    FFXC.set_neutral()
    FFX_memory.waitFrames(120)
    FFX_memory.waitFrames(30 * 0.5)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 0.3)
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
    FFX_memory.waitFrames(30 * 0.25)
    FFXC.set_movement(0, 1)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()
    FFX_memory.clickToDiagProgress(100)
    FFX_memory.clickToDiagProgress(76) #Have you found a way? Well?
    FFX_memory.waitFrames(20)
    FFX_Xbox.tapDown()
    FFX_Xbox.menuB() #We fight Yu Yevon.
    
    FFX_memory.clickToDiagProgress(74)
    FFX_memory.clickToDiagProgress(28)

def facingSin():
    FFX_memory.clickToControl()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(85)
    FFXC.set_movement(-1, 1)
    FFX_Xbox.SkipDialog(0.3)
    FFXC.set_neutral()
    #FFX_memory.waitFrames(30 * 1.5)
    #FFX_Xbox.menuB() #Open the airship travelling menu
    
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
    FFX_memory.waitFrames(30 * 0.2)
    
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
                FFX_memory.waitFrames(30 * 5)
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
    FFX_memory.waitFrames(30 * 0.5)
    if autoEggHunt == True:
        zz_eggHuntAuto.engage()
    else:
        print("Start of egg hunt. User control expected.")
        waitCount = 0
        while FFX_memory.getMap() != 325:
            FFX_memory.waitFrames(30 * 1)
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
