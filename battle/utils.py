import logging
import threading

import memory
import vars

logger = logging.getLogger(__name__)


game_vars = vars.vars_handle()


def speedup_decorator(func):
    def _monitor_battle():
        while not memory.main.battle_active():
            pass
        fast = False
        while memory.main.battle_active():
            if (
                fast
                and memory.main.auditory_dialog_playing()
                or memory.main.diag_skip_possible()
            ):
                memory.main.set_game_speed(0)
                fast = False
            elif not fast:
                memory.main.set_game_speed(2)
                fast = True
        memory.main.set_game_speed(0)

    def wrapper(*args, **kwargs):
        if game_vars.get_battle_speedup():
            logger.debug(f"Speeding battle up: {func.__name__}")
            monitor = threading.Thread(target=_monitor_battle)
            monitor.start()
            ret_val = func(*args, **kwargs)
            monitor.join()
            logger.debug(f"Stopping speedup for {func.__name__}")
            return ret_val
        else:
            return func(*args, **kwargs)

    return wrapper
