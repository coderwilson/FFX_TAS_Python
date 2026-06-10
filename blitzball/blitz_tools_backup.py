import memory.main
import vars
game_vars = vars.vars_handle()
import logging
logger = logging.getLogger(__name__)
from json_ai_files.write_seed import write_big_text
from blitzball import blitz_class
blitz_state = blitz_class.blitz_state_handle()

from enum import Enum, auto
from typing import Optional

class BlitzState(Enum):
    UNKNOWN          = auto()
    CLOCK_ACTIVE     = auto()
    SELECT_FORMATION = auto()
    SELECT_MOVEMENT  = auto()
    SELECT_ACTION    = auto()
    SELECT_SHOT_TYPE = auto()
    SELECT_PASS_TYPE = auto()
    SELECT_TACKLE_TYPE = auto()
    SELECT_TARGET    = auto()
    SELECT_BREAKTHROUGH = auto()
    DIALOG_ON_SCREEN  = auto()

# State -> (menu numbers that trigger it, valid next states)
TRANSITIONS: dict[BlitzState, tuple[set, set]] = {
    BlitzState.CLOCK_ACTIVE:({},         {BlitzState.SELECT_MOVEMENT,BlitzState.SELECT_BREAKTHROUGH,BlitzState.SELECT_ACTION,BlitzState.SELECT_TACKLE_TYPE}),
    BlitzState.SELECT_MOVEMENT:     ({145,146},   {BlitzState.SELECT_FORMATION}),
    BlitzState.SELECT_FORMATION:    ({46,122,133},{}),
    BlitzState.SELECT_ACTION:       ({47,52,102}, {BlitzState.SELECT_SHOT_TYPE, BlitzState.SELECT_PASS_TYPE}),
    BlitzState.SELECT_SHOT_TYPE:    ({113},       {}),
    BlitzState.SELECT_PASS_TYPE:    ({117},       {BlitzState.SELECT_TARGET}),
    BlitzState.SELECT_TACKLE_TYPE:  ({167},       {}),
    BlitzState.SELECT_TARGET:       ({24,226},    {}),
    BlitzState.SELECT_BREAKTHROUGH: ({BlitzState.SELECT_ACTION},          {}),
    BlitzState.DIALOG_ON_SCREEN:     ({},          {}),
}

class BlitzStateTracker:

    def __init__(self):
        self.state: BlitzState = BlitzState.UNKNOWN
        self.previous_state: BlitzState = BlitzState.UNKNOWN
        self._last_clock: int = -1  # -1 so first read always registers

    def update(self) -> BlitzState:
        menu = memory.main.blitz_menu_num()
        input_ready = bool(memory.main.blitz_input_ready())
        clock = memory.main.blitz_clock()
        clock_active = clock != self._last_clock
        self._last_clock = clock

        new_state = self._resolve(menu, clock_active, input_ready)

        if new_state != self.state:
            logger.warning(f"Blitz state: {self.state.name} -> {new_state.name} (menu={menu})")
            self.previous_state = self.state
            self.state = new_state

        return self.state

    def _resolve(self, menu: int, clock_active: bool, input_ready: bool) -> BlitzState:
        if not input_ready:
            if memory.main.diag_skip_possible():
                return BlitzState.DIALOG_ON_SCREEN
            return BlitzState.CLOCK_ACTIVE if clock_active else self.state

        # Check dialog states first (flag-based, not menu-based)
        # flag = memory.main.diag_progress_flag()
        # if flag in (45, 46):
        #     return BlitzState.DIALOG_ON_SCREEN
        # if flag in (47, 48, 49):
        #     return BlitzState.DIALOG_ON_SCREEN

        # Find candidates by menu number
        candidates = [s for s, (menus, _) in TRANSITIONS.items() if menu in menus]

        if not candidates:
            return BlitzState.SELECT_BREAKTHROUGH
        if len(candidates) == 1:
            return candidates[0]

        # Ambiguous - constrain by valid next states from current state
        _, valid_next = TRANSITIONS.get(self.state, (set(), set(BlitzState)))
        constrained = [c for c in candidates if c in valid_next]

        if len(constrained) == 1:
            return constrained[0]

        logger.warning(f"Still ambiguous after transition filter: menu={menu}, candidates={candidates}")
        return constrained[0] if constrained else candidates[0]

def goers_score_first():
    if bool(memory.main.blitz_clock_active()):
        return False
    if memory.main.get_story_progress() > 700:
        return False
    if blitz_state.debug_mode == "flags":
        write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    return memory.main.diag_progress_flag() in [47, 48, 49]


def halftime_dialog():
    if memory.main.get_story_progress() > 700:
        return False
    if blitz_state.debug_mode == "flags":
        write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    return memory.main.diag_progress_flag() in [45, 46]


def select_movement_style() -> bool:
    if not memory.main.blitz_input_ready():
        return False
    if memory.main.get_story_progress() > 700:
        return False
    status = bool(memory.main.blitz_menu_num() in [145,146])  # 39 is sus
    if status:
        logger.warning(f"Selecting movement style: {memory.main.blitz_menu_num()}")
    # memory.main.wait_frames(90)
    return status


def select_formation() -> bool:
    if not memory.main.blitz_input_ready():
        return False
    if memory.main.get_story_progress() > 700:
        return False
    status = bool(memory.main.blitz_menu_num() in [46,122,133])
    if memory.main.blitz_menu_num() == 46 and memory.main.get_story_progress() < 700:
        status = True
    if status:
        logger.warning(f"Selecting formation: {memory.main.blitz_menu_num()}")
    # memory.main.wait_frames(90)
    return status


def select_breakthrough() -> bool:
    if not memory.main.blitz_input_ready():
        return False
    if (
        select_movement_style() or 
        select_formation() or 
        select_action() or
        select_pass_target() or
        select_type_check()
    ):
        return False
    logger.warning(f"Selecting breakthrough: {memory.main.blitz_menu_num()}")
    # memory.main.wait_frames(90)
    return True
    
    status = bool(memory.main.blitz_menu_num() in [12])
    if status:
        logger.warning("Selecting break through")
    return status


def select_action() -> bool:
    if not memory.main.blitz_input_ready():
        return False
    if memory.main.get_story_progress() < 700:
        status = bool(memory.main.blitz_menu_num() in [47,52,102])
        if status:
            logger.warning(f"Selecting action: {memory.main.blitz_menu_num()}")
        # memory.main.wait_frames(90)
    else:
        status = bool(memory.main.blitz_menu_num() in range(47, 53))
    return status


def max_menu_size():
    return memory.main.blitz_menu_size()


def select_pass_target() -> bool:
    if not memory.main.blitz_input_ready():
        return False
    if memory.main.get_story_progress() < 700:
        status = bool(memory.main.blitz_menu_num() in [24,226])
    else:
        status = bool(memory.main.blitz_menu_num() == 226)
    if status:
        logger.warning(f"Selecting pass target: {memory.main.blitz_menu_num()}")
    # memory.main.wait_frames(90)
    return status


def select_type_check() -> bool:
    if not memory.main.blitz_input_ready():
        return False
    return bool(memory.main.blitz_menu_num() in [113,117,167])


def select_shot_type() -> bool:
    if not select_type_check():
        return False
    # We need something here to separate the shot type from others.
    # However, for the TAS, this is the ONLY type used.
    logger.warning(f"Selecting shot type: {memory.main.blitz_menu_num()}")
    # memory.main.wait_frames(90)
    return True


def select_pass_type() -> bool:
    if not select_type_check():
        return False
    # We need something here to separate the shot type from others.
    # However, for the TAS, this is an unused field.
    return True


def select_tackle_type() -> bool:
    if not select_type_check():
        return False
    # We need something here to separate the shot type from others.
    # However, for the TAS, this is an unused field.


def targeted_player():
    return memory.main.blitz_target_player() - 2


def active_clock_broken():
    return memory.main.blitz_clock_active()


def active_clock():
    current_state = state_tracker.update()
    if controlling_player() > 5:
        return False
    
    return current_state == BlitzState.CLOCK_ACTIVE

def input_ready():
    return memory.main.blitz_input_ready()

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


def cursor_1():
    logger.debug(f"Cursor: {memory.main.blitz_cursor()}")
    return memory.main.blitz_cursor()

def storyline():
    write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    current = memory.main.get_story_progress()
    if not game_vars.csr():
        if current == 540:
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
        # 575 - Wakka is in the game


