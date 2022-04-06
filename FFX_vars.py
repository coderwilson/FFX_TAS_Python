class allVars:
    def __init__(self):
        self.setStartVars()
    
    def setStartVars(self):
        #------------------------------------------------------------------
        #The default values assume starting from the beginning of the game.
        #If you are starting from a loaded save, you may need to change one or more
        #of the values below.
        #------------------------------------------------------------------
        
        #----Most important values to review
        self.artificialPauses = True #Set depending on hardware. True = less powerful hardware.
        self.csrValue = False #Set based on if cutscene remover is working.
        self.nemesisValue = True #Set based on if you're doing any% (False) or Nemesis% (True)
        
        
        #----Blitzball
        self.blitzWinValue = True #No default value required
        self.blitzOvertime = False #Set to False, no need to change ever.
        self.blitzFirstShotVal = False
        
        #----Sphere grid
        self.fullKilikMenu = False #Default to False
        self.earlyTidusGridVal = False #Default False
        self.earlyHasteVal = -1 #Default -1
        self.wakkaLateMenuVal = False #Default False
        self.endGameVersionVal = 0 #Default 0
        
        #----Equipment
        self.zombieWeaponVal = 255 #Default 255
        self.lStrikeCount = 0 #Default 0
        
        #----Other
        self.selfDestruct = False #Default False
        self.YTKFarm = 0 #Default to 0
        self.rescueCount = 0 #Default to 0
        self.fluxOverkillVar = False #Default to False
        self.tryNEVal = True #Based on 
        self.firstHits = [0] * 8
        self.neArmorVal = 255 #Default 255
        self.neBattles = 0 #Default to 0
        
        #----Path for save files, used for loading a specific save
        #coderwilson automation PC
        self.savePath = "C:/Users/Thomas Wilson/Documents/SQUARE ENIX/FINAL FANTASY X&X-2 HD Remaster/FINAL FANTASY X/"
        #coderwilson main PC
        #self.savePath = "C:/Users/Thomas/Documents/SQUARE ENIX/FINAL FANTASY X&X-2 HD Remaster/FINAL FANTASY X/"
    
    
    def nemesis(self):
        return self.nemesisValue
    
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
    
    def firstHitsSet(self,values):
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
    
    def SETcsr(self, value):
        print("Setting CSR: ", value)
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
        
    def completedYTKFarm(self):
        return self.YTKFarm >= 2
        
def initVars():
    mainVars = allVars()

def varsHandle():
    return mainVars
    
    
    
    
    
    
    
    
mainVars = allVars()
