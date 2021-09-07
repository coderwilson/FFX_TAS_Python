import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory

FFXC = FFX_Xbox.FFXC
 
def arrival():
    print("Starting Guadosalam section")
    FFX_memory.clickToControl()
    
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3.5)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.6)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0) #Enter the room where we meet Seymour
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', 1)
    FFX_memory.clickToEvent() #Talk to Wakka
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToControl3()
    
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToEvent() #Start conversation with Auron
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl3()
    
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToEvent() #Lulu conversation
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl3()
    
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB() # Yuna's turn
    FFX_memory.clickToControl3()
    
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(66) #Seymour/Trommell
    FFX_Xbox.skipStoredScene(10)
    

def afterSpeech():
    FFX_Screen.clickToMap1() #Skips through the long cutscene
    FFX_menu.guadoRikku()
    FFXC.set_value('AxisLy', -1)
    time.sleep(8) #Out of the room and to the party
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.25)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.7)
    FFXC.set_value('AxisLy', 1)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.awaitMap1() #Doorway to the Farplane
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB()
    time.sleep(2)
    FFX_Xbox.menuB() #Open the chest
    FFXC.set_value('AxisLy', 1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.awaitMap1() #Approach party
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToMap1() #Enter discussion farplane with Auron and Rikku
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToMap1() #Finish with Auron/Rikku, and head to farplane
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.awaitPixel(271,256,(64, 193, 64)) # Farplane, green square
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToPixel(271,256,(64, 193, 64)) # Farplane, green square
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)

def guadoSkip():
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.8)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3.5)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.8)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0) #Approach the party
    
    FFX_Screen.awaitPixel(888,802,(224, 224, 224))
    time.sleep(0.3)
    FFX_Xbox.menuB()
    time.sleep(2.1)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Syopa Cusatyo
    
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    pos = FFX_memory.getCoords()
    while pos[0] > -85:
        pos = FFX_memory.getCoords()
        
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(0.8) #Talk to the walking guado
    FFXC.set_value('AxisLy', 0)
    time.sleep(2.6)
    FFX_Xbox.menuB() #Close dialog
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    while pos[1] < 50:
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    while pos[0] < -44:
        pos = FFX_memory.getCoords()
    
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.48)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.1)
    FFXC.set_value('AxisLy', 0)
    pos = FFX_memory.getCoords()
    
    while pos[0] > 8:
        FFXC.set_value('Dpad', 4)
        time.sleep(0.06)
        FFXC.set_value('Dpad', 0)
        time.sleep(0.07)
        pos = FFX_memory.getCoords()
    while pos[1] < -8.5:
        FFXC.set_value('Dpad', 1)
        time.sleep(0.06)
        FFXC.set_value('Dpad', 0)
        time.sleep(0.07)
        pos = FFX_memory.getCoords()
    
    #FFXC.set_value('AxisLx', 0)
    #time.sleep(1.1)
    #FFX_memory.getCoords()
    #FFXC.set_value('AxisLy', 0)
    #FFXC.set_value('AxisLx', 0) #In the corner
    #time.sleep(0.5)
    #FFX_memory.getCoords()
    #FFXC.set_value('AxisLx', 1) #Face right
    #time.sleep(0.05)
    #FFX_memory.getCoords()
    #FFXC.set_value('AxisLx', 0) #Face right
    #time.sleep(0.4)
    #FFX_memory.getCoords()
    #FFXC.set_value('AxisLx', 1)
    #time.sleep(0.43)
    #FFXC.set_value('AxisLx', 0)
    #FFXC.set_value('AxisLy', -1)
    #time.sleep(0.15)
    #FFX_memory.getCoords()
    #FFXC.set_value('AxisLy', 0) #In position
    time.sleep(0.15)
    #FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.04)
    #FFX_memory.getCoords()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0) #Face downward
    FFX_memory.getCoords()
    time.sleep(0.3)
    val = FFX_Screen.PixelValue(951,568)
    while FFX_Screen.PixelTestTol(951,568,val,10): #Pixel on the door behind us. If it changes, the guado is here.
        pos = FFX_memory.getCoords()
    print("MARK")
    time.sleep(0.26)
    FFXC.set_value('BtnB', 1)
    time.sleep(0.45)
    FFXC.set_value('BtnB', 0)
    time.sleep(0.4)
    
    while not FFX_Screen.PixelTest(995,768,(222, 222, 222)): #Dialog with the running guado
        FFXC.set_value('BtnB', 1)
        time.sleep(0.4)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.4)
    time.sleep(2.5)
    FFX_Xbox.menuB() #Guado potions good!
    FFX_memory.getCoords()
    
    #Run for the Thunder Plains!
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    FFX_memory.getCoords()
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.getCoords()
    time.sleep(2.8)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.getCoords()
    time.sleep(0.55)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    FFX_memory.getCoords()
    time.sleep(1.2)
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.getCoords()
    if FFX_Screen.PixelTest(533,770,(219, 219, 219)):
        print("Skip successful. Moving towards thunder plains.")
        FFX_Logs.writeStats("Guado skip:")
        FFX_Logs.writeStats("Yes")
        time.sleep(0.9)
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 1)
        time.sleep(2)
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', 1)
        time.sleep(2)
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 0)
    else:
        print("Skip failed. Recovering.")
        FFX_Logs.writeStats("Guado skip:")
        FFX_Logs.writeStats("No")
        FFXC.set_value('AxisLx', -1)
        FFXC.set_value('AxisLy', 1)
        time.sleep(1.5)
        FFXC.set_value('AxisLy', 1)
        FFXC.set_value('AxisLx', 0)
        time.sleep(2)
        FFXC.set_value('AxisLy', 1)
        FFXC.set_value('AxisLx', 1)
        time.sleep(0.6)
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', -1)
        time.sleep(2)
        FFXC.set_value('AxisLx', -1)
        time.sleep(1)
        FFXC.set_value('AxisLy', 1)
        time.sleep(2)
        FFXC.set_value('AxisLx', 0)
        time.sleep(1)
        FFXC.set_value('AxisLy', 0)
        FFX_Screen.clickToMap1() #Talk to Shelinda
        FFXC.set_value('AxisLy', 1)
        time.sleep(4)
        FFXC.set_value('AxisLy', 0)
        FFX_Screen.clickToMap1() #Talk to party
        FFXC.set_value('AxisLy', -1)
        time.sleep(3)
        FFXC.set_value('AxisLy', 1)
        time.sleep(2)
        FFXC.set_value('AxisLx', 1)
        time.sleep(2)
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 0)
        FFX_Screen.clickToMap1()