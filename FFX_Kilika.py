import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_menuGrid
import FFX_memory

FFXC = FFX_Xbox.FFXC

def arrival():
    print("Arrived at Kilika docks.")
    
    #Save sphere
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    #FFXC.set_value('AxisLx', -1)
    #time.sleep(0.2)
    #FFXC.set_value('AxisLx', 0)
    #FFX_Xbox.touchSaveSphere()
    
    #To next screen
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.6)
    FFXC.set_value('AxisLx', 0)
    time.sleep(5)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.awaitMap2()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(78)
    FFX_Xbox.skipSceneSpec()
    time.sleep(0.1)
    FFX_Xbox.menuX()
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToMap1() #Talking to the Aurochs guy.
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2.5)
    FFXC.set_value('AxisLy', 0)
    
    #Now to talk to Wakka
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.clickToMap1() #Talking to Wakka
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    #Save the girl, then to the forest
    #Actually, don't save the girl. Too slow.
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(3.5)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)


def forest1():
    FFX_Screen.awaitMap1()
    FFX_menu.autoSortItems('n')
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(10)
    FFX_Screen.clickToBattle()
    FFX_Battle.lancetTutorial()
    FFX_memory.clickToControl()
    
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.awaitPixel(905,444,(212, 212, 212)) #Obtained Scout
    FFX_memory.clickToControl()
    
    #Tidus learning Flee
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB() #Sphere grid on Tidus
    FFX_menuGrid.moveFirst()
    FFX_menuGrid.gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability', 'd', 'none')
    FFX_menuGrid.useAndQuit()
    #Reorder the party
    
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuA()
    time.sleep(0.2)
    #FFX_Xbox.menuA()
    #time.sleep(0.2)
    
    #Now for Wakka's weapon, Scout with icestrike
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Equip
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Wakka
    time.sleep(0.4)
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    
def forest2():
    speedCount = 0
    checkpoint = 0
    lastCP = 0
    valeforCharge = False
    while checkpoint != 1000:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_Screen.BattleScreen():
            valeforCharge = FFX_Battle.KilikaWoods(valeforCharge)
            FFX_memory.getSpeed()
        elif FFX_memory.userControl() == False:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if checkpoint == 80 or checkpoint > 600:
                FFX_Xbox.menuB()
        else:
            pos = FFX_memory.getCoords()
            if checkpoint == 0:
                if pos[1] > -300:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 10:
                if pos[1] > -108:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] > -230:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20:
                if pos[1] > -37:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < -240: #Slight juke right
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if pos[1] > 30:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 40:
                if pos[0] > -115:
                    checkpoint = 50
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] > 70:
                        FFXC.set_value('AxisLy', -1)
                    elif pos[1] < 63:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 50:
                if pos[1] > 135:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < -90:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60:
                if pos[1] > 200:
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((-1.93 * pos[0]) -11.00):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 70:
                if pos[0] < -230:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > 210:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 80:
                if FFX_memory.getItemSlot(94) != 255:
                    checkpoint = 90
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
                    FFXC.set_value('BtnB', 1)
                    time.sleep(0.04)
                    FFXC.set_value('BtnB', 0)
                    time.sleep(0.04)
            elif checkpoint == 90:
                if pos[1] < 100:
                    checkpoint = 400
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] > ((-2.22 * pos[0]) -41.78):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 400:
                if pos[0] > 166:
                    checkpoint = 500
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] > 70:
                        FFXC.set_value('AxisLy', -1)
                    elif pos[1] < 63:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 500:
                if pos[1] > 190:
                    checkpoint = 600
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > 179:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 600:
                if pos[0] < -70:
                    checkpoint = 650
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > 280:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 650:
                print("Valefor charge state: ", valeforCharge)
                if valeforCharge == True:
                    checkpoint = 700
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
                    time.sleep(1)
                    FFXC.set_value('AxisLy', -1)
                    time.sleep(1)
                    FFXC.set_value('AxisLy', 0)
            elif checkpoint == 700:
                if pos[1] < 200:
                    checkpoint = 1000
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < -75:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)

def forest2_old() :
    speedCount = 0
    stepCount = 0
    stepMax = 160
    while stepCount < stepMax :
        if FFX_Screen.Minimap1() and not FFX_Screen.PixelTest(326,154,(193, 193, 193)) :
            print("Kilika movement, North, stepCounter: ",stepCount)
            if stepCount < 4 :
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 10 :
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 20:
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 21 : #Align with the narrow path
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 28 : #Align with the narrow path
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 40 :
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 54 :
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 58 : #Slightly up to avoid getting stuck
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 76 : #To the far right
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 79 :
                FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 100 :
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 110 : #Diagonal, towards the temple
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                FFX_Xbox.SkipDialog(0.3)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 120 :
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            else  :
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
            stepCount += 1
        elif FFX_Screen.Minimap1() and FFX_Screen.PixelTest(326,154,(193, 193, 193)) :
            stepCount = stepMax
        elif FFX_Screen.BattleScreen() :
            speedCount += FFX_Battle.KilikaWoods()
        elif stepCount > 100:
            FFX_Xbox.menuB()
    print("Speed spheres obtained through Kilika North: ", speedCount)
    return speedCount

def Geneaux():
    FFX_menu.Geneaux()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.touchSaveSphere()
    FFXC.set_value('AxisLx', -1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Battle.Geneaux()
    
    #After the battle, head to the temple.
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    
    #Approach scene with the Luca Goers
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    
    #Enter the temple
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(5)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    
def trials():
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(3)
    FFXC.set_value('AxisLx', 0)
    
    #Scene with Donna
    print("Let's talk to Donna. Such a charming woman!")
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.6)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    
    #Onto the lift, then to the door. Just keep clicking.
    pos = FFX_memory.getCoords()
    while pos[1] < 150:
        FFXC.set_value('AxisLy', 1)
        FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFX_memory.awaitEvent()
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.awaitPixel(850,500,(202, 202, 202))
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(0.1)
    
    #Wait for control in trials room
    FFX_memory.clickToControl()
    print("Move to pedestol")
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB()
    FFX_memory.clickToControl3()
    print("Sphere picked up")
    
    print("Move to burn down first door")
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.6)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB()
    FFX_memory.clickToControl3()
    print("Door is now on fire and we have control back.")
    time.sleep(0.1)
    FFX_Xbox.menuB()
    FFX_memory.clickToControl3()
    
    #Make the glyph appear
    print("Moving through the door")
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.2)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.35)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2)
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        if pos[0] < -5:
            FFXC.set_value('AxisLx', 1)
        elif pos[0] > 5:
            FFXC.set_value('AxisLx', -1)
        else:
            FFXC.set_value('AxisLx', 0)
        FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB()
    print("Inserting sphere")
    FFX_memory.clickToControl3()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    FFX_memory.clickToControl3()
    
    print("Moving to place the sphere out of the way")
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.6)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB()
    FFX_memory.clickToControl3()
    
    print("Now touch the glyph")
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.7)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB()
    FFX_memory.clickToControl3()
    
    print("Into the next room")
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[1] < 120:
            FFXC.set_value('AxisLy', 1)
            FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', 1)
            if pos[1] < 172:
                FFXC.set_value('AxisLy', 1)
            else:
                FFXC.set_value('AxisLy', 0)
            FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.1)
    FFX_Xbox.menuB()
    FFX_memory.clickToControl3()
    
    print("Back with the extra fire sphere")
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.3)
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[1] > 25:
            FFXC.set_value('AxisLy', -1)
            if pos[0] < -5:
                FFXC.set_value('AxisLx', 1)
            elif pos[0] > 5:
                FFXC.set_value('AxisLx', -1)
            else:
                FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', -1)
            if pos[1] > -1:
                FFXC.set_value('AxisLy', -1)
            else:
                FFXC.set_value('AxisLy', 0)
            FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.1)
    FFX_Xbox.menuB()
    FFX_memory.clickToControl3()
    
    print("Moving to glyph sphere")
    pos = FFX_memory.getCoords()
    while pos[0] < -25:
        pos = FFX_memory.getCoords()
        FFXC.set_value('AxisLy', 0)
        FFXC.set_value('AxisLx', 1)
    while FFX_memory.userControl():
        if pos[1] < -33:
            FFXC.set_value('AxisLy', 1)
            if pos[0] < -22:
                FFXC.set_value('AxisLx', 1)
            else:
                FFXC.set_value('AxisLx', -1)
        else:
            FFXC.set_value('AxisLy', -1)
            FFXC.set_value('AxisLx', 0)
        FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFX_Xbox.SkipDialog(1.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl3()
    
    print("Back into the fire room")
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[1] < 120:
            FFXC.set_value('AxisLy', 1)
            if pos[0] < -5:
                FFXC.set_value('AxisLx', 1)
            elif pos[0] > 5:
                FFXC.set_value('AxisLx', -1)
            else:
                FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', 1)
            if pos[1] < 172:
                FFXC.set_value('AxisLy', 1)
            else:
                FFXC.set_value('AxisLy', 0)
            FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.1)
    FFX_Xbox.menuB()
    FFX_memory.clickToControl3()
    
    print("Circle back for the spare fire sphere")
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.3)
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[1] > 25:
            FFXC.set_value('AxisLy', -1)
            if pos[0] < -5:
                FFXC.set_value('AxisLx', 1)
            elif pos[0] > 5:
                FFXC.set_value('AxisLx', -1)
            else:
                FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', -1)
            if pos[1] > -1:
                FFXC.set_value('AxisLy', -1)
            else:
                FFXC.set_value('AxisLy', 0)
        FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.1)
    FFX_Xbox.menuB()
    FFX_memory.clickToControl3()
    
    print("Heading to the exit")
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.3)
    pos = FFX_memory.getCoords()
    while pos[1] < 165:
        if pos[1] < 120:
            FFXC.set_value('AxisLy', 1)
            if pos[0] < -5:
                FFXC.set_value('AxisLx', 1)
            elif pos[0] > 5:
                FFXC.set_value('AxisLx', -1)
            else:
                FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', -1)
            FFXC.set_value('AxisLy', 1)
        pos = FFX_memory.getCoords()
    while pos[0] < 30:
        if pos[1] < 200:
            FFXC.set_value('AxisLy', 1)
            if pos[0] < -35:
                FFXC.set_value('AxisLx', 1)
            else:
                FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', 1)
            if pos[1] > 220:
                FFXC.set_value('AxisLy', -1)
            else:
                FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
    while pos[1] < 260:
        FFXC.set_value('AxisLy', 1)
        FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[1] < 275:
            FFXC.set_value('AxisLy', 1)
        else:
            FFXC.set_value('AxisLy', 0)
        if pos[0] > 13:
            FFXC.set_value('AxisLx', -1)
        else:
            FFXC.set_value('AxisLx', 0)
        FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    print("Attempting to open the door")
    FFX_memory.clickToControl3()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    #Into the cloyster room
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    FFX_Xbox.SkipDialog(2)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    FFX_Xbox.SkipDialog(15)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    FFX_memory.clickToControl()
    time.sleep(0.5)
    FFX_Xbox.SkipDialog(6)
    FFXC.set_value('AxisLy', 0)
    
    #Name Ifrit and get out of here.
    FFX_Screen.clickToPixel(270,348,(0,0,0))
    FFX_Screen.awaitPixel(270,348,(246, 211, 161))
    time.sleep(0.15)
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFXC.set_value('AxisLy', -1)
    FFX_Xbox.SkipDialog(10)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToControl()

def forest3():
    
    #First, re-order the party
    FFX_memory.fullPartyFormat('kilika')
    
    speedCount = 0
    checkpoint = 0
    lastCP = 0
    while checkpoint != 1000:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_Screen.BattleScreen():
            FFX_Battle.KilikaWoods(True)
            print("Speed sphere count:")
            FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(72))
        elif not FFX_memory.userControl():
            if FFX_Screen.PixelTestTol(652,447,(205, 205, 205),5):
                print("Chest is opened.")
                FFX_Xbox.menuB()
                checkpoint = 60
            else:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
        else:
            pos = FFX_memory.getCoords()
            if checkpoint == 0:
                if pos[1] < 300:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10:
                if pos[1] < 90:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] < 50:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20: #Skipping direct to 80, no need to pick up chest now.
                if pos[0] < -50:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] < 75:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 30:
                if pos[0] < -150:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 40:
                if pos[0] < -254:
                    checkpoint = 50
                else:
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', 1)
            elif checkpoint == 50:
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', -1)
                FFX_Xbox.SkipDialog(1)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60:
                if pos[0] > -120:
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', -1)
            elif checkpoint == 70:
                if pos[1] < 72:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] < -100:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > -80:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 80:
                if pos[0] < -233:
                    checkpoint = 90
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] > 70:
                        FFXC.set_value('AxisLy', -1)
                    elif pos[1] < 63:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 90: #Down to the four-way spot.
                if pos[1] < -105:
                    checkpoint = 100
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 100: #Across the four-way spot
                if pos[1] < -150:
                    checkpoint = 110
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] > -242:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 110:
                if pos[1] < -300:
                    checkpoint = 115 #Skip 120, no need to farm Speed Spheres now.
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 115: #Don't get stuck.
                if pos[1] < -410:
                    checkpoint = 130
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] > -219:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 120: #Delay for Speed Spheres. Disabled at this time.
                if FFX_memory.getSpeed() < 16:
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(1)
                    FFXC.set_value('AxisLy', -1)
                    time.sleep(1)
                else:
                    checkpoint = 130
            elif checkpoint == 130:
                if pos[0] > -70:
                    checkpoint = 140
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] < (0.07 * (float(pos[0])) - 400):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 140:
                if pos[1] > 1:
                    checkpoint = 1000
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)

def forest3_old():
    speedCount = 0
    stepCount = 0
    stepMax = 250
    #Now for pathing/battles
    while stepCount < stepMax :
        if FFX_Screen.Minimap1() and not FFX_Screen.PixelTest(338,196,(64, 193, 64)) :
            print("Kilika movement, South, stepCounter: ",stepCount)
            if stepCount < 10 :
                FFXC.set_value('AxisLy', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 20 :
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 40:
                FFXC.set_value('AxisLy', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 42 :
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 45 :
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 48 :
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 65 :
                FFXC.set_value('AxisLx', -1)
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 75 :
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 88 : #Grab the chest
                FFXC.set_value('AxisLx', -1)
                FFXC.set_value('AxisLy', 1)
                FFX_Xbox.SkipDialog(0.5)
                FFXC.set_value('AxisLx', 0)
                FFX_Xbox.SkipDialog(0.15)
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 105 :
                FFXC.set_value('AxisLy', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 109 :
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                FFX_Xbox.SkipDialog(1)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 120 :
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 144 :
                FFXC.set_value('AxisLx', -1)
                FFXC.set_value('AxisLy', -1)
                time.sleep(0.15)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.3)
                FFXC.set_value('AxisLy', 0)
            else :
                FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', -1)
                time.sleep(0.15)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.3)
                FFXC.set_value('AxisLy', 0)
            stepCount += 1
        elif FFX_Screen.Minimap1() and FFX_Screen.PixelTest(338,196,(64, 193, 64)) :
            stepCount = stepMax
        elif FFX_Screen.BattleScreen() :
            speedCount += FFX_Battle.KilikaWoods()

def departure():
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(2.4)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
        
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    #FFXC.set_value('AxisLy', 1)
    #FFXC.set_value('AxisLx', 0)
    #time.sleep(1.2)
    #FFXC.set_value('AxisLx', -1)
    #time.sleep(4)
    #FFX_Xbox.menuB()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', -1)
        FFXC.set_value('AxisLx', 0)
        
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    #Keep running south until Embark comes up on the screen
    FFX_Xbox.SkipDialog(10)