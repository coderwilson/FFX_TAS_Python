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
    while not memory.main.nextDropRNG13(1):
        memory.main.advanceRNG13()
    print("Mark 1")
    while memory.main.nextChanceRNG12():
        memory.main.advanceRNG12()
    print("Mark 2")
    while memory.main.nextChanceRNG10():
        memory.main.advanceRNG10()
    print("------------------")
    print("Should now drop NE armor.")
print("------------------")
time.sleep(3)
