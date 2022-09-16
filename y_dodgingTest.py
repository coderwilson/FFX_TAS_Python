import xbox
import memory
import targetPathing

FFXC = xbox.FFXC

memory.start()
lStrikeCount = memory.lStrikeCount()
print("Starting count of lightning strikes:", lStrikeCount)
lStrikeStart = lStrikeCount

complete = False
while lStrikeCount - lStrikeStart < 250:
    if memory.dodgeLightning(lStrikeCount):
        lStrikeCount = memory.lStrikeCount()
        print("Dodge,", lStrikeCount - lStrikeStart)
    elif memory.userControl():
        targetPathing.setMovement([62, 780])

print("Program has terminated, or similar effect.")
