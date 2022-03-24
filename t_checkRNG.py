import FFX_memory
import time
FFX_memory.start()

print("------------------")
print("------------------")
print("------------------")
print("------------------")
print("Here goes nothing!")
print("------------------")
while not FFX_memory.nextDropRNG13(1):
    FFX_memory.advanceRNG13()
print("Mark 1")
while FFX_memory.nextChanceRNG12():
    FFX_memory.advanceRNG12()
print("Mark 2")
while FFX_memory.nextChanceRNG10():
    FFX_memory.advanceRNG10()
    
print("------------------")
print("------------------")
print("Should now drop NE armor.")
print("------------------")
time.sleep(3)