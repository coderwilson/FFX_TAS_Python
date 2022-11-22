import logging
import threading

import memory
import vars
import xbox

logger = logging.getLogger(__name__)


game_vars = vars.vars_handle()


def speedup_decorator(func):
    def _monitor_battle():
        while not memory.main.battle_active():
            pass
        fast = False
        old_game_speed = memory.main.get_game_speed()
        while memory.main.battle_active():
            if fast and memory.main.auditory_dialog_playing():
                memory.main.set_game_speed(0)
                fast = False
            elif not fast:
                memory.main.set_game_speed(2)
                fast = True
        memory.main.set_game_speed(old_game_speed)

    def wrapper(*args, **kwargs):
        if game_vars.get_battle_speedup():
            logger.debug(f"Speeding battle up: {func.__name__}")
            monitor = threading.Thread(target=_monitor_battle, daemon=True)
            monitor.start()
            ret_val = func(*args, **kwargs)
            monitor.join()
            logger.debug(f"Stopping speedup for {func.__name__}")
            return ret_val
        else:
            return func(*args, **kwargs)

    return wrapper


def _navigate_to_position(position, battle_cursor=memory.main.battle_cursor_2):
    while battle_cursor() == 255:
        pass
    if battle_cursor() != position:
        logger.debug(f"Wrong position targeted {battle_cursor() % 2}, {position % 2}")
        while battle_cursor() % 2 != position % 2:
            if battle_cursor() < position:
                xbox.tap_right()
            else:
                xbox.tap_left()
        while battle_cursor() != position:
            logger.debug(f"Battle_cursor: {battle_cursor()}")
            if battle_cursor() > position:
                xbox.tap_up()
            else:
                xbox.tap_down()


def _navigate_to_single_column_index(position, cursor):
    while cursor() != position:
        if cursor() < position:
            xbox.tap_down()
        else:
            xbox.tap_up()


def tap_targeting():
    logger.debug(
        f"In Tap Targeting. Not battle menu: {not memory.main.main_battle_menu()}, Battle active: {memory.main.battle_active()}"
    )
    while (not memory.main.main_battle_menu()) and memory.main.battle_active():
        xbox.tap_b()
    logger.debug(
        f"Done. Not battle menu: {not memory.main.main_battle_menu()}, Battle active: {memory.main.battle_active()}"
    )
