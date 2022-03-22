import pyxinput
import time
import FFX_Xbox
import FFX_memory

from math import copysign
import numpy as np

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def setMovement(target) -> bool:
    #print("Blitz movement target: ", target)
    player = FFX_memory.getCoords()
    #(forward, right) = FFX_memory.getMovementVectors()
    (forward, right) = ((1, 0), (0, -1))

    targetPos = np.array([target[0], target[1]])
    playerPos = np.array(player)

    # Calculate forward and right directions relative to camera space
    pX = player[0]
    pY = player[1]
    eX = target[0]
    eY = target[1]
    fX = forward[0]
    fY = forward[1]
    rX = right[0]
    rY = right[1]

    Ly = fX * (eX-pX) + rX * (eY-pY)
    Lx = fY * (eX-pX) + rY * (eY-pY)
    sumsUp = abs(Lx)+abs(Ly)
    if sumsUp == 0:
        sumsUp = 0.01
    Lx /= sumsUp
    Ly /= sumsUp
    if abs(Lx) > abs(Ly):
        Ly = copysign(Ly/Lx if Lx else 0, Ly)
        Lx = copysign(1, Lx)
    elif abs(Ly) > abs(Lx):
        Lx = copysign(Lx/Ly if Ly else 0, Lx)
        Ly = copysign(1, Ly)
    
    FFXC.set_movement(Lx, Ly)
    #FFX_memory.waitFrames(frames=1)
    
    if abs(player[1] - target[1]) < 3 and abs(player[0] - target[0]) < 3:
        return True #Checkpoint reached
    else:
        return False
