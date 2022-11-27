import logging
import math

import memory.main
import screen
from memory.main import rng_array_from_index

logger = logging.getLogger(__name__)


def resistance(z_level: int = 5):
    if z_level in [3, 4, 5]:
        return 0.4
    return 0.8


def compatability():
    return memory.main.yojimobo_compatability()


def first_turn_action_occurs() -> bool:
    upcoming_array = rng_array_from_index(index=17, array_len=10)

    first_action_rng = upcoming_array[1] & 255
    if compatability() // 4 > first_action_rng:
        return True
    logger.debug("++ Yojimbo no action before first turn.")
    return False


def first_turn_compat_change() -> int:
    # Assumes we aren't using Yojimbo vs weak monsters (Zan level 0)
    if not first_turn_action_occurs():
        return 0
    motiv_rng = rng_array_from_index(index=17, array_len=2)[2] & 63
    motiv = (compatability() // 4) + motiv_rng

    if motiv < 32:
        logger.debug("++ Yojimbo first turn, expect Daigoro")
        return -1
    elif motiv < 48:
        logger.debug("++ Yojimbo first turn, expect Kozuka")
        return 0
    elif motiv < 63:
        logger.debug("++ Yojimbo first turn, expect Wakizashi (single)")
        return 1
    else:
        logger.debug("++ Yojimbo first turn, expect Wakizashi (multi)")
        return 3


def zan_amount(zan_level: int = 5) -> int:
    # This function assumes the following option was chosen during recruiting:
    # "To defeat the most powerful of enemies"
    # Any other option will affect the Zanmatou chances.
    # https://grayfox96.github.io/FFX-Info/rng/yojimbo-hd
    compat_val = compatability()
    if memory.main.battle_active() and screen.turn_aeon():
        logger.debug("-- A")
        rng_value = rng_array_from_index(index=17, array_len=1)[1] & 63
    else:
        if first_turn_action_occurs():
            logger.debug("-- B")
            rng_value = rng_array_from_index(index=17, array_len=3)[3] & 63
            compat_val += first_turn_compat_change()
        else:
            logger.debug("-- C")
            rng_value = rng_array_from_index(index=17, array_len=2)[2] & 63

    # Now formulas
    motiv_rng = rng_value & 63
    motivation = 0
    gil_amount = 1
    base_motiv = compat_val // 10
    (base_motiv * resistance()) + motiv_rng

    # This formula increses gil until we find a success case.
    while motivation < 80:
        gil_amount *= 2
        math.floor(math.log2(gil_amount / 4)) * 4
        logger.debug(f"RNG: {motiv_rng}, Gil: {gil_amount}, motivation: {motivation}")

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
