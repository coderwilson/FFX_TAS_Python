import logging
import math
import time
from typing import List

import blitz_pathing
import logs
import memory.main
import rng_track
import vars
import xbox
from memory.main import BlitzActor

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()
tidus_xp = False

FFXC = xbox.controller_handle()

report_state = False
player_array: List[BlitzActor] = []

# Initialize the player array
for i in range(12):
    player_array.append(memory.main.BlitzActor(player_num=i))

global engage_defender
engage_defender = False


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
    ret_val = memory.main.blitz_target_player() - 2
    return ret_val


def active_clock():
    return not memory.main.blitz_clock_pause()


def aurochs_control():
    return memory.main.blitz_target_player() < 8


def controlling_player():
    ret_val = memory.main.blitz_current_player() - 2
    if ret_val < 200:
        return ret_val
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
    logger.info("Prepping for next period of play.")
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
            logger.info("Attempting to proceed.")
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
    logger.info("Prep complete.")


def storyline(force_blitz_win):
    current = memory.main.get_story_progress()
    if not game_vars.csr():
        if current == 540:
            if force_blitz_win:
                memory.main.blitzball_patriots_style()
            logger.info("Halftime hype")
            memory.main.click_to_diag_progress(164)
            memory.main.click_to_diag_progress(20)
        elif current == 560 and memory.main.diag_progress_flag() > 1:
            logger.info("Wakka story happening.")
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
    shot_distance = distance(0, 11)
    shot_mod = int(shot_distance / 160)
    if 540 <= memory.main.get_story_progress() < 570:
        base_timing = int(156 - shot_mod)
    else:
        base_timing = int(265 - shot_mod)

    for x in range(5):
        if distance(0, x + 6) < 180:
            base_timing = int(base_timing - 4)
    return base_timing


def tidus_shot_timing() -> int:
    shot_distance = distance(0, 11)
    shot_mod = int(shot_distance / 160)
    if 540 <= memory.main.get_story_progress() < 570:
        base_timing = int(170 - shot_mod)
    else:
        base_timing = int(288 - shot_mod)

    for x in range(5):
        if distance(0, x + 6) < 180:
            base_timing = int(base_timing - 4)
    return base_timing


def game_stage():
    # Stage 0: Killing time
    # Stage 1: Defensive, Letty dribble, consumes Jassu HP
    # Stage 2: Jassu position near the edge of the pool, look for opportunity.
    # Stage 3: Positioning Defender so Tidus can shoot/score
    # Stage 4: Pass to Tidus
    # Stage 5: Shoot for goal
    current_stage = 0
    global engage_defender
    # Logic that immediately moves to scoring phases if in overtime.
    if 570 < memory.main.get_story_progress() < 700:
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
            current_stage = 20  # default 20
        else:
            current_stage = 30
    else:
        if game_vars.get_blitz_ot():
            stages = [0, 2, 2, 2, 300, 300]
        else:
            # logger.info("After Wakka")
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
        current_stage = 30
    elif memory.main.blitz_own_score() - memory.main.blitz_opp_score() >= 1 and (
        570 < memory.main.get_story_progress() < 700
    ):
        # Ahead by 1 goal after Wakka enters, just end the game.
        current_stage = 30
    elif memory.main.get_story_progress() < 540:
        if not game_vars.blitz_first_shot():
            current_stage = 20
        else:
            current_stage = 30
    elif current_stage == 0:
        for i in range(6):
            if stages[i] < game_clock():
                current_stage = i

        if memory.main.get_story_progress() < 700 and current_stage >= 1:
            # Only apply following logic for the storyline game
            # Logic that updates stage based on defender movements
            if player_array[0].get_coords()[1] - player_array[10].get_coords()[1] > 300:
                if current_stage < 3:
                    current_stage = 4

            # Logic that reduces stage if score is too far apart.
            if (
                memory.main.blitz_own_score() - memory.main.blitz_opp_score() >= 2
                and memory.main.get_story_progress() >= 570
            ):
                current_stage = 0

            # Logic if we're in defensive zone trying to move forward
            if (
                current_stage == 3
                and player_array[controlling_player()].get_coords()[1] < -200
            ):
                current_stage = 2
    if current_stage == 3 and not engage_defender:
        logger.debug("Start engaging defender!")
        engage_defender = True
    elif current_stage == 2 and engage_defender:
        current_stage = 3
    elif current_stage in [0, 1, 20, 30] and engage_defender:
        logger.debug("Disengaging defender logic")
        engage_defender = False

    if current_stage < 3 and controlling_player() == 0:
        current_stage = 30
    return current_stage


def distance_special():
    try:
        player1 = player_array[6].get_coords()
        player2 = [222, -238]  # Formerly 230,-260
        total_distance = abs(player1[1] - player2[1]) + abs(player1[0] - player2[0])
        return total_distance
    except Exception as x:
        logger.exception(x)
        return 999


def get_char_radius(player_index: int = 10):
    player_coords = player_array[player_index].get_coords()
    try:
        result = math.sqrt(
            (player_coords[0] * player_coords[0])
            + (player_coords[1] * player_coords[1])
        )
    except Exception:
        logger.error("Math error, using default value.")
        logger.error(f"Coords: {player_coords[0] ** 2}")
        result = 999
    return result


def radius_movement(radius: int = 580, direction="forward"):
    player_coords = player_array[controlling_player()].get_coords()
    target_coords = [-400, -400]
    char_radius = get_char_radius(controlling_player())
    if char_radius != 0:
        player_coords[0] *= radius / char_radius
        player_coords[1] *= radius / char_radius

    if direction == "forward" and -30 < player_coords[0] < 30:
        FFXC.set_movement(-1, -1)
    else:
        if direction == "forward":
            target_coords = [player_coords[0], player_coords[1] + 10]
        else:
            target_coords = [player_coords[0], player_coords[1] - 10]
        try:
            target_coords[0] = math.sqrt((radius**2) - (target_coords[1] ** 2))
            if player_coords[0] < -1:
                target_coords[0] *= -1
        except Exception as e:
            logger.warning(e)
            player_coords = player_array[controlling_player()].get_coords()
            target_coords = [-400, -400]
            char_radius = get_char_radius(controlling_player())
            if char_radius != 0:
                player_coords[0] *= radius / char_radius
                player_coords[1] *= radius / char_radius

            if direction == "forward":
                target_coords = [player_coords[0], player_coords[1]]
            else:
                target_coords = [player_coords[0], player_coords[1]]

            if player_coords[1] < -1:
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
                if player_coords[1] < -1:
                    target_coords[1] *= -1
            except Exception as e:
                logger.warning(e)
                if direction == "forward":
                    target_coords[0] = player_coords[0] - 10
                    target_coords[1] = player_coords[1] + 10
                else:
                    target_coords[0] = player_coords[0] + 10
                    target_coords[1] = player_coords[1] - 10
    blitz_pathing.set_movement(target_coords)
    return target_coords


def working_forward():
    c_player = player_array[controlling_player()].get_coords()
    # if distance(3,10) < 330:
    #    radius_movement(direction='back')
    if c_player[1] > -180:
        # logger.debug("In position")
        blitz_pathing.set_movement([-585, -130])
    else:
        radius_movement()


def find_safe_place():
    # current player
    c_player = player_array[controlling_player()].get_coords()
    c_player_num = controlling_player()
    # graav coords
    player_array[8].get_coords()
    player_array[7].get_coords()
    target_coords = [-2, -595]
    safe_spot = 255

    # Determin target coords based on character and state.
    if c_player_num in [1, 4]:
        target_coords = [520, -20]
    elif c_player_num in [2, 3]:
        if player_array[7].get_coords()[1] < 10 or player_array[6].get_coords()[1] < 10:
            safe_spot = 3
        else:
            safe_spot = 2
    else:  # Should never occur, should never get Tidus/Wakka into this logic.
        safe_spot = 3

    if safe_spot == 1:  # Near the left wall
        target_coords = [-521, -266]
    elif safe_spot == 2:  # About half way
        target_coords = [-340, -497]
    elif safe_spot == 3:  # All the way back
        target_coords = [-2, -595]

    # I think this is still the best option.
    # target_coords = [-2, -595]

    if abs(c_player[0] - target_coords[0]) + abs(c_player[1] - target_coords[1]) > 120:
        if c_player[1] > target_coords[1]:
            radius_movement(radius=570, direction="back")
        else:
            radius_movement(radius=570, direction="forward")
    else:
        if blitz_pathing.set_movement(target_coords):
            return True
        else:
            return False


def jassu_train():
    logger.debug("All aboard the Jassu train! Choo choo!")
    jassu_coords = player_array[3].get_coords()
    if abs(jassu_coords[0]) < 30:
        if jassu_coords[1] > 400:
            FFXC.set_movement(0, -1)
        else:
            FFXC.set_movement(0, -1)
    elif jassu_coords[0] < 10:
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
    other_distance = 0
    if distance(0, 6) < 360:
        other_distance += 1
    if distance(0, 7) < 360:
        other_distance += 1
    if distance(0, 9) < 360:
        other_distance += 1
    if distance(0, 10) < 360:
        other_distance += 1
    if other_distance >= 2:
        return True

    # Specific cases depending on player.
    if player_num in [3, 4]:
        if distance(player_num, 9) < 340:
            return True
        if distance(player_num, 10) < 340:
            return True
    return False


def tidus_move():
    current_stage = game_stage()
    if report_state:
        logger.debug("Tidus movement")
    graav_distance = distance(0, 8)

    other_distance = 0
    if distance(0, 6) < 180:
        other_distance += 1
    if distance(0, 7) < 180:
        other_distance += 1
    if distance(0, 9) < 180:
        other_distance += 1
    if distance(0, 10) < 180:
        other_distance += 1

    shoot_target = [-170, 540]

    if current_stage > 15:
        radius_movement(radius=400, direction="back")
        if distance(0, 3) < 330:
            xbox.tap_x()
    elif memory.main.get_story_progress() > 700:
        if other_distance >= 2:
            xbox.tap_x()
        elif current_stage == 4:
            xbox.tap_x()
        elif blitz_pathing.set_movement(shoot_target):
            xbox.tap_x()
    elif current_stage in [0, 1, 2, 5]:
        FFXC.set_movement(-1, -1)
        xbox.tap_x()
    elif current_stage == 4:
        if graav_distance < 240:
            # Graav too close.
            FFXC.set_movement(-1, -1)
            xbox.tap_x()
        elif other_distance >= 2:
            # Too many players closing in.
            FFXC.set_movement(-1, -1)
            xbox.tap_x()
        elif (
            blitz_pathing.set_movement(shoot_target)
            and memory.main.get_story_progress() >= 570
        ):
            FFXC.set_movement(-1, -1)
            xbox.tap_x()
    else:  # stages 3 and 4 only. All other stages we try to pass, or just shoot.
        if player_array[0].get_coords()[1] > 470:  # Force shot
            FFXC.set_movement(-1, -1)
            xbox.tap_x()
        else:
            radius_movement(radius=570, direction="forward")


def tidus_act():
    current_stage = game_stage()
    if report_state:
        logger.debug("Tidus act")

    other_distance = 0
    if distance(0, 6) < 280:
        other_distance += 1
    if distance(0, 7) < 280:
        other_distance += 1
    if distance(0, 9) < 280:
        other_distance += 1
    if distance(0, 10) < 280:
        other_distance += 1

    if current_stage > 15:
        pass_ball(target=3)
        game_vars.blitz_first_shot_taken()
    elif memory.main.get_story_progress() > 700:
        shoot_ball(break_through=0)
    elif current_stage in [4, 5]:
        # Late on the timer. Shoot at all costs.
        if memory.main.get_story_progress() < 540:
            logger.debug("First half, shooting without breakthrough.")
            shoot_ball(break_through=0)
        else:
            logger.debug("Stage 5 - shoot the ball!")
            shoot_ball(break_through=0)
    elif current_stage in [0, 1, 2]:
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
    if report_state:
        logger.debug("Letty movement")
    current_stage = game_stage()
    graav_distance = distance(2, 8)

    if current_stage == 20:
        find_safe_place()
        if distance(0, 8) > 400 and distance(0, 10) > 400:
            xbox.tap_x()
        else:
            find_safe_place()
    elif current_stage == 30:
        find_safe_place()
        xbox.tap_x()
    elif current_stage >= 3:
        FFXC.set_movement(1, 0)
        xbox.tap_x()
    elif current_stage == 2:
        target_coords = [-20, -585]
        blitz_pathing.set_movement(target_coords)
        if not player_guarded(3):
            xbox.tap_x()
        elif not player_guarded(2):
            xbox.tap_x()
    else:
        # if not player_guarded(3) and distance(3, 10) > 380 and graav_distance > 380:
        if distance(3, 8) > 400:
            xbox.tap_x()
        else:
            if find_safe_place() and graav_distance < 280:
                xbox.tap_x()


def letty_act():
    current_stage = game_stage()
    distance(0, 2)

    if current_stage == 20:
        if distance(0, 8) > 400:
            pass_ball(target=0)
        else:
            dribble_ball()
    elif current_stage == 30:
        pass_ball(target=3)
    elif memory.main.get_story_progress() > 700:  # Post-storyline blitzball only
        if player_array[0].get_coords()[1] > player_array[1].get_coords()[1]:
            pass_ball(target=0, break_through=0)
        else:
            pass_ball(target=1, break_through=0)
    elif current_stage >= 4:
        pass_ball(target=0)
        if report_state:
            logger.debug("Letty Action 1")
    elif current_stage == 3:
        pass_ball(target=3)
        if report_state:
            logger.debug("Letty Action 2")
    elif player_array[2].current_hp() < 10:
        pass_ball(target=3)
    elif current_stage == 2:
        if distance(2, 8) < 250:
            break_through_val = 5
        else:
            break_through_val = 0

        if not player_guarded(3):
            tar = 3
        elif not player_guarded(0):
            tar = 0
        else:
            tar = 3
        pass_ball(target=tar, break_through=break_through_val)
    else:
        if not game_vars.blitz_first_shot() and distance(0, 8) > 400:
            logger.debug("Letty pass to Tidus")
            pass_ball(target=0)
        else:
            logger.debug("Letty pass to Jassu")
            pass_ball(target=3)


def jassu_move():
    target_coords = [999, 999]
    current_stage = game_stage()
    player_array[controlling_player()].get_coords()
    target_coords = [-585, -130]
    p10C = player_array[10].get_coords()
    graav_c = player_array[8].get_coords()
    tidus_c = player_array[0].get_coords()
    find_safety = False
    move_forward = False
    graav_distance = distance(3, 8)
    other_distance = 0
    target_coords = [-600, -100]
    if distance(3, 6) < 350:
        other_distance += 1
    if distance(3, 7) < 350:
        other_distance += 1
    if distance(3, 9) < 350:
        other_distance += 1
    if distance(3, 10) < 350:
        other_distance += 1

    if current_stage == 20:
        find_safe_place()
        if distance(0, 8) > 300 and distance(0, 10) > 360:
            if player_array[9].get_coords()[1] > 100:
                xbox.tap_x()
    elif current_stage == 30:
        # jassu_train()
        find_safe_place()
        move_forward = True
    elif current_stage <= 1 and player_array[3].current_hp() < 10:
        if player_array[2].current_hp() >= 40 and distance(2, 8) > 360:
            xbox.tap_x()
        elif graav_distance < 320:
            xbox.tap_x()
        else:
            find_safety = True
    elif current_stage == 0:
        # Defend in the goal for safety.
        find_safety = True
        if player_array[2].current_hp() >= 40 and current_stage == 0:
            if distance(2, 8) > 360 and distance(2, 7) > 360 and distance(2, 6) > 360:
                xbox.tap_x()
    elif current_stage == 1:
        if player_array[10].get_coords()[1] < 150:
            find_safe_place()
        elif distance(3, 8) < 350:
            find_safe_place()
        else:
            working_forward()
        move_forward = True
    elif current_stage == 2:
        # Move forward to staging position, prep for shot.
        working_forward()
        move_forward = True
    elif current_stage == 3:
        rel_dist = int((tidus_c[1] - p10C[1]) + (tidus_c[0] - p10C[0]))
        int((tidus_c[1] - graav_c[1]) + (tidus_c[0] - graav_c[0]))
        if rel_dist > 220:  # Tidus in position behind defender
            xbox.tap_x()
            move_forward = True
        elif distance(3, 10) > 340:
            move_radius = min(int(get_char_radius() + 150), 570)
            target_coords = radius_movement(radius=move_radius, direction="forward")
            move_forward = True
        else:
            move_radius = min(int(get_char_radius() + 150), 570)
            target_coords = radius_movement(radius=move_radius, direction="back")
            move_forward = True
    else:  # Pass to Tidus
        target_coords = [p10C[0] - 180, p10C[1] - 150]
        xbox.tap_x()

    if current_stage < 15 and target_coords != [999, 999]:
        if find_safety:
            if find_safe_place() and graav_distance < 320:
                xbox.tap_x()
        elif not move_forward:
            try:
                blitz_pathing.set_movement(target_coords)
            except Exception as e:
                logger.warning(e)


def jassu_act():
    current_stage = game_stage()
    player_array[controlling_player()].get_coords()
    p10C = player_array[10].get_coords()
    graav_c = player_array[8].get_coords()
    tidus_c = player_array[0].get_coords()
    current_stage = game_stage()
    if report_state:
        logger.debug("Jassu Action")
        logger.debug(f"Stage: {current_stage}")
    graav_distance = distance(3, 8)
    other_distance = 0
    if distance(3, 6) < 350:
        other_distance += 1
    if distance(3, 7) < 350:
        other_distance += 1
    if distance(3, 9) < 350:
        other_distance += 1
    if distance(3, 10) < 350:
        other_distance += 1

    if current_stage == 20:
        if distance(0, 8) > 280:
            pass_ball(0)
        else:
            dribble_ball()
    elif current_stage == 30:
        dribble_ball()
    elif current_stage == 0:
        if player_array[2].current_hp() >= 40 and distance(2, 8) > 360:
            pass_ball(target=2)
        else:
            dribble_ball()
    elif current_stage == 1:
        dribble_ball()
    elif player_array[3].current_hp() < 10:
        pass_ball(target=0)
    elif current_stage == 2:
        dribble_ball()
    elif current_stage == 3:
        rel_dist = int((tidus_c[1] - p10C[1]) + (tidus_c[0] - p10C[0]))
        int((tidus_c[1] - graav_c[1]) + (tidus_c[0] - graav_c[0]))
        if rel_dist > 180:
            pass_ball(target=0)
        elif graav_distance < 150:
            # Graav too close
            pass_ball(target=0)
        elif player_array[0].get_coords()[1] - player_array[10].get_coords()[1] > 280:
            # Tidus in position for break-away.
            pass_ball(target=0)
        else:
            dribble_ball()
    else:  # Pass to Tidus
        pass_ball(target=0)


def other_move():  # fix
    if get_char_radius(controlling_player()) < 540:
        FFXC.set_movement(0, 1)
    elif player_array[controlling_player()].get_coords()[1] < -400:
        xbox.tap_x()
    elif distance(controlling_player(), 8) < 300:
        xbox.tap_x()
    else:
        radius_movement(radius=570, direction="back")


def other_act():
    current_stage = game_stage()

    if report_state:
        logger.debug("Botta/Datto action")
        logger.debug(f"Stage: {current_stage}")

    if memory.main.get_story_progress() > 700:
        if controlling_player() == 1:
            shoot_ball()
        else:
            if player_array[0].get_coords()[1] > player_array[1].get_coords()[1]:
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
        player1 = player_array[n1].get_coords()
        player2 = player_array[n2].get_coords()
        return abs(player1[1] - player2[1]) + abs(player1[0] - player2[0])
    except Exception as x:
        logger.exception(x)
        return 999


def update_player_array():
    for i in range(12):
        player_array[i].update_coords()


def blitz_main(force_blitz_win):
    logger.info("-Start of Blitzball program")
    logger.info("-First, clicking to the start of the match.")
    memory.main.click_to_story_progress(535)
    logger.info("-Match is now starting.")
    start_time = logs.time_stamp()

    game_vars.blitz_first_shot_reset()
    movement_set_flag = False
    last_state = 0
    last_menu = 0
    last_phase = 99
    while (
        memory.main.get_story_progress() < 582 or memory.main.get_story_progress() > 700
    ):  # End of Blitz
        try:
            if last_phase != game_stage() and game_clock() > 0 and game_clock() < 301:
                last_phase = game_stage()
                logger.debug(f"New phase reached: {last_phase}")
            if goers_score_first() or halftime_dialog():
                if last_menu != 3:
                    logger.debug("Dialog on-screen")
                    last_menu = 3
                FFXC.set_neutral()
                xbox.menu_b()
            if memory.main.get_map() == 62:
                if active_clock():
                    if last_state != 1:
                        logger.debug("Clock running.")
                        last_state = 1
                    if aurochs_control():
                        if last_menu != 2:
                            # logger.debug("Camera focusing Aurochs player")
                            last_menu = 2
                        if not movement_set_flag:
                            xbox.tap_y()
                        else:
                            blitz_movement()
                    else:
                        if last_menu != 8:
                            # logger.debug("Camera focusing opposing player")
                            last_menu = 8
                else:
                    FFXC.set_neutral()
                    if last_state != 2:
                        logger.debug("Menu should be coming up")
                        last_state = 2
                    if select_movement():
                        if last_menu != 4:
                            logger.debug("Selecting movement method")
                            last_menu = 4
                        if cursor_1() == 1:
                            xbox.menu_b()
                            movement_set_flag = True
                        else:
                            xbox.menu_down()
                            logger.debug(cursor_1())
                    elif select_formation():
                        if last_menu != 5:
                            logger.debug("Selecting Formation")
                            last_menu = 5
                        if cursor_1() == 0:
                            xbox.menu_b()
                        else:
                            xbox.menu_up()
                    elif select_formation_2():
                        if last_menu != 5:
                            logger.debug("Selecting Formation")
                            last_menu = 5
                        if cursor_1() == 7:
                            xbox.menu_b()
                        else:
                            xbox.menu_up()
                    elif select_breakthrough():
                        if last_menu != 6:
                            logger.debug("Selecting Break-through")
                            memory.main.wait_frames(2)
                            last_menu = 6
                        decide_action()
                    elif select_pass_target():
                        if last_menu != 11:
                            logger.debug("Selecting pass target.")
                            last_menu = 11
                        decide_action()
                    elif select_shot_type():
                        if last_menu != 12:
                            logger.debug("Selecting shot type")
                            last_menu = 12
                        if cursor_1() == 1:
                            xbox.menu_b()
                        else:
                            xbox.menu_down()
                            memory.main.wait_frames(3)
                    elif select_action():
                        if last_menu != 7:
                            logger.debug("Selecting action (Shoot/Pass/Dribble)")
                            last_menu = 7
                        decide_action()
            else:
                FFXC.set_neutral()
                if last_state != 3:
                    logger.debug("Screen outside the Blitz sphere")
                    last_state = 3
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
                    if force_blitz_win:
                        memory.main.blitzball_patriots_style()
                    if memory.main.diag_progress_flag() == 347:
                        # Used for repeated Blitz games, not for story.
                        movement_set_flag = False
                    prep_half()
                else:
                    storyline(force_blitz_win)
        except Exception as x_val:
            logger.error("Caught exception in blitz memory.main.:")
            logger.exception(x_val)

    logger.info("Blitz game has completed.")
    # Set the blitz_win flag for the rest of the run.
    logger.info(
        f"Final scores: Aurochs: {memory.main.blitz_own_score()}, Opponent score: {memory.main.blitz_opp_score()}"
    )
    FFXC.set_neutral()
    if memory.main.blitz_own_score() > memory.main.blitz_opp_score():
        game_vars.set_blitz_win(True)
    else:
        game_vars.set_blitz_win(False)

    end_time = logs.time_stamp()
    time_diff = end_time - start_time
    total_time = int(time_diff.total_seconds())
    if game_vars.get_force_blitz_win():
        pass
    else:
        rng_track.record_blitz_results(duration=total_time)
    logger.info(f"--Blitz Win value: {game_vars.get_blitz_win()}")
