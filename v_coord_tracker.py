# currently unused file, should be removed if abandoned
import time

import memory.main
import reset

memory.main.start()

last_time = int(time.time())  # Record the starting time as an integer.
map = memory.main.get_map()

while map == memory.main.get_map():
    current_time = int(time.time())
    if current_time != last_time:
        coords = memory.main.get_actor_coords(actor_index=0)
        print(f"Coords: [{round(coords[0], 2)}, {round(coords[1],2)}] | Dialog: {memory.main.diag_progress_flag()}")
        last_time = current_time
print(f"Map change, ({memory.main.get_map()}) - ending program.")