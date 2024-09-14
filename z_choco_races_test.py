# Libraries and Core Files
import logging
import log_init

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

# This sets up console and file logging (should only be called once)
log_init.initialize_logging()

logger = logging.getLogger(__name__)

FFXC = xbox.controller_handle()
while not memory.main.start():
    pass

logger.warning("START CHOCO TEST")
load_game.load_into_game(gamestate="Showcase", step_counter=199)

nemesis.arena_prep.return_to_airship()
godhand = 0
baaj = 0

area.chocobos.sun_crest(godhand=godhand, baaj=baaj)

area.chocobos.all_races()
area.chocobos.to_remiem()
area.chocobos.remiem_races()
area.chocobos.leave_temple()

area.chocobos.butterflies()
area.chocobos.upgrade_mirror()
area.chocobos.spirit_lance()

area.chocobos.rusty_sword()
area.chocobos.saturn_crest()
area.chocobos.masamune()

area.chocobos.cactuars()
area.chocobos.cactuars_finish()

baaj = area.chocobos.onion_knight()
area.chocobos.venus_crest(godhand=godhand, baaj=baaj)
godhand = area.chocobos.godhand(baaj=baaj)
area.chocobos.sun_sigil(godhand=godhand, baaj=baaj)

area.chocobos.upgrade_celestials(godhand=godhand, baaj=baaj, Yuna=False, Wakka=False)




# We aren't doing Yuna until we change the pre-dark-aeon logic in temples.
#area.chocobos.moon_crest()
#area.chocobos.belgemine()


logger.warning("END CHOCO TEST")
reset.reset_no_battles()
