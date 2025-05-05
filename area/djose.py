import logging

import battle.main
import memory.main
import menu
import pathing
from pathing import approach_coords
import vars
import xbox
from paths import DjoseDance, DjoseExit, DjosePath, DjoseTrials
from players import Auron, Tidus, Wakka
from area.dream_zan import split_timer

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def path():
    memory.main.click_to_control()
    if game_vars.story_mode():
        menu.equip_weapon(character=2, ability=0x8002, full_menu_close=False)
    memory.main.update_formation(Tidus, Wakka, Auron)
    memory.main.close_menu()

    count_battles = 0
    checkpoint = 0
    last_cp = 0
    stone_breath = 0
    logger.info("Starting Djose pathing section")

    while memory.main.get_map() != 76:  # All the way into the temple
        if last_cp != checkpoint:
            logger.debug(f"Checkpoint {checkpoint}")
            last_cp = checkpoint

        if memory.main.user_control():
            if checkpoint in [47, 48] and stone_breath == 1:
                checkpoint = 49
            elif checkpoint == 49 and stone_breath == 0:
                checkpoint = 47
            # This is for the fabled Djose skip and not yet viable. Feel free to re-try.
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
                #elif (
                #    DjosePath.execute(checkpoint)[0]
                #    < memory.main.get_actor_coords(0)[0]
                #    and checkpoint < 48
                #    and checkpoint > 18
                #):
                #    checkpoint += 1
                #elif (
                #    DjosePath.execute(checkpoint)[1]
                #    < memory.main.get_actor_coords(0)[1]
                #    and checkpoint < 49
                #    and checkpoint > 18
                #):
                #    checkpoint += 1
                # General pathing
                elif pathing.set_movement(DjosePath.execute(checkpoint)):
                    checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                logger.debug("Starting battle")
                if stone_breath == 0:
                    logger.debug("Still looking for Stone Breath.")
                stone_breath = battle.main.djose(stone_breath, battle_count=count_battles)
                logger.debug("Battles complete.")
                count_battles += 1
            elif memory.main.menu_open():
                xbox.menu_b()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.menu_b()
    split_timer()
    
    while memory.main.get_map() != 81:  # All the way into the temple
        if last_cp != checkpoint:
            logger.debug(f"Checkpoint {checkpoint}")
            last_cp = checkpoint

        if memory.main.user_control():
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
                stone_breath = battle.main.djose(stone_breath, battle_count=count_battles)
                logger.debug("Battles complete.")
                count_battles += 1
            elif memory.main.menu_open():
                xbox.menu_b()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.menu_b()

    # logs.write_stats("Djose battles:")
    # logs.write_stats(count_battles)


def temple():
    logger.info("Djose Temple.")
    memory.main.click_to_control()
    if not game_vars.mrr_skip_val:
        menu.djose_temple()
    if not game_vars.csr():
        FFXC.set_movement(0, -1)
        memory.main.wait_frames(30 * 0.3)
        FFXC.set_movement(-1, -1)
        memory.main.click_to_event()  # Talk to Auron
        memory.main.wait_frames(30 * 0.2)
        memory.main.click_to_control()  # Done talking

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
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()


def trials(destro:bool=False):
    logger.info("Starting Trials section.")
    if game_vars.story_mode():
        destro = True
    memory.main.click_to_control()

    checkpoint = 0
    while memory.main.get_map() != 90:
        if memory.main.user_control():
            if checkpoint == 1:  # First sphere
                logger.info("First sphere")
                approach_coords([-34,-221])
                checkpoint += 1
            elif checkpoint == 3:  # Sphere door
                logger.info("Sphere door")
                approach_coords([-3,-185])
                checkpoint += 1
            elif checkpoint == 5:  # Second sphere
                logger.info("Second sphere")
                approach_coords([34,-221])
                checkpoint += 1
            elif checkpoint == 7:  # Sphere door opens
                logger.info("Sphere door opens")
                approach_coords([3,-185])
                checkpoint += 1
            elif checkpoint == 13:  # Left Sphere
                logger.info("Left sphere")
                approach_coords([-24,48])
                checkpoint += 1
            elif checkpoint == 16:  # Insert Left Sphere
                logger.info("Insert left sphere")
                approach_coords([68,36])
                checkpoint += 1
            elif checkpoint == 19:  # Right Sphere
                logger.info("Right sphere")
                approach_coords([24,48])
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
                approach_coords([58,36])
                FFXC.set_movement(-1, 1)
                memory.main.wait_frames(30 * 0.2)
                checkpoint += 1
            elif checkpoint == 24:  # Insert Right Sphere
                logger.info("Insert right sphere, left spot.")
                approach_coords([58,36])
                checkpoint = 27
            elif checkpoint == 28:
                logger.info("Pick up from left spot")
                FFXC.set_neutral()
                approach_coords([58,36])
                checkpoint += 1
            elif checkpoint == 31 or checkpoint == 56:  # Reset switch event
                logger.info("Reset switch")
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 34:
                logger.info("Insert left sphere")
                approach_coords([-4,24])
                checkpoint += 1
            elif checkpoint == 38:
                logger.info("Powered sphere")
                approach_coords([4,24])
                checkpoint += 1
            elif checkpoint == 40:
                logger.info("Insert powered sphere")
                approach_coords([24,48])
                checkpoint += 1
            elif checkpoint == 43:
                logger.info("Right sphere")
                approach_coords([68,36])
                checkpoint += 1
            elif checkpoint == 45:
                logger.info("Insert right sphere")
                approach_coords([4,24])
                checkpoint += 1
            elif checkpoint == 48:  # All of the hidden room stuff at once
                logger.info("Pushing pedestal")
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                memory.main.wait_frames(270)  # Nine seconds of pushing.
                logger.info("Push complete.")
                memory.main.await_control()
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(15)
                FFXC.set_neutral()
                memory.main.wait_frames(60)  # Initiates the jump animation.
                memory.main.await_control()
                memory.main.wait_frames(2)
                logger.info("Extra pedestal")
                approach_coords([1,180])  # Pushes pedestol.
                FFXC.set_neutral()
                memory.main.await_control()
                while not pathing.set_movement([1,74]):  # Jumps all the way back.
                    pass
                checkpoint += 1
            elif checkpoint == 51:
                logger.info("Powered sphere")
                approach_coords([24,48])
                checkpoint += 1
            elif checkpoint == 53:
                logger.info("Insert powered sphere")
                approach_coords([-24,48])
                checkpoint += 1
            elif checkpoint == 58:
                logger.info("Left sphere")
                approach_coords([-4,24])
                checkpoint += 1
            elif checkpoint == 63:
                logger.info("Final insert Left sphere")
                approach_coords([-34,-221])
                checkpoint += 1
            elif checkpoint == 68:
                logger.info("Right sphere")
                approach_coords([4,24])
                checkpoint += 1
            elif checkpoint == 73:
                logger.info("Final insert Right sphere")
                approach_coords([34,-221])
                checkpoint += 1
            elif checkpoint == 76 and not destro:  # No longer doing Destruction Sphere stuff.
                checkpoint = 85
            elif checkpoint == 80:
                logger.info("Destruction Glyph")
                approach_coords([-60,34])
                checkpoint += 1
            elif checkpoint == 82:
                logger.info("Destruction sphere")
                approach_coords([-64,65])
                checkpoint += 1
            elif checkpoint == 85:  # Lift
                if pathing.set_movement([0, 30]):
                    FFXC.set_neutral()
                    memory.main.wait_frames(6)
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
            elif checkpoint == 88:
                logger.info("Pedestal 1")
                approach_coords([-27,117])
                checkpoint += 1
            elif checkpoint == 90:
                logger.info("Pedestal 2")
                approach_coords([-23,148])
                checkpoint += 1
            elif checkpoint == 92:
                logger.info("Pedestal 3")
                approach_coords([0,162])
                checkpoint += 1
            elif checkpoint == 94:
                logger.info("Pedestal 4")
                approach_coords([23,148])
                checkpoint += 1
            elif checkpoint == 96:
                logger.info("Pedestal 5")
                approach_coords([27,117])
                checkpoint += 1
            elif checkpoint == 100:
                if destro:
                    approach_coords([0,71])
                    FFXC.set_neutral()
                    memory.main.click_to_control()
                    checkpoint += 1
                else:
                    checkpoint += 2
            elif checkpoint == 102:
                if destro:
                    approach_coords([24,40])
                checkpoint += 1
            elif checkpoint == 104:
                if memory.main.get_story_progress() > 2000:
                    FFXC.set_movement(-1, 1)
                    memory.main.await_event()
                    FFXC.set_neutral()
                    return
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
                logger.debug(f"Checkpoint {checkpoint}")

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
                logger.debug(f"Checkpoint {checkpoint}")

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
            logger.debug(f"Checkpoint {checkpoint}")
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
                # if checkpoint == 9:
                #    checkpoint = 35
                # else:
                checkpoint += 1
            elif checkpoint == 14:
                FFXC.set_movement(1,0)
                while memory.main.user_control():
                    xbox.tap_confirm()
                memory.main.click_to_control()
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
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()

    FFXC.set_neutral()
