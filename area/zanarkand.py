import logging

import battle.main
import logs
import memory.get
import memory.main
import menu
import pathing
import rng_track
import save_sphere
import screen
import vars
import xbox
from paths import (
    YunalescaToAirship,
    ZanarkandDome,
    ZanarkandOutdoors,
    ZanarkandTrials,
    ZanarkandYunalesca,
)
from players import Auron, CurrentPlayer, Rikku, Tidus, Yuna

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def print_nea_zone(battles: int):
    logger.debug(f"Charging Rikku zone: {game_vars.get_nea_zone()}")
    logger.debug(f"This will take {battles} number of battles (99 = unknown)")


def decide_nea(bonus_advance: int = 0):
    import rng_track

    max_battles = 1
    zan_outdoors = rng_track.coming_battles(
        area="zanarkand_(overpass)",
        battle_count=max_battles,
        extra_advances=bonus_advance,
    )
    zan_indoors = rng_track.coming_battles(
        area="zanarkand_(dome)", battle_count=max_battles, extra_advances=bonus_advance
    )
    sea_sorrows = rng_track.coming_battles(
        area="inside_sin_(front)",
        battle_count=max_battles,
        extra_advances=bonus_advance + 6,
    )

    for i in range(max_battles):
        if "behemoth" in zan_outdoors[i]:
            game_vars.set_nea_zone(1)
            print_nea_zone(i + 1)
            return
        elif "defender_z" in zan_indoors[i]:
            game_vars.set_nea_zone(2)
            print_nea_zone(i + 1)
            return
        elif "behemoth_king" in sea_sorrows[i]:
            game_vars.set_nea_zone(3)
            print_nea_zone(i + 1)
            return
        elif "adamantoise" in sea_sorrows[i]:
            game_vars.set_nea_zone(3)
            print_nea_zone(i + 1)
            return
    # If we won't get it in next five per zone, default to Inside Sin. The most possible battles there.
    game_vars.set_nea_zone(99)
    print_nea_zone(99)
    return


def arrival():
    memory.main.await_control()
    decide_nea()
    # Starts from the map just after the fireplace chat.
    re_equip_ne = False
    if memory.main.overdrive_state_2()[6] != 100 and game_vars.get_nea_zone() == 1:
        memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
        menu.equip_armor(character=game_vars.ne_armor(), ability=99)
        re_equip_ne = True

    game_vars.set_skip_zan_luck(rng_track.decide_skip_zan_luck())
    logs.write_stats("Zanarkand Luck Skip:")
    logs.write_stats(game_vars.get_skip_zan_luck())
    # game_vars.set_skip_zan_luck(True) #For testing
    logger.info("Outdoor Zanarkand pathing section")
    while memory.main.get_map() != 225:
        if memory.main.user_control():
            if memory.main.get_coords()[1] > -52:
                pathing.set_movement([103, -54])
            elif memory.main.get_coords()[0] < 172:
                pathing.set_movement([176, -118])
            else:
                FFXC.set_movement(-1, 1)
        else:
            FFXC.set_neutral()

    fortune_slot = memory.main.get_item_slot(74)
    if fortune_slot == 255:
        fortune_count = 0
    else:
        fortune_count = memory.main.get_item_count_slot(fortune_slot)

    checkpoint = 0
    while memory.main.get_map() != 314:
        if memory.main.user_control():
            if checkpoint == 3 and game_vars.get_skip_zan_luck():
                checkpoint = 5
            elif checkpoint == 4:  # First chest
                fortune_slot = memory.main.get_item_slot(74)
                if fortune_slot == 255:
                    fortune_count = 0
                    FFXC.set_movement(-1, 1)
                    xbox.tap_b()
                else:
                    if memory.main.get_item_count_slot(fortune_slot) > fortune_count:
                        checkpoint += 1
                        memory.main.click_to_control()
                    else:
                        FFXC.set_movement(-1, 1)
                        xbox.tap_b()
            elif pathing.set_movement(ZanarkandOutdoors.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()

            if screen.battle_screen():
                battle.main.charge_rikku_od()
                if re_equip_ne and memory.main.overdrive_state_2()[6] == 100:
                    re_equip_ne = False
                    memory.main.click_to_control()
                    memory.main.update_formation(
                        Tidus, Yuna, Auron, full_menu_close=False
                    )
                    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                    memory.main.close_menu()
            elif memory.main.diag_skip_possible() and not memory.main.battle_active():
                xbox.tap_b()
            elif memory.main.menu_open():
                xbox.tap_b()

    # Outside the dome
    logger.info("Now approaching the Blitz dome.")
    logger.info("Close observation will reveal this is the same blitz dome")
    logger.info("as the one from the opening of the game.")
    while memory.main.get_map() != 222:
        FFXC.set_movement(0, 1)
        xbox.tap_b()

    logger.info("Start of Zanarkand Dome section")
    friend_slot = memory.main.get_item_slot(97)
    if friend_slot == 255:
        friend_count = 0
    else:
        friend_count = memory.main.get_item_count_slot(friend_slot)

    luck_slot = memory.main.get_item_slot(94)
    if luck_slot == 255:
        friend_count = 0
    else:
        luck_count = memory.main.get_item_count_slot(luck_slot)

    if memory.main.overdrive_state_2()[6] != 100 and game_vars.get_nea_zone() == 2:
        memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
        menu.equip_armor(character=game_vars.ne_armor(), ability=99)
        re_equip_ne = True

    checkpoint = 0
    while memory.main.get_map() != 320:
        if memory.main.user_control():
            if checkpoint == 13:  # Second chest
                friend_slot = memory.main.get_item_slot(97)
                if friend_slot == 255:
                    friend_count = 0
                    pathing.set_movement([8, 90])
                    memory.main.wait_frames(1)
                    xbox.tap_b()
                else:
                    if memory.main.get_item_count_slot(friend_slot) > friend_count:
                        checkpoint += 1
                        memory.main.click_to_control()
                    else:
                        pathing.set_movement([8, 90])
                        memory.main.wait_frames(1)
                        xbox.tap_b()
            if checkpoint == 23 and game_vars.get_skip_zan_luck():
                checkpoint = 25
            elif checkpoint == 24:  # Third chest
                luck_slot = memory.main.get_item_slot(94)
                if luck_slot == 255:
                    luck_count = 0
                    FFXC.set_movement(1, 1)
                    xbox.tap_b()
                else:
                    if memory.main.get_item_count_slot(luck_slot) > luck_count:
                        checkpoint += 1
                        logger.debug(f"Updating Checkpoint {checkpoint}")
                        memory.main.click_to_control()
                    else:
                        FFXC.set_movement(1, 1)
                        xbox.tap_b()
            elif checkpoint == 29:  # Save sphere
                save_sphere.touch_and_go()
                checkpoint += 1
            elif (
                memory.main.get_map() == 316 and checkpoint < 21
            ):  # Final room before trials
                logger.info("Final room before trials")
                checkpoint = 21
            elif pathing.set_movement(ZanarkandDome.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle.main.charge_rikku_od()
                if re_equip_ne and memory.main.overdrive_state_2()[6] == 100:
                    re_equip_ne = False
                    memory.main.click_to_control()
                    memory.main.update_formation(
                        Tidus, Yuna, Auron, full_menu_close=False
                    )
                    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                    memory.main.close_menu()
            elif memory.main.diag_skip_possible() and not memory.main.battle_active():
                xbox.tap_b()
            elif memory.main.menu_open():
                xbox.tap_b()


def trials():
    checkpoint = 0
    while checkpoint < 89:
        checkpoint = trials_0(checkpoint)
        checkpoint = trials_1(checkpoint)
        checkpoint = trials_2(checkpoint)
        checkpoint = trials_3(checkpoint)
        checkpoint = trials_4(checkpoint)


def trials_0(checkpoint):
    memory.main.await_control()

    while checkpoint < 9:
        if memory.main.user_control():
            if checkpoint == 8:
                FFXC.set_movement(-1, 0)
                while memory.main.user_control():
                    xbox.tap_b()
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 0.2)
                memory.main.await_control()
                memory.main.wait_frames(30 * 1.3)
                FFXC.set_movement(0, 1)
                checkpoint += 1
            elif pathing.set_movement(ZanarkandTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
    return checkpoint


def trials_1(checkpoint):
    memory.main.await_control()

    while checkpoint < 31:
        if memory.main.user_control():
            if checkpoint == 20:
                FFXC.set_movement(-1, 1)
                memory.main.click_to_event()
                FFXC.set_neutral()
                xbox.skip_dialog(0.5)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 26 or checkpoint == 28:
                FFXC.set_movement(-1, -1)
                memory.main.click_to_event()
                FFXC.set_neutral()
                xbox.skip_dialog(0.5)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 30:
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                memory.main.wait_frames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif pathing.set_movement(ZanarkandTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
    return checkpoint


def trials_2(checkpoint):
    memory.main.await_control()

    while checkpoint < 49:
        if memory.main.user_control():
            if checkpoint == 46:
                FFXC.set_movement(1, 0)
                memory.main.click_to_event()
                FFXC.set_neutral()
                xbox.skip_dialog(0.5)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 48:
                FFXC.set_movement(-1, 1)
                memory.main.await_event()
                memory.main.wait_frames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif pathing.set_movement(ZanarkandTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
    return checkpoint


def trials_3(checkpoint):
    memory.main.await_control()

    while checkpoint < 69:
        if memory.main.user_control():
            if checkpoint == 66:
                FFXC.set_movement(1, 0)
                memory.main.click_to_event()
                FFXC.set_neutral()
                xbox.skip_dialog(0.7)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 68:
                FFXC.set_movement(-1, 1)
                memory.main.await_event()
                memory.main.wait_frames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif pathing.set_movement(ZanarkandTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
    return checkpoint


def trials_4(checkpoint):
    memory.main.await_control()

    while checkpoint < 89:
        if memory.main.user_control():
            if checkpoint == 81:
                FFXC.set_movement(0, 1)
                memory.main.click_to_event()
                FFXC.set_neutral()
                xbox.skip_dialog(0.5)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 87:
                while memory.main.user_control():
                    pathing.set_movement([141, 1])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif pathing.set_movement(ZanarkandTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
    FFXC.set_neutral()
    return checkpoint


def s_keeper_print_bahamut_crit_chance():
    crit_chance = memory.main.next_crit(character=7, char_luck=17, enemy_luck=15)
    logger.debug(f"Next Aeon Crit: {crit_chance}")


def sanctuary_keeper():
    ver = game_vars.end_game_version()
    logger.info("Now prepping for Sanctuary Keeper fight")

    if ver == 4:
        logger.info("Pattern for four return spheres off of the B&Y fight")
        menu.sk_return()
    elif ver == 3:
        menu.sk_friend()
    else:
        menu.sk_mixed()
    memory.main.update_formation(Tidus, Yuna, Auron)
    memory.main.close_menu()

    while not pathing.set_movement([110, 20]):
        pass
    FFXC.set_movement(-1, 1)
    memory.main.await_event()
    xbox.click_to_battle()
    if Tidus.is_turn():
        CurrentPlayer().defend()
        xbox.click_to_battle()
    battle.main.aeon_summon(4)  # This is the whole fight. Kinda sad.
    s_keeper_print_bahamut_crit_chance()
    while not memory.main.battle_complete():
        if memory.main.turn_ready():
            logger.debug(memory.main.rng_array_from_index(index=43, array_len=4))
            battle.main.attack("none")
    memory.main.click_to_control()


def yunalesca():
    ver = game_vars.end_game_version()
    while not pathing.set_movement([-2, -179]):
        if memory.main.diag_skip_possible():
            xbox.tap_b()

    if ver == 4:
        logger.info("Final pattern for four return spheres off of the B&Y fight")
        menu.sk_return_2()
        memory.main.close_menu()
    else:
        logger.info("No further sphere gridding needed at this time.")

    logger.info("Sphere grid is done. Moving on to storyline and eventually Yunalesca.")

    save_sphere.touch_and_go()

    checkpoint = 0
    # Gets us to Yunalesca battle through multiple rooms.
    while not memory.main.battle_active():
        if memory.main.menu_open():
            memory.main.close_menu()
        elif memory.main.user_control():
            if checkpoint in [2, 4]:
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
            elif pathing.set_movement(ZanarkandYunalesca.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            FFXC.set_value("btn_b", 1)
            FFXC.set_value("btn_a", 1)
            memory.main.wait_frames(1)
            FFXC.set_value("btn_b", 0)
            FFXC.set_value("btn_a", 0)
            memory.main.wait_frames(1)
    xbox.click_to_battle()
    battle.main.aeon_summon(4)  # Summon Bahamut and attack.
    memory.main.click_to_control()  # This does all the attacking and dialog skipping

    # Now to check for zombie strike and then report to logs.
    logger.info("Ready to check for Zombiestrike")
    logs.write_stats("Zombiestrike:")
    logs.write_stats(game_vars.zombie_weapon())
    logger.info("++Zombiestrike:")
    logger.info(f"++ {game_vars.zombie_weapon()}")


def post_yunalesca(checkpoint=0):
    logger.info("Heading back outside.")
    FFXC.set_neutral()
    if game_vars.nemesis():
        menu.equip_weapon(character=0, ability=0x807A, full_menu_close=True)
    memory.main.wait_frames(2)
    while memory.main.get_map() != 194:
        if memory.main.user_control():
            if checkpoint < 2 and memory.main.get_map() == 319:
                # Back to room before Yunalesca
                checkpoint = 2
                logger.debug(f"Checkpoint {checkpoint}")
            elif checkpoint < 4 and memory.main.get_map() == 318:
                # Exit to room with the inert Aeon
                checkpoint = 4
                logger.debug(f"Checkpoint {checkpoint}")
            elif checkpoint == 7:
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
            elif checkpoint < 10 and memory.main.get_map() == 320:
                # Back to larger of the puzzle rooms
                checkpoint = 10
                logger.debug(f"Checkpoint {checkpoint}")
            elif checkpoint < 18 and memory.main.get_map() == 316:
                # Hallway before puzzle rooms
                checkpoint = 18
                logger.debug(f"Checkpoint {checkpoint}")
                save_sphere.touch_and_go()
            elif checkpoint < 25 and memory.main.get_map() == 315:
                # Leaving dome
                checkpoint = 25
                logger.debug(f"Checkpoint {checkpoint}")
            elif checkpoint == 26:
                FFXC.set_neutral()
            elif pathing.set_movement(YunalescaToAirship.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle.main.flee_all()
            elif memory.main.diag_skip_possible() and not memory.main.battle_active():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                logger.debug(f"Cutscene ID: {memory.get.cutscene_id()}")
                if memory.get.cutscene_id() == (5673, 2850, 3):
                    memory.main.wait_frames(10)
                    xbox.skip_scene()
