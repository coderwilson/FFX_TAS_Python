# Libraries and Core Files
import area.baaj
import area.besaid
import area.boats
import area.djose
import area.dream_zan
import area.gagazet
import area.guadosalam
import area.home
import area.kilika
import area.luca
import area.mac_temple
import area.mac_woods
import area.miihen
import area.moonflow
import area.MRR
import area.rescue_yuna
import area.sin
import area.thunderPlains
import area.zanarkand
import loadGame
import memory.main
import reset
import targetPathing
import vars
import xbox

game_vars = vars.vars_handle()
game_vars.set_start_vars()

# Plug in controller
FFXC = xbox.controller_handle()
Gamestate = "Macalania"
step_counter = 1  # x9
while not memory.main.start():
    pass

if memory.main.get_map in [23, 348, 349]:
    pass
else:
    reset.reset_to_main_menu()


if Gamestate != "none":
    if not (Gamestate == "Luca" and step_counter == 3):
        area.dream_zan.new_game(Gamestate)

    if Gamestate == "Macalania" and step_counter == 1:  # 1 = south, 2 = north
        loadGame.load_save_num(9)
    if Gamestate == "Macalania" and step_counter == 2:  # 1 = south, 2 = north
        loadGame.load_save_num(7)

# Approach the position
prep_step = [[303, 34], [284, 104], [222, 160], [209, 170]]
for i in range(len(prep_step)):
    while not targetPathing.set_movement(prep_step[i]):
        if memory.main.diag_skip_possible():
            xbox.tap_b()
FFXC.set_neutral()
memory.main.wait_frames(30)
# Into position
while not targetPathing.set_movement([190, 180]):
    memory.main.wait_frames(2)
    FFXC.set_neutral()
    memory.main.wait_frames(6)

print("Position Ready")
FFXC.set_neutral()
memory.main.wait_frames(30)

# Angle
FFXC.set_movement(-1, -1)
memory.main.wait_frames(1)
FFXC.set_neutral()
print("Angle Ready")
memory.main.wait_frames(40)

# Engage
FFXC.set_movement(1, 1)
memory.main.wait_frames(2)
xbox.tap_b()
memory.main.wait_frames(5)
FFXC.set_neutral()
memory.main.wait_frames(60)
