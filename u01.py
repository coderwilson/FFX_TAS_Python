import memory
import area.zanarkand as zanarkand
import vars
memory.start()
gameVars = vars.varsHandle()

memory.advanceRNG01()
forceBreak = 0
zanarkand.decideNEA()

while gameVars.getNEAzone() in [0, 1, 2, 99]:
    memory.advanceRNG01()
    zanarkand.decideNEA()
    print("Updating:", gameVars.getNEAzone())
    forceBreak != 1
    if forceBreak >= 1000:
        print("Could not find a value for NEA zone 3. Breaking program.")
zanarkand.decideNEA()
print("Complete")
