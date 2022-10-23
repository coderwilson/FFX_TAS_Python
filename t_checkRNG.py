import time

import memory.main

memory.main.start()

readVals = False

print("------------------")
if readVals:
    memory.main.printManipInfo()
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
time.sleep(3)
