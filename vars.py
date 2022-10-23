class allVars:
    def __init__(self):
        self.setStartVars()

    def setStartVars(self):
        # ------------------------------
        # The default values assume starting from the beginning of the game.
        # If you are starting from a loaded save, you may need to change one or more
        # of the values below.
        # ------------------------------

        # ----Most important values to review
        self.artificialPauses = False  # Set depending on hardware. True = less powerful hardware.
        self.csrValue = True  # Set automatically on new game. For testing (loading a save file) set for your environment.
        self.nemesisValue = False  # Set based on if you're doing any% (False) or Nemesis% (True)
        self.forceLoop = False  # After game is finished, start again on next seed.
        self.blitzLoop = False  # Loop on the same seed immediately after Blitzball.
        self.blitzLossForceReset = True  # True = reset after blitz loss
        self.setSeed = True  # If you are using Rossy's patch, set to True. Otherwise set to False
        self.kilikaSkip = True  # True == Tidus OD on Evrae instead of Seymour. New strat.
        self.perfectAeonKills = False  # Before YuYevon, True is slower but more swag.
        self.attemptDjose = True  # Try Djose skip? (not likely to succeed)

        # ----Blitzball
        self.blitzWinValue = True  # No default value required
        self.blitzOvertime = False  # Set to False, no need to change ever.
        self.blitzFirstShotVal = False
        self.oblitzAttackVal = "255"  # Used for RNG manip tracking

        # ----Sphere grid
        self.fullKilikMenu = False  # Default to False
        self.earlyTidusGridVal = False  # Default False
        self.earlyHasteVal = 1  # Default -1
        self.wakkaLateMenuVal = False  # Default False
        self.endGameVersionVal = 1  # Default 0

        # ----Equipment
        self.zombieWeaponVal = 255  # Default 255
        self.lStrikeCount = 1  # Default 0

        # ----RNG Manip
        self.yellows = 0  # ?
        self.confirmedSeedNum = 999  # ?
        self.skipZanLuck = False  # ?

        # ----Other
        self.newGame = False  # ?
        self.selfDestruct = False  # Default False
        self.YTKFarm = 0  # Default to 0
        self.rescueCount = 0  # Default to 0
        self.fluxOverkillVar = False  # Default to False
        self.tryNEVal = True  # Based on
        self.firstHits = [0] * 8
        self.neArmorVal = 255  # Default 255
        self.neBattles = 0  # Default to 0
        self.neaZone = (
            0  # Decides which zone we charge Rikku in after reaching Zanarkand.
        )

        # ----Nemesis variables, unused in any%
        self.nemAPVal = 1  # Default to 1
        self.areaResults = [0] * 13
        self.speciesResults = [0] * 14
        self.originalResults = [0] * 7
        self.yojimboIndex = 1

        # ----Path for save files, used for loading a specific save
        # coderwilson automation PC
        # self.savePath = "C:/Users/Thomas Wilson/Documents/SQUARE ENIX/FINAL FANTASY X&X-2 HD Remaster/FINAL FANTASY X/"
        # coderwilson main PC
        self.savePath = "C:/Users/Thomas/Documents/SQUARE ENIX/FINAL FANTASY X&X-2 HD Remaster/FINAL FANTASY X/"
    
    def tryDjoseSkip(self):
        return self.attemptDjose
    
    def blitzLossReset(self):
        return self.blitzLossForceReset

    def useSetSeed(self):
        return self.setSeed

    def printArenaStatus(self):
        print("##############################################")
        print("Area:", self.areaResults)
        print("Species:", self.speciesResults)
        print("Original:", self.originalResults)
        print("##############################################")

    def arenaSuccess(self, arrayNum, index):
        print(arrayNum, "|", index)
        if arrayNum == 0:
            self.areaResults[index] = 1
        if arrayNum == 1:
            self.speciesResults[index] = 1
        if arrayNum == 2:
            self.originalResults[index] = 1
        self.printArenaStatus()

    def yuYevonSwag(self):
        return self.perfectAeonKills

    def skipKilikaLuck(self):
        return self.kilikaSkip

    def dontSkipKilikaLuck(self):
        self.kilikaSkip = False

    def loopBlitz(self):
        return self.blitzLoop

    def loopSeeds(self):
        return self.forceLoop

    def confirmedSeed(self):
        return self.confirmedSeedNum

    def setConfirmedSeed(self, value):
        self.confirmedSeedNum = value

    def setNewGame(self):
        self.newGame = True

    def newGameCheck(self):
        return self.newGame

    def setOblitzRNG(self, value):
        self.oblitzAttackVal = str(value)

    def oblitzRNGCheck(self):
        return self.oblitzAttackVal

    def getYellows(self):
        return self.yellows

    def setYellows(self, newVals):
        self.yellows = newVals

    def yojimboGetIndex(self):
        return self.yojimboIndex

    def yojimboIncrementIndex(self):
        self.yojimboIndex += 1

    def nemesis(self):
        return self.nemesisValue

    def getNEAzone(self):
        return self.neaZone

    def setNEAzone(self, value):
        self.neaZone = value

    def nemCheckpointAP(self):
        return self.nemAPVal

    def setNemCheckpointAP(self, value):
        self.nemAPVal = value

    def neExtraBattles(self):
        return self.neBattles

    def neBattlesIncrement(self):
        self.neBattles += 1

    def neArmor(self):
        return self.neArmorVal

    def setneArmor(self, value):
        self.neArmorVal = value

    def tryForNE(self):
        return self.tryNEVal

    def firstHitsSet(self, values):
        for x in range(8):
            self.firstHits[x] = values[x]

    def firstHitsValue(self, index):
        return self.firstHits[index]

    def printFirstHits(self):
        print(self.firstHits)

    def gameSavePath(self):
        return self.savePath

    def blitzFirstShot(self):
        return self.blitzFirstShotVal

    def blitzFirstShotTaken(self):
        self.blitzFirstShotVal = True

    def blitzFirstShotReset(self):
        self.blitzFirstShotVal = False

    def fluxOverkill(self):
        return self.fluxOverkillVar

    def fluxOverkillSuccess(self):
        self.fluxOverkillVar = True

    def csr(self):
        return self.csrValue

    def setCSR(self, value):
        print("Setting CSR:", value)
        self.csrValue = value

    def completeFullKilikMenu(self):
        self.fullKilikMenu = True

    def didFullKilikMenu(self):
        return self.fullKilikMenu

    def usePause(self):
        return self.artificialPauses

    def setBlitzWin(self, value):
        self.blitzWinValue = value

    def getBlitzWin(self):
        return self.blitzWinValue

    def setBlitzOT(self, value):
        self.blitzOvertime = value

    def getBlitzOT(self):
        return self.blitzOvertime

    def setLStrike(self, value):
        self.lStrikeCount = value

    def getLStrike(self):
        return self.lStrikeCount

    def zombieWeapon(self):
        return self.zombieWeaponVal

    def setZombie(self, value):
        self.zombieWeaponVal = value

    def earlyTidusGridSetTrue(self):
        self.earlyTidusGridVal = True

    def earlyTidusGrid(self):
        return self.earlyTidusGridVal

    def earlyHasteSet(self, value):
        self.earlyHasteVal = value

    def earlyHaste(self):
        return self.earlyHasteVal

    def wakkaLateMenuSet(self, value):
        self.wakkaLateMenuVal = value

    def wakkaLateMenu(self):
        return self.wakkaLateMenuVal

    def endGameVersionSet(self, value):
        self.endGameVersionVal = value

    def endGameVersion(self):
        return self.endGameVersionVal

    def selfDestructLearned(self):
        self.selfDestruct = True

    def selfDestructGet(self):
        return self.selfDestruct

    def addRescueCount(self):
        self.rescueCount += 1

    def completedRescueFights(self):
        print(f"Completed {self.rescueCount} exp kills")
        return self.rescueCount >= 4

    def addYTKFarm(self):
        self.YTKFarm += 1

    def YTKFarmCount(self):
        return self.YTKFarm

    def completedYTKFarm(self):
        return self.YTKFarm >= 2

    def setSkipZanLuck(self, value):
        self.skipZanLuck = value

    def getSkipZanLuck(self):
        return self.skipZanLuck


def initVars():
    mainVars = allVars()


def varsHandle():
    return mainVars


mainVars = allVars()
