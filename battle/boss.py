import logging

import battle.main
import logs
import memory.main
import screen
import vars
import xbox

FFXC = xbox.controller_handle()
game_vars = vars.vars_handle()

logger = logging.getLogger(__name__)


@battle.utils.speedup_decorator
def ammes():
    battle_complete = 0
    count_attacks = 0
    tidus_od_flag = False

    while battle_complete != 1:
        if memory.main.turn_ready():
            if (
                not tidus_od_flag
                and screen.turn_tidus()
                and memory.main.get_overdrive_battle(0) == 100
            ):
                battle.overdrive.tidus()
                tidus_od_flag = True
            else:
                logger.info("Attacking Sinspawn Ammes")
                battle.main.attack("none")
                count_attacks += 1
        if memory.main.user_control():
            battle_complete = 1
            logger.info("Ammes battle complete")


@battle.utils.speedup_decorator
def tanker():
    logger.info("Fight start: Tanker")
    count_attacks = 0
    tidus_count = 0
    auron_count = 0
    xbox.click_to_battle()

    while not memory.main.battle_complete():
        if memory.main.turn_ready():
            if screen.turn_tidus():
                tidus_count += 1
                if tidus_count < 4:
                    xbox.weap_swap(0)
                else:
                    battle.main.attack("none")
                    count_attacks += 1
            elif screen.turn_auron():
                auron_count += 1
                if auron_count < 2:
                    battle.main.attack_self_tanker()
                else:
                    battle.main.attack("none")
                    count_attacks += 1
        elif memory.main.diag_skip_possible():
            xbox.tap_b()


@battle.utils.speedup_decorator
def klikk():
    logger.info("Fight start: Klikk")
    klikk_attacks = 0
    klikk_revives = 0
    steal_count = 0
    while not memory.main.battle_complete():  # AKA end of battle screen
        if memory.main.turn_ready():
            battle_hp = memory.main.get_battle_hp()
            if battle_hp[0] == 0:
                battle.main.revive()
                klikk_revives += 1
            elif screen.turn_tidus():
                if battle_hp[0] == 0 and memory.main.get_enemy_current_hp()[0] > 125:
                    battle.main.use_potion_character(0, "l")
                else:
                    battle.main.attack("none")
                klikk_attacks += 1
            elif screen.turn_rikku():
                gregrenade_count = memory.main.get_item_count_slot(
                    memory.main.get_item_slot(35)
                )
                if (
                    battle_hp[0] < 120
                    and not (
                        memory.main.get_next_turn() == 0
                        and memory.main.get_enemy_current_hp()[0] <= 181
                    )
                    and not memory.main.rng_seed() == 160
                ):
                    battle.main.use_potion_character(0, "l")
                    klikk_revives += 1
                elif memory.main.get_enemy_current_hp()[0] < 58:
                    battle.main.attack("none")
                    klikk_attacks += 1
                elif gregrenade_count < 6 and memory.main.next_steal(
                    steal_count=steal_count
                ):
                    logger.info("Attempting to steal from Klikk")
                    battle.main.steal()
                    steal_count += 1
                else:
                    battle.main.attack("none")
                    klikk_attacks += 1
        else:
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    logger.info("Klikk fight complete")
    logger.debug(f"map: {memory.main.get_map()}")
    while not (
        memory.main.get_map() == 71
        and memory.main.user_control()
        and memory.main.get_coords()[1] < 15
    ):
        # print(memory.main.get_map())
        if game_vars.csr():
            FFXC.set_value("btn_b", 1)
        else:
            xbox.tap_b()  # Maybe not skippable dialog, but whatever.
    FFXC.set_neutral()
    memory.main.wait_frames(1)


@battle.utils.speedup_decorator
def tros():
    logs.open_rng_track()
    logger.info("Fight start: Tros")
    FFXC.set_neutral()
    battle_clock = 0
    Attacks = 0
    Revives = 0
    Grenades = 0
    Steals = 0
    advances = 0
    while not memory.main.turn_ready():
        pass

    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.diag_skip_possible():
            xbox.tap_b()
        elif memory.main.turn_ready():
            battle_clock += 1
            logger.debug(f"Battle clock: {battle_clock}")
            tros_pos = 2
            logger.debug("Determining Tros position")
            while tros_pos == 2 and not memory.main.battle_complete():
                # Two for "not yet determined". Maybe can be HP-based instead?
                camera = memory.main.get_camera()
                # First, determine position of Tros
                if camera[0] > 2:
                    tros_pos = 1  # One for cannot attack.
                    logger.debug("Tros is long-range. Cannot attack.")
                elif camera[0] < -2:
                    tros_pos = 1  # One for cannot attack.
                    logger.debug("Tros is long-range. Cannot attack.")
                else:
                    tros_pos = 0  # One for "Close range, can be attacked.
                    logger.debug("Tros is short-range.")

            # Assuming battle is not complete:
            if memory.main.battle_active():
                party_hp = memory.main.get_battle_hp()
                # Someone requires reviving.
                if party_hp[0] == 0 or party_hp[1] == 0:
                    logger.debug("Tros: Someone fainted.")
                    battle.main.revive()
                    Revives += 1
                elif screen.turn_rikku():
                    logger.debug("Rikku turn")
                    grenade_slot = memory.main.get_item_slot(35)
                    gregrenade_count = memory.main.get_item_count_slot(grenade_slot)
                    logger.debug("------------------------------")
                    logger.debug(f"Current grenade count: {gregrenade_count}")
                    logger.debug(f"Grenades used: {Grenades}")
                    logger.debug("------------------------------")
                    total_grenades = gregrenade_count + Grenades
                    if total_grenades < 6:
                        if tros_pos == 1:
                            battle.main.defend()
                        else:
                            battle.main.steal()
                            Steals += 1
                    elif gregrenade_count == 0:
                        if tros_pos == 1:
                            battle.main.defend()
                        else:
                            battle.main.steal()
                            Steals += 1
                    else:
                        if tros_pos != 1 and advances in [1, 2]:
                            battle.main.steal()
                            Steals += 1
                        else:
                            grenade_slot = memory.main.get_use_items_slot(35)
                            battle.main.use_item(grenade_slot, "none")
                            Grenades += 1
                elif screen.turn_tidus():
                    logger.debug("Tidus turn")
                    if (
                        tros_pos == 1
                        and memory.main.get_battle_hp()[1] < 200
                        and memory.main.get_enemy_current_hp()[0] > 800
                    ):
                        battle.main.use_potion_character(6, "l")
                    elif tros_pos == 1 or memory.main.get_enemy_current_hp()[0] < 300:
                        battle.main.defend()
                    else:
                        battle.main.attack("none")
                        Attacks += 1

    logger.info("Tros battle complete.")
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def sin_fin():
    logger.info("Fight start: Sin's Fin")
    screen.await_turn()
    fin_turns = 0
    kim_turn = False
    complete = False
    while not complete:
        if memory.main.turn_ready():
            fin_turns += 1
            logger.debug("Determining first turn.")
            if screen.turn_tidus():
                battle.main.defend()
                logger.debug("Tidus defend")
            elif screen.turn_yuna():
                battle.main.buddy_swap_lulu()  # Yuna out, Lulu in
                battle.main.thunder_target(target=23, direction="r")
            elif screen.turn_kimahri():
                battle.main.lancet_target(target=23, direction="r")
                kim_turn = True
            elif screen.turn_lulu():
                battle.main.thunder_target(target=23, direction="r")
            else:
                battle.main.defend()
        if fin_turns >= 3 and kim_turn:
            complete = True

    logger.info("First few turns are complete. Now for the rest of the fight.")
    # After the first two turns, the rest of the fight is pretty much scripted.
    turn_counter = 0
    while not memory.main.battle_complete():
        if memory.main.turn_ready():
            turn_counter += 1
            if screen.turn_kimahri():
                screen.await_turn()
                battle.main.lancet_target(23, "r")
            elif screen.turn_lulu():
                battle.main.thunder_target(23, "r")
            elif screen.turn_tidus():
                if turn_counter < 4:
                    battle.main.defend()
                    memory.main.wait_frames(30 * 0.2)
                else:
                    battle.main.buddy_swap_yuna()
                    battle.main.aeon_summon(0)
            elif screen.turn_aeon():
                battle.overdrive.valefor(sin_fin=1)
                logger.info("Valefor energy blast")
    logger.info("Sin's Fin fight complete")
    xbox.click_to_battle()


@battle.utils.speedup_decorator
def echuilles():
    logger.info("Fight start: Sinspawn Echuilles")
    screen.await_turn()
    logger.info("Sinspawn Echuilles fight start")
    logs.write_rng_track("######################################")
    logs.write_rng_track("Echuilles start")
    logs.write_rng_track(memory.main.rng_10_array(array_len=1))

    tidus_counter = 0
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if screen.faint_check() > 0:
                battle.main.revive()
            elif screen.turn_tidus():
                tidus_counter += 1
                if tidus_counter <= 2:
                    logger.debug("Cheer")
                    battle.main.tidus_flee()  # performs cheer command
                elif (
                    memory.main.get_overdrive_battle(0) == 100
                    and memory.main.get_enemy_current_hp()[0] <= 750
                ):
                    logger.debug("Overdrive")
                    battle.overdrive.tidus()
                else:
                    logger.debug("Tidus attack")
                    battle.main.attack("none")
            elif screen.turn_wakka():
                if tidus_counter == 1:  # and memory.main.rng_seed() != 160:
                    logger.debug("Dark Attack")
                    battle.main.use_skill(0)  # Dark Attack
                # elif memory.main.get_enemy_current_hp()[0] <= 558:
                #    print("Ready for Tidus Overdrive. Wakka defends.")
                #    defend()
                else:
                    logger.debug("Wakka attack")
                    battle.main.attack("none")
    logger.info("Battle is complete. Now awaiting control.")
    while not memory.main.user_control():
        if memory.main.cutscene_skip_possible():
            xbox.skip_scene()
        elif memory.main.menu_open() or memory.main.diag_skip_possible():
            xbox.tap_b()
    logs.write_rng_track("######################################")
    logs.write_rng_track("Echuilles end")
    logs.write_rng_track(memory.main.rng_10_array(array_len=1))


@battle.utils.speedup_decorator
def geneaux():
    logger.info("Fight start: Sinspawn Geneaux")
    xbox.click_to_battle()

    if screen.turn_tidus():
        battle.main.attack("none")
    elif screen.turn_yuna():
        battle.main.buddy_swap_kimahri()
        battle.main.attack("none")
        while not screen.turn_tidus():
            battle.main.defend()
        while screen.turn_tidus():
            battle.main.defend()
        battle.main.buddy_swap_yuna()
    screen.await_turn()
    battle.main.aeon_summon(0)  # Summon Valefor
    screen.await_turn()
    battle.overdrive.valefor()

    while not memory.main.battle_complete():  # AKA end of battle screen
        if memory.main.diag_skip_possible():
            xbox.tap_b()
        elif memory.main.turn_ready():
            logger.debug("Valefor casting Fire")
            battle.main.aeon_spell(0)
        else:
            FFXC.set_neutral()
    logger.info("Battle with Sinspawn Geneaux Complete")
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def oblitzerator(early_haste):
    logger.info("Fight start: Oblitzerator")
    xbox.click_to_battle()
    crane = 0

    if early_haste >= 1:
        # First turn is always Tidus. Haste Lulu if we've got the levels.
        battle.main.tidus_haste(direction="left", character=5)

    while not memory.main.battle_complete():  # AKA end of battle screen
        if memory.main.turn_ready():
            if crane < 3:
                if screen.turn_lulu():
                    crane += 1
                    battle.main.thunder_target(target=21, direction="r")
                else:
                    battle.main.defend()
            elif crane == 3:
                if screen.turn_tidus():
                    crane += 1
                    while memory.main.main_battle_menu():
                        xbox.tap_left()
                    while memory.main.battle_cursor_2() != 1:
                        xbox.tap_down()
                    while memory.main.other_battle_menu():
                        xbox.tap_b()
                    battle.main.tap_targeting()
                elif screen.turn_lulu():
                    battle.main.thunder("none")
                else:
                    battle.main.defend()
            else:
                if screen.turn_lulu():
                    battle.main.thunder("none")
                elif screen.turn_tidus():
                    battle.main.attack_oblitz_end()
                else:
                    battle.main.defend()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    logger.info("End of fight, Oblitzerator")
    memory.main.click_to_control()
    # logs.write_stats("RNG02 after battle:")
    # logs.write_stats(memory.s32(memory.rng02()))


@battle.utils.speedup_decorator
def chocobo_eater():
    logger.info("Fight start: Chocobo Eater")
    rng44Last = memory.main.rng_from_index(44)
    turns = 0
    choco_target = 255
    choco_next = False
    choco_haste = False
    screen.await_turn()
    char_hp_last = memory.main.get_battle_hp()

    # If chocobo doesn't take the second turn, that means it out-sped Tidus.
    if memory.main.get_next_turn() != 20:
        if memory.main.rng_from_index(44) == rng44Last:
            # Eater did not take an attack, but did take first turn. Should register as true.
            choco_next = True
    swapped_yuna = False
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if choco_next:
                choco_next = False
                if memory.main.get_battle_hp() != char_hp_last:  # We took damage
                    pass
                elif memory.main.rng_from_index(44) != rng44Last:
                    # Chocobo eater attacked, covers miss
                    pass
                elif (
                    choco_target == 255
                    and 1 not in memory.main.get_active_battle_formation()
                ):
                    choco_index = memory.main.actor_index(actor_num=4200)
                    logger.debug(f"#####  Chocobo index: {choco_index}")
                    choco_angle = memory.main.get_actor_angle(choco_index)
                    if choco_angle > 0.25:
                        logger.debug(f"#####  Chocobo angle: {choco_angle}")
                        logger.debug("#####  Selecting friendly target 2")
                        choco_target = memory.main.get_active_battle_formation()[0]
                    elif choco_angle < -0.25:
                        logger.debug(f"#####  Chocobo angle: {choco_angle}")
                        logger.debug("#####  Selecting friendly target 0")
                        choco_target = memory.main.get_active_battle_formation()[2]
                    else:
                        logger.debug(
                            f"#####  No Angle, using last hp's: {char_hp_last}"
                        )
                        logger.debug("#####  Selecting friendly target 1")
                        choco_target = memory.main.get_active_battle_formation()[1]
            turns += 1
            if choco_target == memory.main.get_battle_char_turn():
                if 1 not in memory.main.get_active_battle_formation():
                    battle.main.buddy_swap_yuna()
                    battle.main.attack_by_num(1)
                    choco_target = 255
                    swapped_yuna = True
            if memory.main.get_next_turn() == 20:
                choco_next = True
                char_hp_last = memory.main.get_battle_hp()
                rng44Last = memory.main.rng_from_index(44)
            if choco_target != 255:
                logger.debug(f"#####  Target for You're Next attack: {choco_target}")

            # Only if two people are down, very rare but for safety.
            if screen.faint_check() >= 2:
                logger.debug("Attempting revive")
                if screen.turn_kimahri():
                    if 0 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap_tidus()
                    elif 4 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap_wakka()
                    else:
                        battle.main.buddy_swap_auron()
                battle.main.revive()
            # elif 0 not in memory.main.get_active_battle_formation():
            # Doesn't work - it still hits Tidus if he swapped out and back in (instead of Yuna).
            #    buddy_swap_tidus()
            elif (
                swapped_yuna
                and 0 not in memory.main.get_active_battle_formation()
                and memory.main.state_dead(1)
                and not choco_haste
            ):
                battle.main.buddy_swap_tidus()
            elif (
                1 in memory.main.get_active_battle_formation()
                and not choco_haste
                and memory.main.get_battle_char_turn() == 0
            ):
                battle.main.tidus_haste(direction="l", character=20)
                # After Yuna in, haste choco eater.
                choco_haste = True
            else:
                logger.debug("Attempting defend")
                battle.main.defend()
        elif memory.main.diag_skip_possible():
            logger.debug("Skipping dialog")
            xbox.tap_b()
    # logs.write_stats("Chocobo eater turns:")
    # logs.write_stats(str(turns))
    logger.info("Chocobo Eater battle complete.")


@battle.utils.speedup_decorator
def gui():
    logger.info("Fight start: Sinspawn Gui")
    xbox.click_to_battle()
    logger.info("Engaging Gui")
    logger.debug(
        f"##### Expecting crit: {memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)}"
    )
    wakka_turn = False
    yuna_turn = False
    auron_turn = False
    tidus_turn = False
    aeon_turn = False
    kimahri_crit = False

    while not aeon_turn:
        if memory.main.turn_ready():
            if screen.turn_yuna():
                if not yuna_turn:
                    battle.main.buddy_swap_auron()
                    yuna_turn = True
                else:
                    battle.main.aeon_summon(0)
            elif screen.turn_wakka():
                if not wakka_turn:
                    xbox.weap_swap(0)
                    wakka_turn = True
                else:
                    battle.main.buddy_swap_kimahri()
                    logger.debug(
                        f"##### Expecting crit: {memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)}"
                    )
            elif screen.turn_kimahri():
                dmg_before = memory.main.get_enemy_current_hp()[0]
                battle.overdrive.kimahri(2)
                screen.await_turn()
                dmg_after = memory.main.get_enemy_current_hp()[0]
                damage = dmg_before - dmg_after
                logger.debug(f"Kimahri OD damage: {damage}")
                logs.write_stats("gui_crit:")
                if damage > 6000:
                    kimahri_crit = True
                    logs.write_stats("True")
                else:
                    logs.write_stats("False")
            elif screen.turn_tidus():
                if not tidus_turn:
                    battle.main.defend()
                    tidus_turn = True
                elif screen.faint_check() > 0:
                    battle.main.buddy_swap_kimahri()
                else:
                    battle.main.buddy_swap_yuna()
            elif screen.turn_auron():
                if not auron_turn:
                    battle.main.use_skill(0)
                    auron_turn = True
                elif screen.faint_check() > 0:
                    battle.main.buddy_swap_yuna()
                else:
                    battle.main.defend()
            elif screen.turn_aeon():
                battle.overdrive.valefor()
                aeon_turn = True

    screen.await_turn()
    next_hp = memory.main.get_battle_hp()[0]
    last_hp = next_hp
    turn1 = False
    next_turn = 20
    last_turn = 20
    went = False
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready() and memory.main.get_battle_char_turn() == 8:
            next_hp = memory.main.get_battle_hp()[0]
            last_turn = next_turn
            next_turn = memory.main.get_next_turn()
            if went and kimahri_crit:
                battle.main.aeon_spell(1)
            elif memory.main.get_overdrive_battle(8) == 20:
                logger.debug("------Overdriving")
                battle.overdrive.valefor()
                went = True
            elif not turn1:
                turn1 = True
                logger.debug("------Recharge unsuccessful. Attempting recovery.")
                battle.main.aeon_shield()
            elif last_turn == 8:  # Valefor takes two turns in a row
                logger.debug("------Two turns in a row")
                battle.main.aeon_shield()
            elif next_hp > last_hp - 40 and not next_hp == last_hp:
                # Gravity spell was used
                logger.debug("------Gravity was used")
                battle.main.aeon_shield()
            else:
                logger.debug("------Attack was just used. Now boost.")
                battle.main.aeon_boost()
            last_hp = next_hp
        elif memory.main.turn_ready() and memory.main.get_battle_char_turn() == 1:
            logger.warning("Yuna turn, something went wrong.")
        elif memory.main.turn_ready() and memory.main.get_battle_char_turn() == 2:
            logger.warning("Auron turn, something went wrong.")
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
        elif screen.turn_seymour():
            break

    # In between battles
    memory.main.wait_frames(12)
    while not memory.main.turn_ready():
        if (
            memory.main.get_story_progress() >= 865
            and memory.main.cutscene_skip_possible()
        ):
            memory.main.wait_frames(10)
            xbox.skip_scene()
            logger.info("Skipping scene")
        elif memory.main.diag_skip_possible() or memory.main.menu_open():
            xbox.tap_b()

    # Second Gui battle
    seymour_turn = 0
    if (
        memory.main.get_overdrive_battle(8) == 20
        or memory.main.get_overdrive_battle(1) == 100
    ):
        logger.info("Gui2 - with extra Aeon overdrive")
        while memory.main.battle_active():
            if screen.turn_seymour() and seymour_turn < 2:
                battle.main.seymour_spell(target_face=False)
                seymour_turn += 1
            elif screen.turn_yuna() and seymour_turn >= 2:
                logger.debug("Laser Time")
                if memory.main.get_overdrive_battle(1) == 100:
                    while not memory.main.other_battle_menu():
                        xbox.tap_left()
                    while not memory.main.interior_battle_menu():
                        xbox.tap_b()
                    while memory.main.interior_battle_menu():
                        xbox.tap_b()
                else:
                    battle.main.aeon_summon(0)
            elif screen.turn_aeon():
                logger.debug("Firing")
                battle.overdrive.valefor()
            else:
                logger.debug("Defend")
                battle.main.defend()
    else:
        logger.info("Gui2 - standard")
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if screen.turn_seymour():
                    battle.main.seymour_spell(target_face=True)
                else:
                    battle.main.defend()

    while not memory.main.user_control():
        if memory.main.cutscene_skip_possible():
            logger.debug("Intentional delay to get the cutscene skip to work.")
            memory.main.wait_frames(2)
            xbox.skip_scene_spec()
            memory.main.wait_frames(60)
        elif memory.main.diag_skip_possible() or memory.main.menu_open():
            xbox.tap_b()


@battle.utils.speedup_decorator
def extractor():
    logger.info("Fight start: Extractor")
    FFXC.set_neutral()

    screen.await_turn()
    battle.main.tidus_haste("none")

    screen.await_turn()
    battle.main.attack("none")  # Wakka attack

    screen.await_turn()
    battle.main.tidus_haste("l", character=4)

    cheer_count = 0
    while not memory.main.battle_complete():  # AKA end of battle screen
        # First determine if cheers are needed.
        if game_vars.get_l_strike() % 2 == 0 and cheer_count < 4:
            tidus_cheer = True
        elif game_vars.get_l_strike() % 2 == 1 and cheer_count < 1:
            tidus_cheer = True
        else:
            tidus_cheer = False
        # Then do the battle logic.
        if memory.main.special_text_open():
            xbox.tap_b()
        elif memory.main.turn_ready():
            if (
                screen.faint_check() > 0
                and memory.main.get_enemy_current_hp()[0] > 1100
            ):
                battle.main.revive()
            elif screen.turn_tidus():
                print(memory.main.get_actor_coords(3))
                if tidus_cheer:
                    cheer_count += 1
                    battle.main.cheer()
                elif (
                    memory.main.get_enemy_current_hp()[0] < 1400
                    and not screen.faint_check()
                    and memory.main.get_overdrive_battle(4) == 100
                ):
                    battle.main.defend()
                else:
                    battle.main.attack("none")
            else:
                if (
                    memory.main.get_enemy_current_hp()[0] < 1900
                    and memory.main.get_overdrive_battle(4) == 100
                ):
                    battle.overdrive.wakka()
                else:
                    battle.main.attack("none")
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    memory.main.click_to_control()


# Process written by CrimsonInferno
@battle.utils.speedup_decorator
def spherimorph():
    logger.info("Fight start: Spherimorph")
    xbox.click_to_battle()

    FFXC.set_neutral()

    spell_num = 0
    tidus_turns = 0
    rikkuturns = 0
    yuna_turn = False
    kim_turn = False
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if game_vars.use_pause():
                memory.main.wait_frames(2)
            turnchar = memory.main.get_battle_char_turn()
            party_hp = memory.main.get_battle_hp()
            if turnchar == 0:
                if tidus_turns == 0:
                    battle.main.equip_in_battle(equip_type="armor", ability_num=0x8028)
                elif tidus_turns == 1:
                    battle.main.defend()
                else:
                    battle.main.buddy_swap_rikku()
                tidus_turns += 1
            elif turnchar == 1:
                rikkuslotnum = memory.main.get_battle_char_slot(6)
                if rikkuslotnum < 3 and party_hp[rikkuslotnum] == 0:
                    battle.main.revive()
                    yuna_turn = True
                elif not yuna_turn:
                    battle.main.defend()
                    yuna_turn = True
                elif not battle.main.spheri_spell_item_ready():
                    if 5 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap_lulu()
                    elif 6 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap_rikku()
                    else:
                        battle.main.defend()
                elif 6 not in memory.main.get_active_battle_formation():
                    battle.main.buddy_swap_rikku()
                else:
                    battle.main.defend()
                    yuna_turn = True
            elif turnchar == 3:
                rikkuslotnum = memory.main.get_battle_char_slot(6)
                if rikkuslotnum < 3 and party_hp[rikkuslotnum] == 0:
                    battle.main.revive()
                    kim_turn = True
                elif not kim_turn:
                    logger.debug(
                        f"RNG11 before Spherimorph: {memory.main.rng_array_from_index(index=11, array_len=30)}"
                    )
                    logs.write_rng_track("RNG11 before Spherimorph")
                    logs.write_rng_track(
                        memory.main.rng_array_from_index(index=11, array_len=30)
                    )
                    # if memory.main.next_steal_rare(pre_advance=6):
                    # One each for Spherimorph, Negator, Crawler, and guados.
                    # Except we haven't learned Steal yet. That's no good.
                    #    _steal()
                    # else:
                    battle.main.defend()
                    kim_turn = True
                elif 6 not in memory.main.get_active_battle_formation():
                    battle.main.buddy_swap_rikku()
                elif 5 not in memory.main.get_active_battle_formation():
                    battle.main.buddy_swap_lulu()
                else:
                    battle.main.defend()
            elif turnchar == 5:
                if not battle.main.spheri_spell_item_ready():
                    if spell_num == 1:
                        battle.main.ice()
                    elif spell_num == 2:
                        battle.main.water()
                    elif spell_num == 3:
                        battle.main.thunder()
                    else:
                        battle.main.fire()
                    screen.await_turn()
                    if memory.main.get_char_weakness(20) == 1:
                        spell_num = 4  # Ice
                    elif memory.main.get_char_weakness(20) == 2:
                        spell_num = 1  # Fire
                    elif memory.main.get_char_weakness(20) == 4:
                        spell_num = 3  # Water
                    elif memory.main.get_char_weakness(20) == 8:
                        spell_num = 2  # Thunder
                elif 6 not in memory.main.get_active_battle_formation():
                    battle.main.buddy_swap_rikku()
                else:
                    battle.main.defend()
            elif turnchar == 6:
                mix_dmg_rolls = sum(memory.main.rikku_mix_damage())
                logger.debug(f"Mix will do {mix_dmg_rolls} damage.")
                if mix_dmg_rolls < memory.main.get_enemy_current_hp()[0]:
                    logger.debug("Throwing Grenade because of damage rolls")
                    grenadeslotnum = memory.main.get_use_items_slot(35)
                    battle.main.use_item(grenadeslotnum, "none")
                elif not battle.main.spheri_spell_item_ready():
                    if 5 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap_lulu()
                    else:
                        battle.main.defend()
                elif yunaTurn and kimTurn:
                    logger.debug("Starting Rikkus overdrive")
                    logger.debug("Full Damage Values:")
                    logger.debug(memory.main.rikku_mix_damage())
                    if spellNum == 1:
                        logger.debug("Creating Ice")
                        battle.main.rikku_full_od("spherimorph1")
                    elif spellNum == 2:
                        logger.debug("Creating Water")
                        battle.main.rikku_full_od("spherimorph2")
                    elif spellNum == 3:
                        logger.debug("Creating Thunder")
                        battle.main.rikku_full_od("spherimorph3")
                    elif spellNum == 4:
                        logger.debug("Creating Fire")
                        battle.main.rikku_full_od("spherimorph4")
                else:
                    battle.main.defend()

    if not game_vars.csr():
        xbox.skip_dialog(5)


@battle.utils.speedup_decorator
def crawler():
    logger.info("Starting battle with Crawler")
    xbox.click_to_battle()

    if memory.main.next_steal_rare(pre_advance=5):
        # One each for two Negators, Crawler, and guados.
        battle.main.negator_with_steal()
    else:
        tidus_turns = 0
        rikkuturns = 0
        kimahriturns = 0
        luluturns = 0
        yunaturns = 0

        while not memory.main.turn_ready():
            pass
        while memory.main.battle_active():  # AKA end of battle screen
            FFXC.set_neutral()
            if memory.main.turn_ready():
                turnchar = memory.main.get_battle_char_turn()
                if turnchar == 0:
                    if tidus_turns == 0:
                        logger.debug("Swapping Tidus for Rikku")
                        battle.main.buddy_swap_rikku()
                    else:
                        battle.main.defend()
                    tidus_turns += 1
                elif turnchar == 6:
                    if luluturns < 2:
                        logger.debug("Using Lightning Marble")
                        lightningmarbleslot = memory.main.get_use_items_slot(30)
                        if rikkuturns < 1:
                            battle.main.use_item(lightningmarbleslot, target=21)
                        else:
                            battle.main.use_item(lightningmarbleslot, target=21)
                    else:
                        logger.debug("Starting Rikkus overdrive")
                        battle.main.rikku_full_od("crawler")
                    rikkuturns += 1
                elif turnchar == 3:
                    if kimahriturns == 0:
                        lightningmarbleslot = memory.main.get_use_items_slot(30)
                        battle.main.use_item(lightningmarbleslot, target=21)
                    else:
                        battle.main.buddy_swap_yuna()
                    kimahriturns += 1
                elif turnchar == 5:
                    battle.main.revive()
                    luluturns += 1
                elif turnchar == 1:
                    if yunaturns == 0:
                        battle.main.defend()
                    else:
                        battle.main.buddy_swap_tidus()
                    yunaturns += 1
                else:
                    battle.main.defend()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()

    memory.main.click_to_control()


@battle.utils.speedup_decorator
def wendigo():
    logger.info("Starting battle with Wendigo")

    phase = 0
    yuna_ap = False
    guadosteal = False
    powerbreak = False
    powerbreakused = False
    usepowerbreak = False
    tidushealself = False
    tidus_max_hp = 1520
    tidushaste = False

    screen.await_turn()

    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            party_hp = memory.main.get_battle_hp()
            turnchar = memory.main.get_battle_char_turn()
            tidus_slot = memory.main.get_battle_char_slot(0)

            if party_hp[memory.main.get_battle_char_slot(0)] == 0:
                logger.debug("Tidus is dead")
                tidushaste = False
                powerbreak = True
                usepowerbreak = powerbreak and not powerbreakused

            if turnchar == 1:
                logger.debug("Yunas Turn")
                # If Yuna still needs AP:
                if not yuna_ap:
                    logger.debug("Yuna still needs AP")
                    # If both other characters are dead Mega-Phoenix if available, otherwise PD
                    if (
                        battle.main.wendigo_res_heal(
                            turnchar=turnchar,
                            use_power_break=usepowerbreak,
                            tidus_max_hp=tidus_max_hp,
                        )
                        == 0
                    ):
                        xbox.weap_swap(0)
                    yuna_ap = True
                # If Yuna has had a turn swap for Lulu
                else:
                    if 5 not in memory.main.get_active_battle_formation():
                        logger.debug("Swapping to Lulu")
                        battle.main.buddy_swap_lulu()
                    elif 6 not in memory.main.get_active_battle_formation():
                        battle.main.buddy_swap_rikku()
                    else:
                        xbox.weap_swap(0)
            elif turnchar == 0:
                if not tidushaste:
                    logger.debug("Tidus Haste self")
                    battle.main.tidus_haste("none")
                    tidushaste = True
                elif phase == 0:
                    logger.debug("Switch to Brotherhood")
                    battle.main.equip_in_battle(special="brotherhood")
                    phase += 1
                elif phase == 1:
                    logger.debug("Attack top Guado")
                    battle.main.attack_by_num(22, "d")
                    phase += 1
                elif (
                    memory.main.get_enemy_current_hp()[1] != 0
                    and screen.faint_check() == 2
                ):
                    logger.debug("2 Characters are dead")
                    tidushealself = True
                    if memory.main.get_throw_items_slot(7) < 255:
                        battle.main.revive_all()
                    elif memory.main.get_throw_items_slot(6) < 255:
                        battle.main.revive()
                elif (
                    memory.main.get_enemy_current_hp()[1] < 6000
                    and memory.main.get_overdrive_battle(0) == 100
                    and not game_vars.skip_kilika_luck()
                ):
                    battle.overdrive.tidus("left", character=21)
                elif tidushealself:
                    if party_hp[memory.main.get_battle_char_slot(0)] < tidus_max_hp:
                        logger.debug(
                            "Tidus just used Phoenix Down / Mega Phoenix so needs to heal himself"
                        )
                        if battle.main.fullheal(target=0, direction="l") == 0:
                            if screen.faint_check():
                                logger.debug(
                                    "No healing items so revive someone instead"
                                )
                                battle.main.revive()
                            else:
                                logger.debug("No healing items so just go face")
                                battle.main.attack_by_num(21, "l")
                    else:
                        logger.debug("No need to heal. Ver 1")
                        battle.main.attack_by_num(21, "l")
                    tidushealself = False
                else:
                    logger.debug("No need to heal. Ver 2")
                    battle.main.attack_by_num(21, "l")
                memory.main.wait_frames(30 * 0.2)
            elif turnchar == 6:
                if phase == 2:
                    phase += 1
                    lightcurtainslot = memory.main.get_use_items_slot(57)
                    if lightcurtainslot < 255:
                        logger.debug("Using Light Curtain on Tidus")
                        battle.main.use_item(lightcurtainslot, target=0)
                    else:
                        logger.debug("No Light Curtain")
                        logger.debug("Swapping to Auron to Power Break")
                        battle.main.buddy_swap_auron()  # Swap for Auron
                        powerbreak = True
                        usepowerbreak = True
                # elif memory.main.get_enemy_current_hp()[1] < stop_healing:
                #    defend()
                elif (
                    battle.main.wendigo_res_heal(
                        turnchar=turnchar,
                        use_power_break=usepowerbreak,
                        tidus_max_hp=tidus_max_hp,
                    )
                    == 0
                ):
                    if (
                        not guadosteal
                        and memory.main.get_enemy_current_hp().count(0) != 2
                    ):
                        battle.main.steal()
                        guadosteal = True
                    # elif memory.main.get_enemy_current_hp().count(0) == 2 and not 5 in memory.main.get_active_battle_formation():
                    #    buddy_swap_lulu()
                    else:
                        battle.main.defend()
            elif turnchar == 2:
                if usepowerbreak:
                    logger.debug("Using Power Break")
                    battle.main.use_skill(position=0, target=21)
                    powerbreakused = True
                    usepowerbreak = False
                # elif memory.main.get_enemy_current_hp()[1] < stop_healing and memory.main.get_battle_hp()[tidus_slot] != 0:
                #    defend()
                elif (
                    battle.main.wendigo_res_heal(
                        turnchar=turnchar,
                        use_power_break=usepowerbreak,
                        tidus_max_hp=tidus_max_hp,
                    )
                    == 0
                ):
                    battle.main.buddy_swap_kimahri()
            elif turnchar == 5:
                if (
                    battle.main.wendigo_res_heal(
                        turnchar=turnchar,
                        use_power_break=usepowerbreak,
                        tidus_max_hp=tidus_max_hp,
                    )
                    == 0
                ):
                    xbox.weap_swap(0)
            else:
                if (
                    usepowerbreak
                    and not powerbreakused
                    and 2 not in memory.main.get_active_battle_formation()
                ):
                    logger.debug("Swapping to Auron to Power Break")
                    battle.main.buddy_swap_auron()
                # if memory.main.get_enemy_current_hp()[1] < stop_healing and memory.main.get_battle_hp()[tidus_slot] != 0:
                #    logger.debug("End of battle, no need to heal.")
                #    defend()
                elif (
                    memory.main.get_enemy_current_hp()[1] != 0
                    and memory.main.get_battle_hp()[tidus_slot] != 0
                ):
                    if (
                        battle.main.wendigo_res_heal(
                            turnchar=turnchar,
                            use_power_break=usepowerbreak,
                            tidus_max_hp=tidus_max_hp,
                        )
                        == 0
                    ):
                        battle.main.defend()
                else:
                    battle.main.defend()


# Process written by CrimsonInferno
@battle.utils.speedup_decorator
def evrae():
    logger.info("Starting battle: Evrae")
    tidus_prep = 0
    tidus_attacks = 0
    rikku_turns = 0
    kimahri_turns = 0
    lunar_curtain = False
    if memory.main.rng_seed() == 31:
        steal_count = 2
    else:
        steal_count = 0
    FFXC.set_neutral()
    # This gets us past the tutorial and all the dialog.
    xbox.click_to_battle()

    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            turnchar = memory.main.get_battle_char_turn()
            logger.debug(f"Tidus prep turns: {tidus_prep}")
            if turnchar == 0:
                logger.debug("Registering Tidus' turn")
                if game_vars.skip_kilika_luck():
                    if tidus_prep == 0:
                        tidus_prep = 1
                        battle.main.tidus_haste("none")
                    elif tidus_prep in [1, 2]:
                        tidus_prep += 1
                        battle.main.cheer()
                    elif (
                        tidus_attacks == 4
                        or memory.main.get_enemy_current_hp()[0] <= 9999
                    ):
                        tidus_attacks += 1
                        battle.overdrive.tidus()
                    else:
                        tidus_attacks += 1
                        battle.main.attack("none")
                elif game_vars.get_blitz_win():  # Blitz win logic
                    if tidus_prep == 0:
                        tidus_prep = 1
                        battle.main.tidus_haste("none")
                    elif tidus_prep == 1:
                        tidus_prep += 1
                        battle.main.cheer()
                    elif tidus_prep == 2 and rikku_turns == 0:
                        tidus_prep += 1
                        battle.main.equip_in_battle(
                            equip_type="armor", ability_num=0x8028
                        )
                    elif tidus_prep == 2 and tidus_attacks == 2:
                        tidus_prep += 1
                        battle.main.cheer()
                    else:
                        tidus_attacks += 1
                        battle.main.attack("none")
                else:  # Blitz loss logic
                    if tidus_prep == 0:
                        tidus_prep = 1
                        battle.main.tidus_haste("none")
                    elif tidus_prep <= 2:
                        tidus_prep += 1
                        battle.main.cheer()
                    elif tidus_prep == 3:
                        logger.debug("Equip Baroque Sword.")
                        battle.main.equip_in_battle(special="baroque")
                        tidus_prep += 1
                    elif tidus_attacks == 4 and game_vars.skip_kilika_luck():
                        tidus_attacks += 1
                        battle.overdrive.tidus()
                    else:
                        tidus_attacks += 1
                        battle.main.attack("none")
            elif turnchar == 6:
                logger.debug("Registering Rikkus turn")
                if rikku_turns == 0:
                    rikku_turns += 1
                    logger.debug("Rikku overdrive")
                    battle.main.rikku_full_od("Evrae")
                elif not game_vars.get_blitz_win() and not lunar_curtain:
                    logger.debug("Use Lunar Curtain")
                    lunar_slot = memory.main.get_use_items_slot(56)
                    battle.main.use_item(lunar_slot, direction="l", target=0)
                    lunar_curtain = True
                elif memory.main.get_battle_hp()[
                    memory.main.get_battle_char_slot(0)
                ] < 1520 and (tidus_attacks < 3 or not game_vars.get_blitz_win()):
                    logger.debug("Rikku should attempt to heal a character.")
                    kimahri_turns += 1
                    if battle.main.fullheal(target=0, direction="d") == 0:
                        logger.debug("Restorative item not found.")
                        battle.main.use_item(memory.main.get_use_items_slot(20))
                    else:
                        logger.debug("Heal should be successful.")
                elif game_vars.skip_kilika_luck():
                    if memory.main.get_use_items_slot(32) != 255:
                        throw_slot = memory.main.get_use_items_slot(32)
                    elif memory.main.get_use_items_slot(24) != 255:
                        throw_slot = memory.main.get_use_items_slot(24)
                    elif memory.main.get_use_items_slot(27) != 255:
                        throw_slot = memory.main.get_use_items_slot(27)
                    else:
                        throw_slot = memory.main.get_use_items_slot(30)
                    if throw_slot == 255:
                        battle.main.steal()
                    else:
                        battle.main.use_item(throw_slot)
                else:
                    battle.main.steal()
                    steal_count += 1
            elif turnchar == 3:
                logger.debug("Registering Kimahri's turn")
                if not game_vars.get_blitz_win() and not lunar_curtain:
                    logger.debug("Use Lunar Curtain")
                    lunar_slot = memory.main.get_use_items_slot(56)
                    battle.main.use_item(lunar_slot, direction="l", target=0)
                    lunar_curtain = True
                elif memory.main.get_battle_hp()[
                    memory.main.get_battle_char_slot(0)
                ] < 1520 and (tidus_attacks < 3 or not game_vars.get_blitz_win()):
                    logger.debug("Kimahri should attempt to heal a character.")
                    kimahri_turns += 1
                    if battle.main.fullheal(target=0, direction="u") == 0:
                        logger.debug("Restorative item not found.")
                        battle.main.use_item(memory.main.get_use_items_slot(20))
                    else:
                        logger.debug("Heal should be successful.")
                elif game_vars.skip_kilika_luck():
                    if memory.main.get_use_items_slot(32) != 255:
                        throw_slot = memory.main.get_use_items_slot(32)
                    elif memory.main.get_use_items_slot(24) != 255:
                        throw_slot = memory.main.get_use_items_slot(24)
                    elif memory.main.get_use_items_slot(27) != 255:
                        throw_slot = memory.main.get_use_items_slot(27)
                    else:
                        throw_slot = memory.main.get_use_items_slot(30)
                    if throw_slot == 255:
                        battle.main.steal()
                    else:
                        battle.main.use_item(throw_slot)
                else:
                    battle.main.steal()
                    steal_count += 1
        elif memory.main.diag_skip_possible():
            xbox.tap_b()

    if not game_vars.csr():
        while not memory.main.cutscene_skip_possible():
            if memory.main.menu_open():
                xbox.tap_b()
        xbox.skip_scene_spec()


@battle.utils.speedup_decorator
def isaaru():
    xbox.click_to_battle()
    if memory.main.get_encounter_id() < 258:
        game_vars.add_rescue_count()

    logger.info("Starting battle: Isaaru")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if screen.turn_yuna():
                if memory.main.get_encounter_id() in [257, 260]:
                    battle.main.aeon_summon(2)  # Summon Ixion for Bahamut
                else:
                    battle.main.aeon_summon(4)  # Summon Bahamut for other aeons
            else:
                battle.main.attack("none")  # Aeon turn
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(30 * 2.8)
    FFXC.set_value("btn_b", 0)


@battle.utils.speedup_decorator
def evrae_altana():
    xbox.click_to_battle()
    if memory.main.get_encounter_id() != 266:
        logger.info("Not Evrae this time.")
        battle.main.flee_all()
    else:
        logger.info("Evrae Altana fight start")
        if memory.main.next_steal_rare():
            battle.main.evrae_altana_steal()
        else:
            logger.debug("===================================")
            logger.debug("Next steal will crit, do not steal.")
            logger.debug("===================================")
        thrown_item = False
        while memory.main.battle_active():  # AKA end of battle screen
            if memory.main.turn_ready():
                if memory.main.get_item_slot(18) != 255 and not thrown_item:
                    battle.main._use_healing_item(item_id=18)
                    thrown_item = True
                elif memory.main.get_item_slot(16) != 255 and not thrown_item:
                    battle.main._use_healing_item(item_id=16)
                    thrown_item = True
                else:
                    battle.main.altana_heal()

    memory.main.click_to_control()


@battle.utils.speedup_decorator
def seymour_natus():
    aeon_summoned = False
    while not memory.main.user_control():
        if memory.main.get_encounter_id() == 272:  # Seymour Natus
            logger.info("Seymour Natus engaged")
            while not memory.main.battle_complete():
                if memory.main.turn_ready():
                    if screen.turn_tidus():
                        if memory.main.get_lulu_slvl() < 35 or game_vars.nemesis():
                            battle.main.buddy_swap_lulu()
                            screen.await_turn()
                            xbox.weap_swap(0)
                        elif aeon_summoned:
                            battle.main.tidus_haste("d", character=1)
                        else:
                            battle.main.attack("none")
                    elif screen.turn_lulu():
                        battle.main.buddy_swap_tidus()
                        screen.await_turn()
                        xbox.tap_up()
                        battle.main.attack("none")
                    elif screen.turn_yuna():
                        if not aeon_summoned:
                            battle.main.aeon_summon(4)
                            aeon_summoned = True
                        else:
                            battle.main.aeon_summon(2)
                    elif screen.turn_aeon():
                        xbox.skip_dialog(3)  # Finishes the fight.
                    else:
                        battle.main.defend()
            return 1
        elif memory.main.get_encounter_id() == 270:  # YAT-63 x2
            while memory.main.battle_active():
                if game_vars.completed_rescue_fights():
                    battle.main.flee_all()
                elif memory.main.turn_ready():
                    if screen.turn_tidus() or screen.turn_yuna():
                        if memory.main.get_enemy_current_hp().count(0) == 1:
                            battle.main.flee_all()
                            game_vars.add_rescue_count()
                        else:
                            battle.main.attack_by_num(22, "r")
                    else:
                        battle.main.defend()
        elif memory.main.get_encounter_id() == 269:  # YAT-63 with two guard guys
            while memory.main.battle_active():
                if game_vars.completed_rescue_fights():
                    battle.main.flee_all()
                elif memory.main.turn_ready():
                    if screen.turn_tidus() or screen.turn_yuna():
                        if memory.main.get_enemy_current_hp().count(0) == 1:
                            battle.main.flee_all()
                            game_vars.add_rescue_count()
                        else:
                            battle.main.attack("none")
                    else:
                        battle.main.defend()
        elif memory.main.get_encounter_id() == 271:  # one YAT-63, two YAT-99
            while memory.main.battle_active():
                if game_vars.completed_rescue_fights():
                    battle.main.flee_all()
                elif memory.main.turn_ready():
                    if screen.turn_tidus() or screen.turn_yuna():
                        if memory.main.get_enemy_current_hp().count(0) == 1:
                            battle.main.flee_all()
                            game_vars.add_rescue_count()
                        else:
                            battle.main.attack_by_num(21, "l")
                    else:
                        battle.main.defend()
        if memory.main.menu_open() or memory.main.diag_skip_possible():
            xbox.tap_b()
    return 0


@battle.utils.speedup_decorator
def biran_yenke():
    logger.info("Starting battle with Biran & Yenke")
    xbox.click_to_battle()
    battle.main.steal()

    # Nemesis logic
    if game_vars.nemesis():
        screen.await_turn()
        battle.main.steal_right()

    screen.await_turn()
    gem_slot = memory.main.get_use_items_slot(34)
    if gem_slot == 255:
        gem_slot = memory.main.get_use_items_slot(28)
    battle.main.use_item(gem_slot, "none")

    xbox.click_to_battle()
    gem_slot = memory.main.get_use_items_slot(34)
    if gem_slot == 255:
        gem_slot = memory.main.get_use_items_slot(28)
    battle.main.use_item(gem_slot, "none")

    while not memory.main.user_control():
        xbox.tap_b()

    ret_slot = memory.main.get_item_slot(96)  # Return sphere
    friend_slot = memory.main.get_item_slot(97)  # Friend sphere

    if friend_slot == 255:  # Four return sphere method.
        logger.debug("Double return sphere drops.")
        end_game_version = 4
    elif ret_slot == 255:
        logger.warning("Double friend sphere, effective game over. :( ")
        end_game_version = 3
    else:
        logger.debug("Split items between friend and return spheres.")
        end_game_version = 1

    game_vars.end_game_version_set(end_game_version)


@battle.utils.speedup_decorator
def seymour_flux():
    stage = 1
    logger.info("Start: Seymour Flux battle")
    bahamut_crit = memory.main.next_crit(character=7, char_luck=17, enemy_luck=15)
    logger.debug(f"Next Aeon Crit: {bahamut_crit}")
    yuna_xp = memory.main.get_slvl_yuna()
    xbox.click_to_battle()
    if bahamut_crit == 2:
        while not memory.main.battle_complete():
            if memory.main.turn_ready():
                if screen.turn_aeon():
                    battle.main.attack("none")
                elif screen.turn_yuna():
                    battle.main.aeon_summon(4)
                else:
                    battle.main.defend()
    elif game_vars.end_game_version() == 3:
        bahamut_summoned = False
        while not memory.main.battle_complete():  # AKA end of battle screen
            if memory.main.turn_ready():
                if screen.turn_tidus():
                    battle.main.buddy_swap_yuna()
                elif screen.turn_yuna():
                    if not bahamut_summoned:
                        battle.main.aeon_summon(4)
                        bahamut_summoned = True
                    else:
                        battle.main.attack("none")
                elif screen.turn_aeon():
                    if game_vars.get_blitz_win():
                        battle.main.attack("none")
                    else:
                        battle.main.impulse()
                elif screen.faint_check() >= 1:
                    battle.main.revive()
                else:
                    battle.main.defend()
    else:
        while not memory.main.battle_complete():  # AKA end of battle screen
            if memory.main.turn_ready():
                last_hp = memory.main.get_enemy_current_hp()[0]
                logger.debug("Last HP")
                if screen.turn_yuna():
                    logger.debug(f"Yunas turn. Stage: {stage}")
                    if stage == 1:
                        battle.main.attack("none")
                        stage += 1
                    elif stage == 2:
                        battle.main.aeon_summon(4)
                        battle.main.attack("none")
                        stage += 1
                    else:
                        battle.main.attack("none")
                elif screen.turn_tidus():
                    logger.debug(f"Tidus' turn. Stage: {stage}")
                    if stage < 3:
                        battle.main.tidus_haste("down", character=1)
                    elif last_hp > 3500:
                        battle.main.attack("none")
                    else:
                        battle.main.defend()
                elif screen.turn_auron():
                    logger.debug("Auron's turn. Swap for Rikku and overdrive.")
                    battle.main.buddy_swap_rikku()
                    logger.debug("Rikku overdrive")
                    battle.main.rikku_full_od("Flux")
                else:
                    logger.debug("Non-critical turn. Defending.")
                    battle.main.defend()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
    memory.main.click_to_control()
    if memory.main.get_slvl_yuna() - yuna_xp == 15000:
        game_vars.flux_overkill_success()
    logger.info("-----------------------------")
    logger.info(f"Flux Overkill: {game_vars.flux_overkill()}")
    logger.info("Seymour Flux battle complete.")
    logger.info("-----------------------------")
    # time.sleep(60) #Testing only


def s_keeper_bahamut_crit() -> int:
    bahamut_crit = memory.main.next_crit(character=7, char_luck=17, enemy_luck=15)
    logger.debug(f"Next Aeon Crit: {bahamut_crit}")
    return bahamut_crit


@battle.utils.speedup_decorator
def s_keeper():
    xbox.click_to_battle()
    logger.info("Start of Sanctuary Keeper fight")
    s_keeper_bahamut_crit()
    xbox.click_to_battle()
    bahamut_crit = s_keeper_bahamut_crit()
    if bahamut_crit == 2 or bahamut_crit == 7:
        while not memory.main.battle_complete():
            if memory.main.turn_ready():
                s_keeper_bahamut_crit()
                if screen.turn_aeon():
                    battle.main.attack("none")
                elif screen.turn_yuna():
                    battle.main.aeon_summon(4)
                else:
                    battle.main.defend()
    elif game_vars.end_game_version() == 3 and game_vars.get_blitz_win():
        while not memory.main.battle_complete():
            if memory.main.turn_ready():
                s_keeper_bahamut_crit()
                if screen.turn_yuna():
                    battle.main.aeon_summon(4)
                elif screen.turn_aeon():
                    battle.main.attack("none")
                else:
                    battle.main.defend()
    else:
        armor_break = False
        while not memory.main.battle_complete():
            if memory.main.turn_ready():
                s_keeper_bahamut_crit()
                if screen.turn_tidus():
                    battle.main.use_skill(0)
                    armor_break = True
                elif screen.turn_yuna():
                    if armor_break:
                        battle.main.aeon_summon(4)
                    else:
                        battle.main.defend()
                elif screen.turn_aeon():
                    battle.main.attack("none")
                else:
                    battle.main.defend()
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def omnis():
    logger.info("Fight start: Seymour Omnis")
    xbox.click_to_battle()
    battle.main.defend()  # Yuna defends
    rikku_in = False
    backup_cure = False

    while memory.main.get_enemy_max_hp()[0] == memory.main.get_enemy_current_hp()[0]:
        if memory.main.turn_ready():
            if screen.turn_tidus():
                battle.main.use_skill(0)
            elif screen.turn_auron():
                battle.main.buddy_swap_rikku()
                battle.main.rikku_full_od(battle="omnis")
                rikku_in = True
            elif screen.turn_yuna() and rikku_in:
                if not backup_cure:
                    battle.main.yuna_cure_omnis()
                    backup_cure = True
                else:
                    battle.main.equip_in_battle(
                        equip_type="weap", ability_num=0x8001, character=1
                    )
            else:
                battle.main.defend()

    logger.debug("Ready for aeon.")
    while not memory.main.battle_complete():  # AKA end of battle screen
        if memory.main.turn_ready():
            logger.debug(f"Character turn: {memory.main.get_battle_char_turn()}")
            if screen.turn_yuna():
                battle.main.aeon_summon(4)
            elif screen.turn_aeon():
                battle.main.attack("none")
            elif screen.turn_tidus():
                battle.main.attack("none")
            else:
                battle.main.defend()
        elif memory.main.diag_skip_possible():
            logger.debug("Skipping dialog maybe?")
            xbox.tap_b()
    logger.debug("Should be done now.")
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def bfa():
    if memory.main.get_gil_value() < 150000:
        swag_mode = True
    else:
        swag_mode = game_vars.yu_yevon_swag()
    FFXC.set_movement(1, 0)
    memory.main.wait_frames(30 * 0.4)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_neutral()

    xbox.click_to_battle()
    battle.main.buddy_swap_rikku()
    if memory.main.overdrive_state()[6] == 100:
        battle.main.rikku_full_od("bfa")
    else:
        battle.main.use_skill(0)

    screen.await_turn()
    while memory.main.main_battle_menu():
        xbox.tap_left()
    while memory.main.battle_cursor_2() != 1:
        xbox.tap_down()
    while memory.main.other_battle_menu():
        xbox.tap_b()
    battle.main.tap_targeting()
    battle.main.buddy_swap_yuna()
    battle.main.aeon_summon(4)

    # Bahamut finishes the battle.
    while memory.main.battle_active():
        xbox.tap_b()

    # Skip the cutscene
    logger.info("BFA down. Ready for Aeons")

    if not game_vars.csr():
        while not memory.main.cutscene_skip_possible():
            xbox.tap_b()
        xbox.skip_scene()

    while memory.main.get_story_progress() < 3380:
        if memory.main.turn_ready():
            encounter_id = memory.main.get_encounter_id()
            logger.info(f"Battle engaged. Battle number: {encounter_id}")
            if screen.turn_yuna():
                if memory.main.battle_menu_cursor() != 20:
                    while memory.main.battle_menu_cursor() != 20:
                        if memory.main.battle_menu_cursor() in [22, 1]:
                            xbox.tap_up()
                        else:
                            xbox.tap_down()
                while memory.main.main_battle_menu():
                    xbox.tap_b()
                while memory.main.other_battle_menu():
                    xbox.tap_b()
                logger.info(f"Enemy max hp: {memory.main.get_enemy_max_hp()}")
                aeon_hp = memory.main.get_enemy_max_hp()[0]
                if swag_mode or aeon_hp % 1000 == 0:
                    use_gil = aeon_hp * 10
                else:
                    use_gil = (int(aeon_hp / 1000) + 1) * 10000
                logger.info(f"#### USING GIL #### {use_gil}")
                battle.main.calculate_spare_change_movement(use_gil)
                while memory.main.spare_change_open():
                    xbox.tap_b()
                while not memory.main.main_battle_menu():
                    xbox.tap_b()
            else:
                battle.main.defend()
        elif not memory.main.battle_active():
            xbox.tap_b()


@battle.utils.speedup_decorator
def yu_yevon():
    logger.info("Ready for Yu Yevon.")
    screen.await_turn()  # No need for skipping dialog
    logger.info("Awww such a sad final boss!")
    zombie_attack = False
    za_char = game_vars.zombie_weapon()
    weap_swap = False
    while memory.main.get_story_progress() < 3400:
        if memory.main.turn_ready():
            logger.debug("-----------------------")
            logger.debug("-----------------------")
            logger.debug(f"za_char: {za_char}")
            logger.debug(f"zombie_attack: {zombie_attack}")
            logger.debug(f"weap_swap: {weap_swap}")
            logger.debug("-----------------------")
            logger.debug("-----------------------")
            if za_char == 1 and not zombie_attack:  # Yuna logic
                if not weap_swap and screen.turn_yuna():
                    battle.main.equip_in_battle(
                        equip_type="weap", ability_num=0x8032, character=1
                    )
                    weap_swap = True
                elif screen.turn_yuna():
                    battle.main.attack("none")
                    zombie_attack = True
                elif weap_swap and not zombie_attack and screen.turn_tidus():
                    xbox.weap_swap(0)
                else:
                    battle.main.defend()
            elif za_char == 0 and not zombie_attack:  # Tidus logic:
                if screen.turn_yuna():
                    battle.main.defend()
                elif screen.turn_tidus() and not weap_swap:
                    battle.main.equip_in_battle(
                        equip_type="weap", ability_num=0x8032, character=0
                    )
                    weap_swap = True
                elif screen.turn_tidus():
                    battle.main.attack("none")
                    zombie_attack = True
                else:
                    battle.main.defend()
            elif za_char == 2 and not zombie_attack:  # Auron logic:
                if screen.turn_yuna():
                    battle.main.buddy_swap_auron()
                elif screen.turn_auron() and not weap_swap:
                    battle.main.equip_in_battle(
                        equip_type="weap", ability_num=0x8032, character=2
                    )
                    weap_swap = True
                elif screen.turn_auron():
                    battle.main.attack("none")
                    zombie_attack = True
                else:
                    battle.main.defend()
            elif za_char == 6 and not zombie_attack:  # Rikku logic:
                if screen.turn_yuna() and not weap_swap:
                    # Piggy back off the weap_swap function
                    battle.main.defend()
                    weap_swap = True
                elif screen.turn_yuna():
                    xbox.weap_swap(0)
                elif screen.turn_tidus():
                    battle.main.tidus_haste("r", character=6)
                elif screen.turn_rikku():
                    battle.main.attack("none")
                    zombie_attack = True
                else:
                    battle.main.defend()
            elif zombie_attack:  # Throw P.down to end game
                item_num = battle.main.yu_yevon_item()
                if item_num == 99:
                    battle.main.attack("none")
                else:
                    while memory.main.battle_menu_cursor() != 1:
                        xbox.tap_down()
                    while memory.main.main_battle_menu():
                        xbox.tap_b()
                    item_pos = memory.main.get_throw_items_slot(item_num)
                    battle.main._navigate_to_position(item_pos)
                    while memory.main.other_battle_menu():
                        xbox.tap_b()
                    while not memory.main.enemy_targetted():
                        xbox.tap_up()
                    battle.main.tap_targeting()
                logger.info("Phoenix Down on Yu Yevon. Good game.")
            elif screen.turn_tidus() and za_char == 255:
                # Tidus to use Zombie Strike ability
                battle.main.use_skill(0)
                zombie_attack = True
            elif za_char == 255 and not screen.turn_tidus():
                # Non-Tidus char to defend so Tidus can use Zombie Strike ability
                battle.main.defend()
            else:
                if memory.main.get_battle_char_turn() == za_char:
                    battle.main.attack("none")
                    zombie_attack = True
                elif memory.main.get_battle_char_slot(za_char) >= 3:
                    battle.main.buddy_swap_char(za_char)
                elif screen.turn_tidus():
                    battle.main.tidus_haste("l", character=za_char)
                else:
                    battle.main.defend()
        elif not memory.main.battle_active():
            xbox.tap_b()
