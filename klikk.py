import area.dreamZan
import loadGame
import logs
import memory.main
import reset
import targetPathing
import vars
import xbox

gameVars = vars.varsHandle()
gameVars.set_start_vars()

memory.main.start()
# Plug in controller
FFXC = xbox.controllerHandle()

area.dreamZan.NewGame("Klikk testing")
loadGame.load_save_num(101)
memory.main.awaitControl()
while memory.main.userControl():
    targetPathing.set_movement([0, 0])
    if memory.main.getCoords()[0] > -40:
        xbox.tapB()
area.baaj.Klikk_fight()

reset.mid_run_reset(land_run=False, start_time=logs.time_stamp())
