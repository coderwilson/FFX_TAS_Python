import FFX_Xbox
import time

FFXC = FFX_Xbox.FFXC

print("Clearing all values")

FFXC.set_value('AxisLx', 0)
FFXC.set_value('AxisLy', 0)
FFXC.set_value('BtnA', 0)
FFXC.set_value('BtnB', 0)
FFXC.set_value('BtnStart', 0)
FFXC.set_value('BtnX', 0)
FFXC.set_value('BtnY', 0)

    
print("Unplugging controller")
FFXC.UnPlug(FFXC)
print("Controller is now unplugged")

time.sleep(2)