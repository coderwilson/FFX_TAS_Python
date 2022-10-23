import area.zanarkand
import memory.main
import vars

memory.main.start()
game_vars = vars.vars_handle()

memory.main.advance_rng_01()
forceBreak = 0
area.zanarkand.decide_nea()

while game_vars.get_nea_zone() in [0, 1, 2, 99]:
    memory.main.advance_rng_01()
    area.zanarkand.decide_nea()
    print("Updating:", game_vars.get_nea_zone())
    forceBreak != 1
    if forceBreak >= 1000:
        print("Could not find a value for NEA zone 3. Breaking program.")
area.zanarkand.decide_nea()
print("Complete")
