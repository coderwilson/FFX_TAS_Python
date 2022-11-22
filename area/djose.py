import logging

import battle.main
import logs
import memory.main
import menu
import pathing
import vars
import xbox
from paths import DjoseDance, DjoseExit, DjosePath, DjoseTrials
from players import Auron, CurrentPlayer, Kimahri, Lulu, Rikku, Tidus, Wakka, Yuna

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def path():
    memory.main.click_to_control()
    memory.main.close_menu()
    memory.main.update_formation(Tidus, Wakka, Auron)
    memory.main.close_menu()

    count_battles = 0
    checkpoint = 0
    last_cp = 0
    stone_breath = 0
    logger.info("Starting Djose pathing section")

    while memory.main.get_map() != 81:  # All the way into the temple
        if last_cp != checkpoint:
            logger.debug(f"Checkpoint reached: {checkpoint}")
            last_cp = checkpoint

        if memory.main.user_control():
            if checkpoint in [47, 48] and stone_breath == 1:
                checkpoint = 49
            elif checkpoint == 49 and stone_breath == 0:
                checkpoint = 47
            # This is for the attempted Djose skip. It is not yet viable. Feel free to re-try this.
            elif checkpoint == 42 and game_vars.try_djose_skip():
                FFXC.set_movement(-1, 1)
                memory.main.wait_frames(2)
                xbox.tap_b()
                FFXC.set_movement(-1, 1)
                memory.main.wait_frames(1)
                xbox.tap_b()
                FFXC.set_neutral()
                while (
                    memory.main.user_control()
                    and memory.main.get_actor_coords(11)[1] < 790
                ):
                    xbox.tap_b()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 43 and game_vars.try_djose_skip():
                while (
                    memory.main.get_actor_coords(0)[1] < 790
                    and memory.main.get_actor_coords(11)[1] < 790
                ):
                    memory.main.wait_frames(1)
                memory.main.click_to_control_3()
                checkpoint += 1
            else:
                # Map changes
                if memory.main.get_map() == 76 and checkpoint < 51:
                    checkpoint = 52
                if checkpoint in [51, 56, 58]:
                    memory.main.click_to_event_temple(0)
                    checkpoint += 1
                elif (
                    DjosePath.execute(checkpoint)[0]
                    < memory.main.get_actor_coords(0)[0]
                    and checkpoint < 48
                    and checkpoint > 18
                ):
                    checkpoint += 1
                elif (
                    DjosePath.execute(checkpoint)[1]
                    < memory.main.get_actor_coords(0)[1]
                    and checkpoint < 48
                    and checkpoint > 18
                ):
                    checkpoint += 1
                # General pathing
                elif pathing.set_movement(DjosePath.execute(checkpoint)):
                    checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                logger.debug("Starting battle")
                if stone_breath == 0:
                    logger.debug("Still looking for Stone Breath.")
                stone_breath = battle.main.djose(stone_breath)
                logger.debug("Battles complete.")
                count_battles += 1
            elif memory.main.menu_open():
                xbox.menu_b()
            elif memory.main.diag_skip_possible():
                xbox.menu_b()

    # logs.write_stats("Djose battles:")
    # logs.write_stats(count_battles)


def temple():
    logger.info("Djose Temple.")
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
            if pathing.set_movement(target[checkpoint]):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def trials():
    logger.info("Starting Trials section.")
    memory.main.click_to_control()

    checkpoint = 0
    while memory.main.get_map() != 90:
        if memory.main.user_control():
            if checkpoint == 1:  # First sphere
                logger.info("First sphere")
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 3:  # Sphere door
                logger.info("Sphere door")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 5:  # Second sphere
                logger.info("Second sphere")
                memory.main.click_to_event_temple(3)
                checkpoint += 1
            elif checkpoint == 7:  # Sphere door opens
                logger.info("Sphere door opens")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 13:  # Left Sphere
                logger.info("Left sphere")
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 16:  # Insert Left Sphere
                logger.info("Insert left sphere")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 19:  # Right Sphere
                logger.info("Right sphere")
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 22:
                logger.info("Pushing pedestal")
                FFXC.set_movement(1, 0)
                memory.main.await_event()
                while memory.main.get_actor_coords(0)[0] < 62:
                    FFXC.set_movement(1, 0)
                FFXC.set_neutral()
                memory.main.wait_frames(15)
                logger.info("Push complete.")
                checkpoint += 1
                logger.info("Insert right sphere")
                memory.main.click_to_event_temple(0)
                FFXC.set_movement(-1, 1)
                memory.main.wait_frames(30 * 0.2)
                checkpoint += 1
            elif checkpoint == 24:  # Insert Right Sphere
                logger.info("Insert right sphere")
                memory.main.click_to_event_temple(1)
                checkpoint = 27
            elif checkpoint == 28:
                logger.info("Left sphere")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 31 or checkpoint == 56:  # Reset switch event
                logger.info("Reset switch")
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 34:
                logger.info("Insert left sphere")
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 38:
                logger.info("Powered sphere")
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 40:
                logger.info("Insert powered sphere")
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 43:
                logger.info("Right sphere")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 45:
                logger.info("Insert right sphere")
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 48:  # All of the hidden room stuff at once
                logger.info("Pushing pedestal")
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                memory.main.wait_frames(30 * 9)
                logger.info("Push complete.")
                memory.main.await_control()
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 0.4)
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 0.5)
                memory.main.await_control()
                logger.info("Extra pedestal")
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
                logger.info("Powered sphere")
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 53:
                logger.info("Insert powered sphere")
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 58:
                logger.info("Left sphere")
                while memory.main.user_control():
                    pathing.set_movement([-5, 24])
                    memory.main.wait_frames(3)
                    FFXC.set_neutral()
                    memory.main.wait_frames(3)
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 63:
                logger.info("Final insert Left sphere")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 68:
                logger.info("Right sphere")
                while memory.main.user_control():
                    pathing.set_movement([5, 24])
                    memory.main.wait_frames(3)
                    FFXC.set_neutral()
                    memory.main.wait_frames(3)
                    xbox.tap_b()
                    memory.main.wait_frames(3)
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 73:
                logger.info("Final insert Right sphere")
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 76:  # No longer doing Destruction Sphere stuff.
                checkpoint = 85
            elif checkpoint == 80:
                logger.info("Destruction Glyph")
                while memory.main.user_control():
                    pathing.set_movement([-58, 38])
                    memory.main.wait_frames(3)
                    FFXC.set_neutral()
                    memory.main.wait_frames(4)
                    xbox.tap_b()
                    memory.main.wait_frames(3)
                FFXC.set_neutral()
                logger.info("Glyph touched.")
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 82:
                logger.info("Destruction sphere")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 85:  # Lift
                if pathing.set_movement([0, 30]):
                    FFXC.set_neutral()
                    memory.main.wait_frames(30 * 0.2)
                    checkpoint += 1
                    logger.debug(f"Checkpoint reached: {checkpoint}")
            elif checkpoint == 88:
                logger.info("Pedestal 1")
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 90:
                logger.info("Pedestal 2")
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 92:
                logger.info("Pedestal 3")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 94:
                logger.info("Pedestal 4")
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 96:
                logger.info("Pedestal 5")
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 100:
                checkpoint += 2
            elif checkpoint == 102:
                checkpoint += 1
            elif checkpoint == 104:
                logger.info("End of Trials")
                if game_vars.csr():
                    FFXC.set_movement(-1, 1)
                    memory.main.await_event()
                    FFXC.set_neutral()
                    break
                else:
                    memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif pathing.set_movement(DjoseTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")

    FFXC.set_neutral()
    if not game_vars.csr():
        memory.main.await_control()
        memory.main.wait_frames(30 * 0.3)
        logger.info("Talk to Auron while we wait.")
        FFXC.set_movement(1, -1)
        memory.main.click_to_event()
        FFXC.set_movement(-1, -1)
        memory.main.click_to_control_3()
        memory.main.wait_frames(30 * 0.07)

        # Dance
        checkpoint = 0
        while memory.main.user_control():
            if pathing.set_movement(DjoseDance.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")

            if checkpoint == 8:
                checkpoint = 0

        memory.main.click_to_control()
        logger.info("Leaving the fayth room")

        while not pathing.set_movement([-1, -61]):
            pass
        FFXC.set_movement(1, 1)
        memory.main.await_event()
        FFXC.set_neutral()

    xbox.name_aeon("Ixion")


def leaving_djose():
    memory.main.await_control()

    checkpoint = 0
    last_cp = 0
    while memory.main.get_map() != 75:
        if last_cp != checkpoint:
            logger.debug(f"Checkpoint reached: {checkpoint}")
            last_cp = checkpoint
        if memory.main.user_control():
            if checkpoint == 1:
                if not game_vars.csr():
                    FFXC.set_movement(1, 0)
                    memory.main.click_to_event_temple(6)
                checkpoint += 1
            # Do we need this chest for kilika luck skip? I think not.
            elif checkpoint == 11:  # and not game_vars.skip_kilika_luck():
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
                    pathing.set_movement([-18, 35])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint = 13
            elif pathing.set_movement(DjoseExit.execute(checkpoint)):
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
