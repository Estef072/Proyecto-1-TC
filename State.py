


class State(object):
    def __init__(self, name:str = None, transitions:dict = None) -> None:
        self.transitions = transitions if transitions else {}
        self.name = name
        pass
        
    def AddTransition(self,state, edge):
        if state in self.transitions:
            self.transitions[state] = [self.transitions[state]]
            self.transitions[state].append(edge)
        else:
            self.transitions[state] = edge
            
    def GetTransitions(self):
        return self.transitions
        
