import logging

import battle.boss
import battle.main
import manip_planning.baaj_to_tros
import memory.main
import menu
import pathing
import save_sphere
import screen
import vars
import xbox
from paths import BaajHallway, BaajPuzzle, BaajRamp
from players import CurrentPlayer, Rikku, Tidus

logger = logging.getLogger(__name__)

FFXC = xbox.controller_handle()
game_vars = vars.vars_handle()


def entrance_truerng(checkpoint: int = 0):
    memory.main.await_control()
    logger.info("Starting Baaj exterior area")
    FFXC.set_neutral()

    # Now back into the water

    while not memory.main.battle_active():
        if memory.main.user_control():
            if checkpoint == 6:
                memory.main.click_to_event_temple(0)
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(BaajRamp.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()

    FFXC.set_neutral()

    # Battles
    while memory.main.get_story_progress() < 48:
        if screen.battle_screen():
            if memory.main.get_encounter_id() == 2:
                CurrentPlayer().attack()
            else:
                CurrentPlayer().defend()
        elif memory.main.diag_skip_possible():
            xbox.menu_b()

    # Out of the frying pan, into the furnace
    memory.main.click_to_control()
    logger.info("Hallway before main puzzle.")
    checkpoint = 0
    menu.short_aeons()
    while memory.main.get_map() != 63:
        if memory.main.user_control():
            if checkpoint == 9:
                FFXC.set_movement(-1, 1)
                memory.main.await_event()
                FFXC.set_neutral()
            # General pathing
            elif pathing.set_movement(BaajHallway.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def entrance(sahagin_b_first: bool, geos_potion: bool, geos_attacks: int, checkpoint: int = 0):
    memory.main.await_control()
    logger.info("Starting Baaj exterior area")
    FFXC.set_neutral()

    # Now back into the water

    while not memory.main.battle_active():
        if memory.main.user_control():
            if checkpoint == 6:
                memory.main.click_to_event_temple(0)
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(BaajRamp.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()

    FFXC.set_neutral()

    # Battles
    potion_count = 0
    attack_count = 0

    while memory.main.get_story_progress() < 48:
        if screen.battle_screen():
            if memory.main.get_encounter_id() == 2:
                if sahagin_b_first:
                    CurrentPlayer().attack(target_id=21, direction_hint="u")
                else:
                    CurrentPlayer().attack()
            else:
                if geos_potion and potion_count == 0:
                    battle.main.use_potion_character(Tidus, "l")
                    potion_count += 1
                elif attack_count < geos_attacks:
                    CurrentPlayer().attack()
                    attack_count += 1
                else:
                    CurrentPlayer().defend()
        elif memory.main.diag_skip_possible():
            xbox.menu_b()

    # Out of the frying pan, into the furnace
    memory.main.click_to_control()
    logger.info("Hallway before main puzzle.")
    checkpoint = 0
    menu_complete = False
    while memory.main.get_map() != 63:
        if checkpoint == 5 and not menu_complete:
            menu.short_aeons()
            menu_complete = True

        if memory.main.user_control():
            if checkpoint == 9:
                FFXC.set_movement(-1, 1)
                memory.main.await_event()
                FFXC.set_neutral()
            # General pathing
            elif pathing.set_movement(BaajHallway.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def baaj_puzzle():
    memory.main.click_to_control()
    logger.info("Ready for the main puzzle.")
    checkpoint = 0
    while not memory.main.battle_active():
        if memory.main.user_control():
            # Events
            # if checkpoint == 3:
            #     save_sphere.touch_and_go()
            #     checkpoint += 1
            # el
            if checkpoint == 5:  # Flint room
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 6:  # Obtain Flint
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 7:  # Exit Flint room
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint == 12:  # Bouquet hallway
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 21:  # Withered bouquet
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 32:  # Back to main room
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 33:  # To the fireplace
                pathing.set_movement([1, 1])
                xbox.menu_b()

            # General pathing
            elif pathing.set_movement(BaajPuzzle.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def klikk_fight_truerng():
    # Before Rikku shows up, we're just going to spam the B button. Simple.
    FFXC.set_neutral()
    while not Rikku.is_turn():
        xbox.tap_b()

    xbox.click_to_battle()
    battle.main.use_item(0, "none")  # Tidus self-potion
    screen.await_turn()
    battle.boss.klikk()


def klikk_fight(tidus_potion_klikk: bool, tidus_potion_turn: int, rikku_potion_klikk: bool, klikk_steals: int):
    # Before Rikku shows up, we're just going to spam the B button. Simple.
    FFXC.set_neutral()
    while not memory.main.turn_ready():
        xbox.tap_b()

    # Possibly replace with the following, for less error messages.
    #while not Rikku.is_turn():
    #    Tidus.attack()
    # Possibly replace with the following, for less error messages.
    while not Rikku.is_turn():
        if memory.main.battle_active() and Tidus.is_turn():
            Tidus.attack()

    xbox.click_to_battle()
    screen.await_turn()
    battle.boss.klikk(tidus_potion_klikk, tidus_potion_turn, rikku_potion_klikk, klikk_steals)


def distance(n1, n2):
    try:
        player1 = memory.main.get_actor_coords(actor_index=n1)
        player2 = memory.main.get_actor_coords(actor_index=n2)
        return abs(player1[1] - player2[1]) + abs(player1[0] - player2[0])
    except Exception as x:
        logger.error(f"Exception: {x}")
        return 999


def ab_boat_1():
    logger.info("Start of Al Bhed boat section.")
    logger.debug("Control restored.")
    logger.info("On the boat!")
    while memory.main.get_actor_coords(actor_index=0)[0] > -50:
        rikku_num = memory.main.actor_index(actor_num=41)
        target = memory.main.get_actor_coords(actor_index=rikku_num)
        pathing.set_movement(target)
        if distance(0, rikku_num) < 10:
            xbox.tap_b()
        elif memory.main.menu_open():
            xbox.menu_a()
            xbox.menu_b()
    logger.info("In the water!")
    FFXC.set_value("btn_a", 1)
    while not memory.main.user_control():
        FFXC.set_value("btn_b", 1)
        memory.main.wait_frames(1)
        FFXC.set_value("btn_b", 0)
        memory.main.wait_frames(1)
    FFXC.set_value("btn_a", 1)
    FFXC.set_movement(-1, -1)
    memory.main.wait_frames(20)

    while memory.main.get_map() != 288:
        FFXC.set_value("btn_a", 1)
        FFXC.set_movement(0, -1)
        if memory.main.battle_active():
            FFXC.set_neutral()
            logger.info("Battle Start (Al Bhed swimming section)")
            battle.main.steal_and_attack()
            logger.info("Battle End (Al Bhed swimming section)")
        elif memory.main.menu_open() or memory.main.diag_skip_possible():
            logger.info("Battle Complete screen")
            xbox.tap_b()


def ab_swimming_1_truerng():
    logger.info("Swimming down from the boat")
    while memory.main.get_map() != 288:
        if memory.main.user_control():
            pathing.set_movement([-300, -300])
            FFXC.set_value("btn_a", 1)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                logger.info("Battle Start (Al Bhed swimming section)")
                battle.main.steal_and_attack()
                logger.info("Battle End (Al Bhed swimming section)")
            elif memory.main.menu_open():
                logger.info("Battle Complete screen")
                xbox.menu_b()

    FFXC.set_neutral()
    logger.info("Swimming towards airship")
    while memory.main.get_map() != 64:
        pos = memory.main.get_coords()
        if memory.main.user_control():
            if memory.main.get_map() == 71:
                FFXC.set_movement(0, -1)
                FFXC.set_value("btn_a", 1)
            else:
                FFXC.set_value("btn_a", 0)
                if pos[1] > -230:
                    pathing.set_movement([-343, -284])
                elif pos[1] > -410:
                    pathing.set_movement([-421, -463])
                else:
                    FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                logger.info("Battle Start (Al Bhed swimming section)")
                battle.main.steal_and_attack()
                logger.info("Battle End (Al Bhed swimming section)")
            elif memory.main.menu_open():
                logger.info("Battle Complete screen")
                xbox.menu_b()


def ab_swimming_1(chain_encounter_strat: int):
    logger.info("Swimming down from the boat")
    while memory.main.get_map() != 288:
        if memory.main.user_control():
            pathing.set_movement([-300, -300])
            FFXC.set_value("btn_a", 1)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                logger.info("Battle Start (Al Bhed swimming section)")
                battle.main.steal_and_attack()
                logger.info("Battle End (Al Bhed swimming section)")
            elif memory.main.menu_open():
                logger.info("Battle Complete screen")
                xbox.menu_b()

    FFXC.set_neutral()
    logger.info("Swimming towards airship")

    enemy_formation = memory.main.rng_array_from_index(index=1)[1] % 2
    logging.debug(f"Chain Encounter Formation Expected: {enemy_formation}")

    if manip_planning.baaj_to_tros.chain_encounter()[0]:
        if Rikku.hp() < 100:
            if Tidus.hp() < 100:
                battle.main.heal_up_2(0, 6, single_item=True)
            else:
                battle.main.heal_up_2(6, single_item=True)
        elif Tidus.hp() < 100:
            battle.main.heal_up_2(0, single_item=True)

    while memory.main.get_map() != 64:
        pos = memory.main.get_coords()
        if memory.main.user_control():
            if memory.main.get_map() == 71:
                FFXC.set_movement(0, -1)
                FFXC.set_value("btn_a", 1)
            else:
                FFXC.set_value("btn_a", 1)
                if pos[1] > -230:
                    pathing.set_movement([-343, -284])
                elif pos[1] > -410:
                    pathing.set_movement([-421, -463])
                else:
                    FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                logger.info("Battle Start (Al Bhed swimming section)")
                battle.main.chain_encounter(strat=chain_encounter_strat, enemy_formation=enemy_formation)
                logger.info("Battle End (Al Bhed swimming section)")
            elif memory.main.menu_open():
                logger.info("Battle Complete screen")
                xbox.menu_b()

    return


def ab_swimming_2_truerng():
    # Quick heal-up to make sure we're full HP on Rikku
    memory.main.await_control()
    FFXC.set_movement(1, -1)
    FFXC.set_value("btn_a", 1)
    memory.main.touch_save_sphere()
    # TODO: adapt save_sphere.touch_and_go() to handle this save sphere

    memory.main.clear_save_menu_cursor_2()
    # Now to get to it
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 1)
    memory.main.click_to_event()
    memory.main.wait_frames(30 * 0.2)
    memory.main.await_control()

    pos = memory.main.get_coords()
    while memory.main.user_control():
        if pos[1] < 135:
            FFXC.set_movement(1, 1)
        else:
            FFXC.set_movement(0, 1)

        pos = memory.main.get_coords()
    FFXC.set_neutral()

    screen.await_turn()
    # Final group of Piranhas
    battle.main.steal_and_attack_pre_tros()
    memory.main.await_control()
    FFXC.set_movement(0, 1)
    logger.info("Technical Support Tidus")
    xbox.skip_dialog(2)
    FFXC.set_movement(0, 0)
    memory.main.click_to_control()
    while not memory.main.battle_active():
        FFXC.set_movement(0, -1)
    logger.info("Engaging Tros")
    FFXC.set_neutral()

    # Tros fight
    xbox.click_to_battle()
    battle.boss.tros()

    FFXC.set_neutral()
    while memory.main.get_story_progress() < 111:
        if memory.main.user_control():
            if (
                memory.main.diag_progress_flag() == 109
                and not memory.main.user_control()
            ):
                FFXC.set_neutral()
                if memory.main.save_menu_cursor_2() == 0:
                    xbox.tap_a()
                else:
                    xbox.tap_b()
                memory.main.wait_frames(4)
            elif memory.main.get_map() == 64:
                if memory.main.get_coords()[0] < -4:
                    pathing.set_movement([-2, 47])
                else:
                    pathing.set_movement([73, 1])
            elif memory.main.get_map() == 380:
                pathing.set_movement([700, 300])
            elif memory.main.get_map() == 71:
                rikku_num = memory.main.actor_index(actor_num=41)
                pathing.set_movement(memory.main.get_actor_coords(rikku_num))
                if distance(0, rikku_num) < 30:
                    xbox.tap_b()
        else:
            FFXC.set_neutral()
            if memory.main.diag_progress_flag() == 109:
                memory.main.csr_baaj_save_clear()
            elif memory.main.diag_skip_possible() and not game_vars.csr():
                xbox.tap_b()

    logger.info("Should now be ready for Besaid")

    if not game_vars.csr():
        xbox.clear_save_popup(0)


def ab_swimming_2(ruins_encounter_strat: int):
    # Quick heal-up to make sure we're full HP on Rikku
    memory.main.await_control()
    FFXC.set_movement(1, -1)
    FFXC.set_value("btn_a", 1)
    memory.main.touch_save_sphere()
    # TODO: adapt save_sphere.touch_and_go() to handle this save sphere

    memory.main.clear_save_menu_cursor_2()
    # Now to get to it
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 1)
    memory.main.click_to_event()
    memory.main.wait_frames(30 * 0.2)
    memory.main.await_control()

    pos = memory.main.get_coords()
    while memory.main.user_control():
        if pos[1] < 135:
            FFXC.set_movement(1, 1)
        else:
            FFXC.set_movement(0, 1)

        pos = memory.main.get_coords()
    FFXC.set_neutral()

    screen.await_turn()
    # Final group of Piranhas
    battle.main.ruins_encounter(strat=ruins_encounter_strat)
    memory.main.click_to_control()
    memory.main.await_control()
    FFXC.set_movement(0, 1)
    logger.info("Technical Support Tidus")
    xbox.skip_dialog(2)
    FFXC.set_movement(0, 0)
    memory.main.click_to_control()

    rng01_array_enemy_formation = memory.main.rng_array_from_index(index=1, array_len=10)
    preempt_roll = rng01_array_enemy_formation[1] % 256
    tros_preempt = (preempt_roll < 32)
    logging.debug(f"Tros pre-empt roll: {rng01_array_enemy_formation[1] % 256} / Pre-empt: {tros_preempt}")

    logging.debug(f"Rikku HP: {Rikku.hp()}")
    rikku_damage_on_tros = manip_planning.baaj_to_tros.rikku_damage_taken_tros()
    logging.debug(f"Rikku damage taken on Tros: {rikku_damage_on_tros}")

    if rikku_damage_on_tros > Rikku.hp():
        logger.debug(f"Healing Rikku so she doesn't die on tros")
        battle.main.heal_up_2(6)

    while not memory.main.battle_active():
        FFXC.set_movement(0, -1)
    logger.info("Engaging Tros")
    FFXC.set_neutral()

    # Tros fight
    xbox.click_to_battle()
    battle.boss.tros(preempt=tros_preempt)

    FFXC.set_neutral()
    while memory.main.get_story_progress() < 111:
        if memory.main.user_control():
            if (
                memory.main.diag_progress_flag() == 109
                and not memory.main.user_control()
            ):
                FFXC.set_neutral()
                if memory.main.save_menu_cursor_2() == 0:
                    xbox.tap_a()
                else:
                    xbox.tap_b()
                memory.main.wait_frames(4)
            elif memory.main.get_map() == 64:
                if memory.main.get_coords()[0] < -4:
                    pathing.set_movement([-2, 47])
                else:
                    pathing.set_movement([73, 1])
            elif memory.main.get_map() == 380:
                pathing.set_movement([700, 300])
            elif memory.main.get_map() == 71:
                rikku_num = memory.main.actor_index(actor_num=41)
                pathing.set_movement(memory.main.get_actor_coords(rikku_num))
                if distance(0, rikku_num) < 30:
                    xbox.tap_b()
        else:
            FFXC.set_neutral()
            if memory.main.diag_progress_flag() == 109:
                memory.main.csr_baaj_save_clear()
            elif memory.main.diag_skip_possible() and not game_vars.csr():
                xbox.tap_b()

    logger.info("Should now be ready for Besaid")

    if not game_vars.csr():
        xbox.clear_save_popup(0)
