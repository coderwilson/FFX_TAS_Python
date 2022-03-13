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
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def makingPlans():
    FFX_memory.clickToControl3()
    print("Final Push! Let's get this show on the road!!! (Highbridge)")
    
    #Start by touching the save sphere
    while not FFX_targetPathing.setMovement([-267,347]):
        pass
    
    #print("Cursor test 2: ", FFX_memory.saveMenuCursor())
    #FFX_memory.touchSaveSphere()
    #print("Cursor test 3: ", FFX_memory.saveMenuCursor())
    #Fix this later.
    #FFX_memory.waitFrames(60)
    #FFX_Xbox.menuA()
    #FFX_Xbox.menuB()
    
    target = [[-242,312],[-239,258],[-243,145],[-243,10]]
    checkpoint = 0
    while FFX_memory.getMap() == 194:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(target[checkpoint]):
                checkpoint += 1
    
    
    FFX_zzairShipPath.airShipPath(2) #Talk to Yuna/Kimahri
    FFXC.set_neutral()
    
    #Fix this later, should be based on memory values.
    print("The hymn is the key")
    while FFX_memory.oakaGilCursor() != 20:
        FFX_Xbox.tapB()
    while FFX_memory.mapCursor() != 10:
        FFX_memory.menuDirection(FFX_memory.mapCursor(), 10, 13)
    FFX_memory.clickToControl()
    
def Shedinja():
    FFX_memory.awaitControl()
    print("Moving to Shedinja")
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 0.25)
    FFXC.set_movement(0, 1)
    FFX_memory.awaitEvent()
    
    if gameVars.csr():
        print("All of Shelinda is skipped.")
        FFXC.set_neutral()
        FFX_memory.awaitControl()
    else:
        FFXC.set_neutral()
        FFX_memory.clickToDiagProgress(100)
        FFX_memory.clickToDiagProgress(76) #Have you found a way? Well?
        FFX_memory.waitFrames(20)
        FFX_Xbox.tapDown()
        FFX_Xbox.menuB() #We fight Yu Yevon.
        
        FFX_memory.clickToDiagProgress(74)
        FFX_memory.clickToDiagProgress(28)
        FFX_memory.clickToControl3()

def exitCockpit():
    print("Attempting to exit cockpit")
    while FFX_memory.getMap() != 265:
        if FFX_memory.userControl():
            tidusCoords = FFX_memory.getCoords()
            if tidusCoords[1] > 318:
                FFX_targetPathing.setMovement([-244,315])
            else:
                FFXC.set_movement(0, -1)
        else:
            FFXC.set_neutral()

def facingSin():
    #FFX_memory.waitFrames(30 * 1.5)
    #FFX_Xbox.menuB() #Open the airship travelling menu
    while not FFX_targetPathing.setMovement([-245,321]):
        pass
    
    while FFX_memory.userControl():
        FFX_targetPathing.setMovement([-256,342])
        FFX_Xbox.tapB()
        FFX_memory.waitFrames(1)
    
    FFXC.set_neutral()
    
    if gameVars.csr():
        FFX_memory.clickToControl()
    else:
        FFX_Xbox.SkipDialog(15) #Gets us through the Airship destination menu.
        while not FFX_memory.userControl():
            if FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.tapB()
    
    if FFX_memory.getMap() in [255,374]:
        exitCockpit()
    FFXC.set_neutral()
    
    FFX_zzairShipPath.airShipPath(3)
    FFX_Battle.SinArms()
    FFX_memory.clickToControl()
    print("To the deck, talk to Yuna")
    if FFX_memory.getMap() in [255,374]:
        exitCockpit()
    FFXC.set_neutral()
    FFX_memory.clickToControl()
    
    FFX_zzairShipPath.airShipPath(4)
    FFXC.set_neutral()
    FFX_memory.clickToControl()
    
    print("To the deck, Sin'se face battle.")
    if FFX_memory.getMap() in [255,374]:
        exitCockpit()
    FFXC.set_neutral()
    FFX_zzairShipPath.airShipPath(5)
    FFX_Battle.SinFace()
    print("End of battle with Sin's face.")

def insideSin():
    FFXC.set_movement(0, -1)
    while FFX_memory.getMap() != 203: #Skip dialog and run to the sea of sorrows map
        if FFX_memory.getStoryProgress() == 3160 and FFX_memory.cutsceneSkipPossible():
            FFX_memory.waitFrames(15)
            FFX_Xbox.skipScene()
        else:
            FFX_Xbox.menuB()
    FFXC.set_neutral()
    
    if FFX_memory.overdriveState()[6] != 100:
        FFX_memory.fullPartyFormat('rikku', fullMenuClose=False)
    else:
        FFX_memory.fullPartyFormat('kimahri', fullMenuClose=False)
    #if gameVars.zombieWeapon() == 255:
    #    FFX_menu.zombieStrikeBackup()
    FFX_memory.closeMenu()
    
    checkpoint = 0
    while FFX_memory.getMap() != 324: #All the way to the egg hunt.
        if FFX_memory.userControl():
            #Events
            if FFX_memory.getMap() == 296: #Seymour battle
                print("We've reached the Seymour screen.")
                FFX_memory.fullPartyFormat('yuna')
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(30 * 5)
                FFXC.set_neutral()
                FFX_Battle.omnis()
                FFX_memory.clickToControl()
                if FFX_memory.overdriveState()[6] != 100:
                    FFX_memory.fullPartyFormat('rikku')
                else:
                    FFX_memory.fullPartyFormat('kimahri')
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
                FFX_Battle.chargeRikkuOD()
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
    if gameVars.zombieWeapon() != 255 and gameVars.zombieWeapon() not in [0, 1, 2]:
        FFX_menu.equipWeapon(character=gameVars.zombieWeapon(),ability=0x8032, fullMenuClose=False)
    FFX_menu.BFA()
