import math
import damage
import logging
import rng_track
from memory import main


def get_rng_damage(
                   base_damage: int,
                   rng_array,
                   rng_rolls: int,
                   user_luck: int,
                   target_luck: int,
                   equipment_bonus: int = 0,
                   can_crit: bool = True
                   ) -> (int, bool):

    damage_roll = rng_array[rng_rolls + 1] % 32

    if can_crit:
        crit = calculate_crit(rng_array=rng_array, rng_rolls=rng_rolls, user_luck=user_luck, target_luck=target_luck,
                              equipment_bonus=equipment_bonus)
    else:
        crit = 0

    return math.floor(base_damage * (240 + damage_roll) / 256) * (2 if crit else 1)


def calculate_crit(rng_array, rng_rolls, user_luck: int, target_luck: int, equipment_bonus: int = 0) -> bool:

    crit_roll = rng_array[rng_rolls + 2] % 101
    crit_chance = user_luck - target_luck + equipment_bonus
    return crit_roll < crit_chance


def get_seed() -> int:

    tidus_luck = 18
    auron_luck = 18
    enemy_luck = 1
    equipment_bonus = 6

    damage_rolls = [0] * 6

    rng_array_tidus = main.rng_array_from_index(index=20, array_len=7)
    rng_array_auron = main.rng_array_from_index(index=22, array_len=7)

    # Initialise Tidus and Auron rolls at 1 for ICV roll on sinscale encounter
    rng20_rolls = 1
    rng22_rolls = 1

    # Auron's attacks
    for i in range(3):
        base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF, user_stat=20)
        var_damage = get_rng_damage(base_damage=base_damage, rng_array=rng_array_auron, rng_rolls=rng22_rolls,
                                    user_luck=auron_luck, target_luck=enemy_luck, equipment_bonus=equipment_bonus)
        logging.debug(f"Auron Damage {i+1}: {var_damage}")
        damage_rolls[2 * i] = var_damage
        rng22_rolls += 2

    # Tidus' attacks
    for i in range(3):
        base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF, user_stat=15)
        var_damage = get_rng_damage(base_damage=base_damage, rng_array=rng_array_tidus, rng_rolls=rng20_rolls,
                                    user_luck=tidus_luck, target_luck=enemy_luck, equipment_bonus=equipment_bonus)
        logging.debug(f"Tidus Damage {i + 1}: {var_damage}")
        damage_rolls[2 * i + 1] = var_damage
        rng20_rolls += 2

    seed = rng_track.hits_to_seed(hits_array=damage_rolls)

    return seed
