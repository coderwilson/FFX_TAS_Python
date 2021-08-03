import pyxinput
import time
import FFX_Xbox
import FFX_core

FFXC = FFX_Xbox.FFXC


FFX_core.openFFXwindow()
time.sleep(0.1)

FFX_Xbox.menuUp()
FFX_Xbox.menuDown()
FFX_Xbox.menuLeft()
FFX_Xbox.menuRight()
FFX_Xbox.menuB()
FFX_Xbox.menuY()
FFX_Xbox.menuBack()


FFXC.set_value('BtnA', 1)
time.sleep(0.04)
FFXC.set_value('BtnA', 0)
time.sleep(0.04)

FFXC.set_value('BtnX', 1)
time.sleep(0.04)
FFXC.set_value('BtnX', 0)
time.sleep(0.04)

FFXC.set_value('BtnStart', 1)
time.sleep(0.04)
FFXC.set_value('BtnStart', 0)
time.sleep(0.04)