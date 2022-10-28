import area.gagazet
import battle.main
import memory.main
import nemesis.targetPath
import vars
import xbox

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


# The following functions replace the default ones from the regular Bahamut run.


def arena_npc():
    memory.main.await_control()
    if memory.main.get_map() != 307:
        return
    while not (
        memory.main.diag_progress_flag() == 74 and memory.main.diag_skip_possible()
    ):
        if memory.main.user_control():
            if memory.main.get_coords()[1] > -12:
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(1)
            else:
                nemesis.targetPath.set_movement([2, -15])
                xbox.tap_b()
        else:
            FFXC.set_neutral()
            if memory.main.diag_progress_flag() == 59:
                xbox.menu_a()
                xbox.menu_a()
                xbox.menu_a()
                xbox.menu_a()
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
    memory.main.wait_frames(3)


def next_race():
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(28)
    memory.main.wait_frames(9)
    xbox.tap_b()


def calm_lands():
    # Start chocobo races
    # memory.setGameSpeed(2)
    calm_lands_1()

    FFXC.set_neutral()
    memory.main.click_to_diag_progress(28)
    memory.main.wait_frames(9)
    xbox.tap_b()
    # memory.setGameSpeed(0)
    wobblyComplete = False
    while not wobblyComplete:
        wobblyComplete = choco_tame_1()

    print("Wobbly Chocobo complete")
    # nextRace()
    # dodgerComplete = False
    # while not dodgerComplete:
    #     dodgerComplete = chocoTame2()

    # print("Dodger Chocobo complete")
    # nextRace()

    # hyperComplete = False
    # while not hyperComplete:
    #     hyperComplete = chocoTame3()

    # print("Hyper Chocobo complete")

    # catcherComplete = False
    # while not catcherComplete:
    #     catcherComplete = chocoTame4()

    print("Catcher Chocobo complete")

    to_remiem()


def calm_lands_1():
    # Enter the cutscene that starts Calm Lands
    memory.main.full_party_format("yuna", full_menu_close=True)
    while not (memory.main.get_coords()[1] >= -1650 and memory.main.user_control()):
        if memory.main.user_control():
            FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

    # Now head to the chocobo lady.
    # memory.setEncounterRate(0) #Testing only
    checkpoint = 0
    while memory.main.get_map() != 307:
        if memory.main.user_control():
            # if checkpoint == 10:
            #     if area.gagazet.checkGems() < 2:
            #         checkpoint -= 2
            if (
                nemesis.targetPath.set_movement(
                    nemesis.targetPath.calm_lands_1(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if area.gagazet.check_gems() < 2:
                    battle.main.calm_lands_gems()
                else:
                    battle.main.calm_lands_manip()
                memory.main.full_party_format("yuna")
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()

    print("Now talk to NPC")
    # arenaNPC()
    # arenaPurchase()
    # memory.waitFrames(6)
    # xbox.tapB() #I want to ride a chocobo.


def choco_tame_1():
    memory.main.click_to_diag_progress(43)
    while not memory.main.diag_progress_flag() in [44, 74]:
        angle = memory.main.get_actor_angle(0)
        # print("Angle: ", retVal)
        position = memory.main.get_actor_coords(0)
        # print("Position: ", position)
        if position[0] < -110:  # Need to move right
            if angle > 1.4:
                FFXC.set_value("Dpad", 8)
            elif angle < 1.2:
                FFXC.set_value("Dpad", 4)
            else:
                FFXC.set_value("Dpad", 0)
        elif position[0] > -60:  # Need to move left
            if angle > 1.8:
                FFXC.set_value("Dpad", 8)
            elif angle < 1.6:
                FFXC.set_value("Dpad", 4)
            else:
                FFXC.set_value("Dpad", 0)
        else:
            if angle > 1.6:  # Stay straight
                FFXC.set_value("Dpad", 8)
            elif angle < 1.4:
                FFXC.set_value("Dpad", 4)
            else:
                FFXC.set_value("Dpad", 0)
    FFXC.set_neutral()

    while not memory.main.diag_progress_flag() in [51, 69, 74]:
        # 51 is success
        xbox.tap_b()
    if memory.main.diag_progress_flag() == 51:  # Success
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_down()  # Up for next race, down for quit
        xbox.tap_b()
        # memory.waitFrames(20)
        xbox.tap_up()
        xbox.tap_b()
        return True
    else:
        memory.main.click_to_diag_progress(76)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def choco_tame_2():
    memory.main.click_to_diag_progress(43)
    checkpoint = 0
    while not memory.main.diag_progress_flag() in [44, 74]:
        angle = memory.main.get_actor_angle(0)
        position = memory.main.get_actor_coords(0)

        if position[1] > -1360 and checkpoint == 0:
            # Start off aiming right to manip balls
            checkpoint += 1
            FFXC.set_value("Dpad", 8)  # Right
            memory.main.wait_frames(5)
            FFXC.set_value("Dpad", 0)
        if position[1] > -1200 and checkpoint == 1:  # Slight left
            checkpoint += 1
            FFXC.set_value("Dpad", 4)  # Left
            memory.main.wait_frames(11)
            FFXC.set_value("Dpad", 0)
        if position[1] > -1000 and checkpoint == 2:  # Straighten out
            checkpoint += 1
            FFXC.set_value("Dpad", 8)  # Right
            memory.main.wait_frames(7)
            FFXC.set_value("Dpad", 0)
        if position[1] > -800 and checkpoint == 3:  # Juke right
            checkpoint += 1
            FFXC.set_value("Dpad", 8)  # Right
            memory.main.wait_frames(5)
            FFXC.set_value("Dpad", 0)
        if position[1] > -650 and checkpoint == 4:  # Back to the left
            checkpoint += 1
            FFXC.set_value("Dpad", 4)  # Left
            memory.main.wait_frames(11)
            FFXC.set_value("Dpad", 0)
        if position[1] > -550 and checkpoint == 5:  # Straighten out
            checkpoint += 1
            FFXC.set_value("Dpad", 8)  # Right
            memory.main.wait_frames(6)
            FFXC.set_value("Dpad", 0)
        if position[1] > -450 and checkpoint == 6:  # Juke right again
            checkpoint += 1
            FFXC.set_value("Dpad", 8)
            memory.main.wait_frames(6)
            FFXC.set_value("Dpad", 0)
        if position[1] > -250 and checkpoint == 7:  # Straighten out
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.wait_frames(14)
            FFXC.set_value("Dpad", 0)
        if position[1] > -90 and checkpoint == 8:  # The final juke!
            checkpoint += 1
            FFXC.set_value("Dpad", 8)
            memory.main.wait_frames(13)
            FFXC.set_value("Dpad", 0)
    FFXC.set_neutral()

    while not memory.main.diag_progress_flag() in [54, 69, 77]:
        # 54 is success
        xbox.tap_b()
    if memory.main.diag_progress_flag() == 54:  # Success
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_up()
        xbox.tap_b()
        memory.main.wait_frames(30)
        xbox.tap_up()
        xbox.tap_b()
        return True
    else:
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def choco_tame_3():
    memory.main.click_to_diag_progress(43)
    checkpoint = 0
    while not memory.main.diag_progress_flag() in [44, 74]:
        position = memory.main.get_actor_coords(0)
        if position[1] > -1370 and checkpoint == 0:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)  # Left
            memory.main.wait_frames(3)
            FFXC.set_value("Dpad", 0)
        if position[1] > -1200 and checkpoint == 1:
            checkpoint += 1
            FFXC.set_value("Dpad", 8)  # Right
            memory.main.wait_frames(10)
            FFXC.set_value("Dpad", 0)
        if position[1] > -1100 and checkpoint == 2:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.wait_frames(12)
            FFXC.set_value("Dpad", 0)
        if position[1] > -1040 and checkpoint == 3:
            checkpoint += 1
            FFXC.set_value("Dpad", 8)
            memory.main.wait_frames(9)
            FFXC.set_value("Dpad", 0)
        if position[1] > -950 and checkpoint == 4:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.wait_frames(12)
            FFXC.set_value("Dpad", 0)
        if position[1] > -700 and checkpoint == 5:
            checkpoint += 1
            FFXC.set_value("Dpad", 8)
            memory.main.wait_frames(12)
            FFXC.set_value("Dpad", 0)
        if position[1] > -600 and checkpoint == 6:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.wait_frames(12)
            FFXC.set_value("Dpad", 0)
        if position[1] > -500 and checkpoint == 7:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.wait_frames(6)
            FFXC.set_value("Dpad", 0)
        if position[1] > -400 and checkpoint == 8:
            checkpoint += 1
            FFXC.set_value("Dpad", 8)
            memory.main.wait_frames(16)
            FFXC.set_value("Dpad", 0)
        if position[1] > -250 and checkpoint == 9:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.wait_frames(16)
            FFXC.set_value("Dpad", 0)
        # Still dialing in on this one.
        if position[1] > -120 and checkpoint == 10:
            checkpoint += 1
            FFXC.set_value("Dpad", 8)
            memory.main.wait_frames(16)
            FFXC.set_value("Dpad", 0)
        if position[1] > -20 and checkpoint == 11:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.wait_frames(10)
            FFXC.set_value("Dpad", 0)
    FFXC.set_neutral()

    while not memory.main.diag_progress_flag() in [56, 69, 77]:
        # 56 is success
        xbox.tap_b()
    if memory.main.diag_progress_flag() == 56:  # Success
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_down()  # Up for something else, down for done.
        xbox.tap_b()
        memory.main.wait_frames(30)
        # xbox.tapUp()
        # xbox.tapB()
        return True
    else:
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def choco_tame_4():
    print("START - CATCHER CHOCOBO")
    memory.main.click_to_diag_progress(43)
    checkpoint = 0
    while not memory.main.diag_progress_flag() in [44, 67]:
        angle = memory.main.get_actor_angle(0)
        position = memory.main.get_actor_coords(0)
        print("User control")
        """
        if position[1] > -1360 and checkpoint == 0: #Start off aiming right to manip balls
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            memory.waitFrames(5)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1200 and checkpoint == 1: #Slight left
            checkpoint += 1
            FFXC.set_value('Dpad', 4)#Left
            memory.waitFrames(10)
            FFXC.set_value('Dpad', 0)
        if position[1] > -770 and checkpoint == 3: #Left between balls
            checkpoint += 1
            FFXC.set_value('Dpad', 4)#Left
            memory.waitFrames(10)
            FFXC.set_value('Dpad', 0)
        if position[1] > -600 and checkpoint == 4: #Straighten out
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            memory.waitFrames(6)
            FFXC.set_value('Dpad', 0)
        if position[1] > -100:
            if position[0] > -40:
                FFXC.set_value('Dpad', 4)#Left
            elif position[0] < -100:
                FFXC.set_value('Dpad', 8) #Right
            elif angle > 1.7:
                FFXC.set_value('Dpad', 8) #Right
            elif angle < 1.3:
                FFXC.set_value('Dpad', 4)#Left
            else:
                FFXC.set_value('Dpad', 0)
    """
    print("Race complete.")
    FFXC.set_neutral()

    while not memory.main.diag_progress_flag() in [67, 77]:
        # 67 is 0:00.0 run
        xbox.tap_b()
    if memory.main.diag_progress_flag() == 67:  # Success
        print("Great run! Perfect score!")
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_down()
        xbox.tap_b()
        return True
    else:
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def to_remiem():
    memory.main.click_to_control()
    while memory.main.user_control():
        nemesis.targetPath.set_movement([-1565, 434])
        xbox.tap_b()
        print("Near chocobo lady")
    FFXC.set_neutral()
    memory.main.click_to_control()

    checkpoint = 0
    while checkpoint < 35:
        if memory.main.user_control():
            if memory.main.get_map() == 290 and checkpoint < 13:
                checkpoint = 13

            elif checkpoint == 10:
                print("Feather")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 27:
                print("Orb thing")
                while memory.main.user_control():
                    nemesis.targetPath.set_movement([770, 631])
                    xbox.tap_b()
                memory.main.click_to_control()
                checkpoint += 1
            elif (
                nemesis.targetPath.set_movement(
                    nemesis.targetPath.to_remiem(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)


def remiem_races():
    print("Ready to start races")
    choco_race_1()
    print("Celestial Weapon obtained.")
    # chocoRace2()
    # print("Obtained")
    # chocoRace3()
    # print("Something obtained")
    print("Now heading back to the monster arena.")


def choco_race_1():
    while memory.main.user_control():
        nemesis.targetPath.set_movement([790, 60])
        xbox.tap_b()
    FFXC.set_neutral()
    memory.main.click_to_control()
    checkpoint = 0
    while checkpoint != 37:
        if memory.main.user_control():
            if (
                nemesis.targetPath.set_movement(nemesis.targetPath.race_1(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            else:
                xbox.tap_b()
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(10)
    FFXC.set_neutral()
    memory.main.click_to_control()


def choco_race_2():
    FFXC.set_neutral()
    memory.main.click_to_control()
    while memory.main.user_control():
        nemesis.targetPath.set_movement([790, 60])
        xbox.tap_b()
    FFXC.set_neutral()
    checkpoint = 0
    while checkpoint != 38:
        if memory.main.user_control():
            if checkpoint == 11:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            if checkpoint == 17:
                memory.main.click_to_event_temple(5)
                checkpoint += 1
            if checkpoint == 22:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            if (
                nemesis.targetPath.set_movement(nemesis.targetPath.race_2(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            else:
                xbox.tap_b()
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(10)
    FFXC.set_neutral()
    memory.main.click_to_control()


def choco_race_3():
    FFXC.set_neutral()
    memory.main.click_to_control()
    while memory.main.user_control():
        nemesis.targetPath.set_movement([790, 60])
        xbox.tap_b()
    FFXC.set_neutral()
    checkpoint = 0
    while checkpoint != 44:
        if memory.main.user_control():
            if checkpoint == 11:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            if checkpoint == 17:
                memory.main.click_to_event_temple(5)
                checkpoint += 1
            if checkpoint == 22:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            if checkpoint == 27:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            if checkpoint == 39:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            # if checkpoint == 42: #Since it's not tight enough movement yet
            #     FFXC.set_neutral()
            #     memory.waitFrames(120)
            #     memory.click_to_control()
            #     break
            if (
                nemesis.targetPath.set_movement(nemesis.targetPath.race_3(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            else:
                xbox.tap_b()
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(60)
    FFXC.set_neutral()
    memory.main.click_to_control()


def temple_to_arena():
    memory.main.click_to_control()
    checkpoint = 0
    while memory.main.get_map() != 307:
        if memory.main.user_control():
            if memory.main.get_map() == 223 and checkpoint < 18:
                checkpoint = 18

            elif checkpoint == 20:
                while memory.main.user_control():
                    nemesis.targetPath.set_movement([1261, -1238])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1

            elif checkpoint == 24:
                print("Feather")
                while memory.main.user_control():
                    nemesis.targetPath.set_movement([1101, -940])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.await_control()
                checkpoint += 1
            elif (
                nemesis.targetPath.set_movement(
                    nemesis.targetPath.leave_remiem(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)


def arena_purchase():
    memory.main.click_to_control()

    print("Straight forward to the guy")
    FFXC.set_movement(0, 1)
    memory.main.click_to_event()
    FFXC.set_neutral()
    print("Now for dialog")
    memory.main.click_to_diag_progress(65)
    print("Select Sure")
    memory.main.wait_frames(15)
    xbox.tap_down()
    xbox.tap_b()
    memory.main.click_to_diag_progress(73)
    memory.main.wait_frames(15)
    # xbox.tapUp()
    xbox.tap_b()  # Let's see your weapons
    # memory.waitFrames(9000)
    nemesis.menu.arena_purchase_1()
    # Sell all undesirable equipment
    # Purchase the following weapons:
    # -Tidus x4
    # -Yuna x1

    # ---Done buying.
    memory.main.await_control()
    memory.main.wait_frames(2)
    FFXC.set_movement(0, -1)
    memory.main.await_event()  # Exit the arena map
    FFXC.set_neutral()
    memory.main.await_control()

    checkpoint = 0
    while memory.main.get_map() != 279:
        if memory.main.user_control():
            if checkpoint == 7 and area.gagazet.check_gems() < 2:
                checkpoint -= 2
            elif (
                nemesis.targetPath.set_movement(
                    nemesis.targetPath.calm_lands_2(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if area.gagazet.check_gems() < 2:
                    battle.main.calm_lands_gems()
                else:
                    battle.main.calm_lands_manip()
                memory.main.full_party_format("yuna")
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()


def arena_purchase_with_chocobo():
    while memory.main.user_control():  # Back onto chocobo
        nemesis.targetPath.set_movement([1347, -69])
        xbox.tap_b()

    while not nemesis.targetPath.set_movement([1488, 778]):
        pass
    while not nemesis.targetPath.set_movement([1545, 1088]):
        pass
    while not memory.main.get_map() == 279:
        nemesis.targetPath.set_movement([1700, 1200])

    memory.main.full_party_format("kimahri")
