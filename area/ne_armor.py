import battle.main
import logs
import memory.main
import menu
import pathing
import rng_track
import vars
import xbox
import save_sphere

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
    lastReport = False
    firstSave = False
    checkpoint = 0
    prepBattles = 0
    while memory.main.get_map() != 56:
        if memory.main.user_control():
            if checkpoint < 5 and memory.main.get_map() == 266:
                checkpoint = 5
            if checkpoint == 7 and not firstSave:
                save_sphere.touch_and_go()
                firstSave = True
            _, nextDrop = rng_track.nea_track()
            if checkpoint == 8 and (
                nextDrop >= 1 or memory.main.next_chance_rng_10() >= 9
            ):
                if not lastReport:
                    print("Need more advances before entering cave.")
                    lastReport = True
                checkpoint -= 2
            elif (
                checkpoint == 8
                and memory.main.get_item_slot(39) == 255
                and memory.main.next_chance_rng_10()
            ):
                if not lastReport:
                    print("Need more advances before cave enter | no silence grenade")
                    lastReport = True
                checkpoint -= 2
            elif checkpoint == 9:
                FFXC.set_movement(-1, 1)
            elif pathing.set_movement(pathing.ne_approach(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                _, nextDrop = rng_track.nea_track()
                lastReport = False
                print("### Starting manip battle")
                rng_track.print_manip_info()
                memory.main.wait_frames(2)
                if nextDrop >= 1:
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
                prepBattles += 1
                memory.main.full_party_format("rikku")
                save_sphere.touch_and_go()
                rngTrack.print_manip_info()
            elif memory.main.diag_skip_possible() or memory.main.menu_open():
                xbox.tap_b()
    logs.write_stats("NEA extra manip battles:")
    logs.write_stats(prepBattles)


def next_green():
    nextGreen = memory.main.next_chance_rng_01(version="green")[0][0]
    nextWhite = memory.main.next_chance_rng_01()[0][0]
    print("## Next Ghost coming up:")
    print("## Green: ", nextGreen)
    print("## White: ", nextWhite)
    if nextGreen < nextWhite and memory.main.next_chance_rng_10() == 0:
        if nextGreen >= 2:
            goGreen = True
    if game_vars.accessibilityVars()[2]:
        if goGreen:
            tts.message("Green")
            tts.message(str(nextGreen))
        else:
            tts.message("White")
            tts.message(str(nextWhite))

def drop_hunt():
    print("Now in the cave. Ready to try to get the NE armor.")
    memory.main.full_party_format("rikku")

    goGreen = next_green()

    rng_track.print_manip_info()
    checkpoint = 0
    preGhostBattles = 0
    while game_vars.ne_armor() == 255:
        if memory.main.user_control():
            if goGreen:
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
                    if checkpoint % 2 == 0 and not goGreen:
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
                    if next_green() and not goGreen:
                        goGreen = True
                    preGhostBattles += 1
                memory.main.close_menu()
            elif memory.main.diag_skip_possible() or memory.main.menu_open():
                xbox.tap_b()
    print("The NE armor hunt is complete. Char:", game_vars.ne_armor())
    logs.write_stats("Pre-Ghost flees:")
    logs.write_stats(preGhostBattles)
    logs.write_stats("NEA char:")
    logs.write_stats(game_vars.ne_armor())


def return_to_gagazet():
    unequip = False
    if memory.main.get_coords()[0] > 300:
        goGreen = True
        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
        if memory.main.overdrive_state_2()[6] != 100:
            unequip = True
    else:
        goGreen = False
        if memory.main.overdrive_state_2()[6] == 100:
            menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)

    checkpoint = 0
    while memory.main.get_map() != 259:
        if memory.main.user_control():
            if goGreen:
                if checkpoint == 10:
                    goGreen = False
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
