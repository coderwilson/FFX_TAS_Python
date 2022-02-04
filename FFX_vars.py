
class allVars:
    def __init__(self):
        self.csrValue = True
        self.blitzWinValue = True
        self.artificialPauses = False
        
        self.earlyTidusGridVal = False
        self.earlyHasteVal = -1
        self.wakkaLateMenuVal = False
        self.endGameVersionVal = 0
        
        self.zombieWeaponVal = 255
        self.lStrikeCount = 0
    
    def csr(self):
        return self.csrValue
    
    def SETcsr(self, value):
        self.csrValue = value
    
    def usePause(self):
        return self.artificialPauses
    
    def setBlitzWin(self, value):
        self.blitzWinValue = value
    
    def getBlitzWin(self):
        return self.blitzWinValue
    
    def setLStrike(self, value):
        self.lStrikeCount = value
    
    def getLStrike(self):
        return self.lStrikeCount
    
    def zombieWeapon(self):
        return self.zombieWeaponVal
    
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

def initVars():
    mainVars = allVars()

def varsHandle():
    return mainVars
    
    
    
    
    
    
    
    
mainVars = allVars()
