import area.dream_zan
import load_game
import logs
import memory.main
import pathing
import reset
import vars
import xbox

game_vars = vars.vars_handle()
game_vars.set_start_vars()

memory.main.start()
# Plug in controller
FFXC = xbox.controller_handle()

area.dream_zan.new_game("Klikk testing")
load_game.load_save_num(101)
memory.main.await_control()
while memory.main.user_control():
    pathing.set_movement([0, 0])
    if memory.main.get_coords()[0] > -40:
        xbox.tap_b()
area.baaj.Klikk_fight()

reset.mid_run_reset(land_run=False, start_time=logs.time_stamp())
