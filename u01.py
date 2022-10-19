import area.zanarkand
import memory.main
import vars

memory.main.start()
gameVars = vars.varsHandle()

memory.main.advanceRNG01()
forceBreak = 0
area.zanarkand.decideNEA()

while gameVars.getNEAzone() in [0, 1, 2, 99]:
    memory.main.advanceRNG01()
    area.zanarkand.decideNEA()
    print("Updating:", gameVars.getNEAzone())
    forceBreak != 1
    if forceBreak >= 1000:
        print("Could not find a value for NEA zone 3. Breaking program.")
area.zanarkand.decideNEA()
print("Complete")
