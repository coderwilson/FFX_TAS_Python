# currently unused file, should be removed if abandoned
import memory.main
import pathing
import xbox

FFXC = xbox.FFXC

memory.main.start()
l_strike_count = memory.main.l_strike_count()
print("Starting count of lightning strikes:", l_strike_count)
l_strike_start = l_strike_count

complete = False
while l_strike_count - l_strike_start < 250:
    if memory.main.dodge_lightning(l_strike_count):
        l_strike_count = memory.main.l_strike_count()
        print("Dodge,", l_strike_count - l_strike_start)
    elif memory.main.user_control():
        pathing.set_movement([62, 780])

print("Program has terminated, or similar effect.")
