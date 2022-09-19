


class State(object):
    def __init__(self, name = None, transitions = None) -> None:
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
        for key,value in self.transitions.items():
            print(value, self.name, "-->", key.name)
        
hola = State(name = "q0")
hola2 = State(name = "q1")
hola3 = State(name = "q2")

hola.AddTransition(hola2, 2)
hola.AddTransition(hola2, 3)
hola.AddTransition(hola3, 3)
