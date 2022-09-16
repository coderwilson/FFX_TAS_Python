import memory
import time
memory.start()

readVals = False

print("------------------")
if readVals:
    memory.printManipInfo()
else:
    print("Here goes nothing!")
    print("------------------")
    while not memory.nextDropRNG13(1):
        memory.advanceRNG13()
    print("Mark 1")
    while memory.nextChanceRNG12():
        memory.advanceRNG12()
    print("Mark 2")
    while memory.nextChanceRNG10():
        memory.advanceRNG10()
    print("------------------")
    print("Should now drop NE armor.")
print("------------------")
time.sleep(3)
