import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_memory

FFXC = FFX_Xbox.FFXC
 
 
def Beach():
    print("Starting Besaid section. Beach")
    FFXC.set_value('AxisLy', -1)
    FFX_memory.awaitControl()
    time.sleep(4.5)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(20)
    FFX_memory.clickToControl()
    print("Run to Wakka")
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    #Time to head to the village (via Pirahnas, it's fine)
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.2)
    #FFXC.set_value('AxisLy', 0)
    #FFXC.set_value('AxisLx', 1)
    #time.sleep(0.8)
    #FFXC.set_value('AxisLx', 0)
    #FFXC.set_value('AxisLy', -1)
    #time.sleep(0.5)
    #FFXC.set_value('AxisLy', 0)
    
    #FFX_Xbox.touchSaveSphere()
    
    FFXC.set_value('AxisLy', -1)
    FFX_memory.awaitEvent()
    time.sleep(0.1)
    FFX_memory.awaitControl()
    time.sleep(0.6)
    while FFX_memory.getCoords()[1] < -20:
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(12)
    FFXC.set_value('AxisLx', 0)
    
    #Now in the water
    FFX_memory.clickToControl() #Wakka pushing Tidus into the water.
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    

def swimming1():
    print("Start of swimming section in Besaid.")
    checkpoint = 0
    lastCP = 0
    while checkpoint < 100:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            pos = FFX_memory.getCoords()
            if checkpoint == 0:
                if pos[0] > 250:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((-0.63 * pos[0]) -572):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10:
                if pos[0] > 435:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((0.29 * pos[0]) -780.57):
                        FFXC.set_value('AxisLx', 1)
                    elif pos[1] < ((0.29 * pos[0]) -790.57):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20:
                if pos[1] > -420:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((2.65 * pos[0]) -1826.94):
                        FFXC.set_value('AxisLx', 1)
                    elif pos[1] < ((2.65 * pos[0]) -1856.94):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if FFX_memory.getMap() != 41:
                    checkpoint = 100
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 535:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 545:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
        elif FFX_Screen.BattleScreen():
            battleNum = FFX_memory.getBattleNum()
            #11 = two pirhanas
            #12 = three pirhanas with one being a triple formation (takes two hits)
            #13 = four pirhanas
            if battleNum == 11:
                FFX_Battle.attack('none')
            else:
                FFX_Battle.escapeAll()
        elif FFX_Screen.BattleComplete():
            FFXC.set_value('BtnB', 1)
            time.sleep(0.035)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.035)
        elif not FFX_memory.userControl():
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if checkpoint > 20:
                FFX_Xbox.menuB()

def swimming1_old() :
    Complete = 0
    path = 0
    
    straight = 13
    turn = straight + 3
    recover = turn + 5
    
    print("Swimming towards Besaid village. Pirahnas section.")
    while Complete == 0 :
        if FFX_Screen.PixelTest( 269, 191, (183, 183, 61) ) :
            #We're now on the hill.
            Complete = 1
        elif not FFX_Screen.Minimap1() and not FFX_Screen.BattleScreen() :
            #Skip dialog if it is occurring, for speed's sake
            FFXC.set_value('BtnB', 1)
            time.sleep(0.1)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.1)
        elif FFX_Screen.Minimap1() and not FFX_Screen.PixelTest( 269, 191, (183, 183, 61) )  :
            path += 1
            print("Swimming: ", path)
            if path == 100 :
                Complete = 1
            elif path >= recover and path < recover +5 :
                print("Angle to the finish line")
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(3)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
            elif path < straight:
                FFXC.set_value('AxisLy', 1)
                time.sleep(1)
                FFXC.set_value('AxisLy', 0)
            elif path >= straight and path < turn:
                print("Turning")
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.6)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.1)
                FFXC.set_value('AxisLy', 0)
            elif path >= turn :
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                
        elif FFX_Screen.BattleScreen() :
                print("Battle: Tidus and Wakka attack.")
                FFX_Battle.FinishWithAttacksOnly()

def enteringVillage():
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(10)
    FFXC.set_value('AxisLy', 0)
    
    #Conversation with Luzzu and Gatta
    #FFX_Xbox.SkipDialog(18)
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    #Learning about the prayer
    FFX_Screen.awaitPixel(973,506,(187, 187, 187))
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    
    #Wait for Tidus to gain control
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.9)
    FFXC.set_value('AxisLx', 0)
    time.sleep(13)
    FFXC.set_value('AxisLy', 0)
    
    #Next, run towards the Braska statue
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl() #Finally receive our statue.
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.4)
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLx', 1)
        if pos[0] > 8:
            FFXC.set_value('AxisLy', -1)
        elif pos[0] < -5:
            FFXC.set_value('AxisLy', 1)
        else:
            FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
        
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    
    #Temple to Wakka's tent
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(7)
    FFXC.set_value('AxisLx', 1)
    time.sleep(4)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    #Approach Wakka
    FFX_Screen.awaitPixel(198,160, (64, 193, 64))
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.SkipDialog(2.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(3)
    
    #Sleeping
    FFX_memory.clickToControl()
    
    #Awake
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.3)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        if pos[0] > 18:
            FFXC.set_value('AxisLx', 1)
        elif pos[0] < -18:
            FFXC.set_value('AxisLx', -1)
        else:
            FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    
    
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    FFX_memory.awaitControl()
    
    #Start of conversation with Wakka and the priest.
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLx', -1)
        if pos[0] > 10:
            FFXC.set_value('AxisLy', -1)
        else:
            FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
        
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    print("Pathing is complete. Ready for trials")
