
import memory.main
import time
import xbox
FFXC = xbox.controller_handle()
import math
import logging
logger = logging.getLogger(__name__)
from blitzball import blitz_class, blitz_pathing
blitz_state = blitz_class.blitz_state_handle()
from blitzball.blitz_tools import (
    game_clock,
    active_clock,
    cursor_1,
    select_tackle,
    select_breakthrough,
    select_action,
    select_pass_target,
    select_type,
    targeted_player,
    dialog,
    max_menu_size,
    update_tracker,
    tracker_helper,
    input_ready,
    reset_input_helpers
)

def tidus_needs_xp():
    logger.info("We're going to try to get Tidus some XP now.")
    while not blitz_state.tidus_xp_gained:
        # logger.debug(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
        if memory.main.get_map() != 62:
            return
        if dialog():
            FFXC.set_neutral()
            xbox.tap_confirm()
            return
        blitz_state.update()
        # x = round(blitz_state.player_array[0].position[0],2)
        # y = round(blitz_state.player_array[0].position[1],2)
        # logger.debug(f"Test: [{x},{y}]")
        if blitz_state.controlling_player_index == 0:
            # Tidus in control. Pass if not guarded, otherwise shoot.
            if active_clock():
                # logger.debug(f"Tidus has the ball: {round(blitz_state.get_distance(0,3),2)}")
                if blitz_state.get_distance(0,3) < 280:
                    xbox.tap_x()
                elif game_clock() > 280:
                    xbox.tap_x()
                elif blitz_state.player_array[0].radius < 350:
                    blitz_pathing.set_movement([-300, -400])
                else:
                    radius_movement(radius=380,direction="back")
            elif game_clock() > 280:
                if shoot_ball(break_through=0):
                    blitz_state.tidus_xp_gained = True
            elif (
                blitz_state.get_distance(0,8) < 150 or
                blitz_state.get_distance(0,10) < 150
            ):
                logger.debug(f"8 distance: {blitz_state.get_distance(0,8)}")
                logger.debug(f"10 distance: {blitz_state.get_distance(0,10)}")
                if shoot_ball(break_through=0):
                    blitz_state.tidus_xp_gained = True
            elif blitz_state.get_distance(0,3) < 280:
                if pass_ball(target=3, break_through=1):
                    blitz_state.tidus_xp_gained = True
            else:
                if shoot_ball(break_through=0):
                    blitz_state.tidus_xp_gained = True
        elif blitz_state.controlling_player_index == 2:
            if active_clock():
                if game_clock() > 270:
                    FFXC.set_neutral()
                    xbox.tap_x()
                else:
                    blitz_pathing.set_movement([-10, -592])
                    if blitz_state.player_array[8].is_aggro:
                        xbox.tap_x()
            elif game_clock() > 270:
                pass_ball(target=3)
            elif blitz_state.player_array[8].is_aggro:
                if not blitz_state.player_array[3].is_guarded:
                    pass_ball(target=3,break_through=0)
                elif not blitz_state.player_array[0].is_guarded:
                    pass_ball(target=0,break_through=0)
                elif not blitz_state.player_array[4].is_guarded:
                    pass_ball(target=4,break_through=0)
                elif not blitz_state.player_array[1].is_guarded:
                    pass_ball(target=1,break_through=0)
                else:
                    pass_ball(target=0,break_through=0)
            else:
                dribble_ball()
        elif blitz_state.controlling_player_index == 3:
            if active_clock():
                if game_clock() > 280:
                    FFXC.set_neutral()
                    xbox.tap_x()
                if blitz_state.player_array[2].is_guarded:
                    blitz_pathing.set_movement([-10, -592])
                else:
                    FFXC.set_neutral()
                    xbox.tap_x()
            elif game_clock() > 280:
                pass_ball(target=0)
            elif not blitz_state.player_array[2].is_guarded:
                pass_ball(target=2)
            elif (
                blitz_state.player_array[7].is_aggro and
                not blitz_state.player_array[8].is_aggro and 
                not blitz_state.player_array[10].is_aggro
            ):
                dribble_ball()
            else:
                pass_ball(target=0)
        else:
            defensive_movements()

        blitz_state.update()

def jassu_train():
    defensive_movements()
    return
    # logger.debug("All aboard the Jassu train! Choo choo!")
    blitz_state.update()
    idx = blitz_state.controlling_player_index
    if active_clock():
        if blitz_state.controlling_player_index != 3:
            if blitz_state.player_array[idx].is_guarded:
                find_safe_place()
                if blitz_state.player_array[idx].is_engaged:
                    xbox.tap_x()
                elif not (
                    blitz_state.player_array[idx].is_guarded or
                    blitz_state.player_array[3].is_guarded
                ) and blitz_state.get_distance(idx, 3) < 450:
                    xbox.tap_x()
        else:
            jassu_coords = blitz_state.player_array[idx].position
            if abs(jassu_coords[0]) < 40:
                if jassu_coords[1] > 400:
                    blitz_pathing.set_movement([jassu_coords[0]+20, jassu_coords[1]])
                else:
                    blitz_pathing.set_movement([jassu_coords[0]-720, jassu_coords[1]])
            elif jassu_coords[0] < 1:
                radius_movement(direction="forward")
            else:
                radius_movement(direction="back")
            
            aggros = 0
            for i in range(6,11):
                if blitz_state.player_array[i].is_aggro:
                    aggros += 1
            logger.debug(f"JASSU TRAIN CHOO CHOO!!! We have {aggros} passengers!")
    else:
        if blitz_state.controlling_player_index != 3:
            pass_ball(target=3, break_through=5)
        else:
            dribble_ball()

def attempt_goals(timed:bool=True):
    st = blitz_state
    while memory.main.get_map() == 62:
        st.update(timed=timed)
        update_tracker()
        if dialog():
            FFXC.set_neutral()
            xbox.tap_confirm()
        elif input_ready() and select_tackle():
            cursor(target=1)
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
        elif st.current_stage == st.IDLE:
            FFXC.set_neutral()
        elif st.current_stage == st.SHOOTING_FOR_GOAL:
            if active_clock():
                blitz_pathing.set_movement([-20, 590])
                xbox.menu_x()
            else:
                if (
                    blitz_state.player_array[7].is_engaged and
                    not blitz_state.player_array[8].is_engaged and
                    not blitz_state.player_array[9].is_engaged and
                    not blitz_state.player_array[10].is_engaged
                ):
                    shoot_ball()
                else:
                    shoot_ball()

        elif st.current_stage == st.RUSH_GOAL:
            if active_clock():
                if blitz_state.player_array[0].position[1] < 550:
                    blitz_pathing.set_movement([-120, 580])
                else:
                    if blitz_pathing.set_movement([-90, 585]):
                        xbox.tap_x()
            elif blitz_state.controlling_player_index == 0:
                shoot_ball()
            else:
                dribble_ball()
        elif st.current_stage == st.PASSING_TO_TIDUS:
            if active_clock():
                FFXC.set_movement(-1,-1)
                xbox.menu_x()
            elif blitz_state.controlling_player_index == 0:
                blitz_pathing.set_movement([-50, 580])
            else:
                pass_ball()
        elif st.current_stage == st.BAITING_DEFENDER:
            jassu_bait()
            # if active_clock():
            #     jassu_bait()
            # else:
            #     dribble_ball()
        elif st.current_stage == st.JASSU_STAGING:
            if active_clock():
                working_forward()
            else:
                dribble_ball()
        else:
            # stage == st.DEFENSIVE_HOLD
            defensive_movements()

def get_bait_position(defender_idx, target_radius_offset=40, desired_dist=250):
    st = blitz_state
    def_pos = st.player_array[defender_idx].position
    
    # 1. Calculate actual distance of defender from center (0,0)
    actual_def_dist = math.sqrt(def_pos[0]**2 + def_pos[1]**2)
    target_r = actual_def_dist + target_radius_offset
    
    # 2. Get Defender's current angle
    def_angle = math.atan2(def_pos[1], def_pos[0])
    
    # 3. Angular Gap (Law of Cosines)
    cos_val = 1 - (desired_dist**2 / (2 * target_r**2))
    angular_gap = math.acos(max(-1, min(1, cos_val)))
    
    # 4. Calculate BOTH possible intersection points
    angle_option_1 = def_angle + angular_gap
    angle_option_2 = def_angle - angular_gap
    
    # Convert both to Y-coordinates to compare
    y1 = target_r * math.sin(angle_option_1)
    y2 = target_r * math.sin(angle_option_2)
    
    # 5. Prioritize the point closer to OWN goal (lower Y value)
    # In Blitzball, your own goal is usually in the negative Y direction
    if y1 < y2:
        final_angle = angle_option_1
    else:
        final_angle = angle_option_2

    # 6. Final Coordinates
    tx = target_r * math.cos(final_angle)
    ty = target_r * math.sin(final_angle)
    
    return [tx, ty]

def jassu_bait():
    st = blitz_state
    st.update()
    
    # Indices for clarity
    TARGET = 0
    JASSU = 3
    DEFENDER = 10
    OTHER_AGGRO = 8

    if active_clock():
        # Condition A: Defender has engaged (Aggro) -> Retreat using your new radius logic
        if st.player_array[OTHER_AGGRO].is_aggro or st.player_array[DEFENDER].is_aggro:
            jassu_radius = min(st.player_array[JASSU].radius + 20, 585)
            # Move back toward goal while staying on the current radius
            radius_movement(radius=jassu_radius, direction="back")
            return
            
        # If we are too far, or just maintaining the bait position
        else:
            target = get_bait_position(DEFENDER, target_radius_offset=40, desired_dist=250)
            blitz_pathing.set_movement(target)
            return

    else:
        # Ball handling when clock is paused/menu interaction
        if (
            st.get_distance(TARGET, DEFENDER) > 160 and
            st.player_array[TARGET].position[1] > st.player_array[DEFENDER].position[1]
        ):
            pass_ball(0)
        else:
            dribble_ball()

def defensive_movements():
    st = blitz_state
    st.update()
    update_tracker()
    idx = st.controlling_player_index
    if active_clock():
        # logger.debug(f"Moving defensively (A) {idx}")
        if idx == 1:
            # logger.debug(f"Moving defensively (1) {idx}")
            if blitz_pathing.set_movement([295, 510]):
                xbox.tap_x()
        elif idx == 4:
            if not st.player_array[4].is_guarded and not st.player_array[3].is_guarded:
                # logger.debug(f"Moving defensively (4A) {idx}")
                blitz_pathing.set_movement([10, -590])
                xbox.tap_x()
            elif st.player_array[8].is_aggro:
                # logger.debug(f"Moving defensively (4B) {idx}")
                blitz_pathing.set_movement([295, -510])
                if st.get_distance(8, 3) > 360:
                    xbox.menu_x()
                elif st.get_distance(8, 4) < 240:
                    xbox.menu_x()
            elif st.player_array[9].is_aggro and st.get_distance(9, 4) < 240:
                # logger.debug(f"Moving defensively (4C) {idx}")
                blitz_pathing.set_movement([10, -590])
                xbox.menu_x()
            else:
                # logger.debug(f"Moving defensively (4D) {idx}")
                blitz_pathing.set_movement([10, -590])
        elif idx == 2:
            if st.player_array[8].position[1] < st.player_array[2].position[1]:
                # logger.debug(f"Moving defensively (2A) {idx}")
                blitz_pathing.set_movement([15, 585])
                xbox.tap_x()
            else:
                # logger.debug(f"Moving defensively (2B) {idx}")
                blitz_pathing.set_movement([15, -585])
            if st.own_score > st.opp_score and memory.main.get_story_progress() < 700:
                pass
            elif not st.player_array[3].is_guarded and not st.player_array[2].is_guarded:
                xbox.tap_x()
        elif idx == 3:
            if st.player_array[8].is_aggro:
                # logger.debug(f"Moving defensively (3A) {idx}")
                blitz_pathing.set_movement([-295, -510])
                if st.get_distance(8, 3) < 220:
                    xbox.menu_x()
            elif abs(st.player_array[3].position[0]) > 30:
                # logger.debug(f"Moving defensively (3B) {idx}")
                radius_movement(direction="back")
            else:
                # logger.debug(f"Moving defensively (3C) {idx}")
                blitz_pathing.set_movement([-10, -592])
        else:
            if st.player_array[0].position[1] > st.player_array[10].position[1] + 90:
                # logger.debug(f"Moving defensively (9A) {idx}")
                if blitz_pathing.set_movement([520, -80]):
                    xbox.tap_x()
            else:
                # logger.debug(f"Moving defensively (9B) {idx}")
                blitz_pathing.set_movement([-520, -80])
                if st.player_array[idx].is_engaged:
                    xbox.tap_x()
    else:
        FFXC.set_neutral()
        if idx > 5:
            return
        if input_ready():
            logger.debug(f"Time to select an action. {idx}")
            if idx == 1:
                if st.player_array[idx].position[1] > 300:
                    shoot_ball()
                else:
                    pass_ball(target=3, break_through=5)
            elif idx == 3:
                if st.player_array[8].is_aggro:
                    if st.player_array[0].position[1] > st.player_array[8].position[1] + 40:
                        pass_ball(target=0)
                    elif st.get_distance(8, 4) > 360:
                        pass_ball(target=4)
                    elif not st.player_array[2].is_guarded:
                        pass_ball(target=2)
                    else:
                        pass_ball(target=4)
                else:
                    dribble_ball()
            elif idx == 4:
                if not st.player_array[3].is_guarded:
                    pass_ball(target=3)
                elif st.player_array[8].is_aggro:
                    if st.player_array[1].position[1] > st.player_array[9].position[1]:
                        pass_ball(target=1)
                    else:
                        pass_ball(target=3)
                else:
                    dribble_ball()
            elif idx == 2:
                if not st.player_array[3].is_guarded:
                    pass_ball(target=3)
                elif st.player_array[0].position[1] > st.player_array[10].position[1] + 120:
                    pass_ball(target=0)
                elif st.player_array[1].position[1] > st.player_array[10].position[1] + 120:
                    pass_ball(target=1)
                elif not st.player_array[4].is_guarded:
                    pass_ball(target=4)
                else:
                    pass_ball(target=3)
            elif st.player_array[3].position[1] > 500:
                shoot_ball()
            elif not st.player_array[3].is_guarded:
                pass_ball(target=3)
            else:
                dribble_ball()


def prep_half():
    # Map = 347, Dialog = 20
    logger.info("Prepping for next period of play.")

    while memory.main.get_map() != 62:
        logger.info(memory.main.diag_progress_flag())
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
            while memory.main.blitz_char_select_cursor() != 0:
                pass
            while memory.main.blitz_char_select_cursor() != 6:
                xbox.tap_a()
            else:
                xbox.menu_b()
                memory.main.wait_frames(8)
        elif memory.main.diag_progress_flag() == 40:
            logger.info("Attempting to proceed.")
            if memory.main.blitz_proceed_cursor() != 0:
                xbox.menu_up()
            else:
                xbox.menu_b()
            memory.main.wait_frames(2)
        elif memory.main.diag_progress_flag() == 47:
            if cursor_1() != 0:
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
            if cursor_1() != 1:
                xbox.menu_up()
                memory.main.wait_frames(2)
            else:
                xbox.menu_b()
                xbox.menu_b()
                time.sleep(6)
        elif memory.main.diag_progress_flag() == 27:
            logger.warning("Skill setting screen")
            while not memory.main.diag_skip_possible():
                pass
            xbox.tap_back()
            memory.main.wait_frames(9)
            xbox.tap_confirm()
            memory.main.wait_frames(9)
            xbox.tap_back()
            memory.main.wait_frames(25)
            xbox.tap_confirm()
        elif memory.main.diag_progress_flag() == 22:
            logger.warning("Skill setting screen (2)")
            xbox.tap_back()
            memory.main.wait_seconds(1)
            xbox.tap_back()
            memory.main.wait_frames(9)
            xbox.tap_confirm()
            memory.main.wait_frames(9)
        elif memory.main.diag_progress_flag() == 33:
            logger.warning("Skill setting screen (3)")
            xbox.tap_back()
            memory.main.wait_seconds(1)
            xbox.tap_back()
            memory.main.wait_seconds(1)
            xbox.tap_back()
            memory.main.wait_frames(9)
            xbox.tap_confirm()
            memory.main.wait_frames(9)
        elif memory.main.diag_progress_flag() == 103:
            if memory.main.diag_skip_possible():
                xbox.tap_back()
                memory.main.wait_seconds(1)
                xbox.tap_back()
                memory.main.wait_frames(9)
                xbox.menu_b()
        elif memory.main.diag_skip_possible():
            xbox.menu_b()
    logger.info("Prep complete.")



def working_forward():
    blitz_state.update()
    # logger.debug("Working forward")
    idx = blitz_state.controlling_player_index
    c_player = blitz_state.player_array[idx].position
    def_player = blitz_state.player_array[10].position
    # if blitz_state.get_distance(3, 10) < 400:
    #     radius_movement(direction="back")
    if def_player[1] - c_player[1] < 400:
        blitz_pathing.set_movement([def_player[0], def_player[1]-375])
    elif c_player[1] > -180:
        blitz_pathing.set_movement([-585, -130])
    elif c_player[0] > -30:
        blitz_pathing.set_movement([c_player[0]-30, c_player[1]])
    else:
        if active_clock():
            radius_movement(radius = 585, direction="forward")


def radius_movement(radius: int = 590, direction="forward"):
    # logger.debug(f"Radius movement: {radius}")
    try:
        blitz_state.update()
        idx = blitz_state.controlling_player_index
        player_pos = blitz_state.player_array[idx].position
        current_radius = blitz_state.player_array[idx].radius

        # 1. Get current angle
        current_angle = math.atan2(player_pos[1], player_pos[0])

        # 2. Determine Angular Direction
        # In Blitzball, "forward" usually means +Y (Opponent Goal)
        # and "backward" means -Y (Your Goal).
        
        # We calculate the step based on whether we want Y to increase or decrease
        angular_step = 0.08 
        
        # If we are on the Right side (X > 0), increasing the angle moves us UP (+Y)
        # If we are on the Left side (X < 0), increasing the angle moves us DOWN (-Y)
        if player_pos[0] >= 0:
            actual_step = angular_step if direction == "forward" else -angular_step
        else:
            actual_step = -angular_step if direction == "forward" else angular_step

        next_angle = current_angle + actual_step

        # 3. Radial Push (Spiral out)
        expansion_speed = 20
        next_radius = min(current_radius + expansion_speed, radius) if current_radius < radius else radius

        # 4. Convert to Cartesian
        target_x = next_radius * math.cos(next_angle)
        target_y = next_radius * math.sin(next_angle)

        # 5. The "Explosion" Ratio
        # Project the vector to the outer edge so the AI "re-aims" aggressively
        ratio = radius / max(1, next_radius)
        
        target_coords = [target_x * ratio, target_y * ratio]

        blitz_pathing.set_movement(target_coords)
        return target_coords
    except Exception as e:
        logger.warning(f"Error during radius movement: {e}")
        return [-200,-500]

def radius_movement_coder(radius: int = 585, direction="forward"):
    logger.debug(f"Radius movement test")
    blitz_state.update()
    idx = blitz_state.controlling_player_index
    player_pos = blitz_state.player_array[idx].position

    if abs(player_pos[0]) < 20:
        if player_pos[1] > 1:
            target_coords = [player_pos[0]+40,player_pos[1]]
        else:
            target_coords = [player_pos[0]-40,player_pos[1]]
        blitz_pathing.set_movement(target_coords)
    
    # 1. How far to 'step' along the Y axis per frame
    step_size = 15 
    
    # 2. Determine target Y based on direction
    if direction == "forward":
        target_y = player_pos[1] + step_size
    else:
        target_y = player_pos[1] - step_size

    # 3. Clamp target_y to the radius so the math doesn't explode at the poles
    target_y = max(min(target_y, radius - 1), -radius + 1)

    # 4. Calculate the corresponding X to keep them on the circle (or moving towards circle)
    # x^2 + y^2 = r^2  =>  x = sqrt(r^2 - y^2)
    target_x = math.sqrt(max(0, radius**2 - target_y**2))

    # 5. Maintain the "Side" of the circle
    # If the player was on the left (negative X), keep them on the left
    if player_pos[0] < 0:
        target_x *= -1
    
    current_radius = blitz_state.player_array[idx].radius
    radius_ratio = radius / current_radius
    target_x *= radius_ratio
    target_y *= radius_ratio

    target_coords = [target_x, target_y]
    
    # 6. Execute
    blitz_pathing.set_movement(target_coords)
    return target_coords


def pass_ball(target=0, break_through=5):
    tracker_helper("Pass")
    if not input_ready():
        tracker_helper(None)
        return False
    if memory.main.get_map() != 62:
        logger.warning(f"Pass ball error - wrong map: {memory.main.get_map()}")
        tracker_helper(None)
        return False
    logger.debug(f"Pass Ball command - {target} | Break {break_through}")
    FFXC.set_neutral()
    blitz_state.update()
    idx = blitz_state.controlling_player_index
    if idx == 4:
        break_through = 0
    logger.debug("Test 3")
    while not active_clock():
        if memory.main.get_map() != 62:
            return
        if select_breakthrough():
            logger.debug("Selecting breakthrough value (A)")
            if break_through == 5:
                cursor(any_non_zero=True)
            else:
                xbox.menu_b()
                xbox.menu_b()
                xbox.menu_b()
                memory.main.wait_frames(9)
                reset_input_helpers()
                return True
        elif select_action():
            cursor(target=0)
        elif select_pass_target():
            logger.debug(f"Selecting pass target value, target {target}")
            cursor(target_player=target)
            tracker_helper(None)
            return True
        else:
            logger.debug("Pass - other")
            xbox.menu_b()
    tracker_helper(None)
    return False


def shoot_ball(break_through=None):
    tracker_helper("Shoot")
    if not input_ready():
        return False
        tracker_helper(None)
    if memory.main.get_map() != 62:
        logger.warning(f"Shoot ball error - wrong map: {memory.main.get_map()}")
        tracker_helper(None)
        return False
    logger.debug(f"Shoot Ball command - Break {break_through}")
    FFXC.set_neutral()
    idx = blitz_state.controlling_player_index
    if break_through is None:
        if memory.main.get_story_progress() > 700 and idx == 0:
            break_through = 0
        elif memory.main.get_story_progress() < 570 and idx == 0:
            if game_clock() > 167:
                break_through = 5
            else:
                break_through = 5
        else:
            break_through = 5
    
    while not active_clock():
        if memory.main.get_map() != 62:
            return
        if select_type():
            cursor(target=1)
            tracker_helper(None)
            return True
        elif select_breakthrough():
            logger.debug("Selecting breakthrough value (B)")
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
            cursor(target=1)
            if idx != 0:
                return True
                # game_vars.blitz_first_shot_taken()


def dribble_ball():
    if not input_ready():
        return False
    if memory.main.get_map() != 62:
        logger.warning(f"Dribble error - wrong map: {memory.main.get_map()}")
        return
    logger.debug("Dribble Ball command")
    FFXC.set_neutral()
    memory.main.wait_frames(2)
    blitz_state.update()
    logger.debug(f"Variable check: {active_clock()} | {select_breakthrough()}")
    while not active_clock():
        if memory.main.get_map() != 62:
            return
        if input_ready():
            cursor(max=True)
            memory.main.wait_frames(3)

def cursor(target:int=0,any_non_zero:bool=False,target_player=None,max:bool=False):
    if not input_ready():
        return False
    FFXC.set_neutral()
    if any_non_zero:
        max = True
    if max:
        target = max_menu_size()-1
    if target > max_menu_size()-1:
        logger.debug(f"Cursor Error: {target}/{max_menu_size()-1}")
        if any_non_zero:
            target = 1
        else:
            target = 0
    start = memory.main.get_frame()
    end = start
    logger.debug("Reset cursor")
    while cursor_1() != 0 and not max:
        if memory.main.get_map() != 62:
            return
        logger.debug(f"Cursor Base: {cursor_1()} | 0")
        if not input_ready():
            return False
        logger.debug("Reset cursor *")
        if memory.main.get_map() != 62:
            return
        if end < start:
            return
        if end - start > 45:  # 1.5 seconds more than enough.
            return
        
        # Now move the cursor
        xbox.menu_up()
        
    counter = 0
    if target_player is not None:
        logger.debug(f"Target: {target_player}")
        while targeted_player() != target_player:
            if memory.main.get_map() != 62:
                return
            logger.debug(f"Target Player: {cursor_1()} | 0")
            if memory.main.get_map() != 62:
                return
            if max:
                xbox.menu_a()
            elif target_player <= 2:
                xbox.menu_down()
            else:
                xbox.menu_up()
            memory.main.wait_frames(3)
            counter += 1
            if counter > 12:
                break
    else:
        logger.debug("Regular cursor method")
        while cursor_1() != target:
            if memory.main.get_map() != 62:
                return
            logger.debug(f"Cursor Target: {cursor_1()} | {target}")
            if memory.main.get_map() != 62:
                return
            if max:
                xbox.menu_a()
            elif target <= 1:
                xbox.menu_down()
            else:
                xbox.menu_up()
            memory.main.wait_frames(3)
            counter += 1
            if counter > 12:
                break
    logger.debug("Final Cursor Trigger.")
    if not input_ready():
        return False
    xbox.menu_b()
    memory.main.wait_frames(18)


def find_safe_place():
    blitz_state.update()
    idx = blitz_state.controlling_player_index
    # current player
    c_player = blitz_state.player_array[idx].position
    # graav coords
    target_coords = [-2, -595]
    safe_spot = 255

    # Determin target coords based on character and state.
    if idx in [1, 4]:
        target_coords = [520, -20]
        blitz_pathing.set_movement(target_coords)
        return
    elif idx in [2, 3]:
        if (
            blitz_state.player_array[7].position[1] < -10
            or blitz_state.player_array[6].position[1] < -10
        ):
            safe_spot = 3
            # safe_spot = 2
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
    
    blitz_pathing.set_movement(target_coords)
    return

    # I think this is still the best option.
    # target_coords = [-2, -595]

