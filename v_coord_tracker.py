import time

import memory.main
from memory.main import get_coords,get_actor_coords,get_map,diag_progress_flag,get_story_progress, get_encounter_id

memory.main.start()

last_time = int(time.time())  # Record the starting time as an integer.
map = get_map()
print("=================================")
memory.main.check_near_actors_print()
print("=================================")

while map == get_map():
    coords = memory.main.get_actor_coords(0)
    angle = memory.main.get_actor_angle(0)
    cam = memory.main.get_camera()
    
    current_time = int(time.time())
    if current_time != last_time:
        coords = get_actor_coords(actor_index=0)
        #coords = get_coords()
        print(f"Coords: [{round(coords[0], 2)}, {round(coords[1],2)}, {round(coords[2],2)}] | " + \
            f" | Angle: {round(angle,2)} | Dialog: {diag_progress_flag()}" + \
            f" | Story: {get_story_progress()} | Map: {get_map()}")
        #print(f"Battle Number: {get_encounter_id()} | Battle: {memory.main.battle_active()}")
        #print(f"Grid Cursor coords: {memory.main.s_grid_cursor_coords()}")
        #memory.main.check_near_actors_print()
        #print(memory.main.get_enemy_current_hp())
        #print(memory.main.get_camera())
        last_time = current_time
print(f"Map change, ({get_map()}) - ending program.")