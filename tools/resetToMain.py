import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import memory.main
import reset

memory.main.start()
memory.main.clearEncounterID()
reset.resetToMainMenu()
