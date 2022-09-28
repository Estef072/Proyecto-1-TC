from anld import *

class S : 
    """
    Operaciones sobre una pila
    """
    def __init__(self) : 
        self.items = [] 

    def push(self, item) : 
        self.items.append(item) 

    def pop(self) : 
        return self.items.pop() 
        

    def isEmpty(self) : 
        if (self.items == []):
            return True
        else :
            return False
    
    def getFin(self):
        return self.items[-1]

