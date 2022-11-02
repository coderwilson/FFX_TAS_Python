import battle.main
import logs
import memory.main
import menu
import pathing
import rng_track
import save_sphere
import vars
import xbox

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def loop_back_from_ronso(checkpoint=0):
    memory.main.full_party_format("rikku")
    battle.main.heal_up(full_menu_close=True)
    rng_track.print_manip_info()
    print("Looping back to the Ronso")
    while checkpoint != 18:
        if memory.main.user_control():
            if checkpoint < 13 and memory.main.get_map() == 279:
                checkpoint = 13
            elif pathing.set_movement(pathing.gagazet_nea_loop_back(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() or memory.main.menu_open():
                xbox.tap_b()


def to_hidden_cave():
    memory.main.full_party_format("rikku")
    battle.main.heal_up(full_menu_close=True)
    rng_track.print_manip_info()
    last_report = False
    first_save = False
    checkpoint = 0
    prep_battles = 0
    while memory.main.get_map() != 56:
        if memory.main.user_control():
            if checkpoint < 5 and memory.main.get_map() == 266:
                checkpoint = 5
            if checkpoint == 7 and not first_save:
                save_sphere.touch_and_go()
                first_save = True
            _, next_drop = rng_track.nea_track()
            if checkpoint == 8 and (
                next_drop >= 1 or memory.main.next_chance_rng_10() >= 9
            ):
                if not last_report:
                    print("Need more advances before entering cave.")
                    last_report = True
                checkpoint -= 2
            elif (
                checkpoint == 8
                and memory.main.get_item_slot(39) == 255
                and memory.main.next_chance_rng_10()
            ):
                if not last_report:
                    print("Need more advances before cave enter | no silence grenade")
                    last_report = True
                checkpoint -= 2
            elif checkpoint == 9:
                FFXC.set_movement(-1, 1)
            elif pathing.set_movement(pathing.ne_approach(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                _, next_drop = rng_track.nea_track()
                last_report = False
                print("### Starting manip battle")
                rng_track.print_manip_info()
                memory.main.wait_frames(2)
                if next_drop >= 1:
                    if memory.main.next_chance_rng_10() != 0:
                        battle.main.advance_rng_10(memory.main.next_chance_rng_10())
                    else:
                        battle.main.advance_rng_12()
                elif memory.main.next_chance_rng_10():
                    battle.main.advance_rng_10(memory.main.next_chance_rng_10())
                else:
                    print("Failed to determine next steps, requires dev review.")
                    print("RNG10: ", memory.main.next_chance_rng_10())
                    print("RNG12: ", memory.main.next_chance_rng_12())
                    battle.main.flee_all()
                prep_battles += 1
                memory.main.full_party_format("rikku")
                save_sphere.touch_and_go()
                rng_track.print_manip_info()
            elif memory.main.diag_skip_possible() or memory.main.menu_open():
                xbox.tap_b()
    logs.write_stats("NEA extra manip battles:")
    logs.write_stats(prep_battles)


def next_green():
    next_green = memory.main.next_chance_rng_01(version="green")[0][0]
    next_white = memory.main.next_chance_rng_01()[0][0]
    print("## Next Ghost coming up:")
    print("## Green: ", next_green)
    print("## White: ", next_white)
    if next_green < next_white and memory.main.next_chance_rng_10() == 0:
        if next_green >= 2:
            go_green = True
    if game_vars.accessibility_vars()[2]:
        if go_green:
            tts.message("Green")
            tts.message(str(next_green))
        else:
            tts.message("White")
            tts.message(str(next_white))


def drop_hunt():
    print("Now in the cave. Ready to try to get the NE armor.")
    memory.main.full_party_format("rikku")

    go_green = next_green()

    rng_track.print_manip_info()
    checkpoint = 0
    pre_ghost_battles = 0
    while game_vars.ne_armor() == 255:
        if memory.main.user_control():
            if go_green:
                if checkpoint == 15:
                    checkpoint -= 2
                elif pathing.set_movement(
                    pathing.ne_force_encounters_green(checkpoint)
                ):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            else:
                if pathing.set_movement(pathing.ne_force_encounters_white(checkpoint)):
                    checkpoint += 1
                    if checkpoint % 2 == 0 and not go_green:
                        checkpoint = 0
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if memory.main.get_encounter_id() in [319, 323]:
                    battle.main.ghost_kill()
                else:
                    battle.main.flee_all()
                memory.main.click_to_control_3()
                memory.main.full_party_format("rikku")
                battle.main.heal_up(full_menu_close=False)
                memory.main.check_nea_armor()
                if game_vars.ne_armor() == 255:
                    if next_green() and not go_green:
                        go_green = True
                    pre_ghost_battles += 1
                memory.main.close_menu()
            elif memory.main.diag_skip_possible() or memory.main.menu_open():
                xbox.tap_b()
    print("The NE armor hunt is complete. Char:", game_vars.ne_armor())
    logs.write_stats("Pre-Ghost flees:")
    logs.write_stats(pre_ghost_battles)
    logs.write_stats("NEA char:")
    logs.write_stats(game_vars.ne_armor())


def return_to_gagazet():
    unequip = False
    if memory.main.get_coords()[0] > 300:
        go_green = True
        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
        if memory.main.overdrive_state_2()[6] != 100:
            unequip = True
    else:
        go_green = False
        if memory.main.overdrive_state_2()[6] == 100:
            menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)

    checkpoint = 0
    while memory.main.get_map() != 259:
        if memory.main.user_control():
            if go_green:
                if checkpoint == 10:
                    go_green = False
                    checkpoint = 0
                elif pathing.set_movement(pathing.ne_return_green(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            elif checkpoint < 1 and memory.main.get_map() == 266:
                checkpoint = 1
            elif checkpoint == 2 and unequip:
                menu.equip_armor(character=game_vars.ne_armor(), ability=99)
                unequip = False
            elif checkpoint == 2:
                save_sphere.touch_and_go()
                checkpoint += 1
            elif checkpoint < 7 and memory.main.get_map() == 279:
                checkpoint = 7
            elif pathing.set_movement(pathing.ne_return(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            elif memory.main.diag_skip_possible() or memory.main.menu_open():
                xbox.tap_b()
