import State
import Keys

#Clase Automata para el algoritmo de thompson

#Automata tiene un estado inicial y uno final, estado de aceptación
#start - Estado inicial
#final - Estado final

class Estado :
    ID = 1

    def __init__ (self, final=False, id=None, prefijo="E") :
        if id == None:
            self.id = prefijo + str(Estado.ID)
            Estado.ID += 1
        else :
            self.id = id

        self.final = final

    def merge (self, estado) :
        
        self.id = estado.id
        self.final = estado.final

    def copy(self) :
       
        estado = Estado()
        estado.id = self.id + Keys.COPY_LABEL
        estado.final = self.final

        return estado


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
            
    def get_estado_inicial(self):

        return self.start
    
    def get_estado_final(self):

        return self.final

    
    
