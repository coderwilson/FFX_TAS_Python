import logging

import battle.main
import battle.boss
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
from battle import avina_memory
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
    # If we won't get it in next five per zone,
    # default to Inside Sin. The most possible battles there.
    game_vars.set_nea_zone(99)
    print_nea_zone(99)
    return


def decide_luck():
    return False  # Marathon safety.
    # Pull from JSON file to get dynamic value.
    decision = False
    force_luck = True
    if game_vars.story_mode():
        force_luck = False
        return force_luck
    try:
        records = avina_memory.retrieve_memory()
        logger.debug(records.keys())
        seed_str = str(memory.main.rng_seed())
        if seed_str in records.keys():
            if records[seed_str]["zan_luck"] == ["True", "False"]:
                if records[seed_str]["zan_luck"] == "False":
                    force_luck = False
                logger.manip(f"Luck decision based on memory: {force_luck}")
                decision = True
            else:
                logger.manip("I have no memory of this seed. (A)")
        else:
            logger.manip("I have no memory of this seed. (B)")
    except Exception:
        logger.manip("I have no memory of this seed. (C)")
    if not decision:
        force_luck = rng_track.decide_skip_zan_luck()
        logger.manip(f"RNG track logic indicates: {force_luck}")
    return force_luck


def decide_advance_spectral_keeper(report:bool=False) -> int:
    # NOT WORKING YET
    bahamut_hp = 2899
    if game_vars.end_game_version() == 4:
        bahamut_hp = 2710
    if (
        rng_track.future_enemy_attack_damage(character=8, enemy="spectral_keeper", attack_index=1) and
        rng_track.future_enemy_attack_damage(character=8, enemy="spectral_keeper", attack_index=2)
    ):
        damage1 = rng_track.future_enemy_attack_damage(
            character=8, 
            enemy="spectral_keeper", 
            attack_index=1, 
            report= True
        )
        damage2 = rng_track.future_enemy_attack_damage(
            character=8, 
            enemy="spectral_keeper", 
            attack_index=2, 
            report= True
        )
        total_damage = damage1 + damage2
        remaining_hp = max(bahamut_hp - total_damage, 0)
        if report:
            logger.warning(f"Bahamut damage on Spectral: {total_damage}/{bahamut_hp} | remaining HP: {remaining_hp}")
        return remaining_hp
    if report:
        logger.debug("Spectral will miss at least once. No calc needed.")
    return 9999


def arrival():
    memory.main.await_control()
    # Campfire / storytelling map
    while memory.main.get_map() == 363:
        if memory.main.user_control():
            if memory.main.get_coords()[1] > -67:
                pathing.set_movement([115,-74])
            else:
                pathing.set_movement([270,-165])
        elif memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.tap_confirm()

    re_equip_ne = False
    level_need = 0
    if game_vars.story_mode():
        game_vars.set_nea_zone(99)
        menu.equip_armor(character=game_vars.ne_armor(), ability=99)
        memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
        menu.equip_armor(character=game_vars.ne_armor(), ability=99)
        level_need = 7
        re_equip_ne = True
    else:
        decide_nea()
        # This point should be on the map just after the fireplace chat.
        
        if memory.main.overdrive_state_2()[6] != 100 and game_vars.get_nea_zone() == 1:
            memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
            menu.equip_armor(character=game_vars.ne_armor(), ability=99)
            re_equip_ne = True

        game_vars.set_skip_zan_luck(decide_luck())
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
                    pathing.approach_coords([-110,-433],click_through=True)
                else:
                    if memory.main.get_item_count_slot(fortune_slot) > fortune_count:
                        checkpoint += 1
                        memory.main.click_to_control_3()
                    else:
                        pathing.approach_coords([-110,-433],click_through=True)
            elif pathing.set_movement(ZanarkandOutdoors.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()

            if memory.main.battle_active():
                if game_vars.story_mode():
                    if memory.main.overdrive_state_2()[6] != 100:
                        battle.main.charge_rikku_od()
                    else:
                        battle.main.zanarkand_levels()
                    battle.main.wrap_up()
                    if (
                        level_need <= memory.main.get_yuna_slvl() and 
                        memory.main.overdrive_state_2()[6] == 100
                    ):
                        re_equip_ne = False
                        memory.main.update_formation(
                            Tidus, Yuna, Auron, full_menu_close=False
                        )
                        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                        memory.main.close_menu()
                else:
                    battle.main.charge_rikku_od()
                    if re_equip_ne and memory.main.overdrive_state_2()[6] == 100:
                        re_equip_ne = False
                        memory.main.click_to_control()
                        memory.main.update_formation(
                            Tidus, Yuna, Auron, full_menu_close=False
                        )
                        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                        memory.main.close_menu()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif memory.main.menu_open():
                xbox.tap_confirm()

    # Outside the dome
    logger.info("Now approaching the Blitz dome.")
    logger.info("Close observation will reveal this is the same blitz dome")
    logger.info("as the one from the opening of the game.")
    while memory.main.get_map() != 222:
        FFXC.set_movement(0, 1)
        if not game_vars.story_mode():
            xbox.tap_confirm()

def dome_interior():
    re_equip_ne = False
    logger.info("Start of Zanarkand Dome section")
    friend_slot = memory.main.get_item_slot(97)
    yuna_levels_needed = 0
    # if game_vars.story_mode() or game_vars.end_game_version() == 4:
    #     yuna_levels_needed = 8
    # else:
    #     yuna_levels_needed = 6
    if friend_slot == 255:
        friend_count = 0
    else:
        friend_count = memory.main.get_item_count_slot(friend_slot)

    luck_slot = memory.main.get_item_slot(94)
    if luck_slot == 255:
        friend_count = 0
    else:
        luck_count = memory.main.get_item_count_slot(luck_slot)
    if memory.main.get_yuna_slvl() < yuna_levels_needed:
        memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
        menu.equip_armor(character=game_vars.ne_armor(), ability=99)
        re_equip_ne = True
    elif memory.main.overdrive_state_2()[6] != 100 and game_vars.get_nea_zone() == 2:
        memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
        menu.equip_armor(character=game_vars.ne_armor(), ability=99)
        re_equip_ne = True

    if memory.main.get_map() == 316:
        checkpoint = 21  # Reset from failing Spectral Keeper fight.
    else:
        checkpoint = 0
    while memory.main.get_map() != 320:
        if memory.main.user_control():
            if checkpoint == 11 and game_vars.end_game_version() != 4:
                logger.debug("Do not need friend sphere. Skipping forward.")
                checkpoint = 15
            elif checkpoint == 13:  # Second chest
                friend_slot = memory.main.get_item_slot(97)
                if friend_slot == 255:
                    friend_count = 0
                    pathing.approach_coords([8, 90],click_through=True)
                else:
                    if memory.main.get_item_count_slot(friend_slot) > friend_count:
                        checkpoint += 1
                        memory.main.click_to_control_3()
                    else:
                        pathing.approach_coords([8, 90],click_through=True)
            elif checkpoint == 20 and re_equip_ne:
                checkpoint = 18
            elif checkpoint == 23 and game_vars.get_skip_zan_luck():
                checkpoint = 25
            elif checkpoint == 24:  # Third chest
                luck_slot = memory.main.get_item_slot(94)
                if luck_slot == 255:
                    luck_count = 0
                    pathing.approach_coords([26,-83],click_through=True)
                else:
                    if memory.main.get_item_count_slot(luck_slot) > luck_count:
                        checkpoint += 1
                        logger.debug(f"Updating Checkpoint {checkpoint}")
                        memory.main.click_to_control_3()
                    else:
                        pathing.approach_coords([26,-83],click_through=True)
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
            if memory.main.battle_active():
                logger.debug(f"Rikku OD check: {memory.main.overdrive_state()[6]}")
                logger.debug(f"Yuna Slvls: {memory.main.get_yuna_slvl()}")
                if memory.main.overdrive_state()[6] < 100 and memory.main.get_encounter_id() == 361:
                    logger.info("Attempting to charge Rikku overdrive")
                    battle.main.charge_rikku_od()
                    memory.main.click_to_control()
                    memory.main.update_formation(
                        Tidus, Yuna, Auron, full_menu_close=False
                    )
                    if (
                        re_equip_ne and 
                        Rikku.has_overdrive() and
                        memory.main.get_yuna_slvl() >= yuna_levels_needed
                    ):
                        re_equip_ne = False
                        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                    memory.main.close_menu()
                elif memory.main.get_yuna_slvl() < yuna_levels_needed and memory.main.get_encounter_id() != 361:
                    logger.info("Attempting to gain levels on Yuna")
                    battle.main.calm_impulse()
                    memory.main.click_to_control()
                    memory.main.update_formation(
                        Tidus, Yuna, Auron, full_menu_close=False
                    )
                    if re_equip_ne and memory.main.get_yuna_slvl() >= yuna_levels_needed:
                        re_equip_ne = False
                        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                    memory.main.close_menu()
                else:
                    logger.info("Unsure purpose of this branch, should not have occurred???")
                    # This shouldn't occur, but programming as backup anyway.
                    battle.main.flee_all()
                    memory.main.click_to_control()
                    memory.main.update_formation(
                        Tidus, Yuna, Auron, full_menu_close=False
                    )
                    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                    memory.main.close_menu()
                    re_equip_ne = False
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif memory.main.menu_open():
                xbox.tap_confirm()
    
    ver = game_vars.end_game_version()
    logger.info(f"Now prepping for Sanctuary Keeper fight. Version {ver}")
    if ver == 4:
        menu.sk_return()
    elif ver == 3:
        menu.sk_friend()
    else:
        menu.sk_mixed()
    memory.main.update_formation(Tidus, Yuna, Auron)
    memory.main.close_menu()


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
                pathing.approach_coords([68,25],click_through=True)  # Push the pedestol
                pathing.approach_coords([78,60],click_through=True)  # Room to room
                
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
            elif checkpoint == 26:
                pathing.approach_coords([68,-1],click_through=True)  # Place red sphere
                checkpoint += 1
            elif checkpoint == 28:
                pathing.approach_coords([68,-24],click_through=True)  # Push second pedestol
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
                    xbox.tap_confirm()
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
    logger.info("Start section - Engage Sanctuary Keeper")
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
    while memory.main.battle_active():
        if memory.main.turn_ready():
            logger.debug(memory.main.rng_array_from_index(index=43, array_len=4))
            battle.main.attack("none")
    if memory.main.game_over():
        return False
    memory.main.click_to_control()
    return True


def yunalesca_prep():
    ver = game_vars.end_game_version()
    logger.info("Start section - Prep/Grid before Yunalesca")
    #while not pathing.set_movement([-2, -179]):
    #    if memory.main.diag_skip_possible() and not game_vars.story_mode():
    #        xbox.tap_confirm()

    if ver == 4:
        logger.info("Final pattern for four return spheres off of the B&Y fight")
        menu.sk_return_2()
        memory.main.close_menu()
    else:
        logger.info("No further sphere gridding needed at this time.")

    save_sphere.touch_and_go()
    logger.info("Sphere grid is done. End of Yunalesca prep")
    
    if game_vars.god_mode():
        rng_track.force_equip(equip_type = 0, character = 3)
        rng_track.force_drop()

def yunalesca():
    checkpoint = 0
    last_map = memory.main.get_map()
    # Gets us to Yunalesca battle through multiple rooms.
    logger.info("Starting section - approach and engage Yunalesca")
    while not memory.main.battle_active():
        if memory.main.menu_open():
            memory.main.close_menu()
        elif memory.main.user_control():
            coords = memory.main.get_actor_coords(0)
            pathing.set_movement([0,coords[1]+20])
            '''
            if memory.main.get_map() == 244 and checkpoint < 3:
                checkpoint = 3
            #elif checkpoint in [2, 4]:
            #    FFXC.set_movement(0, 1)
            #    memory.main.await_event()
            #    checkpoint += 1
            #    logger.debug(f"Checkpoint {checkpoint}")
            elif pathing.set_movement(ZanarkandYunalesca.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
            '''
        else:
            FFXC.set_neutral()
            if last_map != memory.main.get_map():
                last_map = memory.main.get_map()
                if last_map == 270:
                    logger.info("Now! Now is the time!")
                elif last_map == 224:
                    logger.info("Now choose. Choose who will become your fayth.")
            if not game_vars.story_mode():
                # Double mashing.
                xbox.skip_dialog_special()
            '''
            FFXC.set_confirm()
            FFXC.set_back()
            memory.main.wait_frames(1)
            FFXC.release_confirm()
            FFXC.release_back()
            memory.main.wait_frames(1)
            '''
    if not battle.boss.yunalesca():
        return False
    memory.main.click_to_control()  # This does all the attacking and dialog skipping

    # Now to check for zombie strike and then report to logs.
    logger.info("Ready to check for Zombiestrike")
    game_vars.set_zombie(value=confirm_zombie())
    logs.write_stats("Zombiestrike:")
    logs.write_stats(game_vars.zombie_weapon())
    logger.info("++Zombiestrike:")
    logger.info(f"++ {game_vars.zombie_weapon()}")
    return True


def confirm_zombie() -> int:
    equip_handles = memory.main.all_equipment()
    while len(equip_handles) > 0:
        current_handle = equip_handles.pop(0)
        if current_handle.has_ability(0x8032):
            return current_handle.owner()
    return 255


def post_yunalesca(checkpoint=0):
    logger.info("Heading back outside.")
    FFXC.set_neutral()
    if game_vars.nemesis() or game_vars.platinum():
        menu.equip_weapon(character=0, ability=0x807A, full_menu_close=True)

        # Grab sun sigil
        while not pathing.set_movement([-36,-22]):
            pass
        while not pathing.set_movement([-29,94]):
            pass
        while memory.main.get_actor_coords(0)[1] > 50:
            FFXC.set_movement(1,0)
        while not pathing.set_movement([-59,-146]):
            pass
        while not pathing.set_movement([-36,-22]):
            pass
        while not pathing.set_movement([-45,94]):
            pass
        
        # Open chest
        #check_near_actors(False)
        pathing.approach_actor_by_id(20482)
        memory.main.click_to_control()
        
        while not pathing.set_movement([-36,-22]):
            pass
        while not pathing.set_movement([-13,-173]):
            pass
    
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
            if memory.main.cutscene_skip_possible():
                logger.debug(f"Cutscene ID: {memory.get.cutscene_id()}")
                if memory.get.cutscene_id() == (0, 2850, 3):
                    memory.main.wait_frames(2)
                    xbox.skip_scene(fast_mode=True)
            else:
                if not game_vars.story_mode():
                    xbox.tap_confirm()
