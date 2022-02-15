import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_targetPathing
import FFX_Xbox
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def arrival():
    if not gameVars.csr():
        FFX_Xbox.skipStoredScene(2)
    print("Starting Luca section")
    FFX_memory.clickToControl()
    
    earlyHaste = 0
    checkpoint = 0
    while checkpoint < 46:
        if FFX_memory.userControl():
            #events
            if checkpoint == 4: #Seymour intro scene
                print("Event: Seymour intro scene")
                FFXC.set_movement(1, 0)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                if not gameVars.csr():
                    FFX_memory.clickToDiagProgress(18) #Seymour scene
                    FFX_Xbox.awaitSave(index=2)
                    
                    FFX_memory.clickToDiagProgress(82) #Let's go over the basics
                    #FFX_memory.clickToDiagProgress(39)
                    FFX_Xbox.SkipDialog(1)
                while FFX_memory.blitzCursor() != 12:
                    FFX_Xbox.tapA()
                FFX_Xbox.menuB()
                if not gameVars.csr():
                    FFX_Xbox.SkipDialogSpecial(45) #Skip the Wakka Face scene
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 8: #Upside down T section
                print("Event: Upside down T section")
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 17: #Into the bar
                print("Event: Into the bar looking for Auron")
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 23: #Back to the front of the Blitz dome
                print("Event: Back to Blitz dome entrance")
                FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 26: #To the docks
                print("Event: Towards the docks")
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 30 or checkpoint == 32: #First and second battles
                print("Event: First/Second battle")
                FFXC.set_movement(1, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_Battle.LucaWorkers()
                checkpoint += 1
            elif checkpoint == 34: #Third battle
                print("Tidus's XP: ", FFX_memory.getTidusXP())
                if FFX_memory.getTidusXP() >= 312:
                    FFXC.set_neutral()
                    earlyHaste = FFX_menu.LucaWorkers()
                    if earlyHaste != 0:
                        earlyHaste = 2
                print("Event: Third battle")
                FFXC.set_movement(1, 0)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_Battle.LucaWorkers2(earlyHaste)
                print("Tidus's XP: ", FFX_memory.getTidusXP())
                FFX_memory.clickToControl()
                if earlyHaste == 0 and FFX_memory.getTidusXP() >= 312:
                    earlyHaste = FFX_menu.LucaWorkers()
                        
                checkpoint += 1
            elif checkpoint == 36 or checkpoint == 45:
                print("Event: Touch Save Sphere")
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 38: #Oblitzerator
                print("Event: Oblitzerator fight")
                FFXC.set_movement(1, 0)
                #FFX_memory.waitFrames(30 * 2)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_Battle.Oblitzerator(earlyHaste)
                checkpoint += 1
            elif checkpoint == 40:
                FFX_memory.clickToEventTemple(4)
                
                if earlyHaste == 0:
                    earlyHaste = FFX_menu.LucaWorkers() - 1
                checkpoint += 1
            elif checkpoint == 42:
                FFX_memory.clickToEventTemple(5)
                checkpoint += 1
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.Luca1(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipScene()
                
            #Map changes
            elif checkpoint < 3 and FFX_memory.getMap() == 268:
                checkpoint = 3
                print("Map change: ", checkpoint)
            elif checkpoint < 6 and FFX_memory.getMap() == 123: #Front of the Blitz dome
                print("Map change: ", checkpoint)
                checkpoint = 6
            elif checkpoint < 11 and FFX_memory.getMap() == 104:
                print("Map change: ", checkpoint)
                checkpoint = 11
    
    FFX_Logs.writeStats("Early Haste:")
    FFX_Logs.writeStats(earlyHaste)
    gameVars.earlyHasteSet(earlyHaste)
    
    print("##Checking for thunderstrike weapons for Tidus or Wakka")
    thunderStrike = FFX_memory.checkThunderStrike()
    if thunderStrike == 0:
        print("##Neither character got a thunderstrike weapon.")
    elif thunderStrike == 1:
        print("##Tidus got a thunderstrike weapon.")
    elif thunderStrike == 2:
        print("##Wakka got a thunderstrike weapon.")
    else:
        print("##Both Tidus and Wakka somehow got a thunderstrike weapon.")
    
    FFX_Logs.writeStats("Thunderstrike results:")
    FFX_Logs.writeStats(thunderStrike)
    
    if thunderStrike != 0:
        if thunderStrike % 2 == 1:
            print("Equipping Tidus")
            #if thunderStrike >= 2:
            #    fullClose = False
            #else:
            fullClose = True
            FFX_menu.equipWeapon(character=0,ability=0x8026, fullMenuClose=fullClose)
        #if thunderStrike >= 2:
            #After review, this does not deal enough damage.
        #    print("Equipping Wakka")
        #    FFX_menu.equipWeapon(character=4,ability=0x8026, fullMenuClose=True)
    gameVars.setLStrike(thunderStrike)

def followYuna():
    print("followYuna function no longer used")

def preBlitz():
    print("preBlitz function is no longer used.")

def blitzStart():
    print("Starting the Blitzball game via lots of storyline.")
    checkpoint = 0
    while FFX_memory.getStoryProgress() < 519:
        #print(checkpoint)
        if FFX_memory.userControl():
            if FFX_memory.getMap() == 72 and checkpoint < 3:
                checkpoint = 3
            elif FFX_memory.getMap() == 72 and FFX_memory.getCoords()[0] < -18 \
                and checkpoint < 5:
                checkpoint = 5
            elif FFX_memory.getMap() == 72 and FFX_memory.getCoords()[0] > -15 \
                and checkpoint >= 5:
                checkpoint = 4
            elif checkpoint == 8:
                FFX_targetPathing.setMovement([-103, -4])
                FFX_Xbox.tapB()
            elif FFX_targetPathing.setMovement(FFX_targetPathing.LucaPreBlitz(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def afterBlitz():
    FFX_Xbox.clickToBattle()
    battleNum = 0
    checkpoint = 0
    while checkpoint < 36:
        if FFX_memory.userControl():
            print("Checkpoint: ", checkpoint)
            #Events
            if checkpoint == 8: #First chest
                if gameVars.earlyHaste() == -1:
                    FFX_menu.lateHaste()
                #if gameVars.getLStrike() >= 2:
                #    FFX_menu.equipWeapon(character=4,ability=0x8022, fullMenuClose=False)
                FFX_menu.mrrGrid1()
                FFX_memory.closeMenu()
                print("First chest")
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-635,-410])
                    FFX_Xbox.menuB()
                FFXC.set_neutral()
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 10: #Second chest
                print("Second chest")
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-620,-424])
                    FFX_Xbox.menuB()
                FFXC.set_neutral()
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 20: #Target Auron
                if not gameVars.csr():
                    while FFX_memory.affectionArray()[2] == 0: #First Auron affection, always zero
                        auronCoords = FFX_memory.getActorCoords(3)
                        FFX_targetPathing.setMovement(auronCoords)
                        FFX_Xbox.tapB()
                checkpoint += 1 #After affection changes
            elif checkpoint == 35: #Bring the party together
                print("Bring the party together")
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
                
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.Luca3(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
            
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                battleNum += 1
                print("After-Blitz Battle Number: ", battleNum)
                if battleNum == 1:
                    FFX_Battle.afterBlitz1(gameVars.earlyHaste())
                elif battleNum == 2:
                    FFX_Xbox.clickToBattle()
                    FFX_Battle.attack('none') #Hardest boss in the game.
                    print("Well that boss was difficult.")
                    FFX_memory.waitFrames(30 * 6)
                elif battleNum == 3:
                    if gameVars.earlyHaste() == -1:
                        FFX_Battle.afterBlitz3LateHaste(gameVars.earlyHaste())
                    else:
                        FFX_Battle.afterBlitz3(gameVars.earlyHaste())
                    FFX_memory.clickToControl()
                    FFX_memory.waitFrames(4)
                    FFXC.set_neutral()
                    checkpoint = 0
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_memory.waitFrames(2)
                FFX_Xbox.skipScene()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
                
            #Map changes
            elif checkpoint < 23 and FFX_memory.getMap() == 123:
                checkpoint = 23
                print("Map change: ", checkpoint)
            elif checkpoint < 26 and FFX_memory.getMap() == 77:
                checkpoint = 26
                print("Map change: ", checkpoint)
            elif checkpoint < 31 and FFX_memory.getMap() == 104:
                checkpoint = 31
                print("Map change: ", checkpoint)
    FFXC.set_movement(-1, -1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_neutral()