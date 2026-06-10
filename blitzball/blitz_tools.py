import memory.main
import vars
import logging
import xbox
from enum import Enum, auto
from json_ai_files.write_seed import write_big_text

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

# --- ENUMS AND TRACKER CLASS ---

class BlitzState(Enum):
    UNKNOWN             = auto()
    CLOCK_ACTIVE        = auto()
    SELECT_FORMATION    = auto()
    SELECT_MOVEMENT     = auto()
    SELECT_ACTION       = auto()
    SELECT_TYPE         = auto()
    SELECT_TACKLE_TYPE  = auto()
    SELECT_TARGET       = auto()
    SELECT_BREAKTHROUGH = auto()
    DIALOG_ON_SCREEN    = auto()

# State -> (menu numbers that trigger it, valid next states)
TRANSITIONS = {
    BlitzState.CLOCK_ACTIVE:    ({},             {BlitzState.SELECT_MOVEMENT, BlitzState.SELECT_BREAKTHROUGH, BlitzState.SELECT_ACTION, BlitzState.SELECT_TACKLE_TYPE}),
    BlitzState.SELECT_MOVEMENT: ({145, 146},     {BlitzState.SELECT_FORMATION}),
    BlitzState.SELECT_FORMATION:({46, 122, 133}, {}),
    BlitzState.SELECT_BREAKTHROUGH: ({},     {BlitzState.SELECT_ACTION}),
    BlitzState.SELECT_ACTION:   ({47, 52, 102},  {BlitzState.SELECT_TYPE, BlitzState.SELECT_TARGET}),
    BlitzState.SELECT_TYPE:({117,113},          {BlitzState.SELECT_TARGET}),
    BlitzState.SELECT_TACKLE_TYPE: ({},          {}),
    BlitzState.SELECT_TARGET:   ({24, 226},      {})
}

class BlitzStateTracker:
    def __init__(self):
        self.state = BlitzState.UNKNOWN
        self._last_clock = 0
        self._last_helper = None
        self._last_menu = None

    def set_last_helper(self, value):
        self._last_helper = value

    def update(self) -> BlitzState:
        menu = memory.main.blitz_menu_num()

        current_state = self._resolve()
        # logger.debug(f"State: {current_state}")
        if memory.main.get_story_progress() >= 700 and current_state == BlitzState.DIALOG_ON_SCREEN:
            current_state = self.state
        if current_state != self.state:
            self._last_menu = menu
            logger.warning(f"Blitz state shift: {self.state.name} -> {current_state.name} (menu={menu})")
            self.state = current_state
        return current_state

    def _resolve(self) -> BlitzState:
        if memory.main.get_map() != 62:
            return BlitzState.UNKNOWN

        menu = memory.main.blitz_menu_num()
        input_ready = bool(memory.main.blitz_input_ready())
        clock = memory.main.blitz_clock()
        
        if clock != self._last_clock:
            self._last_clock = clock
            self._last_menu = 999
            return BlitzState.CLOCK_ACTIVE

        if memory.main.get_story_progress() < 700 and game_clock() == 300:
            logger.debug(f"DIALOG_ON_SCREEN - {game_clock()} - {memory.main.get_camera()[3]}")
            return BlitzState.DIALOG_ON_SCREEN
        elif memory.main.get_camera()[3] < -800:
            logger.debug(f"DIALOG_ON_SCREEN - {game_clock()} - {memory.main.get_camera()[3]}")
            return BlitzState.DIALOG_ON_SCREEN
            
        if not input_ready:
            return self.state
        
        if memory.main.blitz_menu_num() == self._last_menu:
            logger.debug(f"No menu change!")
            return self.state

        logger.debug(f"New menu: {memory.main.blitz_menu_num()}")
        if not aurochs_control():
            return BlitzState.SELECT_TACKLE_TYPE

        _, allowed_moves = TRANSITIONS.get(self.state, (set(), set()))
        
        for potential_state in allowed_moves:
            valid_menus, _ = TRANSITIONS.get(potential_state, (set(), set()))
            if menu in valid_menus:
                return potential_state

        current_menus, _ = TRANSITIONS.get(self.state, (set(), set()))
        if menu in current_menus:
            return self.state

        if allowed_moves:
            if len(allowed_moves) == 1:
                return list(allowed_moves)[0]
            else:
                return self._resolve_by_menu_size(allowed_moves)

        # Default to breakthrough if nothing else works.
        if self.state == BlitzState.CLOCK_ACTIVE:
            return BlitzState.SELECT_BREAKTHROUGH
        return self.state

    def _resolve_by_menu_size(self, allowed_moves: set) -> BlitzState:
        logger.debug(f"Checking by menu size: {self.state}, {self._last_helper}")
        logger.debug(max_menu_size())
        if self.state == BlitzState.SELECT_ACTION:
            if self._last_helper == "Pass":
                if int(max_menu_size()) == 4:
                    logger.debug("Selecting target")
                    return BlitzState.SELECT_TARGET
                else:
                    logger.debug("Selecting pass type")
                    return BlitzState.SELECT_TYPE
            elif self._last_helper == "Shoot":
                logger.debug("Selecting shot type")
                return BlitzState.SELECT_TYPE
        if self.state == BlitzState.CLOCK_ACTIVE:
            return BlitzState.SELECT_BREAKTHROUGH
        logger.warning(f"Unidentified situation: {self.state}, {self._last_helper}")
        return self.state

# GLOBAL INSTANCE
tracker = BlitzStateTracker()

# --- HELPER FUNCTIONS (The Bridge) ---

def update_tracker():
    tracker.update()

def tracker_helper(value:str):
    tracker.set_last_helper(value)

def select_type_check() -> bool:
    if not memory.main.blitz_input_ready():
        return False
    return bool(memory.main.blitz_menu_num() in [113,117,167])

def active_clock() -> bool:
    """True if the game is unpaused and clock is ticking."""
    # We check memory directly for the player index to avoid circular dependencies
    if (memory.main.blitz_current_player() - 2) > 5:
        return False
    return tracker.update() == BlitzState.CLOCK_ACTIVE

def select_action() -> bool:
    """True if we are on the main 'Pass/Shoot/Dribble' menu."""
    return tracker.update() == BlitzState.SELECT_ACTION

def select_breakthrough() -> bool:
    """True if we are currently stuck behind a 'Break Through' choice."""
    return tracker.update() == BlitzState.SELECT_BREAKTHROUGH

def select_pass_target() -> bool:
    return tracker.update() == BlitzState.SELECT_TARGET

def select_type() -> bool:
    return tracker.update() == BlitzState.SELECT_TYPE

def select_formation() -> bool:
    return tracker.update() == BlitzState.SELECT_FORMATION

def select_movement_style() -> bool:
    return tracker.update() == BlitzState.SELECT_MOVEMENT

def select_tackle() -> bool:
    return tracker.update() == BlitzState.SELECT_TACKLE_TYPE

# --- REMAINING UTILITIES ---

def game_clock():
    return memory.main.blitz_clock()

def cursor_1():
    return memory.main.blitz_cursor()

def max_menu_size():
    return memory.main.blitz_menu_size()

def targeted_player():
    return memory.main.blitz_target_player() - 2

# def goers_score_first():
#     return tracker.update() == BlitzState.DIALOG_ON_SCREEN

def dialog():
    return tracker.update() == BlitzState.DIALOG_ON_SCREEN

# def halftime_dialog():
#     return tracker.update() == BlitzState.DIALOG_ON_SCREEN

def new_half():
    return memory.main.get_map() == 347

def half_summary_screen():
    return memory.main.get_map() == 212

def aurochs_control():
    return targeted_player() < 6

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

def input_ready():
    return memory.main.blitz_input_ready()

def reset_input_helpers():
    tracker_helper(None)
    tracker._last_menu = 999