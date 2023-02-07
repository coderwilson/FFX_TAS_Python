# Libraries and Core Files
import logging
import random
import sys

# This needs to be before the other imports in case they decide to log things when imported
import log_init

# This sets up console and file logging (should only be called once)
log_init.initialize_logging()

logger = logging.getLogger(__name__)

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
import area.mrr
import area.ne_armor
import area.rescue_yuna
import area.sin
import area.thunder_plains
import area.zanarkand
import area.chocobos
import battle.boss
import battle.main
import blitz
import config
import load_game
import logs
import memory.main
import nemesis.arena_battles
import nemesis.arena_prep
import nemesis.advanced_farm
import nemesis.changes
import pathing
import reset
import rng_track
import save_sphere
import screen
import vars
import xbox
import nemesis.arena_prep
from gamestate import game
from image_to_text import maybe_show_image

FFXC = xbox.controller_handle()
while not memory.main.start():
    pass

logger.warning("START CHOCO TEST")

load_game.load_into_game(gamestate="Nem_Farm", step_counter=1)
nemesis.arena_prep.return_to_airship()
nemesis.arena_prep.air_ship_destination(dest_num=12)
area.chocobos.all_races()
# Use the following to go straight into remiem races.
#while not pathing.set_movement([-637, -246]):
#    pass
area.chocobos.to_remiem()
area.chocobos.remiem_races()


logger.warning("END CHOCO TEST")
memory.main.wait_frames(60)