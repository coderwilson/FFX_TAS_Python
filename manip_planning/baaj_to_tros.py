import logging
import math
import damage
import rng_track
from memory import main
from manip_planning import rng

rng01_array_enemy_formation = []
rng04_array_enemy_targetting = []
rng10_array_drop_steal_chance = []
rng11_array_rare_steal_chance = []
rng20_array_tidus = []
rng26_array_rikku = []
rng28_array_enemy1 = []
rng44_array_enemy1_hit = []

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
klikk_attack_time = 2
single_piranha_attack_time = 2
multi_piranha_gnaw_time = 3

grenade_count = 0
rare_steal_chance = 32


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


def plan_klikk(klikk_steals: int):

    global rng01_array_enemy_formation
    global rng04_array_enemy_targetting
    global rng10_array_drop_steal_chance
    global rng11_array_rare_steal_chance
    global rng20_array_tidus
    global rng26_array_rikku
    global rng28_array_enemy1
    global rng44_array_enemy1_hit

    rng01_array_enemy_formation = main.rng_array_from_index(index=1, array_len=200)
    rng04_array_enemy_targetting = main.rng_array_from_index(index=4, array_len=200)
    rng10_array_drop_steal_chance = main.rng_array_from_index(index=10, array_len=200)
    rng11_array_rare_steal_chance = main.rng_array_from_index(index=11, array_len=200)
    rng20_array_tidus = main.rng_array_from_index(index=20, array_len=200)
    rng26_array_rikku = main.rng_array_from_index(index=26, array_len=200)
    rng28_array_enemy1 = main.rng_array_from_index(index=28, array_len=200)
    rng44_array_enemy1_hit = main.rng_array_from_index(index=44, array_len=200)

    logging.debug(rng04_array_enemy_targetting)

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

    for i in range(68):
        rng_memory.append(rng_rolls[i])

    for tidus_potion_geos in range(2):

        for tidus_attacks_geos in range(4-geos_ambush-tidus_potion_geos):

            for i in range(68):
                rng_rolls[i] = rng_memory[i]

            rng_rolls[20] = rng_rolls[20] + tidus_potion_geos + 2 * tidus_attacks_geos

            # tidus_crits = simulate_klikk_crits(rng_array_tidus=rng20_array_tidus, rng20_rolls=rng20_rolls)

            klikk_tros_time_value, tidus_potion, tidus_potion_turn, rikku_potion, rikku_underwater_attacks, tros_low_roll = simulate_klikk_to_tros(rng_rolls=rng_rolls, klikk_steals=klikk_steals)

            time_value = klikk_tros_time_value + underwater_potion_time * tidus_potion_geos + 2 * tidus_attacks_geos

            if best_time_value == -99 or time_value < best_time_value:
                best_time_value = time_value
                best_geos_potion = tidus_potion_geos
                best_geos_attacks = tidus_attacks_geos
                best_tidus_potion_klikk = tidus_potion
                best_potion_turn = tidus_potion_turn
                best_rikku_potion_klikk = rikku_potion
                best_rikku_underwater_attacks = rikku_underwater_attacks
                best_tros_low_roll = tros_low_roll

    log_string = f"Sahagin B First: {best_sahagin_b_first}"
    log_string += f" / Potion on Geos: {best_geos_potion}"
    log_string += f" / Attacks on Geos: {best_geos_attacks}"
    log_string += f" / Potion: {'Tidus' if best_tidus_potion_klikk else ('Rikku' if best_rikku_potion_klikk else 'None')}"
    log_string += f" / Rikku Underwater Attacks: {best_rikku_underwater_attacks}"
    log_string += f" / Tros Low Roll: {best_tros_low_roll}"
    log_string += f" / Time: {best_time_value}"

    logging.debug(log_string)

    return best_sahagin_b_first, best_geos_potion, best_geos_attacks, best_tidus_potion_klikk, best_potion_turn, best_rikku_potion_klikk, best_rikku_underwater_attacks


def simulate_klikk_to_tros(rng_rolls, klikk_steals):

    tros_time_value = 0
    best_klikk_to_tros_time_value = 0

    klikk1_time_value, hp_tidus = simulate_klikk1(rng_rolls=rng_rolls)

    tidus_potion_turn = best_tidus_potion_turn(rng20_rolls=rng_rolls[20])

    logging.debug(f"Tidus Potion Turn: {tidus_potion_turn}")

    rng_memory = []

    for i in range(68):
        rng_memory.append(rng_rolls[i])

    # Run the simulation without a potion, with tidus using potion and with rikku using potion
    for potion in range(3):

        for i in range(68):
            rng_rolls[i] = rng_memory[i]

        tidus_potion = (True if potion == 1 else False)
        rikku_potion = (True if potion == 2 else False)

        klikk2_time_value = simulate_klikk2(rng_rolls=rng_rolls, klikk_steals=klikk_steals, hp_tidus=hp_tidus,
                                            tidus_potion=tidus_potion, tidus_potion_turn=tidus_potion_turn,
                                            rikku_potion=rikku_potion)

        rare_steals_underwater = [0] * 4
        for steal in range(4):
            if rng11_array_rare_steal_chance[rng_rolls[11] + steal + 1] < rare_steal_chance:
                rare_steals_underwater[steal] = 1

        if grenade_count < 6:
            steals_required = max(1, 6 - grenade_count - max(rare_steals_underwater))
        else:
            steals_required = 0

        logging.debug(f"Steals Required: {steals_required}")

        tros_time_value, rikku_underwater_attacks, tros_low_roll = simulate_underwater_ruins(rng01_rolls=rng_rolls[1],
                                                                                             rng26_rolls=rng_rolls[26],
                                                                                             steals_required=steals_required)

        klikk_to_tros_time_value = klikk1_time_value + klikk2_time_value + tros_time_value
        logging.debug(f"Klikk 1 Time: {klikk1_time_value} / Klikk 2 Time: {klikk2_time_value} / Tros Time: {tros_time_value}")

        if best_klikk_to_tros_time_value == 0 or klikk_to_tros_time_value < best_klikk_to_tros_time_value:

            best_klikk_to_tros_time_value = klikk_to_tros_time_value
            best_tidus_potion = tidus_potion
            best_rikku_potion = rikku_potion
            best_rikku_underwater_attacks = rikku_underwater_attacks
            best_tros_low_roll = tros_low_roll

    logging.debug(f"Potion: {'Tidus' if best_tidus_potion else ('Rikku' if best_rikku_potion else 'None')} / Time: {best_klikk_to_tros_time_value}")

    return best_klikk_to_tros_time_value, best_tidus_potion, tidus_potion_turn, best_rikku_potion, best_rikku_underwater_attacks, best_tros_low_roll


def best_tidus_potion_turn(rng20_rolls):

    no_potion_crits = []
    potion_crits = []

    max_crits = 0
    potion_turn = 0

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

        logging.debug(f"Potion Turn: {potion + 1} / Crits: {crits}")

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

    logging.debug(f"Tidus CTB: {tidus_ctb} / Klikk CTB: {klikk_ctb}")

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
                                                user_luck=klikk_luck, target_luck=tidus_luck, equipment_bonus=0)
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

    logging.debug(f"Tidus CTB: {tidus_ctb} / Rikku CTB: {rikku_ctb} / Klikk CTB: {klikk_ctb}")

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

            target_roll = rng04_array_enemy_targetting[rng_rolls[4] + 1] % 2
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
                                                user_luck=klikk_luck, target_luck=tidus_luck, equipment_bonus=0)
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


def simulate_underwater_ruins(rng01_rolls, rng26_rolls, steals_required) -> (int, int, bool):

    formation_roll = None

    if chain_encounter():

        formation_roll = rng01_array_enemy_formation[rng01_rolls + 1] % 2
        ambush_preempt_roll = rng01_array_enemy_formation[rng01_rolls + 2] % 256

        rng01_rolls += 2

        if ambush_preempt_roll < 32:

            logging.debug("Chain encounter is an pre-empt")

        elif ambush_preempt_roll >= 223:

            sahagins_ambush = 1
            logging.debug("Chain encounter is an ambush")

        else:

            rng26_rolls += 1

    # Forced Piranhas
    ambush_preempt_roll = rng01_array_enemy_formation[rng01_rolls + 1] % 256

    rng01_rolls += 1

    if ambush_preempt_roll < 32:

        logging.debug("Forced Piranhas is an pre-empt")

    elif ambush_preempt_roll >= 223:

        sahagins_ambush = 1
        logging.debug("Forced Piranhas is an ambush")

    else:

        rng26_rolls += 1

    # Tros
    ambush_preempt_roll = rng01_array_enemy_formation[rng01_rolls + 1] % 256

    rng01_rolls += 1

    if ambush_preempt_roll < 32:

        # Advance 8 extra rng26 rolls if Tros pre-empt because the relevant low roll grenade the fifth one thrown
        rng26_rolls += 8
        logging.debug("Tros is an pre-empt")

    elif ambush_preempt_roll >= 223:

        logging.debug("Tros is an ambush")

    else:

        rng26_rolls += 1

    rng26_rolls += 4  # 2 Attacks on chain / piranhas

    var_damage = rng.get_rng_damage(base_damage=350, rng_array=rng26_array_rikku, rng_rolls=rng26_rolls,
                                    user_luck=rikku_luck, target_luck=15)
    tros_low_roll_2 = (var_damage < 350)

    logging.debug(f"Tros Low Roll 2: {var_damage}")

    rng26_rolls += 2  # 3rd Attack on chain / piranhas

    var_damage = rng.get_rng_damage(base_damage=350, rng_array=rng26_array_rikku, rng_rolls=rng26_rolls,
                                    user_luck=rikku_luck, target_luck=15)
    tros_low_roll_3 = (var_damage < 350)

    logging.debug(f"Tros Low Roll 3: {var_damage}")

    if steals_required == 0:
        if tros_low_roll_3:
            tros_time_value = 0
            rikku_piranha_attacks = 3
            tros_low_roll = True
        elif tros_low_roll_2:
            tros_time_value = 4  # Have to tank a piranha attack
            rikku_piranha_attacks = 2
            tros_low_roll = True
        else:
            tros_time_value = 7  # No Tros Low Roll
            rikku_piranha_attacks = 3
            tros_low_roll = False

    elif steals_required == 1:
        if tros_low_roll_3:
            tros_time_value = 0
            rikku_piranha_attacks = 3
            tros_low_roll = True
        elif tros_low_roll_2:
            tros_time_value = 1  # Have to do an extra Defend on Rikku
            rikku_piranha_attacks = 2
            tros_low_roll = True
        else:
            tros_time_value = 7  # No Tros Low Roll
            rikku_piranha_attacks = 3
            tros_low_roll = False

    elif steals_required == 2:
        if tros_low_roll_3:
            tros_time_value = 0
            rikku_piranha_attacks = 3
            tros_low_roll = True
        elif tros_low_roll_2:
            tros_time_value = 0  # Alternate strat same time value
            rikku_piranha_attacks = 2
            tros_low_roll = True
        else:
            tros_time_value = 7  # No Tros Low Roll
            rikku_piranha_attacks = 3
            tros_low_roll = False

    # In this case not worth forcing an extra Rikku Attack to get Tros low roll1
    elif steals_required > 2:
        if tros_low_roll_2:
            tros_time_value = 0  # Alternate strat same time value
            rikku_piranha_attacks = 2
            tros_low_roll = True
        else:
            tros_time_value = 7  # No Tros Low Roll
            rikku_piranha_attacks = 2
            tros_low_roll = False

    logging.debug(f"Rikku Piranha Attacks: {rikku_piranha_attacks}")

    return tros_time_value, rikku_piranha_attacks, tros_low_roll


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

    rare_steal_chance = 32

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

    logging.debug(f"Steal Roll: {steal_roll} / Steal Chance: {steal_chance}")

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

    danger_value = 60
    grace_period = danger_value // 2
    steps = 62
    current_distance = 0
    rng00_rolls = 0

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


def chain_encounter_steals(grenades_needed: int) -> (int, int):

    global rng01_array_enemy_formation
    global rng10_array_drop_steal_chance
    global rng11_array_rare_steal_chance

    rng01_array_enemy_formation = main.rng_array_from_index(index=1, array_len=200)
    rng10_array_drop_steal_chance = main.rng_array_from_index(index=10, array_len=200)
    rng11_array_rare_steal_chance = main.rng_array_from_index(index=11, array_len=200)

    formation_roll = 0

    first_rare_steal = 0
    steal_first_turn = True
    second_steal_flip = False

    chain_steals = 0

    rng_rolls = [0] * 68

    for steal in range(5):
        if rng11_array_rare_steal_chance[rng_rolls[11] + steal + 1] < rare_steal_chance:
            first_rare_steal = steal + 1

    steal_roll = rng10_array_drop_steal_chance[rng_rolls[10] + 2] % 255
    steal_chance = 255 // 2

    second_steal_flip = (steal_roll < steal_chance)

    if chain_encounter():

        formation_roll = rng01_array_enemy_formation[rng_rolls[1] + 1] % 2

        if grenades_needed < 1:

            chain_steals = 0

        elif formation_roll == 0:

            if grenades_needed < 3:

                # steal once if rare steal, otherwise steal once per grenade we need
                chain_steals = (1 if first_rare_steal == 1 else grenades_needed)

            else:

                # don't steal twice if rare steal is on an even numbered steal
                if first_rare_steal == 2:
                    steal_first_turn = False
                    chain_steals = 1
                elif first_rare_steal == 5:
                    chain_steals = 1
                else:
                    chain_steals = (1 if first_rare_steal == 4 else 2)

        else:

            if not second_steal_flip:

                # if we can't steal twice from same piranha then steal here unless second steal is rare to avoid missing rare steal
                chain_steals = (0 if first_rare_steal == 2 else 1)

            elif grenades_needed < 3:

                # steal once if rare steal, otherwise steal once per grenade we need
                chain_steals = (1 if first_rare_steal == 1 else grenades_needed)

            else:

                # don't steal twice if rare steal is after second steal as we can pick up on next fight
                if first_rare_steal == 5:
                    chain_steals = 1
                else:
                    chain_steals = (1 if first_rare_steal > 2 else 2)

    return chain_steals, steal_first_turn, formation_roll


def ruins_encounter_steals(grenades_needed: int) -> (int, int):

    global rng01_array_enemy_formation
    global rng10_array_drop_steal_chance
    global rng11_array_rare_steal_chance

    rng01_array_enemy_formation = main.rng_array_from_index(index=1, array_len=200)
    rng10_array_drop_steal_chance = main.rng_array_from_index(index=10, array_len=200)
    rng11_array_rare_steal_chance = main.rng_array_from_index(index=11, array_len=200)

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

                steal_first_turn = False
                ruins_steals = 1

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
