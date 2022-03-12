import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_targetPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC
 
def arrival(rikkucharged):
    FFX_memory.clickToControl()
    if rikkucharged == True:
        FFX_memory.fullPartyFormat("mwoodsgotcharge")
    else:
        FFX_memory.fullPartyFormat("mwoodsneedcharge")
    FFX_memory.closeMenu()
    
    woodsVars = [False, False, False] #Rikku's charge, Fish Scales, and Arctic Winds
    woodsVars[0] = rikkucharged
    
    lastGil = 0 #for first chest
    checkpoint = 0
    while FFX_memory.getMap() != 221: #All the way to O'aka
        if FFX_memory.userControl():
            #Events
            if checkpoint == 14: #First chest
                if lastGil != FFX_memory.getGilvalue():
                    if lastGil == FFX_memory.getGilvalue() - 2000:
                        checkpoint += 1
                        print("Chest obtained. Updating checkpoint: ", checkpoint)
                    else:
                        lastGil = FFX_memory.getGilvalue()
                else:
                    FFXC.set_movement(1, 1)
                    FFX_Xbox.tapB()
            elif checkpoint == 59:
                if woodsVars[0] == False or woodsVars[1] == False or woodsVars[2] == False:
                    checkpoint = 57
                else: #All good to proceed
                    checkpoint += 1
            
            #Map changes
            elif checkpoint < 18 and FFX_memory.getMap() == 241:
                checkpoint = 18
            elif checkpoint < 40 and FFX_memory.getMap() == 242:
                checkpoint = 40
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.mWoods(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                print("variable check 1: ",woodsVars)
                woodsVars = FFX_Battle.mWoods(woodsVars)
                print("variable check 2: ",woodsVars)
            elif not FFX_memory.battleActive() and FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    
    #Save sphere
    FFX_memory.waitFrames(30 * 0.1)
    FFX_memory.awaitControl()
    FFXC.set_movement(-1, 0)
    FFX_memory.waitFrames(30 * 0.3)
    FFXC.set_neutral()
    FFX_memory.touchSaveSphere()
    #FFXC.set_movement(1, 1)
    #FFX_memory.waitFrames(30 * 0.4)
    FFXC.set_neutral()

def lakeRoad():
    #if FFX_memory.getSpeed() < 12:
    #    FFX_memory.setSpeed(12)
    FFX_memory.awaitControl()
    while not FFX_targetPathing.setMovement([174,-96]):
        pass
    while not FFX_targetPathing.setMovement([138,-83]):
        pass
    while not FFX_targetPathing.setMovement([101,-82]):
        pass
    while FFX_memory.userControl():
        FFXC.set_movement(0, 1)
        FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFX_menu.mWoods() #Selling and buying, item sorting, etc
    FFX_memory.fullPartyFormat('spheri')
    while not FFX_targetPathing.setMovement([101,-72]):
        pass
    
    while not FFX_memory.battleActive():
        if FFX_memory.userControl():
            mapVal = FFX_memory.getMap()
            tidusPos = FFX_memory.getCoords()
            if mapVal == 221:
                if tidusPos[0] > 35:
                    FFX_targetPathing.setMovement([33,-35])
                else:
                    FFX_targetPathing.setMovement([-4,15])
            elif mapVal == 248:
                if tidusPos[0] < -131:
                    FFX_targetPathing.setMovement([-129,-343])
                elif tidusPos[1] < -235:
                    FFX_targetPathing.setMovement([-49,-233])
                elif tidusPos[1] < -95:
                    FFX_targetPathing.setMovement([-1,-93])
                else:
                    FFX_targetPathing.setMovement([-1,100])
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            
    FFXC.set_neutral() #Engage Spherimorph
    
    FFX_Battle.spherimorph()
    print("Battle is over.")
    FFX_memory.clickToControl() #Jecht's memories
    
def lakeRoad2():
    FFXC.set_movement(0, -1)
    if gameVars.csr():
        checkpoint = 0
        tidusPos = FFX_memory.getCoords()
        while checkpoint < 5:
            if checkpoint == 0:
                if FFX_targetPathing.setMovement([-6,25]):
                    checkpoint += 1
            elif checkpoint == 1:
                if FFX_targetPathing.setMovement([-4,-50]):
                    checkpoint += 1
            elif checkpoint == 2:
                if FFX_targetPathing.setMovement([-45,-212]):
                    checkpoint += 1
            elif checkpoint == 3:
                if FFX_targetPathing.setMovement([-49,-245]):
                    checkpoint += 1
            else:
                if FFX_targetPathing.setMovement([-145,-358]):
                    checkpoint += 1
    
    else:
        FFX_memory.waitFrames(30 * 6)
        FFXC.set_neutral()
        
        FFX_memory.clickToControl() #Auron's musings.
        print("Affection (before): ", FFX_memory.affectionArray())
        FFX_memory.waitFrames(30 * 0.2)
        auronAffection = FFX_memory.affectionArray()[2]
        while FFX_memory.affectionArray()[2] == auronAffection: #Make sure we get Auron affection
            auronCoords = FFX_memory.getActorCoords(3)
            FFX_targetPathing.setMovement(auronCoords)
            FFX_Xbox.tapB()
        print("Affection (after): ", FFX_memory.affectionArray())
    while FFX_memory.userControl():
        FFXC.set_movement(-1, -1)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl() #Last map in the woods
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(2)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()

def lake():
    print("Now to the frozen lake")
    FFX_memory.fullPartyFormat('crawler', fullMenuClose=False)
    FFX_menu.mLakeGrid()
    FFX_memory.awaitControl()
    
    print("------------------------------------------Affection array:")
    print(FFX_memory.affectionArray())
    print("------------------------------------------")
    
    checkpoint = 0
    while FFX_memory.getBattleNum() != 194:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.mLake(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive() and FFX_memory.getBattleNum() != 194:
                    FFX_Battle.fleeAll()
            elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
                FFX_Xbox.menuB()
    FFX_Xbox.clickToBattle()
    FFX_Battle.negator()

def afterCrawler():
    print("------------------------------------------Affection array:")
    print(FFX_memory.affectionArray())
    print("------------------------------------------")
    FFX_memory.clickToControl()
    while FFX_memory.getMap() != 153:
        pos = FFX_memory.getCoords()
        if FFX_memory.userControl():
            if pos[1] > ((2.94 * pos[0]) + 505.21):
                FFXC.set_movement(1, 1)
            elif pos[1] < ((2.59 * pos[0]) + 469.19):
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()

    FFX_memory.clickToControl()
    
    checkpoint = 0
    lastCP = 0
    while checkpoint != 100:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        pos = FFX_memory.getCoords()
        if checkpoint == 0:
            if pos[0] > 130:
                checkpoint = 10
            else:
                if pos[1] < ((1.99 * pos[0]) + 5):
                    FFXC.set_movement(-1, -1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 10:
            if pos[0] > 450:
                checkpoint = 20
            else:
                if pos[1] > ((0.37 * pos[0]) + 240):
                    FFXC.set_movement(-1, 1)
                elif pos[1] > 385:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 20:
            if pos[0] > 690:
                checkpoint = 40
            else:
                if pos[1] > ((-0.65 * pos[0]) + 693):
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 30:
            if pos[1] < 100:
                checkpoint = 40
            else:
                if pos[1] < ((-1.49 * pos[0]) + 1235):
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 40:
            if FFX_memory.getMap() == 106:
                FFXC.set_neutral()
                checkpoint = 100
            else:
                if pos[0] > 815:
                    FFXC.set_movement(1, 1)
                elif pos[0] < 810:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)
    print("End of Macalania Woods section. Next is temple section.")

