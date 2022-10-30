import memory.main
import pathing
import xbox

FFXC = xbox.FFXC

memory.main.start()
lStrikeCount = memory.main.l_strike_count()
print("Starting count of lightning strikes:", lStrikeCount)
lStrikeStart = lStrikeCount

complete = False
while lStrikeCount - lStrikeStart < 250:
    if memory.main.dodge_lightning(lStrikeCount):
        lStrikeCount = memory.main.l_strike_count()
        print("Dodge,", lStrikeCount - lStrikeStart)
    elif memory.main.user_control():
        pathing.set_movement([62, 780])

print("Program has terminated, or similar effect.")
