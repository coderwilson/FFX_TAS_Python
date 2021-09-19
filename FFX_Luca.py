import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory

FFXC = FFX_Xbox.FFXC
 
def arrival():
    FFX_Xbox.skipStoredScene(7)
    print("Starting Luca section")
    FFX_memory.clickToControl()
    print("Back in control")
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', -1)
    time.sleep(2.2)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.awaitSave()
    FFX_Xbox.skipSave()
    
    FFX_Xbox.SkipDialog(28)
    FFX_Screen.awaitPixel(664,200,(234, 189, 0))
    time.sleep(0.15)
    FFXC.set_value('BtnA', 1)
    time.sleep(0.035)
    FFXC.set_value('BtnA', 0)
    time.sleep(0.035)
    #FFX_Xbox.menuA()
    FFX_Xbox.menuB()
    
    FFX_Xbox.SkipDialogSpecial(45) #Skip the Wakka Face scene
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToMap4()
    FFXC.set_value('AxisLy', -1)
    time.sleep(9)
    FFXC.set_value('AxisLy', 0)
    
    #whistling scene, then run right.
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLx', 1)
    time.sleep(4)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToMap2()
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2.1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(5)
    FFXC.set_value('AxisLy', 0) #Into the shop
    
    #Blitzball introduction skip at the end of lots of talking.
    FFX_Xbox.SkipDialog(70)
    FFX_Xbox.skipScene()
    FFX_Screen.clickToMap1()
    
    FFXC.set_value('AxisLx', -1)
    time.sleep(3.5)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)

def followYuna():
    print("On hold")
    FFX_Screen.awaitMap4()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(6)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.35)
    
    #Enter first battle
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(8)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Battle.LucaWorkers()
    
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Battle.LucaWorkers()
    FFXC.set_value('AxisLx', 1)
    time.sleep(6)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToBattle()
    FFX_Battle.LucaWorkers2()
    
    #earlyHaste = 0
    #if FFX_memory.getTidusSlvl() >= 3:
    #    earlyHaste = FFX_menu.LucaWorkers() #Heal Lulu and learn haste with Tidus
    #else:
    #    earlyHaste = 2
    
    #Done with worker battles
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.12)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2.45)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.touchSaveSphere()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Battle.Oblitzerator(0)
    FFX_Logs.writeStats("Early Haste:")
    
    FFX_Screen.clickToMap1()
    
    #if earlyHaste == 0:
    #    FFX_Logs.writeStats("No")
    #    FFX_menu.lateHaste()
    #elif earlyHaste == 2:
    #    FFX_menu.LucaWorkers()
    #else:
    #    FFX_Logs.writeStats("Yes")
    

def preBlitz():
    FFXC.set_value('AxisLy', -1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    
    
    FFX_Screen.awaitMap1()
    earlyHaste = 0
    if FFX_memory.getTidusSlvl() >= 3:
        earlyHaste = FFX_menu.LucaWorkers() #Heal Lulu and learn haste with Tidus
    else:
        earlyHaste = 2
    FFXC.set_value('AxisLy', -1)
    time.sleep(5)
    FFXC.set_value('AxisLy', 0)
    
    while not FFX_Screen.Minimap4():
        if FFX_Screen.Minimap1():
            FFXC.set_value('AxisLy', -1)
            time.sleep(1)
            FFXC.set_value('AxisLy', 0)
    
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.15)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.touchSaveSphere()
    return earlyHaste
    
def blitzStart():
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    #Just outside the locker room
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    #Inside locker room
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.8)
    FFXC.set_value('AxisLx', 0)
    
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.SkipDialog(2) #Talk to Wakka, starts the Blitzball game
    FFXC.set_value('AxisLx', 0)

def afterBlitz(earlyHaste):
    print("Blitz is complete. Now for the battles.")
    FFX_Battle.afterBlitz()
    
    #Skip dialog until Anima is summoned
    FFX_Xbox.SkipDialog(47)
    FFX_Xbox.skipScene()
    FFX_Screen.awaitSave()
    
    #Lots of exposition. Click through it all! Then grab some chests and find the party.
    FFX_memory.clickToControl()
    
    #FFX_menu.afterBlitz()
    if earlyHaste == 0:
        FFX_menu.lateHaste()
    FFXC.set_value('AxisLy', 1)
    time.sleep(2.2) ### Line up
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.2)
    #FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', -1)
    print("Grabbing first chest.")
    FFX_Xbox.SkipDialog(1) #First chest
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    print("Grabbing second chest")
    FFX_Xbox.SkipDialog(1.5) #Second chest
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.clickToControl2()
    time.sleep(1.2)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.7)
    pos = FFX_memory.getCoords()
    while pos[1] < -190:
        FFXC.set_value('AxisLy', -1)
        if pos[1] < ((0.76 * pos[0]) + 27.47):
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', -1)
        if pos[0] > -270:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
        FFX_Xbox.menuB() #Just in case we can try to talk to Auron here.
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.1)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.5)
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', -1)
        FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.1)
    FFX_memory.awaitControl()
    
    #Reverse T screen
    FFXC.set_value('AxisLx', 1)
    time.sleep(4.5)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    
    #Carnival vendor screen
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3.3)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl2() #Scene, rejoining the party
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0) #Enters laughing scene, ends Luca section.