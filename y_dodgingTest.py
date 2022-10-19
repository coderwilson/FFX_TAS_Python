import memory.main
import targetPathing
import xbox

FFXC = xbox.FFXC

memory.main.start()
lStrikeCount = memory.main.lStrikeCount()
print("Starting count of lightning strikes:", lStrikeCount)
lStrikeStart = lStrikeCount

complete = False
while lStrikeCount - lStrikeStart < 250:
    if memory.main.dodgeLightning(lStrikeCount):
        lStrikeCount = memory.main.lStrikeCount()
        print("Dodge,", lStrikeCount - lStrikeStart)
    elif memory.main.userControl():
        targetPathing.setMovement([62, 780])

print("Program has terminated, or similar effect.")
