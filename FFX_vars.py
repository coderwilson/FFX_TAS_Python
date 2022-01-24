
class allVars:
    def __init__(self):
        self.csrValue = True
        self.blitzWinValue = False
        self.artificialPauses = True
    
    def csr(self):
        return self.csrValue
    
    def SETcsr(self, value):
        self.csrValue = value
    
    def usePause(self):
        return self.artificialPauses

def initVars():
    mainVars = allVars()

def varsHandle():
    return mainVars
    
    
    
    
    
    
    
    
mainVars = allVars()
