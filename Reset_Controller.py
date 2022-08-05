import FFX_Xbox
import time

FFXC = FFX_Xbox.controllerHandle()

print("Clearing all values")

FFXC.set_neutral()
print("Values are now clear.")

#print("Unplugging controller")
# FFXC.UnPlug(FFXC)
#print("Controller is now unplugged")

time.sleep(2)
