import battle.boss
import battle.main
import memory.main
import menu
import screen
import targetPathing
import vars
import xbox

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def arrival():
    print("Starting Moonflow section")

    checkpoint = 0
    while memory.main.get_map() != 235:
        if memory.main.user_control():
            # Chests
            if checkpoint == 2:  # Gil outside Djose temple
                print("Djose gil chest")
                FFXC.set_movement(-1, 1)
                xbox.skip_dialog(1)
                FFXC.set_movement(1, -1)
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 43:  # Moonflow chest
                if memory.main.get_item_slot(90) < 200:
                    checkpoint += 1
                else:
                    targetPathing.set_movement([-1796, -480])
                    xbox.tap_b()

            # Map changes
            elif checkpoint < 6 and memory.main.get_map() == 76:
                checkpoint = 6
            elif checkpoint < 11 and memory.main.get_map() == 93:
                checkpoint = 11
            elif checkpoint < 14 and memory.main.get_map() == 75:
                checkpoint = 14
            elif checkpoint < 49 and memory.main.get_map() == 105:
                checkpoint = 49
            elif checkpoint < 54 and memory.main.get_story_progress() == 1045:
                checkpoint = 54
                print("Updating checkpoint based on story/map progress:", checkpoint)
            elif checkpoint == 54 and memory.main.get_map() == 188:
                checkpoint = 55
                print("Updating checkpoint based on story/map progress:", checkpoint)

            # General pathing
            elif targetPathing.set_movement(targetPathing.moonflow(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle.main.flee_all()
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
    print("End of approaching section, should now be talking to Lucille/Elma/etc.")


def south_bank(checkpoint: int = 0):
    # Arrive at the south bank of the moonflow.
    print("South bank, Save sphere screen")

    memory.main.click_to_control_3()  # "Where there's a will, there's a way."
    FFXC.set_movement(1, -1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_neutral()

    memory.main.click_to_control_3()
    partyHP = memory.main.get_hp()
    if partyHP[4] < 800:
        battle.main.heal_up(2)
    elif partyHP[0] < 700:
        battle.main.heal_up(1)
    memory.main.close_menu()

    while not memory.main.battle_active():
        if memory.main.user_control():
            if checkpoint == 4:
                FFXC.set_neutral()
                memory.main.click_to_event()
                memory.main.wait_frames(18)
                xbox.menu_b()  # Ride ze Shoopuff?
                memory.main.wait_frames(10)
                xbox.menu_down()
                xbox.menu_b()  # All aboardz!
                xbox.skip_dialog(3)  # Just to clear some dialog

            elif targetPathing.set_movement(
                targetPathing.moonflow_bank_south(checkpoint)
            ):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

    battle.boss.extractor()


def north_bank():
    memory.main.click_to_control_3()
    FFXC.set_movement(-1, 0)
    memory.main.await_event()
    memory.main.wait_frames(30 * 1)
    memory.main.await_control()
    if game_vars.csr():
        memory.main.wait_frames(10)
        FFXC.set_movement(-1, -0.7)
        memory.main.wait_frames(6)
        FFXC.set_movement(-1, 0)
        memory.main.await_event()
    else:
        memory.main.wait_frames(45)
        memory.main.click_to_event()  # Talk to Auron
        FFXC.set_neutral()
        memory.main.wait_frames(9)
        memory.main.click_to_control_3()
    FFXC.set_movement(-1, 0)
    memory.main.wait_frames(15)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.wait_frames(15)
    if game_vars.get_l_strike() % 2 == 1:
        menu.equip_weapon(character=0, special="brotherhoodearly")

    checkpoint = 0
    print("Miihen North Bank pattern. Starts after talking to Auron.")
    while memory.main.get_map() != 135:
        if memory.main.user_control():
            if checkpoint == 7:  # Rikku steal/mix tutorial
                FFXC.set_movement(1, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                battle.main.mix_tutorial()
                memory.main.full_party_format("postbunyip")
                memory.main.close_menu()
                checkpoint += 1
            elif memory.main.get_story_progress() >= 1085 and checkpoint < 4:
                checkpoint = 4
                print("Rikku scene, updating checkpoint:", checkpoint)

            # Map changes
            elif checkpoint < 2 and memory.main.get_map() == 109:
                checkpoint = 2
            elif checkpoint < 12 and memory.main.get_map() == 97:
                checkpoint = 12

            # General pathing
            elif targetPathing.set_movement(
                targetPathing.moonflow_bank_north(checkpoint)
            ):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle.main.flee_all()
            elif memory.main.diag_skip_possible() and not memory.main.battle_active():
                xbox.tap_b()
            elif memory.main.menu_open():
                xbox.tap_b()
