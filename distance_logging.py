
from gamestate import game

import memory
import vars
import threading
import logging
import json
import time

logger = logging.getLogger(__name__)


game_vars = vars.vars_handle()

def perform_distance_logging():
    distances = {}
    
    def _update(distance_travelled, location, zone):
        if location in distances:
            cur_loc = distances[location]
        else:
            cur_loc = {}
        if zone not in cur_loc:
            cur_loc[zone] = 0
        cur_loc[zone] += distance_travelled
        distances[location] = cur_loc
        logger.manip(f"Updated {location} - {zone} to {cur_loc[zone]}")
    
    def _monitor():
        distance_travelled = 0
        location = -1
        zone = -1
        previously_added = -1
        last_updated_map_time = time.time()
        while not (game.state == "Sin" and game.step == 4):
            new_travelled = memory.main.total_distance_travelled()
            if (not new_travelled) or (memory.main.get_map() != location) or (memory.main.get_zone() != zone):
                if not distance_travelled or (distance_travelled == previously_added):
                    pass
                else:
                    logger.manip(f"Adding {distance_travelled}")
                    _update(distance_travelled, location, zone)
                    previously_added = distance_travelled
            distance_travelled = new_travelled
            # The map updates faster than the steps reset to 0 on screen transition, so we need a bit of a delay.
            if (time.time() - last_updated_map_time >= 1):
                location = memory.main.get_map()
                last_updated_map_time = time.time()
            zone = memory.main.get_zone()
        logger.manip("Done logging distances.")
        # write_everything
        with open("./json_ai_files/distance_logging.json", "w") as fp:
            json.dump(distances, fp)
        return
        
    monitoring = threading.Thread(target=_monitor, daemon=True)
    monitoring.start()
    return monitoring