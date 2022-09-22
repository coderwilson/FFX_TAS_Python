# Libraries and Core Files
import logs
import area.sin
import area.zanarkand
import area.gagazet
import area.rescueYuna
import area.home
import area.mTemple
import area.mWoods
import area.thunderPlains
import area.guadosalam
import area.moonflow
import area.djose
import area.MRR
import area.miihen
import blitz
import area.luca
import area.kilika
import area.boats
import area.besaid
import area.baaj
import area.dreamZan
import xbox
import memory.main
import battle.main
import screen
import vars
import reset
import loadGame
import targetPathing
gameVars = vars.varsHandle()
gameVars.setStartVars()

memory.main.start()
# Plug in controller
FFXC = xbox.controllerHandle()

area.dreamZan.NewGame("Klikk testing")
loadGame.loadSaveNum(101)
memory.main.awaitControl()
while memory.main.userControl():
    targetPathing.setMovement([0,0])
    if memory.main.getCoords()[0] > -40:
        xbox.tapB()
area.baaj.Klikk_fight()

reset.midRunReset(landRun=False, startTime=logs.timeStamp())
