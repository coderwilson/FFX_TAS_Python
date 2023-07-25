# currently unused file, should be removed if abandoned
import time
import memory.main
import rng_track

memory.main.start()

read_vals = False

"""
print("------------------")
if read_vals:
    memory.main.print_manip_info()
else:
    print("Here goes nothing!")
    print("------------------")
    while not memory.main.next_drop_rng_13(1):
        memory.main.advance_rng_13()
    print("Mark 1")
    while memory.main.next_chance_rng_12():
        memory.main.advance_rng_12()
    print("Mark 2")
    while memory.main.next_chance_rng_10():
        memory.main.advance_rng_10()
    print("------------------")
    print("Should now drop NE armor.")
print("------------------")
"""

to_drop = rng_track.item_to_be_dropped(enemy="yunalesca")[0]
while to_drop.equipment_type() != 0:
    print("No weapon, advancing.")
    memory.main.advance_rng_index(index=12)
    to_drop = rng_track.item_to_be_dropped(enemy="yunalesca")[0]
print("Advance complete.")
print(f"Owner: {to_drop.owner()}")
print(f"Slots: {to_drop.slot_count()}")

time.sleep(3)
