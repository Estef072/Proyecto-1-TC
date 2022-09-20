import State

#Clase Automata para el algoritmo de thompson

#Automata tiene un estado inicial y uno final, estado de aceptación
#start - Estado inicial
#final - Estado final
class Automata():
    def __init__(self, start: State, final:State) -> None:
        self.start = start
        self.final = final
        
    def show(self):
        stack = [self.start]
        visited = []
        while len(stack) != 0:
            afn = stack.pop()
           
            transiciones = afn.transitions.items()

            for key, value in transiciones:
                if afn not in visited:
                    stack.append(key)
                    print("con:", value, afn.name, "->", key.name)
            visited.append(afn)
                
            
    
    
    
