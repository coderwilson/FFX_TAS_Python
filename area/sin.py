import battle.boss
import battle.main
import memory.main
import menu
import targetPathing
import vars
import xbox
import zz_eggHuntAuto
import zzairShipPath

gameVars = vars.vars_handle()

FFXC = xbox.controller_handle()


def making_plans():
    memory.main.click_to_control_3()
    print("Final Push! Let's get this show on the road!!! (Highbridge)")

    # Start by touching the save sphere
    while not targetPathing.set_movement([-267, 347]):
        pass

    target = [[-242, 312], [-239, 258], [-243, 145], [-243, 10]]
    checkpoint = 0
    while memory.main.get_map() == 194:
        if memory.main.user_control():
            if targetPathing.set_movement(target[checkpoint]):
                checkpoint += 1

    zzairShipPath.air_ship_path(2)  # Talk to Yuna/Kimahri
    FFXC.set_neutral()


def shedinja():  # shelinda
    print("The hymn is the key")
    while memory.main.get_map() != 382:
        print("Mark 1")
        xbox.tap_b()
    while not memory.main.diag_progress_flag() in [4, 255]:
        print("Mark 2")
        xbox.tap_b()
    while memory.main.map_cursor() != 10:
        print("The destination is the key")
        memory.main.menu_direction(memory.main.map_cursor(), 10, 13)
    memory.main.click_to_control()

    memory.main.await_control()
    print("Moving to Shedinja")
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(45)
    FFXC.set_movement(0, 1)
    memory.main.await_event()

    FFXC.set_neutral()
    if not gameVars.csr():
        memory.main.click_to_diag_progress(100)
    memory.main.click_to_diag_progress(76)  # Have you found a way? Well?
    memory.main.wait_frames(20)
    xbox.tap_down()
    xbox.menu_b()  # We fight Yu Yevon.

    memory.main.click_to_diag_progress(74)
    memory.main.click_to_diag_progress(28)
    memory.main.click_to_control_3()


def exit_cockpit():
    print("Attempting to exit cockpit")
    while memory.main.get_map() != 265:
        if memory.main.user_control():
            tidusCoords = memory.main.get_coords()
            if tidusCoords[1] > 318:
                targetPathing.set_movement([-244, 315])
            else:
                FFXC.set_movement(0, -1)
        else:
            FFXC.set_neutral()


def facing_sin():
    while not targetPathing.set_movement([-245, 321]):
        pass

    while memory.main.user_control():
        targetPathing.set_movement([-256, 342])
        xbox.tap_b()
        memory.main.wait_frames(1)

    FFXC.set_neutral()

    if gameVars.csr():
        memory.main.click_to_control()
    else:
        # Gets us through the Airship destination menu.
        xbox.skip_dialog(15)
        while not memory.main.user_control():
            if memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.tap_b()

    if memory.main.get_map() in [255, 374]:
        exit_cockpit()
    FFXC.set_neutral()

    zzairShipPath.air_ship_path(3)
    battle.main.sin_arms()
    memory.main.click_to_control()
    print("To the deck, talk to Yuna")
    if memory.main.get_map() in [255, 374]:
        exit_cockpit()
    FFXC.set_neutral()
    memory.main.click_to_control()

    zzairShipPath.air_ship_path(4)
    FFXC.set_neutral()
    memory.main.click_to_control()

    print("To the deck, Sin's face battle.")
    if memory.main.get_map() in [255, 374]:
        exit_cockpit()
    FFXC.set_neutral()
    zzairShipPath.air_ship_path(5)
    battle.main.sin_face()
    print("End of battle with Sin's face.")


def inside_sin():
    while memory.main.get_map() != 203:  # Skip dialog and run to the sea of sorrows map
        if memory.main.cutscene_skip_possible():
            FFXC.set_neutral()
            memory.main.wait_frames(3)
            xbox.skip_scene()
        else:
            FFXC.set_movement(0, -1)
            xbox.tap_b()
    FFXC.set_neutral()

    if memory.main.overdrive_state_2()[6] != 100 and gameVars.get_nea_zone() == 3:
        reEquipNE = True
        memory.main.full_party_format("rikku", full_menu_close=False)
        menu.equip_armor(character=gameVars.ne_armor(), ability=99)
    else:
        reEquipNE = False
        memory.main.full_party_format("yuna", full_menu_close=False)
    memory.main.close_menu()

    checkpoint = 0
    while memory.main.get_map() != 324:  # All the way to the egg hunt.
        if memory.main.user_control():
            # Events
            if memory.main.get_map() == 296:  # Seymour battle
                print("We've reached the Seymour screen.")
                memory.main.full_party_format("yuna")
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 5)
                FFXC.set_neutral()
                battle.boss.omnis()
                memory.main.click_to_control()
            elif checkpoint < 41 and memory.main.get_map() == 204:
                checkpoint = 41
            elif checkpoint < 68 and memory.main.get_map() == 327:
                checkpoint = 68

            # General Pathing
            elif targetPathing.set_movement(targetPathing.inside_sin(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active() and memory.main.turn_ready():
                battle.main.charge_rikku_od()
                if reEquipNE and memory.main.overdrive_state_2()[6] == 100:
                    reEquipNE = False
                    memory.main.click_to_control()
                    memory.main.full_party_format("yuna", full_menu_close=False)
                    menu.equip_armor(character=gameVars.ne_armor(), ability=0x801D)
            elif memory.main.menu_open():
                xbox.tap_b()


def egg_hunt(auto_egg_hunt):
    # Done with pathing, now for egg hunt.
    while not memory.main.user_control():
        FFXC.set_movement(-1, -1)
    memory.main.wait_frames(30 * 0.5)
    if auto_egg_hunt:
        zz_eggHuntAuto.engage()
    else:
        print("Start of egg hunt. User control expected.")
        waitCount = 0
        while memory.main.get_map() != 325:
            memory.main.wait_frames(30 * 1)
            waitCount += 1
            if waitCount % 10 == 0:
                print("Still waiting on user to do this section. ", waitCount / 10)
    print("Done with the egg hunt. Final prep for BFA.")
    if gameVars.nemesis():
        menu.equip_weapon(character=0, ability=0x8019, full_menu_close=True)
        FFXC.set_movement(1, 1)
        memory.main.wait_frames(5)
        memory.main.await_event()
        FFXC.set_neutral()
    else:
        if gameVars.zombie_weapon() != 255 and gameVars.zombie_weapon() not in [
            0,
            1,
            2,
        ]:
            menu.equip_weapon(
                character=gameVars.zombie_weapon(),
                ability=0x8032,
                full_menu_close=False,
            )
        menu.bfa()
