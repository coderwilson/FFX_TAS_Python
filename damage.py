import math
from enum import IntEnum


class Formula(IntEnum):
    STR_VS_DEF = 1
    STR_IGNORE_DEF = 2
    MAG_VS_MDF = 3
    MAG_IGNORE_MDF = 4


def calculate_base_damage(
                          formula: int,
                          user_stat: int,
                          target_stat: int = 1,
                          user_cheer_focus: int = 0,
                          target_cheer_focus: int = 0,
                          ability_power: int = 16,
                          overdrive_timer: float = 0.0,
                          overdrive_timer_remaining: float = 0.0
                          ):

    defense_mod = 730 - math.floor((target_stat * 51 - math.floor(pow(target_stat, 2) / 11)) / 10)
    stat_base = 0
    base_damage = 0

    match formula:
        case Formula.STR_VS_DEF | Formula.STR_IGNORE_DEF:
            stat_base = math.floor(pow(user_stat + user_cheer_focus, 3) / 32) + 30
            base_damage = math.floor(stat_base * defense_mod / 730)
            base_damage = math.floor(base_damage * (15 - target_cheer_focus) / 15)
            base_damage = math.floor(ability_power * base_damage / 16)

        case Formula.MAG_VS_MDF | Formula.MAG_IGNORE_MDF:
            stat_base = (math.floor(pow(user_stat + user_cheer_focus, 2) / 6) + ability_power)
            base_damage = math.floor(ability_power * stat_base / 4)
            base_damage = math.floor(base_damage * defense_mod / 730)
            base_damage = math.floor(base_damage * (15 - target_cheer_focus) / 15)

    if overdrive_timer > 0:
        base_damage = math.floor(base_damage * (1 + 0.5 * overdrive_timer_remaining / overdrive_timer))

    return base_damage

