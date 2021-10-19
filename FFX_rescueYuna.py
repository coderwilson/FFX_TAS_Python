import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_menu
import FFX_targetPathing

FFXC = FFX_Xbox.FFXC

def preEvrae():
    FFX_Screen.clickToMap3()
    print("Starting first Airship section")
    
    #FFXC.set_value('AxisLy', -1)
    #time.sleep(0.5)
    #FFXC.set_value('AxisLy', 0)
    #FFXC.set_value('AxisLx', -1)
    #time.sleep(1.5)
    #FFXC.set_value('AxisLx', 0)
    #FFXC.set_value('AxisLy', -1)
    #time.sleep(0.2)
    #FFXC.set_value('AxisLy', 0)
    #FFX_Xbox.touchSaveSphere()
    
    #FFXC.set_value('AxisLx', 1)
    #time.sleep(0.9)
    #FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    print("Exit cockpit")
    time.sleep(5.5)
    
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    print("Back in cockpit. Auron/Cid arguing")
    
    FFX_Screen.clickToMap3()
    print("Let's go talk to Brother")
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(1)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToMap3()
    
    print("Heading to the deck via Guado attack conversation")
    #FFX_menu.weddingPrep()
    FFX_memory.fullPartyFormat('evrae')
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.1)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.touchSaveSphere()
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Xbox.airShipPath(6)
    # 1 - Path to deck, purchase weap from Rin
    # 6 - Path to deck, no item purchasing
    
def Evrae():
    FFX_Battle.Evrae()
    
def guards():
    #FFX_memory.fullPartyFormat('rikku')
    #FFX_menu.bevelleGuards()
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFX_Battle.guards(1)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFX_Battle.guards(2)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFX_Battle.guards(3)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFX_Battle.guards(4)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFX_Battle.guards(5)
    
    FFX_Xbox.SkipDialog(126)
    FFX_Xbox.skipStoredScene(10)
    
    FFX_Screen.clickToPixel(1591,759,(165, 88, 88))
    print("Yuna can fly")
    
    time.sleep(15.7)
    FFX_Xbox.skipScene()
    FFX_memory.clickToControl()
    
    FFXC.set_value('AxisLx', -1)
    FFX_Xbox.SkipDialog(3)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    time.sleep(4)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3.5)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.touchSaveSphere()
    time.sleep(0.5)

def trials():
    print("Starting Bevelle trials section.")
    
    checkpoint = 0
    while FFX_memory.getMap() != 226:
        if FFX_memory.userControl():
            #Map changes
            if checkpoint < 2 and FFX_memory.getMap() == 306:
                checkpoint = 2
            
            #Spheres, Pedestols, and gliding across glowing paths.
            elif checkpoint == 3: #Pedestol that starts it all.
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                FFX_memory.awaitEvent() #Pedestol - START!!!
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                time.sleep(21.5)
                FFX_Xbox.menuB() #Start moving
                
                #Timing for the first alcove
                time.sleep(9.8)
                FFXC.set_value('BtnB', 1)
                time.sleep(3)
                FFXC.set_value('BtnB', 1)
                
                #Now did we go into the correct alcove?
                FFX_memory.awaitControl()
                if FFX_memory.getCoords()[0] < -10:
                    print("Correct alcove. Moving on with swiftness.")
                    checkpoint += 2
                else:
                    print("Incorrect alcove. Recovering.")
                    checkpoint += 1
            elif checkpoint == 4: #Recovery
                FFXC.set_value('AxisLx', 1)
                time.sleep(1.5)
                FFXC.set_value('AxisLx', -1)
                time.sleep(1.5)
                FFXC.set_value('AxisLx', 0)
                time.sleep(10.5)
                
                print("Mark1")
                FFX_Xbox.SkipDialog(2)
                time.sleep(6.45)
                print("Mark2")
                FFX_Xbox.menuB()
                time.sleep(12)
                FFXC.set_value('AxisLy', 1)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                FFX_Xbox.menuB()
                time.sleep(0.5)
                
            elif checkpoint == 7: #First Bevelle sphere, and then more gliding.
                print("Bevelle sphere")
                FFX_memory.clickToEventTemple(7)
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(1.5)
                FFXC.set_value('AxisLy', 0)
                time.sleep(10)
                FFXC.set_value('BtnB', 1)
                time.sleep(15)
                FFXC.set_value('BtnB', 0)
                checkpoint += 1
            elif checkpoint == 10: #Insert Bevelle sphere. Activate lower areas.
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 13: #Down to the lower areas.
                FFXC.set_value('AxisLx', -1)
                FFXC.set_value('AxisLy', 0)
                time.sleep(2)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                
                time.sleep(10)
                FFXC.set_value('BtnB', 1)
                time.sleep(2)
                FFXC.set_value('BtnB', 0)
                time.sleep(7)
                FFXC.set_value('BtnB', 1) #Down to lower section.
                time.sleep(2)
                FFXC.set_value('BtnB', 0)
                
                time.sleep(11) #Lining up at the lower T
                
                while not FFX_Screen.PixelTestTol(360,50,(29, 146, 244),5):
                    if FFX_Screen.PixelTestTol(477,370,(131, 174, 255),5): #Coming from top side
                        print("Entered T from upper area")
                        while not FFX_Screen.PixelTestTol(449,802,(255, 255, 255),5):
                            time.sleep(0.05)
                        FFX_Xbox.menuB()
                        time.sleep(9)
                        FFXC.set_value('BtnB', 1) #Second alcove
                        time.sleep(2)
                        FFXC.set_value('BtnB', 0)
                    elif FFX_Screen.PixelTestTol(4,3,(167, 166, 246),5): #Looping around
                        print("Entered T from loop")
                        while not FFX_Screen.PixelTestTol(782,691,(255, 255, 255),5):
                            time.sleep(0.05)
                        FFX_Xbox.menuB()
                        time.sleep(9)
                        FFXC.set_value('BtnB', 1) #Second alcove
                        time.sleep(2)
                        FFXC.set_value('BtnB', 0)
                
                checkpoint += 1
            elif checkpoint == 16: #Take Glyph sphere from second alcove
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 18: #To third alcove
                FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', -1)
                time.sleep(2)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                time.sleep(10)
                FFXC.set_value('BtnB', 1) #Third alcove
                time.sleep(8)
                FFXC.set_value('BtnB', 0)
                FFX_memory.awaitControl()
                FFX_memory.clickToEventTemple(0) #Go ahead and insert Glyph sphere.
                checkpoint += 1
            elif checkpoint == 22: #Remove Bevelle sphere
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 24: #Insert Bevelle sphere
                FFX_memory.clickToEventTemple(5)
                checkpoint += 1
            elif checkpoint == 28: #Take Glyph sphere
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.07)
                FFX_memory.clickToEvent()
                time.sleep(0.035)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 32: #Insert Glyph sphere
                FFX_memory.clickToEventTemple(0)
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.07)
                checkpoint += 1
            elif checkpoint == 34: #Take Destro sphere
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 39: #Insert Destro sphere
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.07)
                FFX_memory.clickToEvent()
                time.sleep(0.035)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 41: #Take Bevelle sphere
                FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 44: #Insert Bevelle sphere, and back on the track.
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.07)
                FFX_Xbox.SkipDialog(1)
                FFX_memory.clickToControl3()
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', -1)
                time.sleep(2)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                
                time.sleep(16)
                while not FFX_Screen.PixelTestTol(360,50,(29, 146, 244),5):
                    if FFX_Screen.PixelTestTol(4,3,(167, 166, 246),5): #Looping around
                        print("Entered T from loop")
                        while not FFX_Screen.PixelTestTol(782,691,(255, 255, 255),5):
                            time.sleep(0.05)
                        FFX_Xbox.menuB()
                        time.sleep(9)
                        FFXC.set_value('BtnB', 1) #Second alcove
                        time.sleep(4)
                        FFXC.set_value('BtnB', 0)
                print("Arriving in the second alcove again.")
                checkpoint += 1
            elif checkpoint == 46: #Take Destro sphere
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 50: #Insert Destro sphere
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 52: #Back on track, to the exit
                FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', -1)
                time.sleep(2)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                time.sleep(19)
                while not FFX_Screen.PixelTestTol(381,673,(255, 184, 255),5):
                    if FFX_Screen.PixelTestTol(4,3,(167, 166, 246),5): #Looping around
                        print("Entered T from loop")
                        while not FFX_Screen.PixelTestTol(782,691,(255, 255, 255),5):
                            time.sleep(0.05)
                        FFX_Xbox.menuB()
                        time.sleep(5)
                        FFXC.set_value('BtnB', 1) #First alcove
                        time.sleep(7)
                        FFXC.set_value('BtnB', 0)
                FFX_memory.awaitControl()
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', -1)
                time.sleep(2)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                checkpoint += 1
            elif checkpoint == 58:
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            #elif checkpoint == 61: #Exit to storyline
            #    FFXC.set_value('AxisLx', 1)
            #    FFXC.set_value('AxisLy', 0)
            #    FFX_memory.awaitEvent()
            #    FFXC.set_value('AxisLx', 0)
            #    FFXC.set_value('AxisLy', 0)
                
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.bevelleTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)

    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(108)
    print("Mark")
    FFX_Screen.awaitPixel(371,250,(111, 125, 179))
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Screen.awaitSave()

def trials_old():
    print("Starting Bevelle trials section.")
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(3)
    FFXC.set_value('AxisLy', 1)
    time.sleep(4) #Pedestol to get us all started
    FFXC.set_value('AxisLy', 0)
    time.sleep(22.5)
    FFX_Xbox.menuB() #Start moving
    time.sleep(9.8) #Remember to turn this back on
    FFX_Xbox.SkipDialog(3.5) #Remember to turn this back on
    #time.sleep(15) #Used only for testing
    FFX_Xbox.menuB() #Into the first alcove
    time.sleep(6)
    
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    bevRec = 0
    if not FFX_Screen.PixelTest(713,830,(234, 140, 0)):
        while not FFX_Screen.PixelTest(713,830,(234, 140, 0)): #Found a Bevelle sphere
            bevRec += 1
            print("Wrong alcove. Attempting recovery.")
            FFXC.set_value('AxisLx', 1)
            time.sleep(1.5)
            FFXC.set_value('AxisLx', -1)
            time.sleep(1.5)
            FFXC.set_value('AxisLx', 0)
            time.sleep(10.5)
            
            print("Mark1")
            FFX_Xbox.SkipDialog(2)
            time.sleep(6.45)
            print("Mark2")
            FFX_Xbox.menuB()
            time.sleep(12)
            FFXC.set_value('AxisLy', 1)
            time.sleep(2)
            FFXC.set_value('AxisLy', 0)
            FFX_Xbox.menuB()
            time.sleep(0.5)
            
    print("OK we hit the right alcove. Good to go.")
    
    FFX_Xbox.menuB()
    time.sleep(4)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    
    time.sleep(11.5)
    FFX_Xbox.SkipDialog(2)
    time.sleep(5)
    FFX_Xbox.SkipDialog(2)
    time.sleep(8)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToPixel(909,830,(234, 140, 0)) #Placed Bevelle sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(6)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    
    time.sleep(10)
    FFXC.set_value('BtnB', 1)
    time.sleep(2)
    FFXC.set_value('BtnB', 0)
    time.sleep(7)
    FFXC.set_value('BtnB', 1) #Down to lower section.
    time.sleep(2)
    FFXC.set_value('BtnB', 0)
    
    time.sleep(11)
    while not FFX_Screen.PixelTestTol(360,50,(29, 146, 244),5):
        if FFX_Screen.PixelTestTol(477,370,(131, 174, 255),5): #Coming from top side
            print("Entered T from upper area")
            while not FFX_Screen.PixelTestTol(449,802,(255, 255, 255),5):
                time.sleep(0.05)
            FFX_Xbox.menuB()
            time.sleep(9)
            FFXC.set_value('BtnB', 1) #Second alcove
            time.sleep(2)
            FFXC.set_value('BtnB', 0)
        elif FFX_Screen.PixelTestTol(4,3,(167, 166, 246),5): #Looping around
            print("Entered T from loop")
            while not FFX_Screen.PixelTestTol(782,691,(255, 255, 255),5):
                time.sleep(0.05)
            FFX_Xbox.menuB()
            time.sleep(9)
            FFXC.set_value('BtnB', 1) #Second alcove
            time.sleep(2)
            FFXC.set_value('BtnB', 0)
    print("Successfully arrived at second alcove.")
    time.sleep(0.1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToPixel(805,829,(234, 143, 0)) #Removed glyph sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.2)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    time.sleep(10)
    FFXC.set_value('BtnB', 1) #Third alcove
    time.sleep(10)
    FFXC.set_value('BtnB', 0)
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.05)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.25)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.05)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToPixel(818,830,(234, 140, 0)) #Placed glyph sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(1)
    
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToPixel(912,830,(234, 140, 0)) #Removed Bevelle sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.clickToPixel(909,830,(234, 140, 0)) #Placed Bevelle sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(6.5)
    
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.4)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.05)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.25)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.05)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToPixel(805,829,(234, 143, 0)) #Removed glyph sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(1)
    
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToPixel(818,830,(234, 140, 0)) #Placed glyph sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(4.5)
    
    
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToPixel(948,829,(234, 143, 0)) #Removed destro sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    
    FFXC.set_value('AxisLy', -1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.05)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.25)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.05)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToPixel(942,829,(234, 143, 0)) #Inserted destro sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.clickToPixel(912,830,(234, 140, 0)) #Removed Bevelle sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(2)
    
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToPixel(909,830,(234, 140, 0)) #Placed Bevelle sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    
    FFXC.set_value('AxisLy', -1) #Back onto the track
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(17)
    while not FFX_Screen.PixelTestTol(360,50,(29, 146, 244),5):
        if FFX_Screen.PixelTestTol(4,3,(167, 166, 246),5): #Looping around
            print("Entered T from loop")
            while not FFX_Screen.PixelTestTol(782,691,(255, 255, 255),5):
                time.sleep(0.05)
            FFX_Xbox.menuB()
            time.sleep(9)
            FFXC.set_value('BtnB', 1) #Second alcove
            time.sleep(4)
            FFXC.set_value('BtnB', 0)
    print("Arrived in the second alcove again.")
    
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.15)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.clickToPixel(948,829,(234, 143, 0)) #Removed destro sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToPixel(942,829,(234, 143, 0)) #Inserted destro sphere
    time.sleep(0.2)
    FFX_Xbox.menuB()
    FFX_memory.awaitControl()
    
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.2)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    time.sleep(19)
    while not FFX_Screen.PixelTestTol(381,673,(255, 184, 255),5):
        if FFX_Screen.PixelTestTol(4,3,(167, 166, 246),5): #Looping around
            print("Entered T from loop")
            while not FFX_Screen.PixelTestTol(782,691,(255, 255, 255),5):
                time.sleep(0.05)
            FFX_Xbox.menuB()
            time.sleep(5)
            FFXC.set_value('BtnB', 1) #First alcove
            time.sleep(10)
            FFXC.set_value('BtnB', 0)
    FFX_Screen.awaitPixel(381,673,(255, 184, 255))
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.2) #Push pedestol
    FFXC.set_value('AxisLy', 0)
    
    time.sleep(29)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.9)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', -1)
    FFX_Xbox.SkipDialog(3)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 0)
    time.sleep(4)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Xbox.SkipDialog(108)
    FFX_Screen.awaitPixel(371,250,(111, 125, 179))
    time.sleep(0.2)
    FFX_Xbox.menuA()
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Screen.awaitSave()

def ViaPurifico():
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.15)
    FFXC.set_value('AxisLx', 0)
    time.sleep(5)
    FFXC.set_value('AxisLy', 0)
    
    time.sleep(5.7) #Wait for the right direction
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToMap1()
    FFX_menu.viaPurifico()
    
    complete = 0
    while complete == 0:
        if FFX_memory.userControl():
            if FFX_memory.getSLVLYuna() < 14 and FFX_memory.getCoords()[1] > 1460:
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(2)
            else:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
        elif FFX_Screen.BattleScreen():
            complete = FFX_Battle.isaaru()
        else:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('BtnB',1) #Skipping dialog for Isaaru
            time.sleep(0.035)
            FFXC.set_value('BtnB',0)
            time.sleep(0.035)

def evraeAltana():
    FFX_memory.clickToControl()
    #FFXC.set_value('AxisLx', 1)
    #time.sleep(2)
    #FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    
    checkpoint = 0
    lastCP = 0
    while checkpoint < 100:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.getStoryProgress() > 2220:
            print("End of Evrae Altana section.")
            FFXC.set_value('AxisLx',0)
            FFXC.set_value('AxisLy',0)
            checkpoint = 100
        if FFX_memory.userControl():
            pos = FFX_memory.getCoords()
            cam = FFX_memory.getCamera()
            if checkpoint == 0:
                if pos[1] > -1550 and cam[0] > 0.5:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy',1)
                    FFXC.set_value('AxisLx',0)
            elif checkpoint == 10:
                if pos[1] > -1490:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy',0)
                    FFXC.set_value('AxisLx',1)
            elif checkpoint == 20:
                if pos[0] < 1050:
                    checkpoint = 30
                FFXC.set_value('AxisLy',1)
                if pos[1] < -1470:
                    FFXC.set_value('AxisLx',1)
                elif pos[1] > -1365:
                    FFXC.set_value('AxisLx',-1)
                else:
                    FFXC.set_value('AxisLx',0)
            elif checkpoint == 30:
                if pos[0] < 625:
                    checkpoint = 40
                FFXC.set_value('AxisLy',1)
                if pos[1] < -1410:
                    FFXC.set_value('AxisLx',1)
                elif pos[1] > -1377:
                    FFXC.set_value('AxisLx',-1)
                else:
                    FFXC.set_value('AxisLx',0)
            
            elif checkpoint == 40: #Diagonal with swinging camera
                if pos[1] > -540:
                    checkpoint = 50
                FFXC.set_value('AxisLy',1)
                if pos[1] < ((-9.83 * pos[0]) + 4840):
                    FFXC.set_value('AxisLx',1)
                else:
                    FFXC.set_value('AxisLx',0)
            elif checkpoint == 50:
                FFXC.set_value('AxisLy',1)
                if pos[1] > -310:
                    FFXC.set_value('AxisLx',-1)
                else:
                    FFXC.set_value('AxisLx',0)
        elif FFX_Screen.BattleScreen():
            FFX_Battle.evraeAltana()
        elif FFX_Screen.BattleComplete():
            FFX_Xbox.menuB()
        else:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            if checkpoint == 50:
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
    return 0
    
def seymourNatus(blitzWin):
    FFX_memory.clickToControl()
    
    if blitzWin == True:
        FFX_menu.seymourNatusBlitzWin()
    else:
        FFX_menu.seymourNatusBlitzLoss()
    
    complete = 0
    while complete == 0:
        if FFX_memory.userControl():
            FFX_targetPathing.setMovement(FFX_targetPathing.seymourNatus())
        
        
        
            #print("Movement")
            #FFXC.set_value('AxisLy', 1)
            #pos = FFX_memory.getCoords()
            #if pos[0] > 0:
            #    FFXC.set_value('AxisLx', 1)
            #else:
            #    FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            if FFX_Screen.BattleScreen():
                print("Battle Start")
                complete = FFX_Battle.seymourNatus()
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.2)
    FFX_memory.awaitEvent()
    FFXC.set_value('AxisLy', 0)
    
    time.sleep(0.2)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.awaitEvent()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    time.sleep(0.2)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    time.sleep(372.2)
    FFX_Xbox.skipScene() #Suteki da ne?
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    print("Ready for the Calm Lands section.")