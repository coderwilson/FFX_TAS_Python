import pyxinput
import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_memory

FFXC = FFX_Xbox.FFXC
 
 
def Entrance():
    FFX_Screen.awaitMap1()
    print("Starting Baaj exterior area")
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    #First, we need to change aeon summons ### MOVE THIS TO LATER
    FFX_Xbox.menuY()
    time.sleep(0.6)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    
    #Now back into the water
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    print("Mark 1")
    time.sleep(35)
    print("Mark 2")
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToBattle()
    
    #Once we lose control, just keep clicking until we regain control.
    FFX_Battle.attack('none')
    time.sleep(0.2)
    FFX_Screen.awaitTurn()
    FFX_Battle.attack('none')
    FFX_Screen.clickToBattle()
    while not FFX_memory.userControl():
        if FFX_Screen.BattleScreen():
            FFX_Battle.defend()
        else:
            FFX_Xbox.menuB()
    
    #Out of the frying pan, into the furnace
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[1] < 85:
            FFXC.set_value('AxisLx', -1)
            FFXC.set_value('AxisLy', 0)
        elif pos[1] < 130:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 1)
        elif pos[1] < 170:
            FFXC.set_value('AxisLx', -1)
            FFXC.set_value('AxisLy', 1)
        elif pos[1] < 190:
            FFXC.set_value('AxisLx', 1)
            FFXC.set_value('AxisLy', 1)
        elif pos[1] < 225:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 1)
        else:
            FFXC.set_value('AxisLx', -1)
            FFXC.set_value('AxisLy', 1)
        pos = FFX_memory.getCoords()
    

def Baaj_puzzle():
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToControl()
    print("Starting Baaj puzzle")
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', -1)
    
    time.sleep(2.8)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Xbox.touchSaveSphere()
    
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.5) #Into the first room
    FFX_memory.awaitControl()
    time.sleep(0.04)
    FFX_memory.clickToEvent() #Grab Flint
    FFXC.set_value('AxisLy', -1)
    FFX_memory.clickToControl()
    time.sleep(0.04)
    FFX_memory.clickToEvent() #Exit the room
    time.sleep(0.04)
    
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    #Across the room
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.6)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.25)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2.2)
    
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        pos = FFX_memory.getCoords()
        FFXC.set_value('AxisLy', 1)
        if pos[1] > ((-1.13 * pos[0]) + 11.75):
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    #FFXC.set_value('AxisLy', 1)
    #FFXC.set_value('AxisLx', 0)
    #time.sleep(3) #Enters the stair room/hallway
    #FFXC.set_value('AxisLy', 0)
    
    #Grab the withered bouquet
    FFX_memory.awaitControl()
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        pos = FFX_memory.getCoords()
        FFXC.set_value('AxisLy', 1)
        if pos[1] < ((0.80 * pos[0]) -85.80) or pos[1] < -88:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
        FFX_Xbox.menuB()
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    #Back down the hallway
    while FFX_memory.userControl():
        pos = FFX_memory.getCoords()
        if pos[1] < 82:
            FFXC.set_value('AxisLy', -1)
        else:
            FFXC.set_value('AxisLy', 0)
        if pos[1] < ((0.80 * pos[0]) -85.80) or pos[1] > 82:
            FFXC.set_value('AxisLx', 1)
        elif pos[1] < 25 and pos[0] > 74:
            FFXC.set_value('AxisLx', 1)
        elif pos[0] > 90:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
        FFX_Xbox.menuB()
    
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    #time.sleep(20)
    
    #Back in the main room
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', -1)
    FFX_Xbox.SkipDialog(2)
    
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    if FFX_memory.userControl():
        while FFX_memory.userControl():
            print("We missed the fireplace!")
            pos = FFX_memory.getCoords()
            if pos[0] > 2:
                FFXC.set_value('AxisLy', -1)
            elif pos[0] < -2:
                FFXC.set_value('AxisLy', 1)
            if pos[1] > 2:
                FFXC.set_value('AxisLx', -1)
            elif pos[1] < -2:
                FFXC.set_value('AxisLx', 1)
    
def Klikk_fight() :
    #Before Rikku shows up, we're just going to spam the click button. Simple.
    print("Waiting on Use tutorial")
    FFX_Screen.clickToPixel(897,295,(234, 199, 0))
        
    print("Doing Use tutorial")
    FFX_Screen.clickToBattle()
    FFX_Battle.useItem(1,'none')
    
    #Tidus self-potion
    FFX_Screen.awaitTurn()
    FFX_Battle.Klikk()
    
def ABboat1() :
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.3)
    FFX_Xbox.SkipDialog(4) #Start Sphere Grid tutorial
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', -1)
    FFX_Xbox.SkipDialog(1) #Talk to Rikku a second time.
    
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('BtnA', 1)
    FFX_memory.clickToControl()
    
    time.sleep(12)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('BtnA', 0)
    
def ABswimming1() :
    complete = 0
    
    print("Swimming towards airship")
    while complete == 0 :
        pos = FFX_memory.getCoords()
        ffxMap = FFX_memory.getMap()
        #print(ffxMap)
        if not FFX_memory.userControl():
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('BtnA', 0)
            if FFX_Screen.BattleScreen() :
                FFX_Battle.stealAndAttack()
        else:
            if ffxMap == 71:
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('BtnA', 1)
            elif ffxMap == 64:
                complete = 1
            else:
                checkpoint = 1
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('BtnA', 0)
                if pos[1] < ((2.56 * pos[0]) + 583.79):
                    FFXC.set_value('AxisLx', 1)
                else:
                    FFXC.set_value('AxisLx', 0)
        
def ABswimming2() :
    #Quick heal-up to make sure we're full HP on Rikku
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('BtnA', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('BtnA', 0)
    FFX_Xbox.touchSaveSphere()

    #Now to get to it
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.3)
    FFX_memory.clickToEvent()
    time.sleep(0.2)
    FFX_memory.awaitControl()
    
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        if pos[1] < 135:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
            
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.awaitTurn()
    #Final group of Pirhanas
    FFX_Battle.stealAndAttackPreTros()
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    print("Technical Support Tidus")
    FFX_Xbox.SkipDialog(2)
    FFXC.set_value('AxisLy', -1)
    FFX_Screen.clickToMap1()
    time.sleep(2)
    FFX_memory.clickToEvent()
    print("Engaging Tros")
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    #Tros fight
    FFX_Screen.clickToBattle()
    FFX_Battle.Tros()
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.awaitControl()
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(30)
    FFXC.set_value('AxisLx', 0)
    
    #Back onto the ship
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.35)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    FFX_Xbox.SkipDialog(1)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.awaitSave()