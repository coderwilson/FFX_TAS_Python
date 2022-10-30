import math
import time

import blitz_pathing
import logs
import memory.main
import rngTrack
import vars
import xbox

game_vars = vars.vars_handle()
tidusXP = False

FFXC = xbox.controller_handle()

reportState = False
playerArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Initialize the player array
for i in range(12):
    playerArray[i] = memory.main.BlitzActor(player_num=i)

global engageDefender
engageDefender = False


def goers_score_first():
    return memory.main.diag_progress_flag() in [47, 48, 49]


def halftime_dialog():
    return memory.main.diag_progress_flag() in [45, 46]


def select_movement():
    return memory.main.blitz_menu_num() in [145, 146]


def select_formation():
    return memory.main.blitz_menu_num() in [122, 133]


def select_formation_2():
    return memory.main.blitz_menu_num() == 144


def select_breakthrough():
    if (
        memory.main.blitz_menu_num() >= 0 and memory.main.blitz_menu_num() <= 46
    ) or memory.main.blitz_menu_num() == 246:
        return True
    else:
        return False


def select_action():
    return memory.main.blitz_menu_num() in [47, 52]


def select_pass_target():
    return memory.main.blitz_menu_num() in [226, 228, 236]


def select_shot_type():
    return memory.main.blitz_menu_num() in [113, 117]


def targeted_player():
    retVal = memory.main.blitz_target_player() - 2
    return retVal


def active_clock():
    return not memory.main.blitz_clock_pause()


def aurochs_control():
    return memory.main.blitz_target_player() < 8


def controlling_player():
    retVal = memory.main.blitz_current_player() - 2
    if retVal < 200:
        return retVal
    return 1


def half_summary_screen():
    return memory.main.get_map() == 212


def new_half():
    return memory.main.get_map() == 347


def halftime_spam():
    memory.main.click_to_diag_progress(20)


def game_clock():
    return memory.main.blitz_clock()


def prep_half():
    # Map = 347, Dialog = 20
    print("Prepping for next period of play.")
    while memory.main.get_map() != 62:
        if (
            memory.main.diag_progress_flag() == 135
        ):  # Select game mode (Tourney, League, Exhibiton, etc)
            memory.main.wait_frames(90)
            if memory.main.save_popup_cursor() != 1:
                xbox.menu_down()
                time.sleep(2)
            else:
                xbox.menu_b()
                xbox.menu_b()
                xbox.menu_up()
                xbox.menu_b()
        elif memory.main.diag_progress_flag() in [20, 134]:
            if memory.main.blitz_char_select_cursor() != 6:
                xbox.tap_a()
            else:
                xbox.menu_b()
                memory.main.wait_frames(5)
        elif memory.main.diag_progress_flag() == 40:
            print("Attempting to proceed.")
            if memory.main.blitz_proceed_cursor() != 0:
                xbox.menu_up()
            else:
                xbox.menu_b()
            memory.main.wait_frames(2)
        elif memory.main.diag_progress_flag() == 47:
            if memory.main.blitz_cursor() != 0:
                xbox.menu_up()
                memory.main.wait_frames(2)
            else:
                xbox.menu_b()
        elif memory.main.diag_progress_flag() == 48:
            memory.main.wait_frames(20)
            xbox.menu_left()
            xbox.menu_up()
            xbox.menu_up()
            xbox.menu_b()
        elif memory.main.diag_progress_flag() == 113:
            if memory.main.blitz_cursor() != 1:
                xbox.menu_up()
                memory.main.wait_frames(2)
            else:
                xbox.menu_b()
                xbox.menu_b()
                time.sleep(6)
        elif memory.main.diag_skip_possible():
            xbox.menu_b()
    print("Prep complete.")


def storyline(force_blitz_win):
    current = memory.main.get_story_progress()
    if not game_vars.csr():
        if current == 540:
            if force_blitz_win:
                memory.main.blitzball_patriots_style()
            print("Halftime hype")
            memory.main.click_to_diag_progress(164)
            memory.main.click_to_diag_progress(20)
        elif current == 560 and memory.main.diag_progress_flag() > 1:
            print("Wakka story happening.")
            memory.main.click_to_diag_progress(11)
            while not active_clock():
                xbox.tap_b()
        # First half is 535
        # Hype halftime is 540
        # Second half starts on 560
        # 575 - 9


def cursor_1():
    return memory.main.blitz_cursor()


def jassu_pass_timing() -> int:
    shotDistance = distance(0, 11)
    shotMod = int(shotDistance / 160)
    if 540 <= memory.main.get_story_progress() < 570:
        baseTiming = int(155 - shotMod)
    else:
        baseTiming = int(265 - shotMod)

    for x in range(5):
        if distance(0, x + 6) < 180:
            baseTiming = int(baseTiming - 4)
    return baseTiming


def tidus_shot_timing() -> int:
    shotDistance = distance(0, 11)
    shotMod = int(shotDistance / 160)
    if 540 < memory.main.get_story_progress() < 570:
        baseTiming = int(169 - shotMod)
    else:
        baseTiming = int(288 - shotMod)

    for x in range(5):
        if distance(0, x + 6) < 180:
            baseTiming = int(baseTiming - 4)
    return baseTiming


def game_stage():
    # Stage 0: Killing time
    # Stage 1: Defensive, Letty dribble, consumes Jassu HP
    # Stage 2: Jassu position near the edge of the pool, look for opportunity.
    # Stage 3: Positioning Defender so Tidus can shoot/score
    # Stage 4: Pass to Tidus
    # Stage 5: Shoot for goal
    currentStage = 0
    global engageDefender
    # Logic that immediately moves to scoring phases if in overtime.
    if (
        memory.main.get_story_progress() > 570
        and memory.main.get_story_progress() < 700
    ):
        if game_clock() in [2, 3, 4, 5, 6, 7]:
            game_vars.set_blitz_ot(True)

    if memory.main.get_story_progress() < 570:
        if memory.main.get_story_progress() > 540:
            # Requires special timing before Wakka comes in
            stages = [
                0,
                30,
                90,
                jassu_pass_timing() - 12,
                jassu_pass_timing(),
                tidus_shot_timing(),
            ]
        elif (
            memory.main.get_story_progress() < 540 and not game_vars.blitz_first_shot()
        ):
            currentStage = 20  # default 20
        else:
            currentStage = 30
    else:
        if game_vars.get_blitz_ot():
            stages = [0, 2, 2, 2, 300, 300]
        else:
            # print("After Wakka")
            stages = [
                0,
                160,
                200,
                jassu_pass_timing() - 12,
                jassu_pass_timing(),
                tidus_shot_timing(),
            ]

    # Determine base stage. Modified by following logic.
    if (
        abs(memory.main.blitz_own_score() - memory.main.blitz_opp_score()) >= 2
        and memory.main.get_story_progress() >= 570
    ):
        currentStage = 30
    elif (
        memory.main.blitz_own_score() - memory.main.blitz_opp_score() >= 1
        and 570 < memory.main.get_story_progress() < 700
    ):
        # Ahead by 1 goal after Wakka enters, just end the game.
        currentStage = 30
    elif memory.main.get_story_progress() < 540:
        if not game_vars.blitz_first_shot():
            currentStage = 20
        else:
            currentStage = 30
    else:
        for i in range(6):
            if stages[i] < game_clock():
                currentStage = i

        if memory.main.get_story_progress() < 700 and currentStage >= 1:
            # Only apply following logic for the storyline game
            # Logic that updates stage based on defender movements
            if playerArray[0].get_coords()[1] - playerArray[10].get_coords()[1] > 300:
                if currentStage < 3:
                    currentStage = 4

            # Logic that reduces stage if score is too far apart.
            if (
                memory.main.blitz_own_score() - memory.main.blitz_opp_score() >= 2
                and memory.main.get_story_progress() >= 570
            ):
                currentStage = 0

            # Logic if we're in defensive zone trying to move forward
            if (
                currentStage == 3
                and playerArray[controlling_player()].get_coords()[1] < -200
            ):
                currentStage = 2
    if currentStage == 3 and not engageDefender:
        print("Start engaging defender!")
        engageDefender = True
    elif currentStage == 2 and engageDefender:
        currentStage = 3
    elif currentStage in [0, 1, 20, 30] and engageDefender:
        print("Disengaging defender logic")
        engageDefender = False

    if currentStage < 3 and controlling_player() == 0:
        currentStage = 30
    return currentStage


def distance_special():
    try:
        player1 = playerArray[6].get_coords()
        player2 = [222, -238]  # Formerly 230,-260
        totalDistance = abs(player1[1] - player2[1]) + abs(player1[0] - player2[0])
        return totalDistance
    except Exception as x:
        print("Exception:", x)
        return 999


def get_char_radius(player_index: int = 10):
    playerCoords = playerArray[player_index].get_coords()
    try:
        result = math.sqrt(
            (playerCoords[0] * playerCoords[0]) + (playerCoords[1] * playerCoords[1])
        )
    except Exception as E:
        print("Math error, using default value.")
        print(playerCoords[0] ** 2)
        result = 999
    return result


def radius_movement(radius: int = 580, direction="forward"):
    playerCoords = playerArray[controlling_player()].get_coords()
    target_coords = [-400, -400]
    playerCoords[0] *= radius / get_char_radius(controlling_player())
    playerCoords[1] *= radius / get_char_radius(controlling_player())

    if direction == "forward" and -30 < playerCoords[0] < 30:
        FFXC.set_movement(-1, -1)
    else:
        if direction == "forward":
            target_coords = [playerCoords[0], playerCoords[1] + 10]
        else:
            target_coords = [playerCoords[0], playerCoords[1] - 10]
        try:
            target_coords[0] = math.sqrt((radius**2) - (target_coords[1] ** 2))
            if playerCoords[0] < -1:
                target_coords[0] *= -1
        except:
            playerCoords = playerArray[controlling_player()].get_coords()
            target_coords = [-400, -400]
            playerCoords[0] *= radius / get_char_radius(controlling_player())
            playerCoords[1] *= radius / get_char_radius(controlling_player())
            if direction == "forward":
                target_coords = [playerCoords[0], playerCoords[1]]
            else:
                target_coords = [playerCoords[0], playerCoords[1]]

            if playerCoords[1] < -1:
                if direction == "forward":
                    target_coords[0] -= 10
                else:
                    target_coords[0] += 10
            else:
                if direction == "forward":
                    target_coords[0] += 10
                else:
                    target_coords[0] -= 10
            try:
                target_coords[1] = math.sqrt((radius**2) - (target_coords[0] ** 2))
                if playerCoords[1] < -1:
                    target_coords[1] *= -1
            except:
                if direction == "forward":
                    target_coords[0] = playerCoords[0] - 10
                    target_coords[1] = playerCoords[1] + 10
                else:
                    target_coords[0] = playerCoords[0] + 10
                    target_coords[1] = playerCoords[1] - 10
    blitz_pathing.set_movement(target_coords)
    return target_coords


def working_forward():
    cPlayer = playerArray[controlling_player()].get_coords()
    # if distance(3,10) < 330:
    #    radiusMovement(direction='back')
    if cPlayer[1] > -180:
        # print("In position")
        blitz_pathing.set_movement([-585, -130])
    else:
        radius_movement()


def find_safe_place():
    # current player
    cPlayer = playerArray[controlling_player()].get_coords()
    cPlayerNum = controlling_player()
    # graav coords
    graavPos = playerArray[8].get_coords()
    forwardPos = playerArray[7].get_coords()
    target_coords = [-2, -595]
    safeSpot = 255

    # Determin target coords based on character and state.
    if cPlayerNum in [1, 4]:
        target_coords = [520, -20]
    elif cPlayerNum in [2, 3]:
        if playerArray[7].get_coords()[1] < 10 or playerArray[6].get_coords()[1] < 10:
            safeSpot = 3
        else:
            safeSpot = 2
    else:  # Should never occur, should never get Tidus/Wakka into this logic.
        safeSpot = 3

    if safeSpot == 1:  # Near the left wall
        target_coords = [-521, -266]
    elif safeSpot == 2:  # About half way
        target_coords = [-340, -497]
    elif safeSpot == 3:  # All the way back
        target_coords = [-2, -595]

    # I think this is still the best option.
    # target_coords = [-2, -595]

    if abs(cPlayer[0] - target_coords[0]) + abs(cPlayer[1] - target_coords[1]) > 120:
        if cPlayer[1] > target_coords[1]:
            radius_movement(radius=570, direction="back")
        else:
            radius_movement(radius=570, direction="forward")
    else:
        if blitz_pathing.set_movement(target_coords):
            return True
        else:
            return False


def jassu_train():
    print("All aboard the Jassu train! Choo choo!")
    jassuCoords = playerArray[3].get_coords()
    if abs(jassuCoords[0]) < 30:
        if jassuCoords[1] > 400:
            FFXC.set_movement(0, -1)
        else:
            FFXC.set_movement(0, -1)
    elif jassuCoords[0] < 10:
        radius_movement(direction="back")
    else:
        radius_movement(direction="forward")


def pass_ball(target=0, break_through=5):
    if controlling_player() == 4:
        break_through = 0
    if select_breakthrough():
        if break_through == 5:
            if cursor_1() == 0:
                xbox.menu_up()
                memory.main.wait_frames(1)
            else:
                xbox.menu_b()
        else:
            xbox.menu_b()
    elif select_action():
        if cursor_1() != 0:  # Pass command
            xbox.menu_down()
            memory.main.wait_frames(3)
        else:
            xbox.menu_b()
    elif select_pass_target():
        while not active_clock():
            if targeted_player() != target:
                xbox.menu_down()
            else:
                xbox.tap_b()
    else:
        xbox.menu_b()


def shoot_ball(break_through=5):
    if memory.main.get_story_progress() < 570 and controlling_player() == 0:
        if game_clock() > 167:
            break_through = 5
        else:
            break_through = 0
    else:
        break_through = 5
    if select_shot_type():
        if cursor_1() == 1:
            xbox.menu_b()
        else:
            xbox.menu_down()
            memory.main.wait_frames(3)
    elif select_breakthrough():
        if break_through == 5:
            if cursor_1() == 0:
                xbox.menu_up()
                memory.main.wait_frames(1)
            else:
                xbox.menu_b()
                xbox.menu_b()
        else:
            xbox.menu_b()
            xbox.menu_b()
    elif select_action():
        if cursor_1() != 1:  # Shoot
            xbox.menu_down()
            memory.main.wait_frames(3)
        else:
            xbox.menu_b()
        game_vars.blitz_first_shot_taken()


def dribble_ball():
    if select_breakthrough():
        if cursor_1() == 0:
            xbox.menu_up()
            memory.main.wait_frames(2)
        else:
            xbox.menu_b()
    elif select_action():
        if cursor_1() != 2:
            xbox.menu_up()
            memory.main.wait_frames(3)
        else:
            xbox.menu_b()


def player_guarded(player_num):
    # Graav proximity always counts as guarded.
    if distance(player_num, 8) < 360:
        return True

    # Two or more player proximity always counts as guarded.
    otherDistance = 0
    if distance(0, 6) < 360:
        otherDistance += 1
    if distance(0, 7) < 360:
        otherDistance += 1
    if distance(0, 9) < 360:
        otherDistance += 1
    if distance(0, 10) < 360:
        otherDistance += 1
    if otherDistance >= 2:
        return True

    # Specific cases depending on player.
    if player_num in [3, 4]:
        if distance(player_num, 9) < 340:
            return True
        if distance(player_num, 10) < 340:
            return True
    return False


def tidus_move():
    currentStage = game_stage()
    if reportState:
        print("Tidus movement")
    graavDistance = distance(0, 8)

    otherDistance = 0
    if distance(0, 6) < 180:
        otherDistance += 1
    if distance(0, 7) < 180:
        otherDistance += 1
    if distance(0, 9) < 180:
        otherDistance += 1
    if distance(0, 10) < 180:
        otherDistance += 1

    shootTarget = [-170, 540]

    if currentStage > 15:
        radius_movement(radius=400, direction="back")
        if distance(0, 3) < 330:
            xbox.tap_x()
    elif memory.main.get_story_progress() > 700:
        if otherDistance >= 2:
            xbox.tap_x()
        elif currentStage == 4:
            xbox.tap_x()
        elif blitz_pathing.set_movement(shootTarget):
            xbox.tap_x()
    elif currentStage in [0, 1, 2, 5]:
        FFXC.set_movement(-1, -1)
        xbox.tap_x()
    elif currentStage == 4:
        if graavDistance < 240:
            # Graav too close.
            FFXC.set_movement(-1, -1)
            xbox.tap_x()
        elif otherDistance >= 2:
            # Too many players closing in.
            FFXC.set_movement(-1, -1)
            xbox.tap_x()
        elif (
            blitz_pathing.set_movement(shootTarget)
            and memory.main.get_story_progress() >= 570
        ):
            FFXC.set_movement(-1, -1)
            xbox.tap_x()
    else:  # stages 3 and 4 only. All other stages we try to pass, or just shoot.
        if playerArray[0].get_coords()[1] > 470:  # Force shot
            FFXC.set_movement(-1, -1)
            xbox.tap_x()
        else:
            radius_movement(radius=570, direction="forward")


def tidus_act():
    currentStage = game_stage()
    if reportState:
        print("Tidus act")

    otherDistance = 0
    if distance(0, 6) < 280:
        otherDistance += 1
    if distance(0, 7) < 280:
        otherDistance += 1
    if distance(0, 9) < 280:
        otherDistance += 1
    if distance(0, 10) < 280:
        otherDistance += 1

    if currentStage > 15:
        pass_ball(target=3)
        game_vars.blitz_first_shot_taken()
    elif memory.main.get_story_progress() > 700:
        shoot_ball(break_through=0)
    elif currentStage in [4, 5]:
        # Late on the timer. Shoot at all costs.
        if memory.main.get_story_progress() < 540:
            print("First half, shooting without breakthrough.")
            shoot_ball(break_through=0)
        else:
            print("Stage 5 - shoot the ball!")
            shoot_ball(break_through=0)
    elif currentStage in [0, 1, 2]:
        # Early game. Try to get the ball to Jassu.
        if distance(0, 3) < 350:
            pass_ball(target=3)
            game_vars.blitz_first_shot_taken()
        elif distance(0, 2) < 350:
            pass_ball(target=2)
            game_vars.blitz_first_shot_taken()
        else:
            shoot_ball()
    else:
        shoot_ball(break_through=0)


def letty_move():
    if reportState:
        print("Letty movement")
    currentStage = game_stage()
    graavDistance = distance(2, 8)

    if currentStage == 20:
        find_safe_place()
        if distance(0, 8) > 400 and distance(0, 10) > 400:
            xbox.tap_x()
        else:
            find_safe_place()
    elif currentStage == 30:
        find_safe_place()
        xbox.tap_x()
    elif currentStage >= 3:
        FFXC.set_movement(1, 0)
        xbox.tap_x()
    elif currentStage == 2:
        target_coords = [-20, -585]
        blitz_pathing.set_movement(target_coords)
        if not player_guarded(3):
            xbox.tap_x()
        elif not player_guarded(2):
            xbox.tap_x()
    else:
        # if not playerGuarded(3) and distance(3, 10) > 380 and graavDistance > 380:
        if distance(3, 8) > 400:
            xbox.tap_x()
        else:
            if find_safe_place() and graavDistance < 280:
                xbox.tap_x()


def letty_act():
    currentStage = game_stage()
    graavDistance = distance(0, 2)

    if currentStage == 20:
        if distance(0, 8) > 400:
            pass_ball(target=0)
        else:
            dribble_ball()
    elif currentStage == 30:
        pass_ball(target=3)
    elif memory.main.get_story_progress() > 700:  # Post-storyline blitzball only
        if playerArray[0].get_coords()[1] > playerArray[1].get_coords()[1]:
            pass_ball(target=0, break_through=0)
        else:
            pass_ball(target=1, break_through=0)
    elif currentStage >= 4:
        pass_ball(target=0)
        if reportState:
            print("Letty Action 1")
    elif currentStage == 3:
        pass_ball(target=3)
        if reportState:
            print("Letty Action 2")
    elif playerArray[2].current_hp() < 10:
        pass_ball(target=3)
    elif currentStage == 2:
        if distance(2, 8) < 250:
            breakThroughVal = 5
        else:
            breakThroughVal = 0

        if not player_guarded(3):
            tar = 3
        elif not player_guarded(0):
            tar = 0
        else:
            tar = 3
        pass_ball(target=tar, break_through=breakThroughVal)
    else:
        if not game_vars.blitz_first_shot() and distance(0, 8) > 400:
            print("Letty pass to Tidus")
            pass_ball(target=0)
        else:
            print("Letty pass to Jassu")
            pass_ball(target=3)


def jassu_move():
    target_coords = [999, 999]
    currentStage = game_stage()
    playerCoords = playerArray[controlling_player()].get_coords()
    target_coords = [-585, -130]
    p10C = playerArray[10].get_coords()
    graavC = playerArray[8].get_coords()
    tidusC = playerArray[0].get_coords()
    findSafety = False
    moveForward = False
    graavDistance = distance(3, 8)
    otherDistance = 0
    target_coords = [-600, -100]
    if distance(3, 6) < 350:
        otherDistance += 1
    if distance(3, 7) < 350:
        otherDistance += 1
    if distance(3, 9) < 350:
        otherDistance += 1
    if distance(3, 10) < 350:
        otherDistance += 1

    if currentStage == 20:
        find_safe_place()
        if distance(0, 8) > 300 and distance(0, 10) > 360:
            if playerArray[9].get_coords()[1] > 100:
                xbox.tap_x()
    elif currentStage == 30:
        # jassuTrain()
        find_safe_place()
        moveForward = True
    elif currentStage <= 1 and playerArray[3].current_hp() < 10:
        if playerArray[2].current_hp() >= 40 and distance(2, 8) > 360:
            xbox.tap_x()
        elif graavDistance < 320:
            xbox.tap_x()
        else:
            findSafety = True
    elif currentStage == 0:
        # Defend in the goal for safety.
        findSafety = True
        if playerArray[2].current_hp() >= 40 and currentStage == 0:
            if distance(2, 8) > 360 and distance(2, 7) > 360 and distance(2, 6) > 360:
                xbox.tap_x()
    elif currentStage == 1:
        if playerArray[10].get_coords()[1] < 150:
            find_safe_place()
        elif distance(3, 8) < 350:
            find_safe_place()
        else:
            working_forward()
        moveForward = True
    elif currentStage == 2:
        # Move forward to staging position, prep for shot.
        working_forward()
        moveForward = True
    elif currentStage == 3:
        relDist = int((tidusC[1] - p10C[1]) + (tidusC[0] - p10C[0]))
        relDist2 = int((tidusC[1] - graavC[1]) + (tidusC[0] - graavC[0]))
        if relDist > 220:  # Tidus in position behind defender
            xbox.tap_x()
            moveForward = True
        elif distance(3, 10) > 340:
            moveRadius = min(int(get_char_radius() + 150), 570)
            target_coords = radius_movement(radius=moveRadius, direction="forward")
            moveForward = True
        else:
            moveRadius = min(int(get_char_radius() + 150), 570)
            target_coords = radius_movement(radius=moveRadius, direction="back")
            moveForward = True
    else:  # Pass to Tidus
        target_coords = [p10C[0] - 180, p10C[1] - 150]
        xbox.tap_x()

    if currentStage < 15 and target_coords != [999, 999]:
        if findSafety:
            if find_safe_place() and graavDistance < 320:
                xbox.tap_x()
        elif not moveForward:
            try:
                blitz_pathing.set_movement(target_coords)
            except:
                pass


def jassu_act():
    currentStage = game_stage()
    playerCoords = playerArray[controlling_player()].get_coords()
    p10C = playerArray[10].get_coords()
    graavC = playerArray[8].get_coords()
    tidusC = playerArray[0].get_coords()
    findSafety = False
    currentStage = game_stage()
    if reportState:
        print("Jassu Action")
        print("Stage:", currentStage)
    graavDistance = distance(3, 8)
    otherDistance = 0
    if distance(3, 6) < 350:
        otherDistance += 1
    if distance(3, 7) < 350:
        otherDistance += 1
    if distance(3, 9) < 350:
        otherDistance += 1
    if distance(3, 10) < 350:
        otherDistance += 1

    if currentStage == 20:
        if distance(0, 8) > 280:
            pass_ball(0)
        else:
            dribble_ball()
    elif currentStage == 30:
        dribble_ball()
    elif currentStage == 0:
        if playerArray[2].current_hp() >= 40 and distance(2, 8) > 360:
            pass_ball(target=2)
        else:
            dribble_ball()
    elif currentStage == 1:
        dribble_ball()
    elif playerArray[3].current_hp() < 10:
        pass_ball(target=0)
    elif currentStage == 2:
        dribble_ball()
    elif currentStage == 3:
        relDist = int((tidusC[1] - p10C[1]) + (tidusC[0] - p10C[0]))
        relDist2 = int((tidusC[1] - graavC[1]) + (tidusC[0] - graavC[0]))
        if relDist > 180:
            pass_ball(target=0)
        elif graavDistance < 150:
            # Graav too close
            pass_ball(target=0)
        elif playerArray[0].get_coords()[1] - playerArray[10].get_coords()[1] > 280:
            # Tidus in position for break-away.
            pass_ball(target=0)
        else:
            dribble_ball()
    else:  # Pass to Tidus
        pass_ball(target=0)


def other_move():  # fix
    if get_char_radius(controlling_player()) < 540:
        FFXC.set_movement(0, 1)
    elif playerArray[controlling_player()].get_coords()[1] < -400:
        xbox.tap_x()
    elif distance(controlling_player(), 8) < 300:
        xbox.tap_x()
    else:
        radius_movement(radius=570, direction="back")


def other_act():
    currentStage = game_stage()

    if reportState:
        print("Botta/Datto action")
        print("Stage:", currentStage)

    if memory.main.get_story_progress() > 700:
        if controlling_player() == 1:
            shoot_ball()
        else:
            if playerArray[0].get_coords()[1] > playerArray[1].get_coords()[1]:
                pass_ball(target=2, break_through=0)
            else:
                pass_ball(target=3, break_through=0)
    elif distance(controlling_player(), 8) < 300:
        pass_ball(target=2)
    else:
        pass_ball(target=3)


def blitz_movement():
    update_player_array()

    if controlling_player() == 0:
        tidus_move()
    elif controlling_player() == 2:
        letty_move()
    elif controlling_player() == 3:
        jassu_move()
    else:
        other_move()


def decide_action():
    FFXC.set_neutral()
    update_player_array()
    if controlling_player() == 0:
        tidus_act()
    elif controlling_player() == 2:
        letty_act()
    elif controlling_player() == 3:
        jassu_act()
    else:
        other_act()


def distance(n1, n2):
    try:
        player1 = playerArray[n1].get_coords()
        player2 = playerArray[n2].get_coords()
        return abs(player1[1] - player2[1]) + abs(player1[0] - player2[0])
    except Exception as x:
        print("Exception:", x)
        return 999


def update_player_array():
    for i in range(12):
        playerArray[i].update_coords()


def blitz_main(forceBlitzWin):
    print("-Start of Blitzball program")
    print("-First, clicking to the start of the match.")
    memory.main.click_to_story_progress(535)
    print("-Match is now starting.")
    startTime = logs.time_stamp()

    game_vars.blitz_first_shot_reset()
    movementSetFlag = False
    lastState = 0
    lastMenu = 0
    lastPhase = 99
    while (
        memory.main.get_story_progress() < 582 or memory.main.get_story_progress() > 700
    ):  # End of Blitz
        try:
            if lastPhase != game_stage() and game_clock() > 0 and game_clock() < 301:
                lastPhase = game_stage()
                print("------------------------------")
                print("New phase reached.", lastPhase)
                print("------------------------------")
            if goers_score_first() or halftime_dialog():
                if lastMenu != 3:
                    print("Dialog on-screen")
                    lastMenu = 3
                FFXC.set_neutral()
                xbox.menu_b()
            if memory.main.get_map() == 62:
                if active_clock():
                    if lastState != 1:
                        print("Clock running.")
                        lastState = 1
                    if aurochs_control():
                        if lastMenu != 2:
                            # print("Camera focusing Aurochs player")
                            lastMenu = 2
                        if not movementSetFlag:
                            xbox.tap_y()
                        else:
                            blitz_movement()
                    else:
                        if lastMenu != 8:
                            # print("Camera focusing opposing player")
                            lastMenu = 8
                else:
                    FFXC.set_neutral()
                    if lastState != 2:
                        print("Menu should be coming up")
                        lastState = 2
                    if select_movement():
                        if lastMenu != 4:
                            print("Selecting movement method")
                            lastMenu = 4
                        if cursor_1() == 1:
                            xbox.menu_b()
                            movementSetFlag = True
                        else:
                            xbox.menu_down()
                            print(cursor_1())
                    elif select_formation():
                        if lastMenu != 5:
                            print("Selecting Formation")
                            lastMenu = 5
                        if cursor_1() == 0:
                            xbox.menu_b()
                        else:
                            xbox.menu_up()
                    elif select_formation_2():
                        if lastMenu != 5:
                            print("Selecting Formation")
                            lastMenu = 5
                        if cursor_1() == 7:
                            xbox.menu_b()
                        else:
                            xbox.menu_up()
                    elif select_breakthrough():
                        if lastMenu != 6:
                            print("Selecting Break-through")
                            memory.main.wait_frames(2)
                            lastMenu = 6
                        decide_action()
                    elif select_pass_target():
                        if lastMenu != 11:
                            print("Selecting pass target.")
                            lastMenu = 11
                        decide_action()
                    elif select_shot_type():
                        if lastMenu != 12:
                            print("Selecting shot type")
                            lastMenu = 12
                        if cursor_1() == 1:
                            xbox.menu_b()
                        else:
                            xbox.menu_down()
                            memory.main.wait_frames(3)
                    elif select_action():
                        if lastMenu != 7:
                            print("Selecting action (Shoot/Pass/Dribble)")
                            lastMenu = 7
                        decide_action()
            else:
                FFXC.set_neutral()
                if lastState != 3:
                    print("Screen outside the Blitz sphere")
                    lastState = 3
                if half_summary_screen():
                    if memory.main.diag_progress_flag() == 113:
                        if cursor_1() != 1:  # Pass command
                            xbox.menu_down()
                            memory.main.wait_frames(3)
                        else:
                            xbox.menu_b()
                    elif (
                        memory.main.diag_skip_possible()
                    ):  # Skip through everything else
                        xbox.menu_b()
                elif new_half():
                    if forceBlitzWin:
                        memory.main.blitzball_patriots_style()
                    if memory.main.diag_progress_flag() == 347:
                        # Used for repeated Blitz games, not for story.
                        movementSetFlag = False
                    prep_half()
                else:
                    storyline(forceBlitzWin)
        except Exception as xVal:
            print("Caught exception in blitz memory.main.:")
            print(xVal)

    print("Blitz game has completed.")
    # Set the blitzWin flag for the rest of the run.
    print(
        "Final scores: Aurochs:",
        memory.main.blitz_own_score(),
        ", Opponent score:",
        memory.main.blitz_opp_score(),
    )
    FFXC.set_neutral()
    if memory.main.blitz_own_score() > memory.main.blitz_opp_score():
        game_vars.set_blitz_win(True)
    else:
        game_vars.set_blitz_win(False)

    endTime = logs.time_stamp()
    timeDiff = endTime - startTime
    totalTime = int(timeDiff.total_seconds())
    rngTrack.record_blitz_results(duration=totalTime)
    print("--Blitz Win value:", game_vars.get_blitz_win())
