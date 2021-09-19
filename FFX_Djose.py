import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory

FFXC = FFX_Xbox.FFXC
 
def path():
    FFX_memory.clickToControl()
    FFX_memory.closeMenu()
    time.sleep(1)
    FFX_Screen.mrrFormat()
    FFX_memory.closeMenu()
    
    countBattles = 0
    checkpoint = 0
    lastCP = 0
    stoneBreath = 0
    print("Starting Djose pathing section")
    
    while checkpoint != 100:
        pos = FFX_memory.getCoords()
        if lastCP != checkpoint:
            lastCP = checkpoint
            print("Checkpoint reached: ", checkpoint)
        if FFX_memory.userControl():
            if checkpoint == 0: #First section, very long.
                if pos[1] > 60:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < ((4.07 * pos[0]) + 234.82):
                        FFXC.set_value('AxisLx', -1)
                    elif pos[1] > ((3.18 * pos[0]) + 281.79):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10: #Camera turns
                if pos[1] > 330:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] < ((1.53 * pos[0]) + 147.43):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 20: #Past the chest
                if pos[1] > 600:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((1.14 * pos[0]) + 238.11):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30: #Close to the cutscene
                if pos[1] > 730:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] < ((0.69 * pos[0]) + 368.90):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 40:
                if stoneBreath == 0:
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', -1)
                    time.sleep(1)
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(1)
                else:
                    checkpoint = 50
            elif checkpoint == 50: #Close to the cutscene
                if pos[1] > 835:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] < ((0.69 * pos[0]) + 368.90):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 60: #Start conversation with Auron, then to the temple
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                FFX_Xbox.SkipDialog(0.4)
                FFXC.set_value('AxisLx', 0)
                FFX_Xbox.SkipDialog(4)
                FFXC.set_value('AxisLy', 0)
                FFX_memory.clickToControl()
                FFXC.set_value('AxisLy', 1)
                FFX_Xbox.SkipDialog(3)
                FFXC.set_value('AxisLy', 0)
                checkpoint = 65
            elif checkpoint == 65: #Up to chocobo team
                if pos[1] > 1:
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((4.67 * pos[0]) -289.33):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 70: #Past chocobo team
                if pos[1] < -360:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < ((-2.67 * pos[0]) + 163.71):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 80:
                FFXC.set_value('AxisLy', 1)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                checkpoint = 100
                print("Checkpoing reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            if FFX_Screen.BattleScreen():
                print("Starting battle")
                if stoneBreath == 0:
                    print("Still looking for Stone Breath.")
                stoneBreath = FFX_Battle.djose(stoneBreath)
                print("Battles complete.")
                countBattles += 1
            elif FFX_memory.menuOpen():
                FFX_Xbox.menuB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()
            
    FFX_Logs.writeStats("Djose battles:")
    FFX_Logs.writeStats(countBattles)

def temple():
    FFX_memory.clickToControl()
    FFX_menu.djoseTemple()
    
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', 0)
    time.sleep(6)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.clickToEvent() #Talk to Auron
    time.sleep(0.2)
    FFX_memory.clickToControl3() #Done talking
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.SkipDialog(5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5) #Into the trials
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)

def trials():
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    #FFX_Screen.clickToPixel(794,829,(234, 143, 0)) #Removed Djose sphere
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.2)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    #FFX_Screen.clickToPixel(788,830,(234, 140, 0)) #Inserted Djose sphere
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.2)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    #FFX_Screen.clickToPixel(794,829,(234, 143, 0)) #Removed Djose sphere
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.2)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0) #Inserted Djose sphere. Door opens.
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', 1)
    time.sleep(4)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.3)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    #FFX_Screen.clickToPixel(794,829,(234, 143, 0)) #Removed Djose sphere
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(0.2)
    #FFX_Screen.clickToPixel(788,830,(234, 140, 0)) #Inserted Djose sphere (first)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    #FFX_Screen.clickToPixel(794,829,(234, 143, 0)) #Removed Djose sphere
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    #FFX_Screen.clickToPixel(788,830,(234, 140, 0)) #Inserted Djose sphere (second)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    while FFX_memory.userControl():
        pos = FFX_memory.getCoords() #Aligning
        if pos[0] > -5:
            FFXC.set_value('AxisLx', -1)
            FFXC.set_value('AxisLy', 0)
        elif pos[1] < 23:
            FFXC.set_value('AxisLy', 1)
            FFXC.set_value('AxisLx', 0)
        elif pos[1] > 26:
            FFXC.set_value('AxisLy', -1)
            FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', 1)
            FFXC.set_value('AxisLy', 0)
    
    
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    time.sleep(10) #Push pedestol
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    #FFX_Screen.clickToPixel(794,829,(234, 143, 0)) #Removed super Djose sphere
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToEvent() # Opens the door.
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.35)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    #FFX_Screen.clickToPixel(794,829,(234, 143, 0)) #Removed Djose sphere (first)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLx', 0)
    #FFX_Screen.clickToPixel(788,830,(234, 140, 0)) #Inserted Djose sphere (first)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    #FFX_Screen.clickToPixel(794,829,(234, 143, 0)) #Removed Djose sphere (second)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLx', 0)
    #FFX_Screen.clickToPixel(788,830,(234, 140, 0)) #Inserted Djose sphere (second)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0) #Reset switch
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.6)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.9)
    pos = FFX_memory.getCoords()
    while pos[1] < 165:
        if pos[1] > 79 and pos[1] < 90:
            FFXC.set_value('AxisLy', 0)
            #Have to stop moving when you hit the ledge in order to jump.
        else:
            FFXC.set_value('AxisLy', 1)
        if pos[0] < -5:
            FFXC.set_value('AxisLx', 1)
        elif pos[0] > 5:
            FFXC.set_value('AxisLx', -1)
        else:
            FFXC.set_value('AxisLx', 0)
        
        pos = FFX_memory.getCoords()
     
    FFXC.set_value('AxisLy', 1)
    FFX_Xbox.SkipDialog(3)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl3() #Jumping Back
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl3() #Door closed
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.7)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    #FFX_Screen.clickToPixel(788,830,(234, 140, 0)) #Inserted Djose sphere
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl3() #Reset switch
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.4)
    print("First sphere out of the pedestol")
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[0] < -8:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', -1)
        if pos[1] < 22:
            FFXC.set_value('AxisLy', 1)
        elif pos[1] > 26:
            FFXC.set_value('AxisLy', -1)
        else:
            FFXC.set_value('AxisLy', 0)
        FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    print("First sphere removed.")
    #FFX_Screen.clickToPixel(794,829,(234, 143, 0)) #Removed Djose sphere (first)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    time.sleep(4.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLx', 0)
    #FFX_Screen.clickToPixel(788,830,(234, 140, 0)) #Inserted Djose sphere (first)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3.7)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    print("Second sphere out of the pedestol")
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[0] < 7:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', -1)
        if pos[1] < 22:
            FFXC.set_value('AxisLy', 1)
        elif pos[1] > 26:
            FFXC.set_value('AxisLy', -1)
        else:
            FFXC.set_value('AxisLy', 0)
        FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    print("Second sphere removed.")
    FFX_Screen.clickToPixel(794,829,(234, 143, 0)) #Removed Djose sphere (second)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    time.sleep(4.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLx', 0)
    #FFX_Screen.clickToPixel(788,830,(234, 140, 0)) #Inserted Djose sphere (second)
    
    FFX_memory.clickToControl3()
    
    pos = FFX_memory.getCoords()
    while pos[1] < -10:
        FFXC.set_value('AxisLy', 1)
        if pos[0] < -5:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
        
    pos = FFX_memory.getCoords()
    while pos[0] > -40:
        FFXC.set_value('AxisLx', -1)
        if pos[1] < 17:
            FFXC.set_value('AxisLy', 1)
        else:
            FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
    
    #FFXC.set_value('AxisLx', 0)
    #FFXC.set_value('AxisLy', 0)
    #time.sleep(60) #Testing only
    
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[0] < -57:
            FFXC.set_value('AxisLx', 1)
        elif pos[0] > -51:
            FFXC.set_value('AxisLx', -1)
        else:
            FFXC.set_value('AxisLx', 0)
        if pos[1] < 30:
            FFXC.set_value('AxisLy', 1)
        else:
            FFXC.set_value('AxisLy', -1)
        FFXC.set_value('BtnB', 1)
        time.sleep(0.04)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.04)

        pos = FFX_memory.getCoords()
    
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0) #Door to the destro sphere opens
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    #FFX_Screen.clickToPixel(968,803,(234, 197, 0)) #Removed Destro Sphere
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3) #Elevator
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFX_memory.clickToEvent() #Pedestol 1
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.SkipDialog(5) #Pedestol 2
    FFXC.set_value('AxisLx', -1)
    FFX_Xbox.SkipDialog(5) #Pedestol 3
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    FFX_Xbox.SkipDialog(5) #Pedestol 4
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.SkipDialog(8) #Pedestol 5
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.awaitControl() #Extra pedestol spawns
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.2)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0) #Destro chest is good to go.
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.6)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(2)
    
    FFX_memory.awaitControl() #Green minimap door, aeon room before conversation
    print("Trials complete. Now waiting on Yuna/Donna")
    
    
    print("Talk to Auron while we wait.")
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    FFX_memory.clickToControl3()
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(20)
    
    FFX_memory.clickToControl()
    print("Leaving the fayth room")
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.1)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Xbox.SkipDialog(34)
    
    FFX_Screen.awaitPixel(352,233,(145, 141, 220)) #naming Ixion
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()

def leavingDjose():
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.8)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.clickToControl3()
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFX_memory.awaitControl()
    
    #inside
    print("Now inside the Djose temple.")
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.8)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.awaitEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    
    print("Ready for Yuna's room")
    FFX_memory.awaitControl()
    print("Inside Yuna's room.")
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFX_Xbox.SkipDialog(0.5)
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(0.5)
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.SkipDialog(5) #Starts the Yuna conversation.
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl() #We meet Tidus back outside.
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl() #Finally back in control
    while FFX_memory.userControl():
        pos = FFX_memory.getCoords()
        FFXC.set_value('AxisLx', -1)
        if pos[1] < -250:
            FFXC.set_value('AxisLy', 1)
        elif pos[1] > -230:
            FFXC.set_value('AxisLy', -1)
        else:
            FFXC.set_value('AxisLy', 0)
        FFX_Xbox.menuB()
    
    FFX_memory.clickToControl()
    
    while FFX_memory.userControl():
        pos = FFX_memory.getCoords()
        FFXC.set_value('AxisLy', -1)
        if pos[0] < -100:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToControl() #Conversation with Lucil and her crew
    
    FFXC.set_value('AxisLy', -1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0) #Leave the bridge area
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.clickToEvent() #Last convo in Djose
    FFX_Xbox.SkipDialog(2)
    FFX_memory.clickToControl()
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)