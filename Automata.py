import State

#Clase Automata para el algoritmo de thompson

#Automata tiene un estado inicial y uno final, estado de aceptación
#start - Estado inicial
#final - Estado final
class Automata():
    def __init__(self, start: State, final:State) -> None:
        self.start = start
        self.final = final
        
    #prints transitions
    def show(self):
        stack = [self.start]
        visited = []
        while len(stack) != 0:
            afn = stack.pop()
            transiciones = afn.transitions.items()

            for key, value in transiciones:
                if afn not in visited:
                    stack.append(key)
                    print(afn.name, "-->",value,"-->", key.name)
            visited.append(afn)
    
    #pone todas las transiciones en un diccionario
    def Transiciones(self):
        stack = [self.start]
        visited = []
        trans = {}
        while len(stack) != 0:
            afn = stack.pop()
            transiciones = afn.transitions.items()

            for key, value in transiciones:
                if afn not in visited:
                    stack.append(key)
                    if afn.name in trans.keys():
                        trans[afn.name] = {value: [key.name, anterior]}
                        
                    else:
                        trans[afn.name] = {value: key.name}
                anterior = key.name
                    
            visited.append(afn)
                
        return trans
            
    
    
    
