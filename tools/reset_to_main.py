import inspect
import os
import sys

import memory.main
import reset

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

memory.main.start()
memory.main.clear_encounter_id()
reset.reset_to_main_menu()
