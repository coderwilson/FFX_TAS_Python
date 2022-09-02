import FFX_Xbox
import FFX_memory
import FFX_targetPathing

FFXC = FFX_Xbox.FFXC

FFX_memory.start()
lStrikeCount = FFX_memory.lStrikeCount()
print("Starting count of lightning strikes:", lStrikeCount)
lStrikeStart = lStrikeCount

complete = False
while lStrikeCount - lStrikeStart < 250:
    if FFX_memory.dodgeLightning(lStrikeCount):
        lStrikeCount = FFX_memory.lStrikeCount()
        print("Dodge,", lStrikeCount - lStrikeStart)
    elif FFX_memory.userControl():
        FFX_targetPathing.setMovement([62, 780])

print("Program has terminated, or similar effect.")
