import logging
import math

import memory.main
import screen
from memory.main import rng_array_from_index
from players import Yojimbo

logger = logging.getLogger(__name__)


def resistance(z_level: int = 5):
    logger.warning(f"Enemy zanmato level == {z_level}")
    if z_level in [3, 4, 5]:
        return 0.4
    return 0.8


def compatibility():
    ret_val = memory.main.yojimbo_compatibility()
    logger.warning(f"Yojimbo Compatability {ret_val}")
    return ret_val


def first_turn_action_occurs() -> bool:
    upcoming_array = rng_array_from_index(index=17, array_len=10)

    first_action_rng = upcoming_array[1] & 255
    if (compatibility() & 0x7FFFFFFF) // 4 > first_action_rng:
        return True
    logger.warning("++ Yojimbo no action before first turn.")
    return False


def first_turn_compat_change() -> int:
    # Assumes we aren't using Yojimbo vs weak monsters (Zan level 0)
    if not first_turn_action_occurs():
        return 0
    motiv_rng = rng_array_from_index(index=17, array_len=2)[2] & 63
    motiv = ((compatibility() & 0x7FFFFFFF) // 4) + motiv_rng

    if motiv < 32:
        logger.warning("++ Yojimbo first turn, expect Daigoro")
        return -1
    elif motiv < 48:
        logger.warning("++ Yojimbo first turn, expect Kozuka")
        return 0
    elif motiv < 63:
        logger.warning("++ Yojimbo first turn, expect Wakizashi (single)")
        return 1
    else:
        logger.warning("++ Yojimbo first turn, expect Wakizashi (multi)")
        return 3
    # Note that Zanmatou will never occur on the first turn for end-game bosses.
    # Any time we see it as a first-turn actio is on zan level 0.


def zanmato_gil_needed(zan_level: int = 5) -> int:
    logger.debug(rng_array_from_index(index=17, array_len=4))
    # This function assumes the following option was chosen during recruiting:
    # "To defeat the most powerful of enemies"
    # Any other option will affect the Zanmato chances.
    # https://grayfox96.github.io/FFX-Info/rng/yojimbo-hd

    compat_val = compatibility()
    motiv_rng = rng_value()

    # Now formulas
    gil_amount = 1
    gil_motivation = math.floor(math.log2(gil_amount / 4)) * 4 if gil_amount >= 4 else 0

    # This formula increses gil until we find a success case.
    while gil_amount < 500000:
        base_motiv = (compat_val // 10) + gil_motivation
        # motiv_rng set earlier, does not change until an action is taken.
        motivation = (base_motiv * resistance(z_level=zan_level)) + motiv_rng + 20  # Assume full overdrive

        if motivation >= 80:
            logger.warning(f"Gil amount needed: {gil_amount} | final_motiv: {round(motivation,1)}")
            return gil_amount
        else:
            logger.manip(f"Gil: {gil_amount} | Gil_motiv: {gil_motivation} | final_motiv: {round(motivation,1)}")

        gil_amount *= 2
        gil_motivation = math.floor(math.log2(gil_amount / 4)) * 4 if gil_amount >= 4 else 0
    
    # Unable to find an acceptable value.
    return 999999999
        
        #logger.debug(f"RNG: {motiv_rng}, Gil: {gil_amount}, motivation: {motivation}")

    # This formula not working
    # logger.debug(f"-- Motivation RNG: {motiv_rng}")
    # Assume +20 motivation for having overdrive ready, need motivation 80 total.
    # base_motiv  = (60 - motiv_rng) / resistance()
    # logger.debug(f"-- Base motivation: {base_motiv}")
    # gil_motiv = base_motiv - (compat_val // 10)
    # logger.debug(f"-- Gil motivation: {gil_motiv}")

    # gil_amount = math.floor(pow(2, gil_motiv/4)) * 4

    logger.debug(f"-- Need amount: {gil_amount}")

    return gil_amount


def rng_value():
    if memory.main.battle_active() and screen.turn_aeon():
        logger.info("In-battle RNG used")
        return rng_array_from_index(index=17, array_len=3)[1] & 0x7FFFFFFF & 63
    elif first_turn_action_occurs():
        logger.info("Pre-battle RNG with first turn action")
        return rng_array_from_index(index=17, array_len=3)[3] & 0x7FFFFFFF & 63
    else:
        logger.info("Pre-battle RNG with NO first turn action")
        return rng_array_from_index(index=17, array_len=3)[2] & 0x7FFFFFFF & 63
