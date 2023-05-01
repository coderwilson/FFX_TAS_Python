import logging
import threading

import memory.main
import vars

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
