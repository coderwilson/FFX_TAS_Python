import logging
import logs
import damage
from memory import main
from manip_planning import rng


def plan_ammes() -> (int, bool, int):
    rng_array_tidus = main.rng_array_from_index(index=20, array_len=200)
    rng_array_auron = main.rng_array_from_index(index=22, array_len=200)

    ICV_Rolls = 2

    best_time_value = 0
    best_sinspawn_tidus_count = 0
    best_tidus_potion = 0
    best_spiral_cut_attack = 0

    for sinspawn_attacks_tidus in range(2, 5):

        for tidus_spiral_cut_attack in range(1, 4):

            for tidus_potion in range(2):

                sinspawn_attacks_auron = 6 - sinspawn_attacks_tidus

                rng20_rolls = sinspawn_attacks_tidus * 2 + ICV_Rolls + tidus_potion
                rng22_rolls = sinspawn_attacks_auron * 2 + ICV_Rolls

                demi_count = simulate_demi_count_ammes(rng_array_tidus=rng_array_tidus, rng_array_auron=rng_array_auron,
                                                       rng20_rolls=rng20_rolls, rng22_rolls=rng22_rolls,
                                                       tidus_spiral_cut_attack=tidus_spiral_cut_attack)

                time_value = 13 * demi_count + 5 * tidus_potion + 5 * abs(sinspawn_attacks_tidus - 3)

                logging.debug(f"Tidus Sinspawn Attacks: {sinspawn_attacks_tidus} / Potion: {tidus_potion} / Spiral Cut: {tidus_spiral_cut_attack} / Demi: {demi_count} / Time: {time_value}")

                if best_time_value == 0 or time_value < best_time_value:
                    best_time_value = time_value
                    best_sinspawn_tidus_count = sinspawn_attacks_tidus
                    best_tidus_potion = tidus_potion
                    best_spiral_cut_attack = tidus_spiral_cut_attack

    return best_sinspawn_tidus_count, best_tidus_potion, best_spiral_cut_attack


def simulate_demi_count_ammes(rng_array_tidus, rng_array_auron, rng20_rolls, rng22_rolls, tidus_spiral_cut_attack):

    hp_ammes = 2400
    crit = False

    tidus_luck = 18
    auron_luck = 18
    enemy_luck = 10
    equipment_bonus = 6

    demi_count = 1

    # Auron Overdrive - Burn 12 rolls then calculate Dragon Fang damage
    rng22_rolls += 12

    base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF, user_stat=20, ability_power=17,
                                               overdrive_timer=4.0, overdrive_timer_remaining=3.5)

    var_damage = rng.get_rng_damage(base_damage=base_damage, rng_array=rng_array_auron, rng_rolls=rng22_rolls,
                                    user_luck=auron_luck, target_luck=enemy_luck, equipment_bonus=0)

    hp_ammes -= var_damage

    rng22_rolls += 12

    # Tidus first Attack
    base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF, user_stat=15)

    var_damage = rng.get_rng_damage(base_damage=base_damage, rng_array=rng_array_tidus, rng_rolls=rng20_rolls,
                                    user_luck=tidus_luck, target_luck=enemy_luck, equipment_bonus=equipment_bonus)

    hp_ammes -= var_damage

    rng20_rolls += 2

    for i in range(5):

        demi_count += 1

        # Calculate Tidus damage depending on if he attacks or Spiral Cuts this turn
        if i + 1 == tidus_spiral_cut_attack:
            rng20_rolls += 2

            base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF, user_stat=15, ability_power=32,
                                                       overdrive_timer=3.0, overdrive_timer_remaining=2.4)

            var_damage = rng.get_rng_damage(base_damage=base_damage, rng_array=rng_array_tidus, rng_rolls=rng20_rolls,
                                            user_luck=tidus_luck, target_luck=enemy_luck, equipment_bonus=0)

            if crit:
                var_damage *= 2

            hp_ammes -= var_damage
            rng20_rolls += 2
        else:
            base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF, user_stat=15)

            var_damage = rng.get_rng_damage(base_damage=base_damage, rng_array=rng_array_tidus, rng_rolls=rng20_rolls,
                                            user_luck=tidus_luck, target_luck=enemy_luck, equipment_bonus=equipment_bonus)

            hp_ammes -= var_damage
            rng20_rolls += 2

        # Calculate Auron Attack damage
        base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF, user_stat=20)

        var_damage = rng.get_rng_damage(base_damage=base_damage, rng_array=rng_array_auron, rng_rolls=rng22_rolls,
                                        user_luck=auron_luck, target_luck=enemy_luck, equipment_bonus=equipment_bonus)

        hp_ammes -= var_damage
        rng22_rolls += 2

        if hp_ammes <= 0:
            return demi_count

    return demi_count
