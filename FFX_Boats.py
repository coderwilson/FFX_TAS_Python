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
    time.sleep(50)

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
    time.sleep(1.5)
    FFXC.set_neutral()
    
    #Talk to O'akaXXIII
    FFX_memory.clickToControl()
    FFXC.set_movement(1, -1)
    time.sleep(0.6)
    FFXC.set_movement(0, -1)
    FFX_Xbox.SkipDialog(1)
    FFXC.set_neutral()
    FFX_Xbox.clickToPixel(579,336,(220, 220, 220)) #Lending gil
    time.sleep(0.8)
    FFX_Xbox.gridDown()
    FFX_Xbox.gridLeft()
    FFX_Xbox.gridUp()
    FFX_Xbox.gridRight()
    FFX_Xbox.gridRight()
    FFX_Xbox.gridRight()
    FFX_Xbox.gridUp() #1001
    FFX_Xbox.tapB()
    time.sleep(0.5)
    FFX_Xbox.gridDown()
    FFX_Xbox.menuB() #No Sweat
    time.sleep(0.3)
    FFX_Xbox.menuB() #dialog
    
    #To the deck
    FFX_memory.awaitControl()
    FFXC.set_movement(-1, -1)
    time.sleep(2)
    FFXC.set_neutral()
    
    #Lulu/Wakka talking
    FFX_memory.awaitControl()
    FFXC.set_movement(-1, 1)
    time.sleep(1)
    FFXC.set_movement(-1, -1)
    time.sleep(0.6)
    FFXC.set_movement(1, 0)
    time.sleep(1)
    FFXC.set_neutral()
    
    #Let's go dream of Jecht
    FFX_memory.clickToControl()
    FFXC.set_movement(0, 1)
    time.sleep(3.5)
    FFXC.set_movement(-1, 1)
    time.sleep(1.5)
    FFXC.set_neutral()
    
    #Jecht shot tutorial
    FFX_Xbox.clickToPixelTol(956,404,(234, 152, 0),5) #First tutorial box
    FFX_Xbox.clickToPixelTol(1410,238,(222, 222, 222),5) #Upper right box.
    
    FFXC.set_value('Dpad', 1) #Up
    FFXC.set_value('Dpad', 8) #Right
    FFX_Xbox.SkipDialog(1)
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 4) #Left
    FFX_Xbox.SkipDialog(1)
    FFXC.set_neutral() #Neutral
    FFX_Xbox.SkipDialog(1)
    FFXC.set_value('Dpad', 2) #Down
    FFXC.set_value('Dpad', 8) #Right
    FFX_Xbox.SkipDialog(1)
    FFXC.set_neutral()
    FFX_Xbox.SkipDialog(2)
    
    #Let's attempt the jecht shot!
    print("Start Jecht Shot")
    jechtShot()
    print("End Jecht Shot")
    
    FFX_memory.clickToControl()
    FFXC.set_movement(1, 0)
    time.sleep(3)
    FFXC.set_neutral()
    
    FFX_Xbox.awaitSave()

def jechtShot():
    print("We are intentionally failing the Jecht shot. Save the frames!")
    #for x in range(20):
    #    FFX_Xbox.SkipDialog(1)
