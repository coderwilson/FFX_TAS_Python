
class allVars:
    def __init__(self):
        self.csrValue = True
        self.blitzWinValue = False
    
    def csr(self):
        return self.csrValue
    
    def SETcsr(self, value):
        self.csrValue = value

def initVars():
    mainVars = allVars()

def varsHandle():
    return mainVars
    
    
    
    
    
    
    
    
mainVars = allVars()
