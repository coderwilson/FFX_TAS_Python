import logging
from math import copysign, sqrt

import memory.main
import xbox
import vars
import time
import random
game_vars = vars.vars_handle()

logger = logging.getLogger(__name__)
FFXC = xbox.controller_handle()
from json_ai_files.write_seed import write_big_text

class BonkTracker:
    def __init__(self):
        self.last_pos = (0, 0)
        self.last_frame = 0
        self.threshold = 0.001  # Distance moved to consider "not stuck"
        self.map_center = (0, 0)
        self.zero_pos = (99999, 99999)

    def check_stuck(self, current_pos):
        if game_vars.story_mode():
            return False
        if not game_vars.csr():
            return False
        # Only evaluate every 5 seconds
        waiting_frames = 45
        current_frame = memory.main.get_frame()
        if not (
            memory.main.user_control() and
            not memory.main.battle_active() and
            not memory.main.menu_open()
        ):
            self.last_pos = self.zero_pos
            self.last_frame = current_frame
            return False
        elif current_pos == self.zero_pos or current_pos == self.map_center:
            self.last_pos = self.zero_pos
            self.last_frame = current_frame
            return False
        
        if current_frame < self.last_frame + waiting_frames:
            # Only reset if just over 1 second.
            # This prevents us from resetting the map on longer non-pathing sections
            # or immediately on load.
            return False
        if current_frame > self.last_frame + waiting_frames + 5:
            self.last_pos = self.zero_pos
            self.last_frame = current_frame
            return False

        # Calculate Euclidean distance moved
        dist = ((current_pos[0] - self.last_pos[0])**2 + 
                (current_pos[1] - self.last_pos[1])**2)**0.5
        
        # logger.debug(f"Checking for stuck: {dist} < {self.threshold}")
        
        is_stuck = dist < self.threshold
        
        # Update state for the next check
        self.last_pos = current_pos
        self.last_frame = current_frame
        if is_stuck:
            logger.warning("STUCK IDENTIFIED, PERFORMING RESET!!!")
        
        return is_stuck
    
    def update_last(self):
        self.last_frame = memory.main.get_frame()
        self.last_pos = (0, 0)


# Initialize the global tracker
tracker = BonkTracker()

def set_movement(target, ignore_bonk = False) -> bool:
    player = memory.main.get_coords()
    if tracker.check_stuck(player):
        if not ignore_bonk:
            # Treadmill recovery logic
            memory.main.force_map_load()
            memory.main.await_control()
            tracker.update_last()
            return


    if memory.main.menu_open():
        FFXC.set_neutral()
        xbox.tap_a()
    (forward, right) = memory.main.get_movement_vectors()

    # Calculate forward and right directions relative to camera space
    pX = player[0]
    pY = player[1]
    eX = target[0]
    eY = target[1]
    fX = forward[0]
    fY = forward[1]
    rX = right[0]
    rY = right[1]

    Ly = fX * (eX - pX) + rX * (eY - pY)
    Lx = fY * (eX - pX) + rY * (eY - pY)
    sums_up = abs(Lx) + abs(Ly)
    if sums_up == 0:
        sums_up = 0.01
    Lx /= sums_up
    Ly /= sums_up
    if abs(Lx) > abs(Ly):
        Ly = copysign(Ly / Lx if Lx else 0, Ly)
        Lx = copysign(1, Lx)
    elif abs(Ly) > abs(Lx):
        Lx = copysign(Lx / Ly if Ly else 0, Lx)
        Ly = copysign(1, Ly)
    else:  # Only occurs on perfect diagonals.
        Lx = copysign(1, Lx)
        Ly = copysign(1, Ly)

    FFXC.set_movement(Lx, Ly)
    if memory.main.get_actor_id(0) == 20531:
        d = 10
    else:
        d = 3

    if game_vars.no_battle_music():
        memory.main.disable_battle_music()
    if abs(player[1] - target[1]) < d and abs(player[0] - target[0]) < d:
        return True  # Checkpoint reached
    else:
        return False

def distance(actor_index: int, actor_2:int = 0, use_super_coords:bool = False):
    # Assume index is passed in.
    actor_coords = memory.main.get_actor_coords(actor_index=actor_index)
    if memory.main.user_control():
        player_coords = memory.main.get_coords()
    else:
        player_coords = memory.main.get_actor_coords(actor_index=actor_2)
    distance = sqrt(
        ((player_coords[0] - actor_coords[0]) ** 2)
        + ((player_coords[1] - actor_coords[1]) ** 2)
    )
    return int(distance)

def distance_coords(target_coords, use_raw_coords:bool = False):
    # Assume x/y coords are passed as array.
    if use_raw_coords:
        player_coords = memory.main.get_coords()
    else:
        player_coords = memory.main.get_actor_coords(actor_index=0)
    distance = sqrt(
        ((player_coords[0] - target_coords[0]) ** 2)
        + ((player_coords[1] - target_coords[1]) ** 2)
    )
    return int(distance)


def approach_actor_by_index(actor_index: int, talk: bool = True, use_raw_coords:bool=False):
    logger.debug(f"Approaching actor, index {actor_index}")
    return _approach_actor(actor_index=actor_index, talk=talk, use_raw_coords=use_raw_coords)


def approach_actor_by_id(actor_id: int, talk: bool = True, use_raw_coords:bool=False):
    logger.debug(f"Approaching actor, ID {actor_id}")
    index = memory.main.actor_index(actor_num=actor_id)
    return _approach_actor(actor_index=index, talk=talk, use_raw_coords=use_raw_coords)


def approach_party_member(target_char, talk: bool = True, use_raw_coords:bool=False):
    logger.debug(f"Approaching party member {target_char}")
    index = target_char.actor_id
    return approach_actor_by_id(actor_id=index, talk=talk, use_raw_coords=use_raw_coords)


def _approach_actor(actor_index: int = 999, talk: bool = True, use_raw_coords:bool=False):
    logger.debug(f"Actor index {actor_index}")
    speed_val = memory.main.get_game_speed()
    if speed_val != 0:
        memory.main.set_game_speed(0)

    if use_raw_coords:
        actor_coords = memory.main.get_coords()
    else:
        actor_coords = memory.main.get_actor_coords(actor_index=actor_index)
    target_coords = [actor_coords[0], actor_coords[1]]
    logger.debug(f"Actor's coordinates: {target_coords}")

    logger.debug(f"Control: {memory.main.user_control()} | Naming: {memory.main.name_aeon_ready()}")

    start_time = time.time()
    while memory.main.user_control():
        # Timeout check
        if time.time() - start_time > 4:
            logger.warning("Timeout reached. Executing erratic behavior.")
            # Erratic behavior: move randomly for 0.5 seconds
            directions = [(1,0), (-1,0), (0,1), (0,-1)]
            dx, dy = random.choice(directions)
            erratic_target = [target_coords[0] + dx * 5, target_coords[1] + dy * 5]
            erratic_start = time.time()
            while time.time() - erratic_start < 0.5:
                set_movement(erratic_target, ignore_bonk=True)
            FFXC.set_neutral()
            return _approach_actor(actor_index=actor_index, talk=talk)

        set_movement(target_coords, ignore_bonk=True)
        if talk and distance(actor_index) < 15:
            xbox.tap_b()
        if use_raw_coords:
            actor_coords = memory.main.get_coords()
        else:
            actor_coords = memory.main.get_actor_coords(actor_index=actor_index)
        target_coords = [actor_coords[0], actor_coords[1]]
        if memory.main.get_story_progress() < 20 and memory.main.name_aeon_ready():
            FFXC.set_neutral()
            return True

    logger.debug("Actor engaged.")
    FFXC.set_neutral()
    if speed_val != 0:
        memory.main.set_game_speed(speed_val)
    memory.main.wait_frames(6)
    if memory.main.battle_active():
        return False
    logger.debug("_approach_actor returning True")
    return True


def approach_coords(
    target_coords, 
    diag:int = 999, 
    click_through:bool = True, 
    quick_return:bool=False,
    use_raw_coords:bool=False
):
    logger.debug("approach_coords start")
    start_time = time.perf_counter() # Initialize timeout anchor
    timeout_threshold = 8.0
    
    speed_val = memory.main.get_game_speed()
    if speed_val != 0:
        memory.main.set_game_speed(0)

    if diag != 999:
        logger.debug(f"Moving/tapping until dialog value achieved: {diag}")
        while memory.main.diag_progress_flag() != diag:
            # Check Timeout
            if time.perf_counter() - start_time > timeout_threshold:
                logger.error(f"approach_coords TIMEOUT: Failed to reach diag {diag}")
                break # Exit the while loop to clean up game speed/state
                
            if memory.main.user_control():
                set_movement(target_coords)
                if distance_coords(target_coords, use_raw_coords=use_raw_coords) < 20:
                    xbox.tap_b()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
    else:
        logger.debug(f"Moving/tapping until control lost.")
        while memory.main.user_control():
            # Check Timeout
            if time.perf_counter() - start_time > timeout_threshold:
                logger.error("approach_coords TIMEOUT: Movement took too long.")
                break
                
            set_movement(target_coords)
            if distance_coords(target_coords, use_raw_coords=use_raw_coords) < 20:
                xbox.tap_b()

    logger.debug("Cleaning up movement state.")
    FFXC.set_neutral()

    if quick_return:
        logger.debug("Quick return identified. Returning to parent process.")
        return

    if speed_val != 0:
        memory.main.set_game_speed(speed_val)

    if click_through:
        logger.debug("Tapping until control regained.")
        FFXC.set_neutral()
        # Note: You might want a secondary timeout inside click_to_control_3
        memory.main.click_to_control_3()

    logger.debug("approach_coords end")
    
def blitz_replace(cursor_target):
    while memory.main.blitz_recrut_swap_cursor() != cursor_target:
        while memory.main.blitz_recrut_swap_cursor() != cursor_target:
            xbox.tap_down()
        memory.main.wait_frames(1)


def blitz_recruit(actor_id, use_raw_coords:bool=False):
    if not memory.main.user_control():
        memory.main.await_control()
    actor_index = memory.main.actor_index(actor_num=actor_id)
    if use_raw_coords:
        actor_coords = memory.main.get_coords()
    else:
        actor_coords = memory.main.get_actor_coords(actor_index=actor_index)
    target_coords = [actor_coords[0], actor_coords[1]]
    logger.debug(f"Actor's coordinates: {target_coords}")

    logger.debug(f"Control: {memory.main.user_control()} | Naming: {memory.main.name_aeon_ready()}")

    start_time = time.time()
    while memory.main.user_control():
        # Timeout check
        if time.time() - start_time > 4:
            logger.warning("Timeout reached. Executing erratic behavior.")
            # Erratic behavior: move randomly for 0.5 seconds
            directions = [(1,0), (-1,0), (0,1), (0,-1)]
            dx, dy = random.choice(directions)
            erratic_target = [target_coords[0] + dx * 5, target_coords[1] + dy * 5]
            erratic_start = time.time()
            while time.time() - erratic_start < 0.5:
                set_movement(erratic_target)
            FFXC.set_neutral()
            return blitz_recruit(actor_id=actor_id, use_raw_coords=use_raw_coords)

        set_movement(target_coords)
        if distance(actor_index) < 30:
            xbox.tap_x()
        if use_raw_coords:
            actor_coords = memory.main.get_coords()
        else:
            actor_coords = memory.main.get_actor_coords(actor_index=actor_index)
        target_coords = [actor_coords[0], actor_coords[1]]

    logger.debug("Actor engaged.")
    FFXC.set_neutral()
    memory.main.wait_frames(12)
    xbox.tap_confirm()
    memory.main.wait_frames(30)
    xbox.tap_confirm()
    memory.main.wait_frames(30)
    xbox.tap_left()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_confirm()
    memory.main.wait_seconds(2)
    xbox.tap_confirm()
    memory.main.wait_seconds(2)
    if not memory.main.user_control():
        xbox.tap_confirm()
        memory.main.wait_seconds(2)
        if actor_id == 8329:  # Miyu, Moonflow goalie
            blitz_replace(5)
        elif actor_id == 8324:  # Kyou, Djose goalie
            blitz_replace(5)
        elif actor_id == 8277:  # Ropp, Miihen agency
            blitz_replace(3)
        else:
            blitz_replace(4)
        xbox.tap_confirm()

    while not memory.main.user_control():
        xbox.tap_b()
        memory.main.wait_frames(1)
    logger.debug("Recruit actor returning True")
    return True


def primer():
    logger.debug("Primer!!!")
    write_big_text("Approaching Primer")
    approach_actor_by_id(20491)
    if memory.main.battle_active():
        logger.debug("Primer fail!")
        write_big_text("")
        return False
    while not memory.main.user_control():
        xbox.tap_confirm()
    logger.debug("Got the primer!")
    write_big_text("")
    return True


# TODO: Doesn't appear to be used, but left for historical purposes
def seymour_natus():  # First checkpoint ever written. :D
    x = 15
    y = 150
    return [x, y]




# TODO: This appears to be unused. Was for a showcase in 2021.
def t_plains_dodging(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 29
        y = 149
    if checkpoint == 1:
        x = 16
        y = -59
    if checkpoint == 2:
        x = 115
        y = -297
    if checkpoint == 3:
        x = 35
        y = -616
    if checkpoint == 4:
        x = -91
        y = -866
    if checkpoint == 5:
        x = -121
        y = -1089
    if checkpoint == 6:
        x = -120
        y = -1300
    return [x, y]
