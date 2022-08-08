import FFX_memory
import FFX_Zanarkand
FFX_memory.start()
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFX_memory.advanceRNG01()
forceBreak = 0
FFX_Zanarkand.decideNEA()

while gameVars.getNEAzone() in [0,1,2,99]:
    FFX_memory.advanceRNG01()
    FFX_Zanarkand.decideNEA()
    print("Updating:", gameVars.getNEAzone())
    forceBreak != 1
    if forceBreak >= 1000:
        print("Could not find a value for NEA zone 3. Breaking program.")
FFX_Zanarkand.decideNEA()
print("Complete")