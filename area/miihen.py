import battle.boss
import battle.main
import logs
import memory.main
import pathing
import save_sphere
import screen
import vars
import xbox

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def post_battle_logic(force_charge=False):
    if memory.main.overdrive_state_2()[1] < 43 or (
        force_charge and memory.main.overdrive_state_2()[1] != 100
    ):
        memory.main.full_party_format("kilikawoods1", full_menu_close=False)
    else:
        if game_vars.self_destruct_get():
            memory.main.full_party_format("miihen", full_menu_close=False)
        else:
            memory.main.full_party_format("djose", full_menu_close=False)
    hpCheck = memory.main.get_hp()
    print("------------------ HP check:", hpCheck)
    if hpCheck[0] < 520 or hpCheck[1] < 220:
        battle.main.heal_up()
    else:
        print("No need to heal up. Moving onward.")
    memory.main.close_menu()


def arrival():
    print("Waiting for Yuna/Tidus to stop laughing.")
    FFXC.set_movement(0, 1)
    memory.main.click_to_control()
    print("Now onward to scenes and Mi'ihen skip. Good luck!")
    miihenSkip = False
    battle_count = 0
    SDencounterID = 0

    checkpoint = 0
    while memory.main.get_map() != 120:
        if memory.main.user_control():
            # Miihen skip attempt
            if checkpoint > 3 and checkpoint < 11:
                if game_vars.csr():
                    # Only run this branch if CSR is online.
                    tidusCoords = memory.main.get_coords()
                    hunterCoords = memory.main.miihen_guy_coords()
                    hunterDistance = abs(tidusCoords[1] - hunterCoords[1]) + abs(
                        tidusCoords[0] - hunterCoords[0]
                    )

                    # Get spear
                    if memory.main.hunter_spear():
                        checkpoint = 11
                    elif hunterDistance < 200 or checkpoint in [6, 7, 8, 9, 10]:
                        pathing.set_movement(hunterCoords)
                        xbox.tap_b()

                    elif pathing.set_movement(pathing.miihen(checkpoint)):
                        checkpoint += 1
                        print("Checkpoint reached:", checkpoint)

                else:
                    # Run this branch on a normal Any% run, no CSR
                    tidusCoords = memory.main.get_coords()
                    hunterCoords = memory.main.miihen_guy_coords()
                    if hunterCoords[1] < tidusCoords[1]:
                        checkpoint = 11
                        print("**Late for Mi'ihen skip, forcing recovery.")
                    elif checkpoint == 6:
                        FFXC.set_neutral()
                        memory.main.wait_frames(9)
                        print("Updating checkpoint due to late skip.")
                        print("Checkpoint reached:", checkpoint)
                        checkpoint += 1
                    elif checkpoint == 7:
                        if memory.main.get_coords()[1] > 1356.5:  # Into position
                            if memory.main.get_coords()[0] < -44:
                                FFXC.set_movement(1, 0)
                                memory.main.wait_frames(30 * 0.06)
                                FFXC.set_neutral()
                                memory.main.wait_frames(30 * 0.09)
                            else:
                                checkpoint += 1
                                print("Close to the spot")
                            print(memory.main.get_coords())
                        elif memory.main.get_coords()[0] < -43.5:  # Into position
                            FFXC.set_movement(1, 1)
                            memory.main.wait_frames(2)
                            FFXC.set_neutral()
                            memory.main.wait_frames(3)
                        else:
                            FFXC.set_movement(0, 1)
                            memory.main.wait_frames(2)
                            FFXC.set_neutral()
                            memory.main.wait_frames(3)
                    elif checkpoint == 8:
                        if memory.main.get_coords()[0] > -43.5:  # Into position
                            checkpoint += 1
                            print("Adjusting for horizontal position - complete")
                            print(memory.main.get_coords())
                        else:
                            FFXC.set_movement(1, 0)
                            memory.main.wait_frames(2)
                            FFXC.set_neutral()
                            memory.main.wait_frames(3)
                    elif checkpoint == 9:
                        if memory.main.get_coords()[1] > 1358.5:  # Into position
                            checkpoint = 10
                            print("Stopped and ready for the skip.")
                            print(memory.main.get_coords())
                        else:
                            FFXC.set_movement(0, 1)
                            memory.main.wait_frames(2)
                            FFXC.set_neutral()
                            memory.main.wait_frames(4)
                    elif checkpoint == 10:
                        # Spear guy's position when we start moving.
                        if memory.main.miihen_guy_coords()[1] < 1380:
                            print("Skip engaging!!! Good luck!")
                            # Greater number for spear guy's position means we will start moving faster.
                            # Smaller number means moving later.
                            FFXC.set_movement(0, 1)
                            if game_vars.use_pause():
                                memory.main.wait_frames(2)
                            else:
                                memory.main.wait_frames(3)
                            # Walk into the guy mashing B (or X, or whatever the key is)
                            xbox.skip_dialog(0.3)
                            FFXC.set_neutral()  # Stop trying to move. (recommended by Crimson)
                            print("Starting special skipping.")
                            xbox.skip_dialog_special(3)  # Mash two buttons
                            print("End special skipping.")
                            print("Should now be able to see if it worked.")
                            # Don't move, avoiding a possible extra battle
                            memory.main.wait_frames(30 * 3.5)
                            memory.main.click_to_control_3()
                            print("Mark 1")
                            memory.main.wait_frames(30 * 1)
                            print("Mark 2")
                            try:
                                if (
                                    memory.main.lucille_miihen_coords()[1] > 1400
                                    and memory.main.user_control()
                                ):
                                    miihenSkip = True
                                else:
                                    memory.main.click_to_control_3()
                            except Exception:
                                miihenSkip = False
                            print("Skip successful:", miihenSkip)
                            checkpoint += 1
                    elif pathing.set_movement(pathing.miihen(checkpoint)):
                        checkpoint += 1
                        print("Checkpoint reached:", checkpoint)
            elif checkpoint == 11 and not memory.main.hunter_spear():
                pathing.set_movement(
                    [
                        memory.main.miihen_guy_coords()[0],
                        memory.main.miihen_guy_coords()[1],
                    ]
                )
                xbox.tap_b()

            # Map changes
            elif checkpoint < 15 and memory.main.get_map() == 120:
                checkpoint = 15
            # General pathing
            elif pathing.set_movement(pathing.miihen(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.turn_ready():
                if checkpoint < 4:  # Tutorial battle with Auron
                    while memory.main.battle_active():
                        xbox.tap_b()
                    FFXC.set_movement(0, 1)
                    while not memory.main.user_control():
                        xbox.tap_b()
                    post_battle_logic()
                    FFXC.set_neutral()
                elif checkpoint == 25 and not memory.main.battle_active():
                    # Shelinda dialog
                    FFXC.set_neutral()
                    xbox.tap_b()
                else:
                    FFXC.set_neutral()
                    print("Starting battle")
                    battle_count += 1
                    battle.main.miihen_road()
                    print("Battle complete")
                    post_battle_logic()

                # Kimahri manip
                nextCritKim = memory.main.next_crit(
                    character=3, char_luck=18, enemy_luck=15
                )
                print("#### Next Kimahri crit:", nextCritKim)
            else:
                FFXC.set_movement(1, 1)
                if memory.main.menu_open():
                    FFXC.set_value("btn_b", 1)
                    memory.main.wait_frames(2)
                    FFXC.set_value("btn_b", 0)
                    memory.main.wait_frames(3)
                elif memory.main.diag_skip_possible():
                    FFXC.set_value("btn_b", 1)
                    memory.main.wait_frames(2)
                    FFXC.set_value("btn_b", 0)
                    memory.main.wait_frames(3)
    print("Mi'ihen skip status:", miihenSkip)
    return [game_vars.self_destruct_get(), battle_count, SDencounterID, miihenSkip]


def arrival_2(selfDestruct, battle_count, SDencounterID):
    print("Start of the second map")
    checkpoint = 15
    while memory.main.get_map() != 171:
        if memory.main.user_control():

            # Map changes
            if checkpoint == 27:
                if memory.main.get_coords()[1] > 2810:
                    checkpoint += 1
                elif game_vars.csr():
                    checkpoint += 1
                else:
                    FFXC.set_neutral()
                    xbox.skip_dialog(1)
                    memory.main.click_to_control_3()
                    checkpoint += 1

            # General pathing
            elif pathing.set_movement(pathing.miihen(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle_count += 1
                if (
                    checkpoint == 27 and not memory.main.battle_active()
                ):  # Shelinda dialog
                    xbox.tap_b()
                else:
                    print("Starting battle")
                    battle.main.miihen_road()
                    print("Battle complete")
                    post_battle_logic()
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible():  # Exclude during the Miihen skip.
                if checkpoint < 6 or checkpoint > 12:
                    xbox.tap_b()

            # Map changes
            elif checkpoint < 13 and memory.main.get_map() == 120:
                checkpoint = 13
            elif checkpoint < 20 and memory.main.get_map() == 127:
                checkpoint = 20
            elif checkpoint < 31 and memory.main.get_map() == 58:
                checkpoint = 31
    return [game_vars.self_destruct_get(), battle_count, SDencounterID]


def mid_point():
    checkpoint = 0
    while memory.main.get_map() != 115:
        if memory.main.user_control():
            pDownSlot = memory.main.get_item_slot(6)
            if memory.main.get_map() == 58:
                memory.main.full_party_format("tidkimwak")
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
            # elif checkpoint == 2 and memory.main.getItemCountSlot(pDownSlot) >= 10:
            #    checkpoint = 4
            elif checkpoint in [2, 3]:
                checkpoint = 4
            elif checkpoint == 5:
                FFXC.set_movement(0, -1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint = 4
            elif pathing.set_movement(pathing.miihen_agency(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.battle_active():
                FFXC.set_neutral()
                print("Mi'ihen - ready for Chocobo Eater")
                battle.boss.chocobo_eater()
                print("Mi'ihen - Chocobo Eater complete")


# Starts just after the save sphere.
def low_road(self_destruct, battle_count, sd_encounter_id):
    checkpoint = 0
    post_battle_logic(force_charge=True)
    while memory.main.get_map() != 79:
        if memory.main.user_control():
            # Utility stuff
            if checkpoint == 2:
                save_sphere.touch_and_go()
                checkpoint += 1
            elif checkpoint == 26 and not game_vars.self_destruct_get():
                checkpoint = 24
            elif checkpoint == 34:  # Talk to guard, then Seymour
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 0.2)
                memory.main.click_to_control()
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(30 * 4)
                FFXC.set_neutral()
                checkpoint += 1

            # Map changes
            elif checkpoint < 17 and memory.main.get_map() == 116:
                checkpoint = 17
            elif checkpoint < 28 and memory.main.get_map() == 59:
                checkpoint = 28

            # General pathing
            elif pathing.set_movement(pathing.low_road(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 25:  # Shelinda dialog
                xbox.tap_b()
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle_count += 1
                print("Starting battle")
                battle.main.miihen_road()
                print("Battle complete")
                post_battle_logic(force_charge=True)
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                if checkpoint < 6 or checkpoint > 12:
                    xbox.tap_b()
    # logs.write_stats('Miihen encounters:')
    # logs.write_stats(battle_count)


def wrap_up():
    print("Now ready to meet Seymour")
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 5)
    FFXC.set_neutral()

    memory.main.click_to_control()
    FFXC.set_movement(0, 1)
    xbox.skip_dialog(4.5)
    FFXC.set_neutral()
    xbox.skip_dialog(2.5)
    FFXC.set_movement(0, -1)
    xbox.skip_dialog(12)
    FFXC.set_neutral()
    memory.main.click_to_control()  # Seymour scene
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 12)
    FFXC.set_neutral()
