import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_targetPathing

FFXC = FFX_Xbox.FFXC

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
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
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
                while FFX_memory.cutsceneSkipPossible() == False:
                    time.sleep(0.035)
                FFX_Xbox.skipScene()
                FFX_Xbox.SkipDialog(20) #Avoids repeated pressing of the Start button

def ssLiki_old(earlyTidusGrid):
    print("Boarding SS Liki")
    
    #Save sphere
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.touchSaveSphere()
    
    #To the boat!
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3.05)
    FFXC.set_value('AxisLx', 1)
    time.sleep(7)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    #Separate function to do the dancing
    boatDance()
    
    #Wait for the boat scene
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(4)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.6)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(2)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl()
    
    #Menuing before Sinspawn fights
    if earlyTidusGrid == False:
        FFX_menu.Liki()
    FFX_memory.closeMenu()
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.6)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    #Wait for the four cutscenes, skip each
    print("Standing by to skip scenes")
    time.sleep(219.5)
    FFX_Xbox.skipScene() #Skip 1
    time.sleep(21)
    FFX_Xbox.skipScene() #Skip 2
    time.sleep(6.5)
    FFX_Xbox.skipScene() #Skip 3
    FFX_Xbox.SkipDialog(28)
    FFX_Xbox.skipScene() #Skip 4
    
    print("Ready to start fight with Sin's Fin")
    FFX_Battle.SinFin()
    print("Sin's Fin fight complete. Waiting for next fight")
    FFX_Battle.Echuilles()
    print("Sinspawn Echuilles fight complete")
    FFX_memory.clickToControl()

def ssWinno():
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    
    #Talk to O'akaXXIII
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.6)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(1)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToPixel(579,336,(220, 220, 220)) #Lending gil
    time.sleep(0.8)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuUp() #1001
    FFX_Xbox.menuB()
    time.sleep(0.8)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #No Sweat
    time.sleep(0.5)
    FFX_Xbox.menuB() #dialog
    
    #To the deck
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    #Lulu/Wakka talking
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    
    #Let's go dream of Jecht
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    time.sleep(3.5)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    #Jecht shot tutorial
    FFX_Screen.clickToPixelTol(956,404,(234, 152, 0),5) #First tutorial box
    FFX_Screen.clickToPixelTol(1410,238,(222, 222, 222),5) #Upper right box.
    
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    FFX_Xbox.SkipDialog(0.3)
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(0.4)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(0.4)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    FFX_Xbox.SkipDialog(0.4)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(2)
    
    #Let's attempt the jecht shot!
    print("Start Jecht Shot")
    jechtShot()
    print("End Jecht Shot")
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.awaitSave()
    #FFX_Xbox.skipSave()

def jechtShot():
    print("We are intentionally failing the Jecht shot. Save the frames!")
    for x in range(20):
        FFX_Xbox.SkipDialog(1)

def jechtShot_success():
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.menuB()
    FFXC.set_value('AxisLy', 1)
    FFX_Xbox.menuB()
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB()
    FFXC.set_value('AxisLx', -1)
    FFX_Xbox.menuB()
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB()
    FFXC.set_value('AxisLy', -1)
    FFX_Xbox.menuB()
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB()
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.menuB()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB()