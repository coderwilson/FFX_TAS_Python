import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_targetPathing

FFXC = FFX_Xbox.FFXC

def arrival():
    FFX_Xbox.skipStoredScene(7)
    print("Starting Luca section")
    FFX_memory.clickToControl()
    
    earlyHaste = 0
    checkpoint = 0
    while checkpoint < 46:
        if FFX_memory.userControl():
            #events
            if checkpoint == 4: #Seymour intro scene
                print("Event: Seymour intro scene")
                FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', 0)
                FFX_memory.awaitEvent()
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFX_Screen.awaitSave()
                time.sleep(0.07)
                FFX_Xbox.skipSave()
                
                FFX_Xbox.SkipDialog(26)
                FFX_Screen.awaitPixel(664,200,(234, 189, 0))
                time.sleep(0.6)
                FFX_Xbox.menuA()
                FFX_Xbox.menuB()
                FFX_Xbox.SkipDialogSpecial(45) #Skip the Wakka Face scene
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 8: #Upside down T section
                print("Event: Upside down T section")
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 17: #Into the bar
                print("Event: Into the bar looking for Auron")
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 1)
                FFX_memory.awaitEvent()
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
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
                FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', 1)
                FFX_memory.awaitEvent()
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFX_Battle.LucaWorkers()
                checkpoint += 1
            elif checkpoint == 34: #Third battle
                print("Tidus's XP: ", FFX_memory.getTidusXP())
                if FFX_memory.getTidusXP() >= 312:
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', 0)
                    earlyHaste = FFX_menu.LucaWorkers()
                    if earlyHaste != 0:
                        earlyHaste = 2
                print("Event: Third battle")
                FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', 0)
                FFX_memory.awaitEvent()
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFX_Battle.LucaWorkers2(earlyHaste)
                print("Tidus's XP: ", FFX_memory.getTidusXP())
                FFX_memory.clickToControl()
                if earlyHaste == 0 and FFX_memory.getTidusXP() >= 312:
                    earlyHaste = FFX_menu.LucaWorkers()
                        
                checkpoint += 1
            elif checkpoint == 36 or checkpoint == 45:
                print("Event: Touch Save Sphere")
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.02)
                FFX_Xbox.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 38: #Oblitzerator
                print("Event: Oblitzerator fight")
                FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', 0)
                #time.sleep(2)
                FFX_memory.awaitEvent()
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
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
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
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
    return earlyHaste

def arrival_old():
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
    print("followYuna function no longer used")

def followYuna_old():
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
    print("preBlitz function is no longer used.")

def preBlitz_old():
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
    FFX_Screen.clickToBattle()
    battleNum = 0
    checkpoint = 0
    while checkpoint < 36:
        if FFX_memory.userControl():
            #Events
            if checkpoint == 8: #First chest
                if earlyHaste == -1:
                    FFX_menu.lateHaste()
                    FFX_memory.closeMenu()
                print("First chest")
                FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 10: #Second chest
                print("Second chest")
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 20: #Target Auron
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
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            if FFX_memory.battleActive():
                battleNum += 1
                print("After-Blitz Battle Number: ", battleNum)
                if battleNum == 1:
                    FFX_Battle.afterBlitz1(earlyHaste)
                elif battleNum == 2:
                    FFX_Screen.clickToBattle()
                    FFX_Battle.attack('none') #Hardest boss in the game.
                    print("Well that boss was difficult.")
                    time.sleep(6)
                elif battleNum == 3:
                    FFX_Battle.afterBlitz3(earlyHaste)
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
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
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)

def afterBlitz_old(earlyHaste):
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
        if pos[1] > ((-4.06 * pos[0]) -1320):
            FFXC.set_value('AxisLx', 1)
        elif pos[1] < ((-4.06 * pos[0]) -1370): #1350 was slightly too high
            FFXC.set_value('AxisLx', -1)
        else:
            FFXC.set_value('AxisLx', 0)
        FFXC.set_value('BtnB', 1)
        time.sleep(0.035)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.035)
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