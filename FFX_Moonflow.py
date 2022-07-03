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

def arrival():
    print("Starting Moonflow section")
    
    checkpoint = 0
    while FFX_memory.getMap() != 235:
        if FFX_memory.userControl():
            #Chests
            if checkpoint == 2: #Gil outside Djose temple
                print("Djose gil chest")
                FFXC.set_movement(-1, 1)
                FFX_Xbox.SkipDialog(1)
                FFXC.set_movement(1, -1)
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 43: #Moonflow chest
                if FFX_memory.getItemSlot(90) < 200:
                    checkpoint += 1
                else:
                    FFX_targetPathing.setMovement([-1796,-480])
                    FFX_Xbox.tapB()
            
            #Map changes
            elif checkpoint < 6 and FFX_memory.getMap() == 76:
                checkpoint = 6
            elif checkpoint < 11 and FFX_memory.getMap() == 93:
                checkpoint = 11
            elif checkpoint < 14 and FFX_memory.getMap() == 75:
                checkpoint = 14
            elif checkpoint < 49 and FFX_memory.getMap() == 105:
                checkpoint = 49
            elif checkpoint < 54 and FFX_memory.getStoryProgress() == 1045:
                checkpoint = 54
                print("Updating checkpoint based on story/map progress: ", checkpoint)
            elif checkpoint == 54 and FFX_memory.getMap() == 188:
                checkpoint = 55
                print("Updating checkpoint based on story/map progress: ", checkpoint)
                
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.moonflow(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    print("End of approaching section, should now be talking to Lucille/Elma/etc.")

def southBank(checkpoint:int=0):
    #Arrive at the south bank of the moonflow.
    print("South bank, Save sphere screen")
    
    
    FFX_memory.clickToControl3() # "Where there's a will, there's a way."
    FFXC.set_movement(1, -1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl3()
    partyHP = FFX_memory.getHP()
    if partyHP[4] < 800:
        FFX_Battle.healUp(2)
    elif partyHP[0] < 700:
        FFX_Battle.healUp(1)
    FFX_memory.closeMenu()
    
    while not FFX_memory.battleActive():
        if FFX_memory.userControl():
            if checkpoint == 4:
                FFXC.set_neutral()
                FFX_memory.clickToEvent()
                FFX_memory.waitFrames(18)
                FFX_Xbox.menuB() #Ride ze Shoopuff?
                FFX_memory.waitFrames(10)
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB() #All aboardz!
                FFX_Xbox.SkipDialog(3) #Just to clear some dialog
        
            elif FFX_targetPathing.setMovement(FFX_targetPathing.moonflowBankSouth(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
    
    
    FFX_Battle.extractor()
    
def northBank():
    FFX_memory.clickToControl3()
    FFXC.set_movement(-1, 0)
    FFX_memory.awaitEvent()
    FFX_memory.waitFrames(30 * 1)
    FFX_memory.awaitControl()
    FFX_memory.waitFrames(30 * 1.5)
    if gameVars.csr():
        FFXC.set_movement(-1, 1)
        FFX_memory.waitFrames(4)
    else:
        FFX_memory.clickToEvent() #Talk to Auron
        FFXC.set_neutral()
        FFX_memory.waitFrames(30 * 0.3)
        FFX_memory.clickToControl3()
    FFXC.set_movement(-1, 0)
    FFX_memory.waitFrames(30 * 0.5)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()
    FFX_memory.waitFrames(30 * 0.5)
    
    checkpoint = 0
    print("Miihen North Bank pattern. Starts after talking to Auron.")
    while FFX_memory.getMap() != 135:
        if FFX_memory.userControl():
            if checkpoint == 7: #Rikku steal/mix tutorial
                FFXC.set_movement(1, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_Battle.mixTutorial()
                FFX_memory.fullPartyFormat("postbunyip")
                FFX_memory.closeMenu()
                checkpoint += 1
            elif FFX_memory.getStoryProgress() >= 1085 and checkpoint < 4:
                checkpoint = 4
                print("Rikku scene, updating checkpoint: ", checkpoint)
                
            #Map changes
            elif checkpoint < 2 and FFX_memory.getMap() == 109:
                checkpoint = 2
            elif checkpoint < 12 and FFX_memory.getMap() == 97:
                checkpoint = 12
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.moonflowBankNorth(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            elif FFX_memory.diagSkipPossible() and FFX_memory.battleActive() == False:
                FFX_Xbox.tapB()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()

