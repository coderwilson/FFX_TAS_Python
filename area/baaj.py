import battle.boss
import battle.main
import memory.main
import menu
import screen
import targetPathing
import vars
import xbox
import save_sphere

FFXC = xbox.controller_handle()
game_vars = vars.vars_handle()


def entrance(checkpoint: int = 0):
    memory.main.await_control()
    print("Starting Baaj exterior area")
    FFXC.set_neutral()
    menu.short_aeons()

    # Now back into the water

    while not memory.main.battle_active():
        if memory.main.user_control():
            if checkpoint == 6:
                memory.main.click_to_event_temple(0)
                checkpoint += 1

            # General pathing
            elif targetPathing.set_movement(targetPathing.baaj_ramp(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()

    FFXC.set_neutral()

    # Battles
    while memory.main.get_story_progress() < 48:
        if screen.battle_screen():
            if memory.main.get_encounter_id() == 2:
                battle.main.attack("none")
            else:
                battle.main.defend()
        elif memory.main.diag_skip_possible():
            xbox.menu_b()

    # Out of the frying pan, into the furnace
    memory.main.click_to_control()
    print("Hallway before main puzzle.")
    checkpoint = 0
    while memory.main.get_map() != 63:
        if memory.main.user_control():
            if checkpoint == 9:
                FFXC.set_movement(-1, 1)
                memory.main.await_event()
                FFXC.set_neutral()
            # General pathing
            elif targetPathing.set_movement(targetPathing.baaj_hallway(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def baaj_puzzle():
    memory.main.click_to_control()
    print("Ready for the main puzzle.")
    checkpoint = 0
    while not memory.main.battle_active():
        if memory.main.user_control():
            # Events
            if checkpoint == 3:
                save_sphere.touch_and_go()
                checkpoint += 1
            elif checkpoint == 5:  # Flint room
                memory.main.click_to_event_temple(0)
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
                targetPathing.set_movement([1, 1])
                xbox.menu_b()

            # General pathing
            elif targetPathing.set_movement(targetPathing.baaj_puzzle(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def klikk_fight():
    # Before Rikku shows up, we're just going to spam the B button. Simple.
    FFXC.set_neutral()
    while not screen.turn_rikku():
        xbox.tap_b()

    xbox.click_to_battle()
    battle.main.use_item(0, "none")  # Tidus self-potion
    screen.await_turn()
    battle.boss.klikk()


def distance(n1, n2):
    try:
        player1 = memory.main.get_actor_coords(actor_number=n1)
        player2 = memory.main.get_actor_coords(actor_number=n2)
        return abs(player1[1] - player2[1]) + abs(player1[0] - player2[0])
    except Exception as x:
        print("Exception:", x)
        return 999


def ab_boat_1():
    print("Start of Al Bhed boat section.")
    print("Control restored.")
    print("On the boat!")
    while memory.main.get_actor_coords(actor_number=0)[0] > -50:
        rikkuNum = memory.main.actor_index(actor_num=41)
        target = memory.main.get_actor_coords(actor_number=rikkuNum)
        targetPathing.set_movement(target)
        if distance(0, rikkuNum) < 10:
            xbox.tap_b()
        elif memory.main.menu_open():
            xbox.menu_a()
            xbox.menu_b()
    print("In the water!")
    FFXC.set_value("BtnA", 1)
    while not memory.main.user_control():
        FFXC.set_value("BtnB", 1)
        memory.main.wait_frames(1)
        FFXC.set_value("BtnB", 0)
        memory.main.wait_frames(1)
    FFXC.set_value("BtnA", 1)
    FFXC.set_movement(-1, -1)
    memory.main.wait_frames(20)

    while memory.main.get_map() != 288:
        FFXC.set_value("BtnA", 1)
        FFXC.set_movement(0, -1)
        if memory.main.battle_active():
            FFXC.set_neutral()
            print("Battle Start (Al Bhed swimming section)")
            battle.main.steal_and_attack()
            print("Battle End (Al Bhed swimming section)")
        elif memory.main.menu_open() or memory.main.diag_skip_possible():
            print("Battle Complete screen")
            xbox.tap_b()


def ab_swimming_1():
    print("Swimming down from the boat")
    while memory.main.get_map() != 288:
        if memory.main.user_control():
            targetPathing.set_movement([-300, -300])
            FFXC.set_value("BtnA", 1)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                print("Battle Start (Al Bhed swimming section)")
                battle.main.steal_and_attack()
                print("Battle End (Al Bhed swimming section)")
            elif memory.main.menu_open():
                print("Battle Complete screen")
                xbox.menu_b()

    FFXC.set_neutral()
    print("Swimming towards airship")
    while memory.main.get_map() != 64:
        pos = memory.main.get_coords()
        if memory.main.user_control():
            if memory.main.get_map() == 71:
                FFXC.set_movement(0, -1)
                FFXC.set_value("BtnA", 1)
            else:
                FFXC.set_value("BtnA", 0)
                if pos[1] > -230:
                    targetPathing.set_movement([-343, -284])
                elif pos[1] > -410:
                    targetPathing.set_movement([-421, -463])
                else:
                    FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                print("Battle Start (Al Bhed swimming section)")
                battle.main.steal_and_attack()
                print("Battle End (Al Bhed swimming section)")
            elif memory.main.menu_open():
                print("Battle Complete screen")
                xbox.menu_b()


def ab_swimming_2():
    # Quick heal-up to make sure we're full HP on Rikku
    memory.main.await_control()
    FFXC.set_movement(1, -1)
    FFXC.set_value("BtnA", 1)
    save_sphere.touch_and_go()

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
    print("Technical Support Tidus")
    xbox.skip_dialog(2)
    FFXC.set_movement(0, 0)
    memory.main.click_to_control()
    while not memory.main.battle_active():
        FFXC.set_movement(0, -1)
    print("Engaging Tros")
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
                    targetPathing.set_movement([-2, 47])
                else:
                    targetPathing.set_movement([73, 1])
            elif memory.main.get_map() == 380:
                targetPathing.set_movement([700, 300])
            elif memory.main.get_map() == 71:
                rikkuNum = memory.main.actor_index(actor_num=41)
                targetPathing.set_movement(memory.main.get_actor_coords(rikkuNum))
                if distance(0, rikkuNum) < 30:
                    xbox.tap_b()
        else:
            FFXC.set_neutral()
            if memory.main.diag_progress_flag() == 109:
                memory.main.csr_baaj_save_clear()
            elif memory.main.diag_skip_possible() and not game_vars.csr():
                xbox.tap_b()

    print("Should now be ready for Besaid")

    if not game_vars.csr():
        xbox.clear_save_popup(0)
