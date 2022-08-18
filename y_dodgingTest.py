import pyxinput
import time
import FFX_Xbox
import FFX_Battle
import FFX_Screen
import FFX_core
import FFX_memory
import FFX_targetPathing
#import FFX_Logs

FFXC = FFX_Xbox.FFXC

FFX_memory.start()
# FFX_Logs.nextStats(99)
lStrikeCount = FFX_memory.lStrikeCount()
print("Starting count of lightning strikes:", lStrikeCount)
lStrikeStart = lStrikeCount

complete = False
while lStrikeCount - lStrikeStart < 250:
    if FFX_memory.dodgeLightning(lStrikeCount):
        lStrikeCount = FFX_memory.lStrikeCount()
        print("Dodge, ", lStrikeCount - lStrikeStart)
    elif FFX_memory.userControl():
        FFX_targetPathing.setMovement([62, 780])

    # try:
    #    print("Test value:", (str(FFX_memory.memTestVal0())+","+str(FFX_memory.memTestVal1())+","+str(FFX_memory.memTestVal2())+","+str(FFX_memory.memTestVal3())))
    #    if FFX_Screen.dodgeLightning():
    #        FFX_Logs.writeStats(str(FFX_memory.memTestVal0())+","+str(FFX_memory.memTestVal1())+","+str(FFX_memory.memTestVal2())+","+str(FFX_memory.memTestVal3()))
    # except Exception as x:
    #    print("Could not read value:", x)
    #    complete = True

print("Program has terminated, or similar effect.")
