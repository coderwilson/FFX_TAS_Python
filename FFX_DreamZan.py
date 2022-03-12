import pyxinput
import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_memory
import FFX_targetPathing
import FFX_vars
import FFX_Logs

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def NamingTidus_slow():
    #Clear Tidus
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB() # Delete all but T
    
    #Replace with TAS
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() # A
    FFX_Xbox.menuDown()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() # S
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() # Confirm
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() # Confirm again

def NamingTidus():
    while FFX_memory.equipSellRow() != 1:
        FFX_Xbox.tapB()
    while FFX_memory.equipSellRow() != 0:
        FFX_Xbox.tapUp()
    while FFX_memory.nameConfirmOpen():
        FFX_Xbox.tapB()

def NewGame(Gamestate):
    print("Starting the game")
    print("Gamestate: ", Gamestate)
    
    #New version
    while FFX_memory.getMap() != 0:
        if FFX_memory.diagSkipPossible():
            if Gamestate == 'none':
                if FFX_memory.saveMenuCursor() == 1:
                    FFX_Xbox.menuDown()
                else:
                    FFX_memory.waitFrames(2)
                    FFX_Xbox.menuB()
            else:
                if FFX_memory.saveMenuCursor() == 0:
                    FFX_Xbox.menuDown()
                else:
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()
                    break
        elif FFX_memory.getMap() != 23:
            FFXC.set_value('BtnStart', 1)
            FFX_memory.waitFrames(1)
            FFXC.set_value('BtnStart', 0)
            FFX_memory.waitFrames(1)
    FFX_memory.clearNameAeonReady()
    
def NewGame2():
    #New game selected. Next, select options.
    FFX_memory.waitFrames(30)
    print("Default Sphere Grid")
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(20)
    print("Confirm sphere grid")
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(20)
    print("Orchestrated soundtrack.")
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(20)
    print("Confirm Orchestrated soundtrack.")
    FFX_Xbox.menuB()

def listenStory():
    FFX_memory.waitFrames(10)
    print("Skipping intro scene, we'll watch this properly in about 8 hours.")
    FFX_vars.initVars()
    csModVar = FFX_vars.varsHandle()
    x = 0
    while not FFX_memory.userControl():
        if FFX_memory.getMap() == 132:
            if FFX_memory.diagProgressFlag() == 1:
                #print("Cutscene Remover: ", csModVar.csr())
                csModVar.SETcsr(False)
                #print("Cutscene Remover: ", csModVar.csr())
            FFXC.set_value('BtnBack', 1)
            FFX_memory.waitFrames(1)
            FFXC.set_value('BtnBack', 0)
            FFX_memory.waitFrames(1)
    
    skips = 0
    checkpoint = 0
    while FFX_memory.getBattleNum() != 414: #Sinspawn Ammes
        if FFX_memory.userControl():
            #Events
            if checkpoint == 2:
                while FFX_memory.userControl():
                    FFXC.set_movement(0, -1)
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                
                #Name Tidus
                FFX_Xbox.nameAeon()
                
                checkpoint += 1
            elif checkpoint == 4:
                if not csModVar.csr():
                    while FFX_memory.userControl():
                        FFXC.set_movement(1, -1)
                        FFX_Xbox.tapB()
                    FFXC.set_neutral()
                    FFX_memory.waitFrames(6)
                    while not FFX_memory.userControl():
                        if FFX_memory.diagSkipPossible():
                            FFX_Xbox.tapB()
                    print("Done clicking")
                checkpoint += 1
            elif checkpoint < 6 and FFX_memory.getStoryProgress() >= 5:
                checkpoint = 6
            elif checkpoint < 11 and FFX_memory.getMap() == 371:
                checkpoint = 11
            elif checkpoint < 15 and FFX_memory.getMap() == 370:
                checkpoint = 15
            elif checkpoint == 17: #Don't cry.
                while FFX_memory.userControl():
                    FFXC.set_movement(1, -1)
                FFXC.set_neutral()
                checkpoint += 1
        
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.tidusHome(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                if FFX_memory.getStoryProgress() == 10 and FFX_memory.diagProgressFlag() == 2:
                    print("Special Skip")
                    FFX_memory.waitFrames(130)
                    FFXC.set_value('BtnStart', 1) #Generate button to skip later
                    FFX_memory.waitFrames(1)
                    FFXC.set_value('BtnStart', 0)
                    FFX_Xbox.SkipDialog(10)
                else:
                    if csModVar.usePause():
                        FFX_memory.waitFrames(1)
                    FFX_Xbox.skipScene(fast_mode=True)
                    FFX_Xbox.SkipDialog(3)


def ammesBattle():
    print("Starting ammes")
    FFX_Xbox.clickToBattle()
    FFX_memory.lastHitInit()
    FFX_Battle.defend()
    FFX_Logs.writeStats("First Six Hits:")
    print("First Six Hits:")
    
    print("Killing Sinspawn")
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            FFX_Battle.attack('none')
            while not FFX_memory.lastHitCheckChange():
                pass
    print("Done Killing Sinspawn")
    FFX_memory.waitFrames(6) #Just for no overlap
    print("Clicking to battle.")
    FFX_Xbox.clickToBattle()
    print("Waiting for Auron's Turn")
    print("At Overdrive")
    #Auron overdrive tutorial
    FFX_Battle.auronOD()

def AfterAmmes():
    FFX_memory.clickToControl()
    checkpoint = 0
    
    while FFX_memory.getMap() != 49:
        if FFX_memory.userControl():
            #Map changes and events
            if checkpoint == 6: #Save sphere
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint < 9 and FFX_memory.getStoryProgress() >= 20: #Swim to Jecht
                checkpoint = 9
            elif checkpoint < 11 and FFX_memory.getStoryProgress() >= 30: #Towards Baaj temple
                checkpoint = 11
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.allStartsHere(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.turnReady():
                FFX_Battle.Tanker()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipStoredScene(3)

def SwimToJecht() :
    #FFX_memory.awaitControl()
    
    #FFX_memory.waitFrames(30 * 1.5)
    print("Swimming to Jecht")
    
    FFXC.set_value('BtnA', 1)
    FFXC.set_movement(-1, -1)
    FFX_memory.waitFrames(30 * 8)
    while FFX_memory.userControl():
        FFXC.set_movement(-1, 1)
    
    FFXC.set_neutral()
    FFXC.set_value('BtnA', 0)
    print("We've now reached Jecht.")
    FFX_Xbox.SkipDialog(5)
    
    #Next, swim to Baaj temple
    FFX_memory.clickToControl()
    FFXC.set_movement(1, 0)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 0.6)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 5)
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 14)
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(30 * 1.5) # Line up with stairs
    
    FFXC.set_movement(0, 1)
    #FFX_memory.waitFrames(30 * 600)
    FFX_memory.waitFrames(30 * 3)
    
    while FFX_memory.getMap() == 48:
        pos = FFX_memory.getCoords()
        if pos[1] < 550:
            if pos[0] < -5:
                FFXC.set_movement(1, 1)
            elif pos[0] > 5:
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)
        else:
            if pos[1] > ((-1.00 * pos[0]) + 577.00):
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)
    
    FFXC.set_neutral()
    FFX_memory.waitFrames(30 * 0.3)
