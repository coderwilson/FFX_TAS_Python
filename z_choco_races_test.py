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

try:
    # This sets up console and file logging (should only be called once)
    log_init.initialize_logging()
except:
    pass

logger = logging.getLogger(__name__)

FFXC = xbox.controller_handle()
while not memory.main.start():
    pass

logger.warning("START SHOWCASE")
load_game.load_into_game(gamestate="Showcase", step_counter=199)  # Full run
#load_game.load_into_game(gamestate="Showcase", step_counter=18)  # Load in the middle

godhand = 0
baaj = 0

nemesis.arena_prep.return_to_airship()

area.chocobos.all_races()
area.chocobos.to_remiem()
area.chocobos.remiem_races()
area.chocobos.leave_temple()

area.chocobos.butterflies()
area.chocobos.upgrade_mirror()
area.chocobos.spirit_lance()

area.chocobos.besaid_destro(godhand=godhand, baaj=baaj)
area.chocobos.kilika_destro(godhand=godhand, baaj=baaj)
area.chocobos.djose_destro(godhand=godhand, baaj=baaj)
area.chocobos.ice_destro(godhand=godhand, baaj=baaj)
area.chocobos.sun_crest(godhand=godhand, baaj=baaj)

area.chocobos.rusty_sword()
area.chocobos.saturn_crest()
area.chocobos.masamune()

area.chocobos.cactuars()
area.chocobos.cactuars_finish()

baaj = area.chocobos.onion_knight()
area.chocobos.belgemine(godhand=godhand, baaj=baaj)
area.chocobos.venus_crest(godhand=godhand, baaj=baaj)
godhand = area.chocobos.godhand(baaj=baaj)
area.chocobos.sun_sigil(godhand=godhand, baaj=baaj)

area.chocobos.upgrade_celestials(godhand=godhand, baaj=baaj, Yuna=True, Wakka=False)

logger.warning("END SHOWCASE")
reset.reset_no_battles()
