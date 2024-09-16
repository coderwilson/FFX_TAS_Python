import logging
import math
import damage
import manip_planning.rng
import rng_track
from memory import main
from manip_planning import rng
from players import CurrentPlayer, Rikku, Tidus

rng01_array_enemy_formation = []
rng04_array_enemy_targeting = []
rng10_array_drop_steal_chance = []
rng11_array_rare_steal_chance = []
rng20_array_tidus = []
rng26_array_rikku = []
rng28_array_enemy1 = []
rng29_array_enemy2 = []
rng44_array_enemy1_hit = []
rng45_array_enemy2_hit = []

sahagin_accuracy = 90
sahagin_luck = 1

klikk_strength = 14
klikk_accuracy = 90
klikk_luck = 15

tidus_hp_max = 520
tidus_evasion = 10
tidus_defense = 10
tidus_luck = 18

rikku_hp_max = 360
rikku_evasion = 5
rikku_defense = 8
rikku_luck = 18

equipment_bonus = 6

tidus_base_ctb = 14
rikku_base_ctb = 12
klikk_base_ctb = 20
tidus_icv_variance = 1
rikku_icv_variance = 2
klikk_icv_variance = 1

tidus_attack_time = 2
rikku_attack_time = 2
rikku_steal_time = 2
rikku_grenade_time = 3
land_potion_time = 4
underwater_potion_time = 5
underwater_steal_time = 3
klikk_attack_time = 2
single_piranha_attack_time = 2
multi_piranha_gnaw_time = 3

grenade_count = 0
rare_steal_chance = 32
piranha_item_drop_chance = 205

active_strats = {
    "sahagin_b_first": False,
    "geos_potion": 0,
    "geos_attacks": 0,
    "tidus_potion_klikk": 0,
    "tidus_potion_turn": 0,
    "rikku_potion_klikk": 0,
    "chain_encounter_strat": 0,
    "ruins_encounter_strat": 0
}

fastest_strats = {
    "sahagin_b_first": False,
    "geos_potion": 0,
    "geos_attacks": 0,
    "tidus_potion_klikk": 0,
    "tidus_potion_turn": 0,
    "rikku_potion_klikk": 0,
    "chain_encounter_strat": 0,
    "ruins_encounter_strat": 0
}


def plan_klikk_steals() -> (int, int, bool):

    global rng10_array_drop_steal_chance
    global rng11_array_rare_steal_chance

    rng10_array_drop_steal_chance = main.rng_array_from_index(index=10, array_len=200)
    rng11_array_rare_steal_chance = main.rng_array_from_index(index=11, array_len=200)

    rng_rolls = [0] * 68

    tanker_kills = 1
    sahagin_kills = 2

    best_klikk_steals = 0
    best_klikk_tanker_kill = 0
    best_time_value = 0

    for tanker_sinscale_kill in range(2):

        rng_rolls[10] = 3 * (tanker_sinscale_kill + tanker_kills + sahagin_kills)
        rng_rolls[11] = 0

        klikk_grenades, klikk_steals = simulate_klikk_steals(rng_rolls=rng_rolls)

        time_value = 2 * tanker_sinscale_kill + 1 * klikk_steals - 5 * klikk_grenades

        logging.debug(f"Tanker Kill: {tanker_sinscale_kill} / Steals: {klikk_steals} / Grenades: {klikk_grenades} / Time: {time_value}")

        if best_time_value == 0 or time_value < best_time_value:
            best_time_value = time_value
            best_klikk_steals = klikk_steals
            best_klikk_tanker_kill = tanker_sinscale_kill

    return best_klikk_steals, best_klikk_tanker_kill


def plan_manips(klikk_steals: int):

    global active_strats

    global rng01_array_enemy_formation
    global rng04_array_enemy_targeting
    global rng10_array_drop_steal_chance
    global rng11_array_rare_steal_chance
    global rng20_array_tidus
    global rng26_array_rikku
    global rng28_array_enemy1
    global rng44_array_enemy1_hit

    rng01_array_enemy_formation = main.rng_array_from_index(index=1, array_len=200)
    rng04_array_enemy_targeting = main.rng_array_from_index(index=4, array_len=200)
    rng10_array_drop_steal_chance = main.rng_array_from_index(index=10, array_len=200)
    rng11_array_rare_steal_chance = main.rng_array_from_index(index=11, array_len=200)
    rng20_array_tidus = main.rng_array_from_index(index=20, array_len=200)
    rng26_array_rikku = main.rng_array_from_index(index=26, array_len=200)
    rng28_array_enemy1 = main.rng_array_from_index(index=28, array_len=200)
    rng44_array_enemy1_hit = main.rng_array_from_index(index=44, array_len=200)

    logging.debug(rng04_array_enemy_targeting)

    rng_rolls = [0] * 68

    # rng01_rolls = 0
    # rng04_rolls = 0
    # rng20_rolls = 0
    # rng26_rolls = 0
    # rng28_rolls = 0
    # rng44_rolls = 0

    sahagins_ambush = 0
    sahagins_preempt = 0
    geos_ambush = 0
    geos_preempt = 0

    tidus_crits = 0
    klikk_hits = 0

    best_time_value = -99
    best_geos_potion = 0
    best_geos_attacks = 0
    best_klikk_hits = 0
    best_sahagin_b_first = 0

    # Calculate Sahagins Ambush / Pre-Empt
    ambush_preempt_roll = rng01_array_enemy_formation[rng_rolls[1] + 1] % 256
    rng_rolls[1] += 1

    if ambush_preempt_roll < 32:

        sahagins_preempt = 1
        logging.debug("Sahagins is an pre-empt")

    elif ambush_preempt_roll >= 223:

        sahagins_ambush = 1
        logging.debug("Sahagins is an ambush")
        hit_chance = sahagin_accuracy - tidus_evasion + sahagin_luck - tidus_luck

        if rng44_array_enemy1_hit[rng_rolls[44] + 1] < hit_chance:

            rng_rolls[28] += 1  # If hit roll enemy 1 damage rng (Sahagin can't crit so no crit roll)
            logging.debug("Sahagins A hits")

        else:

            logging.debug("Sahagins A misses")

        rng_rolls[44] += 1  # Enemy 1 Hit Roll
    else:
        # roll tidus ICV
        rng_rolls[20] += 1
        rng_rolls[26] += 1
        rng_rolls[28] += 5  # 4 extra rolls for duplicate monsters

    # Calculate Geos Ambush / Pre-Empt
    ambush_preempt_roll = rng01_array_enemy_formation[rng_rolls[1] + 1] % 256
    rng_rolls[1] += 1

    if ambush_preempt_roll < 32:
        geos_preempt = 1
        logging.debug("Geos is a pre-empt")
    elif ambush_preempt_roll >= 223:
        geos_ambush = 1
        logging.debug("Geos is an ambush")
    else:
        # roll ICVs
        rng_rolls[20] += 1
        rng_rolls[26] += 1
        rng_rolls[28] += 1

    rng_rolls[10] += 6  # 2x Kills on Sahagins
    rng_rolls[20] += 4  # 2x Attack on Sahagins
    rng_rolls[28] += 2  # 2x Geos Attacks (Geos can't crit)

    for target_sahagin_b_first in range(2 - sahagins_preempt):

        rng44_rolls = rng_rolls[44] + target_sahagin_b_first

        klikk_hits = simulate_klikk_hits(rng_array_enemy1_hit=rng44_array_enemy1_hit, rng44_rolls=rng44_rolls)

        logging.debug(f"Sahagin B First: {target_sahagin_b_first} / Klikk Hits: {klikk_hits}")

        if best_klikk_hits == 0 or klikk_hits < best_klikk_hits:
            best_klikk_hits = klikk_hits
            best_sahagin_b_first = target_sahagin_b_first

    rng_rolls[44] = best_sahagin_b_first

    rng_memory = []

    active_strats["sahagin_b_first"] = True

    for i in range(68):
        rng_memory.append(rng_rolls[i])

    for tidus_potion_geos in range(2):

        for tidus_attacks_geos in range(4-geos_ambush-tidus_potion_geos):

            for i in range(68):
                rng_rolls[i] = rng_memory[i]

            active_strats["geos_potion"] = tidus_potion_geos
            active_strats["geos_attacks"] = tidus_attacks_geos

            rng_rolls[20] = rng_rolls[20] + tidus_potion_geos + 2 * tidus_attacks_geos

            # logging.debug(f"==============Potion on Geos: {tidus_potion_geos} / Attacks on Geos: {tidus_attacks_geos}==========================")

            klikk_tros_time_value, tidus_potion, tidus_potion_turn, rikku_potion, chain_strat, ruins_strat = simulate_klikk_to_tros(rng_rolls=rng_rolls, klikk_steals=klikk_steals)

            time_value = klikk_tros_time_value + underwater_potion_time * tidus_potion_geos + 2 * tidus_attacks_geos

            if best_time_value == -99 or time_value < best_time_value:
                best_time_value = time_value
                fastest_strats["geos_potion"] = tidus_potion_geos
                fastest_strats["geos_attacks"] = tidus_attacks_geos
                fastest_strats["tidus_potion_klikk"] = tidus_potion
                fastest_strats["tidus_potion_turn"] = tidus_potion_turn
                fastest_strats["rikku_potion_klikk"] = rikku_potion
                fastest_strats["chain_encounter_strat"] = chain_strat
                fastest_strats["ruins_encounter_strat"] = ruins_strat

    log_string = f"Sahagin B First: {best_sahagin_b_first}"
    log_string += f" / Potion on Geos: {fastest_strats['geos_potion']}"
    log_string += f" / Attacks on Geos: {fastest_strats['geos_attacks'] }"
    log_string += f" / Potion: {'Tidus' if fastest_strats['tidus_potion_klikk'] else ('Rikku' if fastest_strats['rikku_potion_klikk'] else 'None')}"
    log_string += f" / Chain Strat: {fastest_strats['chain_encounter_strat']}"
    log_string += f" / Ruins Strat: {fastest_strats['ruins_encounter_strat']}"
    log_string += f" / Time: {best_time_value}"

    logging.debug(log_string)

    return fastest_strats


def simulate_klikk_to_tros(rng_rolls, klikk_steals):

    global grenade_count

    best_klikk_to_tros_time_value = 0

    klikk1_time_value, hp_tidus = simulate_klikk1(rng_rolls=rng_rolls)

    tidus_potion_turn = best_tidus_potion_turn(rng20_rolls=rng_rolls[20])

    active_strats["tidus_potion_turn"] = tidus_potion_turn

    rng_memory = [0] * 68
    rng_memory2 = [0] * 68

    chain_encounter_happens = chain_encounter()

    for i in range(68):
        rng_memory[i] = rng_rolls[i]

    # Run the Klikk2 simulation without a potion, with tidus using potion and with rikku using potion
    for potion in range(3):

        for i in range(68):
            rng_rolls[i] = rng_memory[i]

        tidus_potion = (True if potion == 1 else False)
        rikku_potion = (True if potion == 2 else False)

        active_strats["tidus_potion_klikk"] = tidus_potion
        active_strats["rikku_potion_klikk"] = rikku_potion

        # logging.debug(f"=======================Potion: {'Tidus' if tidus_potion else ('Rikku' if rikku_potion else 'None')}======================================")

        klikk2_time_value = simulate_klikk2(rng_rolls=rng_rolls, klikk_steals=klikk_steals, hp_tidus=hp_tidus,
                                            tidus_potion=tidus_potion, tidus_potion_turn=tidus_potion_turn,
                                            rikku_potion=rikku_potion)

        for i in range(68):
            rng_memory2[i] = rng_rolls[i]

        grenade_count_memory = grenade_count

        for chain_strat in range(3):

            for ruins_strat in range(4):

                for i in range(68):
                    rng_rolls[i] = rng_memory2[i]

                grenade_count = grenade_count_memory

                active_strats["chain_encounter_strat"] = chain_strat
                active_strats["ruins_encounter_strat"] = ruins_strat

                # logging.debug(f"==================Chain Strat: {chain_strat} / Ruins Strat: {ruins_strat}=====================")

                if chain_encounter_happens:

                    chain_time_value = simulate_chain_encounter(rng_rolls=rng_rolls, strat=chain_strat)

                else:

                    chain_time_value = 0

                ruins_time_value = simulate_ruins_encounter(rng_rolls=rng_rolls, strat=ruins_strat)
                tros_time_value = simulate_tros_encounter(rng_rolls=rng_rolls)

                klikk_to_tros_time_value = klikk1_time_value + klikk2_time_value + chain_time_value + ruins_time_value + tros_time_value
                # logging.debug(f"Klikk 1 Time: {klikk1_time_value} / Klikk 2 Time: {klikk2_time_value} / Chain Time: {chain_time_value} / Ruins Time: {ruins_time_value} / Tros Time: {tros_time_value} / Total Time: {klikk_to_tros_time_value}")

                if best_klikk_to_tros_time_value == 0 or klikk_to_tros_time_value < best_klikk_to_tros_time_value:

                    best_klikk_to_tros_time_value = klikk_to_tros_time_value
                    best_tidus_potion = tidus_potion
                    best_rikku_potion = rikku_potion
                    best_chain_strat = chain_strat
                    best_ruins_strat = ruins_strat

    return best_klikk_to_tros_time_value, best_tidus_potion, tidus_potion_turn, best_rikku_potion, best_chain_strat, best_ruins_strat


def best_tidus_potion_turn(rng20_rolls):

    no_potion_crits = []
    potion_crits = []

    max_crits = 0
    potion_turn = 1

    # roll for klikk 2 ICV roll
    rng20_rolls += 1

    rng20_memory = rng20_rolls

    for attack in range(6):

        crit = rng.calculate_crit(rng_array=rng20_array_tidus, rng_rolls=rng20_rolls,
                                  user_luck=tidus_luck, target_luck=klikk_luck, equipment_bonus=equipment_bonus)

        no_potion_crits.append(1 if crit else 0)

        rng20_rolls += 2

    rng20_rolls = rng20_memory
    rng20_rolls += 1 # Increment for potion usage

    for attack in range(6):
        crit = rng.calculate_crit(rng_array=rng20_array_tidus, rng_rolls=rng20_rolls,
                                  user_luck=tidus_luck, target_luck=klikk_luck, equipment_bonus=equipment_bonus)

        potion_crits.append(1 if crit else 0)

        rng20_rolls += 2

    for potion in range(4):

        crits = 0

        for attack in range(6):

            if attack < potion:

                crits += no_potion_crits[attack]

            else:

                crits += potion_crits[attack]

        if crits > max_crits:

            max_crits = crits
            potion_turn = potion + 1

    return potion_turn


def simulate_klikk1(rng_rolls):

    hp_klikk = 750
    hp_tidus = 520
    hp_rikku = 360

    time_value = 0

    # First Klikk Fight

    # ICV Rolls
    tidus_ctb_roll = rng20_array_tidus[rng_rolls[20] + 1] % (tidus_icv_variance + 1)
    klikk_ctb_roll = 100 - (rng28_array_enemy1[rng_rolls[28] + 1] % 11)

    rng_rolls[1] += 1
    rng_rolls[20] += 1
    rng_rolls[26] += 1
    rng_rolls[28] += 1

    tidus_ctb = 3 * tidus_base_ctb - tidus_ctb_roll
    klikk_ctb = (300 * klikk_base_ctb) // klikk_ctb_roll

    # Battle Simulation

    while True:

        lowest_ctb = min(tidus_ctb, klikk_ctb)

        if lowest_ctb > 0:
            tidus_ctb -= lowest_ctb
            klikk_ctb -= lowest_ctb

        if tidus_ctb == 0:

            base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF, user_stat=15)
            var_damage = rng.get_rng_damage(base_damage=base_damage, rng_array=rng20_array_tidus,
                                            rng_rolls=rng_rolls[20],
                                            user_luck=tidus_luck, target_luck=klikk_luck,
                                            equipment_bonus=equipment_bonus)
            rng_rolls[20] += 2
            hp_klikk -= var_damage
            time_value += tidus_attack_time

            tidus_ctb += 3 * tidus_base_ctb

            if hp_klikk <= 0:
                break

        if klikk_ctb == 0:

            hit_chance = klikk_accuracy - tidus_evasion + klikk_luck - tidus_luck
            hit_roll = rng44_array_enemy1_hit[rng_rolls[44] + 1] % 101
            rng_rolls[44] += 1

            if hit_roll < hit_chance:

                base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF,
                                                           user_stat=klikk_strength, target_stat=tidus_defense)
                var_damage = rng.get_rng_damage(base_damage=base_damage, rng_array=rng28_array_enemy1,
                                                rng_rolls=rng_rolls[28],
                                                user_luck=klikk_luck, target_luck=tidus_luck, can_crit=False)
                rng_rolls[28] += 1  # Klikk can't crit
                hp_tidus -= var_damage
                time_value += klikk_attack_time

            klikk_ctb += 3 * klikk_base_ctb

    return time_value, hp_tidus


def simulate_klikk2(rng_rolls, hp_tidus: int, klikk_steals: int, tidus_potion: bool = False, tidus_potion_turn: int = 1,
                    rikku_potion: bool = False):

    global grenade_count

    hp_klikk = 1500
    hp_rikku = 360

    tidus_ctb_roll = rng20_array_tidus[rng_rolls[20] + 1] % (tidus_icv_variance + 1)
    rikku_ctb_roll = rng26_array_rikku[rng_rolls[26] + 1] % (rikku_icv_variance + 1)
    klikk_ctb_roll = 100 - (rng28_array_enemy1[rng_rolls[28] + 1] % 11)

    rng_rolls[1] += 1
    rng_rolls[20] += 1
    rng_rolls[26] += 1
    rng_rolls[28] += 1

    tidus_ctb = 3 * tidus_base_ctb - tidus_ctb_roll
    rikku_ctb = 3 * rikku_base_ctb - rikku_ctb_roll
    klikk_ctb = 300 * klikk_base_ctb // klikk_ctb_roll

    tidus_turn = 0
    rikku_turn = 0

    steal_successes = 0
    grenade_count = 2  # Start with 2 grenades

    time_value = 0

    while True:

        lowest_ctb = min(tidus_ctb, rikku_ctb, klikk_ctb)

        if lowest_ctb > 0:
            tidus_ctb -= lowest_ctb
            rikku_ctb -= lowest_ctb
            klikk_ctb -= lowest_ctb

        if tidus_ctb == 0:

            tidus_turn += 1

            if tidus_potion and tidus_turn == tidus_potion_turn:

                hp_tidus = min(hp_tidus + 200, tidus_hp_max)
                rng_rolls[20] += 1  # potions roll damage but not crit
                tidus_ctb += 2 * tidus_base_ctb

                time_value += land_potion_time

            else:

                base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF, user_stat=15)
                var_damage = rng.get_rng_damage(base_damage=base_damage, rng_array=rng20_array_tidus, rng_rolls=rng_rolls[20],
                                                user_luck=tidus_luck, target_luck=klikk_luck, equipment_bonus=equipment_bonus)
                rng_rolls[20] += 2
                tidus_ctb += 3 * tidus_base_ctb
                hp_klikk -= var_damage

                time_value += tidus_attack_time

            if hp_klikk <= 0:
                break

        if rikku_ctb == 0:

            rikku_turn += 1

            if rikku_turn == 1:

                base_damage = 350  # Throw Grenade on first turn
                var_damage = rng.get_rng_damage(base_damage=base_damage, rng_array=rng26_array_rikku, rng_rolls=rng_rolls[26],
                                                user_luck=rikku_luck, target_luck=klikk_luck, equipment_bonus=0)
                rng_rolls[26] += 2
                rikku_ctb += 2 * rikku_base_ctb
                hp_klikk -= var_damage

                grenade_count -= 1

                time_value += rikku_grenade_time

            elif rikku_turn == 2 and rikku_potion:

                hp_tidus = min(hp_tidus + 200, tidus_hp_max)
                rng_rolls[26] += 1  # potions roll damage but not crit
                rikku_ctb += 2 * rikku_base_ctb

                time_value += land_potion_time

            # Delay steals by a turn if rikku uses potion
            elif rikku_turn <= klikk_steals + 1 + (1 if rikku_potion else 0):

                base_damage = 0  # Stealing deals no damage
                var_damage = 0
                rikku_ctb += 3 * rikku_base_ctb

                steal_success, grenade_steals = roll_steal(rng_rolls=rng_rolls, steal_successes=steal_successes)

                if steal_success:
                    steal_successes += 1
                    grenade_count += grenade_steals

                time_value += rikku_steal_time

            else:

                base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF, user_stat=10)
                var_damage = rng.get_rng_damage(base_damage=base_damage, rng_array=rng26_array_rikku, rng_rolls=rng_rolls[26],
                                                user_luck=rikku_luck, target_luck=klikk_luck, equipment_bonus=equipment_bonus)
                rng_rolls[26] += 2
                rikku_ctb += 3 * rikku_base_ctb
                hp_klikk -= var_damage

                time_value += rikku_attack_time

            if hp_klikk <= 0:
                break

        if klikk_ctb == 0:

            target_roll = rng04_array_enemy_targeting[rng_rolls[4] + 1] % 2
            rng_rolls[4] += 1

            evasion = (tidus_evasion if target_roll == 0 else rikku_evasion)
            defense = (tidus_defense if target_roll == 0 else rikku_defense)
            target_luck = (tidus_luck if target_roll == 0 else rikku_luck)

            hit_chance = klikk_accuracy - evasion + klikk_luck - target_luck
            hit_roll = rng44_array_enemy1_hit[rng_rolls[44] + 1] % 101
            rng_rolls[44] += 1

            if hit_roll < hit_chance:
                base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF,
                                                           user_stat=klikk_strength, target_stat=defense)
                var_damage = rng.get_rng_damage(base_damage=base_damage, rng_array=rng28_array_enemy1, rng_rolls=rng_rolls[28],
                                                user_luck=klikk_luck, target_luck=tidus_luck, can_crit=False)
                rng_rolls[28] += 1  # Klikk can't crit

                if target_roll == 0:
                    hp_tidus -= var_damage
                else:
                    hp_rikku -= var_damage

            klikk_ctb += 3 * klikk_base_ctb

            time_value += klikk_attack_time

            if hp_tidus < 0:
                time_value += 999
                break

    rng_rolls[10] += 3  # Roll rng10 for klikk2 kill
    rng_rolls[11] += 1  # Roll rng11 for klikk2 kill

    return time_value


def simulate_chain_encounter(rng_rolls, strat: int):

    global grenade_count

    time_value = 0

    # Roll enemy formation, ambush / pre-empt and Tidus / Rikku ICVs
    enemy_formation = rng01_array_enemy_formation[rng_rolls[1] + 1] % 2
    ambush_preempt_roll = rng01_array_enemy_formation[rng_rolls[1] + 2] % 256
    rng_rolls[1] += 2

    if 32 <= ambush_preempt_roll < 223:
        rng_rolls[20] += 1
        rng_rolls[26] += 1

    tidus_crit = manip_planning.rng.calculate_crit(rng_array=rng20_array_tidus, rng_rolls=rng_rolls[20],
                                                   user_luck=tidus_luck, target_luck=15, equipment_bonus=equipment_bonus)

    # Rikku Attack > Tidus Attack
    if strat == 0:

        rng_rolls[20] += 2
        rng_rolls[26] += 2

        time_value += rikku_attack_time + tidus_attack_time

    # Rikku Steal > Tidus Attack > Rikku Attack
    elif strat == 1:

        steal_success, grenade_steals = roll_steal(rng_rolls=rng_rolls, steal_successes=0)

        if steal_success:
            grenade_count += grenade_steals

        rng_rolls[20] += 2

        time_value += underwater_steal_time + tidus_attack_time

        # If Tidus crits and formation is a single piranha group second rikku attack not needed
        if not tidus_crit or enemy_formation == 0:

            rng_rolls[26] += 2
            time_value += rikku_attack_time + multi_piranha_gnaw_time

    # Rikku Steal > Tidus Attack > Rikku Steal > Tidus Attack
    else:

        if enemy_formation == 0:

            steal_success, grenade_steals = roll_steal(rng_rolls=rng_rolls, steal_successes=0)
            if steal_success:
                grenade_count += grenade_steals

            item_drop_roll = rng10_array_drop_steal_chance[rng_rolls[10] + 1] % 255
            if item_drop_roll < piranha_item_drop_chance:
                rng_rolls[11] += 1

            steal_success, grenade_steals = roll_steal(rng_rolls=rng_rolls, steal_successes=0)
            if steal_success:
                grenade_count += grenade_steals

            rng_rolls[20] += 4

            time_value += 2 * underwater_steal_time + 2 * tidus_attack_time + 2 * single_piranha_attack_time

        else:

            steal_success, grenade_steals = roll_steal(rng_rolls=rng_rolls, steal_successes=0)
            if steal_success:
                grenade_count += grenade_steals

            item_drop_roll = rng10_array_drop_steal_chance[rng_rolls[10] + 1] % 255
            if item_drop_roll < piranha_item_drop_chance:
                rng_rolls[11] += 1

            steal_success, grenade_steals = roll_steal(rng_rolls=rng_rolls, steal_successes=1)
            if steal_success:
                grenade_count += grenade_steals

            rng_rolls[20] += 4

            time_value += 2 * underwater_steal_time + 2 * tidus_attack_time + multi_piranha_gnaw_time

    return time_value


def simulate_ruins_encounter(rng_rolls, strat: int):

    global grenade_count

    time_value = 0

    # Roll enemy formation, ambush / pre-empt and Tidus / Rikku ICVs
    ambush_preempt_roll = rng01_array_enemy_formation[rng_rolls[1] + 1] % 256
    rng_rolls[1] += 1

    if 32 <= ambush_preempt_roll < 223:

        rng_rolls[20] += 1
        rng_rolls[26] += 1

    tidus_crit = manip_planning.rng.calculate_crit(rng_array=rng20_array_tidus, rng_rolls=rng_rolls[20],
                                                   user_luck=tidus_luck, target_luck=15, equipment_bonus=equipment_bonus)

    # Rikku Attack > Tidus Attack > Rikku Attack > Tidus Attack
    if strat == 0:

        rng_rolls[20] += 4
        rng_rolls[26] += 4

        time_value = 2 * rikku_attack_time + 2 * tidus_attack_time + multi_piranha_gnaw_time

    # Rikku Attack > Tidus Attack > Rikku Steal > Tidus Attack > Rikku Attack
    elif strat == 1:

        steal_success, grenade_steals = roll_steal(rng_rolls=rng_rolls, steal_successes=0)

        if steal_success:
            grenade_count += grenade_steals

        rng_rolls[20] += 4
        rng_rolls[26] += 4

        time_value = 2 * rikku_attack_time + 2 * tidus_attack_time + underwater_steal_time + 2 * multi_piranha_gnaw_time

    # Rikku Attack > Tidus Attack > Rikku Steal > Tidus Attack > Rikku Defend > Tidus Attack
    elif strat == 2:

        steal_success, grenade_steals = roll_steal(rng_rolls=rng_rolls, steal_successes=0)

        if steal_success:
            grenade_count += grenade_steals

        rng_rolls[20] += 6
        rng_rolls[26] += 2

        time_value = 2 * rikku_attack_time + 2 * tidus_attack_time + underwater_steal_time + 2 * multi_piranha_gnaw_time + 1

    # Rikku Steal > Tidus Attack > Rikku Steal > Tidus Attack > Rikku Attack > Tidus Attack
    elif strat == 3:

        steal_success, grenade_steals = roll_steal(rng_rolls=rng_rolls, steal_successes=0)

        if steal_success:
            grenade_count += grenade_steals

        item_drop_roll = rng10_array_drop_steal_chance[rng_rolls[10] + 1] % 255
        if item_drop_roll < piranha_item_drop_chance:
            rng_rolls[11] += 1

        steal_success, grenade_steals = roll_steal(rng_rolls=rng_rolls, steal_successes=0)

        if steal_success:
            grenade_count += grenade_steals

        rng_rolls[20] += 6
        rng_rolls[26] += 2

        time_value = 1 * rikku_attack_time + 3 * tidus_attack_time + 2 * underwater_steal_time + 3 * multi_piranha_gnaw_time

    return time_value


def simulate_tros_encounter(rng_rolls):

    time_value = 0
    total_damage = 0

    # Roll enemy formation, ambush / pre-empt and Tidus / Rikku ICVs
    ambush_preempt_roll = rng01_array_enemy_formation[rng_rolls[1] + 1] % 256
    rng_rolls[1] += 1

    if 32 <= ambush_preempt_roll < 223:

        rng_rolls[20] += 1
        rng_rolls[26] += 1

    # If pre-empt, advance rng 8 times for the purpose of the calculating low roll as fifth attack is the relevant roll
    if ambush_preempt_roll < 32:

        low_roll_damage = rng.get_rng_damage(base_damage=350, rng_array=rng26_array_rikku, rng_rolls=rng_rolls[26] + 8,
                                             user_luck=rikku_luck, target_luck=15)

    else:

        low_roll_damage = rng.get_rng_damage(base_damage=350, rng_array=rng26_array_rikku, rng_rolls=rng_rolls[26],
                                             user_luck=rikku_luck, target_luck=15)

    if low_roll_damage < 350:

        time_value += 0

    else:

        time_value += 7

    for grenade in range(grenade_count):

        var_damage = rng.get_rng_damage(base_damage=350, rng_array=rng26_array_rikku, rng_rolls=rng_rolls[26],
                                        user_luck=rikku_luck, target_luck=15)
        total_damage += var_damage
        rng_rolls[26] += 2

    for attack in range(2):

        base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF, user_stat=15, target_stat=1)
        var_damage = rng.get_rng_damage(base_damage=base_damage, rng_array=rng20_array_tidus, rng_rolls=rng_rolls[20],
                                        user_luck=tidus_luck, target_luck=15, equipment_bonus=equipment_bonus)
        total_damage += var_damage
        rng_rolls[20] += 2

    # if we don't have enough grenades to kill Tros then this strat line is non-viable
    if total_damage < 2200:
        time_value += 999

    return time_value


def simulate_klikk_hits(rng_array_enemy1_hit, rng44_rolls: int) -> int:

    hit_chance = klikk_accuracy - tidus_evasion + klikk_luck - tidus_luck

    hit_count = 0

    for attack in range(4):

        hit_roll = rng_array_enemy1_hit[rng44_rolls + 1] % 101
        rng44_rolls += 1

        if hit_roll < hit_chance:
            hit_count += 1

    return hit_count


def simulate_klikk_steals(rng_rolls) -> (int, int):

    klikk_steals = 0
    steal_successes = 0
    total_grenades = 0

    for steal_attempt in range(4):

        steal_success, grenade_steals = roll_steal(rng_rolls=rng_rolls, steal_successes=steal_successes)

        if steal_success:
            steal_successes += 1
            klikk_steals = steal_attempt + 1
            total_grenades += grenade_steals

    return total_grenades, klikk_steals


def roll_steal(rng_rolls, steal_successes) -> (bool, int):

    grenade_steals = 0

    steal_chance = 255 // (2 ** steal_successes)
    steal_roll = rng10_array_drop_steal_chance[rng_rolls[10] + 1] % 255
    rng_rolls[10] += 1

    steal_success = (steal_roll < steal_chance)

    if steal_success:

        grenade_steals += 1
        rare_steal_roll = rng11_array_rare_steal_chance[rng_rolls[11] + 1]
        rng_rolls[11] += 1

        if rare_steal_roll < rare_steal_chance:
            grenade_steals += 1

    return steal_success, grenade_steals


def chain_encounter() -> bool:

    rng00_array = main.rng_array_from_index(index=0, array_len=200)
    rng00_rolls = 0

    danger_value = 60
    grace_period = danger_value // 2
    steps = 62
    current_distance = 0

    for step in range(steps):
        current_distance += 1
        if current_distance > grace_period:
            encounter_chance = (current_distance - grace_period) * 256 // (4 * danger_value)
            encounter_roll = rng00_array[rng00_rolls + 1] % 256
            rng00_rolls += 1
            if encounter_roll < encounter_chance:
                logging.debug(f"Chain encounter on step: {step}")
                return True

    return False


def ruins_encounter_steals(grenades_needed: int) -> (int, int):

    global rng01_array_enemy_formation
    global rng10_array_drop_steal_chance
    global rng11_array_rare_steal_chance

    rng01_array_enemy_formation = main.rng_array_from_index(index=1, array_len=200)
    rng10_array_drop_steal_chance = main.rng_array_from_index(index=10, array_len=200)
    rng11_array_rare_steal_chance = main.rng_array_from_index(index=11, array_len=200)

    item_drop_chance = 205

    first_rare_steal = 0
    steal_first_turn = True
    steal_second_turn = True
    steal_twice_first = False
    steal_twice_second = False
    second_steal_flip1 = False
    second_steal_flip2 = False

    ruins_steals = 0

    rng_rolls = [0] * 68

    for steal in range(3):
        if rng11_array_rare_steal_chance[rng_rolls[11] + steal + 1] < rare_steal_chance:
            first_rare_steal = steal + 1

    steal_roll = rng10_array_drop_steal_chance[rng_rolls[10] + 2] % 255
    steal_chance = 255 // 2

    second_steal_flip1 = (steal_roll < steal_chance)

    steal_roll = rng10_array_drop_steal_chance[rng_rolls[10] + 5] % 255
    steal_chance = 255 // 2

    second_steal_flip2 = (steal_roll < steal_chance)

    logging.debug(f"Grenades Needed: {grenades_needed}")

    if grenades_needed < 1:

        ruins_steals = 0

    else:

        if grenades_needed == 1:

            # steal once if rare steal, otherwise steal once per grenade we need
            steal_first_turn = False
            ruins_steals = 1

        elif grenades_needed == 2:

            if first_rare_steal == 1:

                ruins_steals = 1

            elif first_rare_steal == 2:

                item_drop_roll = rng10_array_drop_steal_chance[rng_rolls[10] + 1] % 255

                if item_drop_roll < item_drop_chance:

                    steal_first_turn = False
                    ruins_steals = 1

                else:

                    ruins_steals = 2

            else:

                ruins_steals = 2

        elif grenades_needed > 2:

            if first_rare_steal == 1:

                ruins_steals = 2

            elif first_rare_steal == 2:

                ruins_steals = 2

            elif first_rare_steal == 3:

                steal_second_turn = False
                ruins_steals = 2

            elif second_steal_flip1:

                steal_twice_first = True
                ruins_steals = 2

            elif second_steal_flip2:

                steal_twice_second = True
                steal_first_turn = False
                ruins_steals = 2

            else:

                # idk... cry?
                ruins_steals = 2

    return ruins_steals, steal_first_turn, steal_second_turn, steal_twice_first, steal_twice_second


def rikku_damage_taken_tros():

    global rng01_array_enemy_formation
    global rng04_array_enemy_targeting
    global rng26_array_rikku
    global rng28_array_enemy1

    rng01_array_enemy_formation = main.rng_array_from_index(index=1, array_len=200)
    rng04_array_enemy_targeting = main.rng_array_from_index(index=4, array_len=200)
    rng26_array_rikku = main.rng_array_from_index(index=26, array_len=200)
    rng28_array_enemy1 = main.rng_array_from_index(index=28, array_len=200)

    rng_rolls = [0] * 68

    rikku_damage_taken = 0

    preempt_ambush_roll = rng01_array_enemy_formation[1] % 256

    if 32 <= preempt_ambush_roll < 223:

        rng_rolls[26] += 1
        rng_rolls[28] += 1

    tentacles_base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF,
                                                         user_stat=10, target_stat=8, ability_power=24)

    nautilus_charge_base_damage = damage.calculate_base_damage(formula=damage.Formula.STR_VS_DEF,
                                                               user_stat=10, target_stat=8, ability_power=48)

    first_rikku_damage = manip_planning.rng.get_rng_damage(base_damage=350, rng_array=rng26_array_rikku,
                                                           rng_rolls=rng_rolls[26],
                                                           user_luck=rikku_luck, target_luck=15)
    fifth_rikku_damage = manip_planning.rng.get_rng_damage(base_damage=350, rng_array=rng26_array_rikku,
                                                           rng_rolls=rng_rolls[26] + 8,
                                                           user_luck=rikku_luck, target_luck=15)

    tros_first_target = rng04_array_enemy_targeting[1] % 2
    tros_second_target = rng04_array_enemy_targeting[2] % 2

    logging.debug(f"Tros first target: {tros_first_target}")
    logging.debug(f"Tros second target: {tros_second_target}")

    # preempt fight
    if preempt_ambush_roll < 32:

        rng_rolls[28] += 1  # tidus gets hit by Nautilus Charge first
        var_damage = manip_planning.rng.get_rng_damage(base_damage=nautilus_charge_base_damage,
                                                       rng_array=rng28_array_enemy1,
                                                       rng_rolls=rng_rolls[28], user_luck=15,
                                                       target_luck=rikku_luck, can_crit=False)
        logging.debug(f"Nautilus Charge deals {var_damage} damage to Rikku")
        rikku_damage_taken += var_damage
        rng_rolls[28] += 1

        if fifth_rikku_damage < 350:

            if tros_first_target == 1:

                var_damage = manip_planning.rng.get_rng_damage(base_damage=tentacles_base_damage,
                                                               rng_array=rng28_array_enemy1,
                                                               rng_rolls=rng_rolls[28], user_luck=15,
                                                               target_luck=rikku_luck, can_crit=False)

                logging.debug(f"Tentacles deals {var_damage} damage to Rikku")
                rikku_damage_taken += var_damage

            rng_rolls[28] += 1

    elif preempt_ambush_roll < 223:

        if first_rikku_damage < 350:

            if tros_first_target == 1:

                var_damage = manip_planning.rng.get_rng_damage(base_damage=tentacles_base_damage,
                                                               rng_array=rng28_array_enemy1,
                                                               rng_rolls=rng_rolls[28], user_luck=15,
                                                               target_luck=rikku_luck, can_crit=False)
                logging.debug(f"Tentacles deals {var_damage} damage to Rikku")

                rikku_damage_taken += var_damage

            rng_rolls[28] += 1

        rng_rolls[28] += 1  # tidus gets hit by Nautilus Charge first
        var_damage = manip_planning.rng.get_rng_damage(base_damage=nautilus_charge_base_damage,
                                                       rng_array=rng28_array_enemy1,
                                                       rng_rolls=rng_rolls[28], user_luck=15,
                                                       target_luck=rikku_luck, can_crit=False)
        logging.debug(f"Nautilus Charge deals {var_damage} damage to Rikku")
        rikku_damage_taken += var_damage

    else:

        if tros_first_target == 1:

            var_damage = manip_planning.rng.get_rng_damage(base_damage=tentacles_base_damage,
                                                           rng_array=rng28_array_enemy1,
                                                           rng_rolls=rng_rolls[28], user_luck=15,
                                                           target_luck=rikku_luck, can_crit=False)
            logging.debug(f"Tentacles deals {var_damage} damage to Rikku")
            rikku_damage_taken += var_damage
            rng_rolls[28] += 1

        if first_rikku_damage < 350:

            if tros_second_target == 1:

                var_damage = manip_planning.rng.get_rng_damage(base_damage=tentacles_base_damage,
                                                               rng_array=rng28_array_enemy1,
                                                               rng_rolls=rng_rolls[28], user_luck=15,
                                                               target_luck=rikku_luck, can_crit=False)
                logging.debug(f"Tentacles deals {var_damage} damage to Rikku")
                rikku_damage_taken += var_damage

            rng_rolls[28] += 1

        rng_rolls[28] += 1  # tidus gets hit by Nautilus Charge first
        var_damage = manip_planning.rng.get_rng_damage(base_damage=nautilus_charge_base_damage,
                                                       rng_array=rng28_array_enemy1,
                                                       rng_rolls=rng_rolls[28], user_luck=15,
                                                       target_luck=rikku_luck, can_crit=False)
        logging.debug(f"Nautilus Charge deals {var_damage} damage to Rikku")
        rikku_damage_taken += var_damage

    return rikku_damage_taken


# TO DO: Simulate chain encounter fight to check for deaths (for healing)
def chain_encounter_deaths(strat: int):

    global rng01_array_enemy_formation
    global rng04_array_enemy_targeting
    global rng26_array_rikku
    global rng28_array_enemy1
    global rng29_array_enemy2
    global rng44_array_enemy1_hit
    global rng45_array_enemy2_hit

    rng01_array_enemy_formation = main.rng_array_from_index(index=1, array_len=200)
    rng04_array_enemy_targeting = main.rng_array_from_index(index=4, array_len=200)
    rng26_array_rikku = main.rng_array_from_index(index=26, array_len=200)
    rng28_array_enemy1 = main.rng_array_from_index(index=28, array_len=200)
    rng29_array_enemy2 = main.rng_array_from_index(index=29, array_len=200)
    rng44_array_enemy1_hit = main.rng_array_from_index(index=44, array_len=200)
    rng45_array_enemy2_hit = main.rng_array_from_index(index=45, array_len=200)

    rng_rolls = [0] * 68

    hp_rikku = Rikku.hp()
    hp_tidus = Tidus.hp()

    heal_characters = [0, 0]

    enemy_formation = rng01_array_enemy_formation[rng_rolls[1] + 1] % 2
    ambush_preempt_roll = rng01_array_enemy_formation[rng_rolls[1] + 1] % 256
    rng_rolls[1] += 2

    targets = [0, 0, 0, 0]

    targets[0] = rng04_array_enemy_targeting[rng_rolls[4] + 1] % 2
    targets[1] = rng04_array_enemy_targeting[rng_rolls[4] + 2] % 2
    targets[2] = rng04_array_enemy_targeting[rng_rolls[4] + 3] % 2
    targets[3] = rng04_array_enemy_targeting[rng_rolls[4] + 4] % 2

    return