import battle.main
import logs
import memory.main
import menu
import targetPathing
import vars
import xbox

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def path():
    memory.main.click_to_control()
    memory.main.close_menu()
    memory.main.full_party_format("djose")
    memory.main.close_menu()

    countBattles = 0
    checkpoint = 0
    lastCP = 0
    stoneBreath = 0
    print("Starting Djose pathing section")

    while memory.main.get_map() != 81:  # All the way into the temple
        if lastCP != checkpoint:
            print("Checkpoint reached:", checkpoint)
            lastCP = checkpoint

        if memory.main.user_control():
            if checkpoint in [45, 46] and stoneBreath == 1:
                checkpoint = 47
            elif checkpoint == 47 and stoneBreath == 0:
                checkpoint = 44  # Need to re-confirm.
            # The Djose skip pathing file was removed in commit f18ca78 (PR91)
            # This is for the attempted Djose skip. It is not yet viable. Feel free to re-try this.
            # elif checkpoint == 33:  # and stoneBreath == 0: #Turn/talk
            #     FFXC.set_movement(-1, 1)
            #     memory.main.waitFrames(4)
            #     while memory.main.userControl() and memory.main.getActorCoords(11)[1] < 790:
            #         xbox.tapB()
            #     FFXC.set_neutral()
            #     checkpoint += 1
            # elif checkpoint == 34:  # and stoneBreath == 0:
            #     while memory.main.getActorCoords(0)[1] < 790 and \
            #             memory.main.getActorCoords(11)[1] < 790:
            #         memory.main.waitFrames(1)
            #     memory.main.clickToControl3()
            #     checkpoint += 1
            else:
                # Map changes
                if memory.main.get_map() == 76 and checkpoint < 49:
                    checkpoint = 50
                if checkpoint in [49, 54, 56]:
                    memory.main.click_to_event_temple(0)
                    checkpoint += 1
                elif (
                    targetPathing.djose_path(checkpoint)[0]
                    < memory.main.get_actor_coords(0)[0]
                    and checkpoint < 46
                    and checkpoint > 18
                ):
                    checkpoint += 1
                elif (
                    targetPathing.djose_path(checkpoint)[1]
                    < memory.main.get_actor_coords(0)[1]
                    and checkpoint < 46
                    and checkpoint > 18
                ):
                    checkpoint += 1
                # General pathing
                elif targetPathing.set_movement(targetPathing.djose_path(checkpoint)):
                    checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                print("Starting battle")
                if stoneBreath == 0:
                    print("Still looking for Stone Breath.")
                stoneBreath = battle.main.djose(stoneBreath)
                print("Battles complete.")
                countBattles += 1
            elif memory.main.menu_open():
                xbox.menu_b()
            elif memory.main.diag_skip_possible():
                xbox.menu_b()

    # logs.writeStats("Djose battles:")
    # logs.writeStats(countBattles)


def temple():
    memory.main.click_to_control()
    menu.djose_temple()
    if not game_vars.csr():
        FFXC.set_movement(0, -1)
        memory.main.wait_frames(30 * 0.3)
        FFXC.set_movement(-1, -1)
        memory.main.click_to_event()  # Talk to Auron
        memory.main.wait_frames(30 * 0.2)
        memory.main.click_to_control_3()  # Done talking

    checkpoint = 0
    while not memory.main.get_map() == 214:
        target = [[-1, 32], [-1, 111], [-1, 111], [-1, 200]]
        if checkpoint == 2:
            memory.main.click_to_event_temple(0)
            checkpoint += 1
        elif memory.main.user_control():
            if targetPathing.set_movement(target[checkpoint]):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def trials():
    print("Starting Trials section.")
    memory.main.click_to_control()

    checkpoint = 0
    while memory.main.get_map() != 90:
        if memory.main.user_control():
            if checkpoint == 1:  # First sphere
                print("First sphere")
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 3:  # Sphere door
                print("Sphere door")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 5:  # Second sphere
                print("Second sphere")
                memory.main.click_to_event_temple(3)
                checkpoint += 1
            elif checkpoint == 7:  # Sphere door opens
                print("Sphere door opens")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 13:  # Left Sphere
                print("Left sphere")
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 16:  # Insert Left Sphere
                print("Insert left sphere")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 19:  # Right Sphere
                print("Right sphere")
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 22:
                print("Pushing pedestal")
                FFXC.set_movement(1, 0)
                memory.main.await_event()
                while memory.main.get_actor_coords(0)[0] < 62:
                    FFXC.set_movement(1, 0)
                FFXC.set_neutral()
                memory.main.wait_frames(15)
                print("Push complete.")
                checkpoint += 1
                print("Insert right sphere")
                memory.main.click_to_event_temple(0)
                FFXC.set_movement(-1, 1)
                memory.main.wait_frames(30 * 0.2)
                checkpoint += 1
            elif checkpoint == 24:  # Insert Right Sphere
                print("Insert right sphere")
                memory.main.click_to_event_temple(1)
                checkpoint = 27
            elif checkpoint == 28:
                print("Left sphere")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 31 or checkpoint == 56:  # Reset switch event
                print("Reset switch")
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 34:
                print("Insert left sphere")
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 38:
                print("Powered sphere")
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 40:
                print("Insert powered sphere")
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 43:
                print("Right sphere")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 45:
                print("Insert right sphere")
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 48:  # All of the hidden room stuff at once
                print("Pushing pedestal")
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                memory.main.wait_frames(30 * 9)
                print("Push complete.")
                memory.main.await_control()
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 0.4)
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 0.5)
                memory.main.await_control()
                print("Extra pedestal")
                FFXC.set_movement(0, 1)
                xbox.skip_dialog(2)
                FFXC.set_neutral()
                memory.main.await_control()
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(30 * 0.8)
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 0.5)
                checkpoint += 1
            elif checkpoint == 51:
                print("Powered sphere")
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 53:
                print("Insert powered sphere")
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 58:
                print("Left sphere")
                while memory.main.user_control():
                    targetPathing.set_movement([-5, 24])
                    memory.main.wait_frames(3)
                    FFXC.set_neutral()
                    memory.main.wait_frames(3)
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 63:
                print("Final insert Left sphere")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 68:
                print("Right sphere")
                while memory.main.user_control():
                    targetPathing.set_movement([5, 24])
                    memory.main.wait_frames(3)
                    FFXC.set_neutral()
                    memory.main.wait_frames(3)
                    xbox.tap_b()
                    memory.main.wait_frames(3)
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 73:
                print("Final insert Right sphere")
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 76:  # No longer doing Destruction Sphere stuff.
                checkpoint = 85
            elif checkpoint == 80:
                print("Destruction Glyph")
                while memory.main.user_control():
                    targetPathing.set_movement([-58, 38])
                    memory.main.wait_frames(3)
                    FFXC.set_neutral()
                    memory.main.wait_frames(4)
                    xbox.tap_b()
                    memory.main.wait_frames(3)
                FFXC.set_neutral()
                print("Glyph touched.")
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 82:
                print("Destruction sphere")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 85:  # Lift
                if targetPathing.set_movement([0, 30]):
                    FFXC.set_neutral()
                    memory.main.wait_frames(30 * 0.2)
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            elif checkpoint == 88:
                print("Pedestal 1")
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 90:
                print("Pedestal 2")
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 92:
                print("Pedestal 3")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 94:
                print("Pedestal 4")
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 96:
                print("Pedestal 5")
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 100:
                checkpoint += 2
            elif checkpoint == 102:
                checkpoint += 1
            elif checkpoint == 104:
                print("End of Trials")
                if game_vars.csr():
                    FFXC.set_movement(-1, 1)
                    memory.main.await_event()
                    FFXC.set_neutral()
                    break
                else:
                    memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif targetPathing.set_movement(targetPathing.djose_trials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

    FFXC.set_neutral()
    if not game_vars.csr():
        memory.main.await_control()
        memory.main.wait_frames(30 * 0.3)
        print("Talk to Auron while we wait.")
        FFXC.set_movement(1, -1)
        memory.main.click_to_event()
        FFXC.set_movement(-1, -1)
        memory.main.click_to_control_3()
        memory.main.wait_frames(30 * 0.07)

        # Dance
        checkpoint = 0
        while memory.main.user_control():
            if targetPathing.set_movement(targetPathing.djose_dance(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

            if checkpoint == 8:
                checkpoint = 0

        memory.main.click_to_control()
        print("Leaving the fayth room")

        FFXC.set_movement(1, 1)
        memory.main.await_event()
        FFXC.set_neutral()

    xbox.name_aeon("Ixion")


def leaving_djose():
    memory.main.await_control()

    checkpoint = 0
    lastCP = 0
    while memory.main.get_map() != 75:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if memory.main.user_control():
            if checkpoint == 1:
                if not game_vars.csr():
                    FFXC.set_movement(1, 0)
                    memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif (
                checkpoint == 11
            ):  # and not gameVars.skipKilikaLuck(): #Do we need this chest for kilika luck skip? I think not.
                checkpoint = 13
            elif checkpoint in [3, 9, 12]:
                memory.main.click_to_event_temple(0)
                if checkpoint == 9:
                    checkpoint = 35
                else:
                    checkpoint += 1
            elif checkpoint == 14:
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 18:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint in [22, 29]:
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint == 36:
                while memory.main.user_control():
                    targetPathing.set_movement([-18, 35])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint = 13
            elif targetPathing.set_movement(targetPathing.djose_exit(checkpoint)):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()

    FFXC.set_neutral()
