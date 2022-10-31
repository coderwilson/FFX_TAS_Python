import battle.boss
import battle.main
import logs
import memory.main
import menu
import screen
import targetPathing
import vars
import xbox
import save_sphere

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def arrival(rikku_charged):
    memory.main.click_to_control()
    memory.main.full_party_format("mwoodsneedcharge")
    memory.main.close_menu()

    # Rikkus charge, Fish Scales, and Arctic Winds
    woodsVars = [False, False, False]
    woodsVars[0] = rikku_charged

    lastGil = 0  # for first chest
    checkpoint = 0
    totalBattles = 0
    while memory.main.get_map() != 221:  # All the way to O'aka
        if memory.main.user_control():
            # Events
            if checkpoint == 14:  # First chest
                if lastGil != memory.main.get_gil_value():
                    if lastGil == memory.main.get_gil_value() - 2000:
                        checkpoint += 1
                        print("Chest obtained. Updating checkpoint:", checkpoint)
                    else:
                        lastGil = memory.main.get_gil_value()
                else:
                    FFXC.set_movement(1, 1)
                    xbox.tap_b()
            elif checkpoint == 59:
                if not woodsVars[0]:
                    checkpoint -= 2
                elif not woodsVars[1] and not woodsVars[2]:
                    checkpoint -= 2
                else:  # All good to proceed
                    checkpoint += 1

            # Map changes
            elif checkpoint < 18 and memory.main.get_map() == 241:
                checkpoint = 18
            elif checkpoint < 40 and memory.main.get_map() == 242:
                checkpoint = 40

            # General pathing
            elif targetPathing.set_movement(targetPathing.m_woods(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                print("variable check 1:", woodsVars)
                woodsVars = battle.main.m_woods(woodsVars)
                print("variable check 2:", woodsVars)
                if memory.main.overdrive_state()[6] == 100:
                    memory.main.full_party_format("mwoodsgotcharge")
                else:
                    memory.main.full_party_format("mwoodsneedcharge")
                totalBattles += 1
            elif not memory.main.battle_active() and memory.main.diag_skip_possible():
                xbox.tap_b()

    # logs.writeStats("Mac Woods battles:")
    # logs.writeStats(totalBattles)
    # Save sphere
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(2)
    memory.main.await_control()
    memory.main.wait_frames(1)
    save_sphere.touch_and_go()
    FFXC.set_neutral()


def lake_road():
    memory.main.await_control()
    while not targetPathing.set_movement([174, -96]):
        pass
    while not targetPathing.set_movement([138, -83]):
        pass
    while not targetPathing.set_movement([101, -82]):
        pass
    while memory.main.user_control():
        FFXC.set_movement(0, 1)
        xbox.tap_b()
    FFXC.set_neutral()
    menu.m_woods()  # Selling and buying, item sorting, etc
    memory.main.full_party_format("spheri")
    while not targetPathing.set_movement([101, -72]):
        pass

    while not memory.main.battle_active():
        if memory.main.user_control():
            mapVal = memory.main.get_map()
            tidusPos = memory.main.get_coords()
            if mapVal == 221:
                if tidusPos[0] > 35:
                    targetPathing.set_movement([33, -35])
                else:
                    targetPathing.set_movement([-4, 15])
            elif mapVal == 248:
                if tidusPos[0] < -131:
                    targetPathing.set_movement([-129, -343])
                elif tidusPos[1] < -235:
                    targetPathing.set_movement([-49, -233])
                elif tidusPos[1] < -95:
                    targetPathing.set_movement([-1, -93])
                else:
                    targetPathing.set_movement([-1, 100])
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

    FFXC.set_neutral()  # Engage Spherimorph

    battle.boss.spherimorph()
    print("Battle is over.")
    memory.main.click_to_control()  # Jecht's memories


def lake_road_2():
    FFXC.set_movement(0, -1)
    if game_vars.csr():
        checkpoint = 0
        while checkpoint < 5:
            if checkpoint == 0:
                if targetPathing.set_movement([-6, 25]):
                    checkpoint += 1
            elif checkpoint == 1:
                if targetPathing.set_movement([-4, -50]):
                    checkpoint += 1
            elif checkpoint == 2:
                if targetPathing.set_movement([-45, -212]):
                    checkpoint += 1
            elif checkpoint == 3:
                if targetPathing.set_movement([-49, -245]):
                    checkpoint += 1
            else:
                if targetPathing.set_movement([-145, -358]):
                    checkpoint += 1

    else:
        FFXC.set_movement(0, -1)
        memory.main.wait_frames(3)
        memory.main.await_event()
        FFXC.set_neutral()

        memory.main.click_to_control()  # Auron's musings.
        print("Affection (before):", memory.main.affection_array())
        memory.main.wait_frames(30 * 0.2)
        auronAffection = memory.main.affection_array()[2]
        # Make sure we get Auron affection
        while memory.main.affection_array()[2] == auronAffection:
            auronCoords = memory.main.get_actor_coords(3)
            targetPathing.set_movement(auronCoords)
            xbox.tap_b()
        print("Affection (after):", memory.main.affection_array())
    while memory.main.user_control():
        FFXC.set_movement(-1, -1)
    FFXC.set_neutral()

    memory.main.click_to_control()  # Last map in the woods
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(2)
    memory.main.await_event()
    FFXC.set_neutral()


def lake():
    print("Now to the frozen lake")
    if memory.main.get_hp()[3] < 1000:  # Otherwise we under-level Tidus off of Crawler
        battle.main.heal_up(full_menu_close=False)

    memory.main.full_party_format("crawler", full_menu_close=False)
    menu.m_lake_grid()
    memory.main.await_control()

    print("------------------------------Affection array:")
    print(memory.main.affection_array())
    print("------------------------------")

    checkpoint = 0
    while memory.main.get_encounter_id() != 194:
        if memory.main.user_control():
            if targetPathing.set_movement(targetPathing.m_lake(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active() and memory.main.get_encounter_id() != 194:
                battle.main.flee_all()
            elif memory.main.diag_skip_possible() or memory.main.menu_open():
                xbox.menu_b()
    xbox.click_to_battle()
    battle.boss.crawler()


def after_crawler():
    print("--- Affection array ---")
    print(memory.main.affection_array())
    print("-----------------------")
    memory.main.click_to_control()
    while memory.main.get_map() != 153:
        pos = memory.main.get_coords()
        if memory.main.user_control():
            if pos[1] > ((2.94 * pos[0]) + 505.21):
                FFXC.set_movement(1, 1)
            elif pos[1] < ((2.59 * pos[0]) + 469.19):
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()

    memory.main.click_to_control()

    checkpoint = 0
    lastCP = 0
    while checkpoint != 100:
        if lastCP != checkpoint:
            print("Checkpoint reached:", checkpoint)
            lastCP = checkpoint
        pos = memory.main.get_coords()
        if checkpoint == 0:
            if pos[0] > 130:
                checkpoint = 10
            else:
                if pos[1] < ((1.99 * pos[0]) + 5):
                    FFXC.set_movement(-1, -1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 10:
            if pos[0] > 450:
                checkpoint = 20
            else:
                if pos[1] > ((0.37 * pos[0]) + 240):
                    FFXC.set_movement(-1, 1)
                elif pos[1] > 385:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 20:
            if pos[0] > 690:
                checkpoint = 40
            else:
                if pos[1] > ((-0.65 * pos[0]) + 693):
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 30:
            if pos[1] < 100:
                checkpoint = 40
            else:
                if pos[1] < ((-1.49 * pos[0]) + 1235):
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 40:
            if memory.main.get_map() == 106:
                FFXC.set_neutral()
                checkpoint = 100
            else:
                if pos[0] > 815:
                    FFXC.set_movement(1, 1)
                elif pos[0] < 810:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)
    print("End of Macalania Woods section. Next is temple section.")
