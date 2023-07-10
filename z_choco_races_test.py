# Libraries and Core Files
import logging

# This needs to be before the other imports in case they decide to log things when imported
import log_init

# This sets up console and file logging (should only be called once)
log_init.initialize_logging()

logger = logging.getLogger(__name__)

import area.baaj
import area.besaid
import area.boats
import area.chocobos
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
import area.mrr
import area.ne_armor
import area.rescue_yuna
import area.sin
import area.thunder_plains
import area.zanarkand
import load_game
import memory.main
import nemesis.advanced_farm
import nemesis.arena_battles
import nemesis.arena_prep
import nemesis.changes
import xbox
import reset

FFXC = xbox.controller_handle()
while not memory.main.start():
    pass

logger.warning("START CHOCO TEST")

load_game.load_into_game(gamestate="Nem_Farm", step_counter=1)
nemesis.arena_prep.return_to_airship()
nemesis.arena_prep.air_ship_destination(dest_num=12)
area.chocobos.all_races()
# Use the following to go straight into remiem races.
# while not pathing.set_movement([-637, -246]):
#    pass
area.chocobos.to_remiem()
area.chocobos.remiem_races()


logger.warning("END CHOCO TEST")
memory.main.wait_frames(60)
reset.reset_no_battles()
