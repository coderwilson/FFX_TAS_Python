import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_targetPathing

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def boatDance():
    print("No dancing this time")
    FFX_memory.waitFrames(30 * 50)

def ssLiki(earlyTidusGrid):
    checkpoint = 0
    while FFX_memory.getMap() != 43:
        if FFX_memory.userControl():
            #events
            if checkpoint == 1: #Group surrounding Yuna
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 3: #Talk to Wakka
                FFX_memory.clickToEventTemple(3)
                print("Ready for SS Liki menu")
                if earlyTidusGrid == False:
                    FFX_menu.Liki()
                    FFX_memory.closeMenu()
                checkpoint += 1
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.liki(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
                
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipScene()
            elif FFX_memory.battleActive():            
                print("Ready to start fight with Sin's Fin")
                FFX_Battle.SinFin()
                print("Sin's Fin fight complete. Waiting for next fight")
                FFX_Battle.Echuilles()
                print("Sinspawn Echuilles fight complete")

def ssWinno():
    FFX_memory.clickToControl()
    FFXC.set_movement(1, 0)
    FFX_memory.waitFrames(30 * 1.5)
    FFXC.set_neutral()
    
    #Talk to O'akaXXIII
    FFX_memory.clickToControl()
    FFXC.set_neutral() #Use target pathing later
    while not FFX_targetPathing.setMovement([-17, 32]):
        movingToOaka = True #AKA keep moving
    FFXC.set_movement(1, -1)
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFX_memory.clickToDiagProgress(21)
    FFX_memory.waitFrames(60)
    #FFX_memory.waitFrames(30 * 2)
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(30)
    #FFX_memory.waitFrames(30 * 1)
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(30)
    #FFX_memory.waitFrames(30 * 1)
    FFX_Xbox.tapDown()
    FFX_Xbox.tapLeft()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapRight()
    FFX_Xbox.tapRight()
    FFX_Xbox.tapRight()
    FFX_Xbox.tapUp() #1001
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(30)
    FFX_Xbox.tapDown()
    FFX_Xbox.tapB() #No Sweat
    FFX_memory.clickToControl3()
    
def ssWinno2():
    #To the deck
    FFX_memory.awaitControl()
    FFXC.set_movement(-1, -1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_neutral()
    
    #Lulu/Wakka talking
    FFX_memory.awaitControl()
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_movement(-1, -1)
    FFX_memory.waitFrames(30 * 0.6)
    FFXC.set_movement(1, 0)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_neutral()
    
    #Let's go dream of Jecht
    FFX_memory.clickToControl()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 3.5)
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(30 * 1.5)
    FFXC.set_neutral()
    
    #Jecht shot tutorial
    FFX_memory.clickToDiagProgress(96)
    while FFX_memory.diagProgressFlag() != 100:
        if FFX_memory.diagProgressFlag() == 97:
            FFXC.set_value('Dpad', 1) #Up
            FFXC.set_value('Dpad', 8) #Right
            FFX_Xbox.tapB()
        elif FFX_memory.diagProgressFlag() == 98:
            FFXC.set_value('Dpad', 4) #Left
            FFX_Xbox.tapB()
        elif FFX_memory.diagProgressFlag() == 99:
            FFXC.set_value('Dpad', 2) #Down
            FFXC.set_value('Dpad', 8) #Right
            FFX_Xbox.tapB()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        FFXC.set_neutral()
    
    #Let's attempt the jecht shot!
    FFX_Xbox.SkipDialog(2)
    print("Start Jecht Shot")
    jechtShot()
    print("End Jecht Shot")
    
    FFX_memory.clickToControl()
    FFXC.set_movement(1, 0)
    FFX_memory.waitFrames(30 * 3)
    FFXC.set_neutral()
    
    FFX_memory.clickToDiagProgress(142)
    FFX_Xbox.clearSavePopup(0)

def jechtShot():
    print("We are intentionally failing the Jecht shot. Save the frames!")
    #for x in range(20):
    #    FFX_Xbox.SkipDialog(1)
