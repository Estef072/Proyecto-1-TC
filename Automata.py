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
                        
                    #Transiiciones
                    #Trans = transiciones
                    #trans[afn.name] = {nombre del estado actual: {simobolo: estado al que va}}
                    
                    else:
                        trans[afn.name] = {value: key.name}
                anterior = key.name
                    
            visited.append(afn)
                
        return trans
    
    def subconjuntos(self):
        
        stack = []
        visited = []
        trans = {}
        #
        
        #if simbolo =="epsilon":
            #stack.append(key) (Se añade el estado al que lleva con la transicion epsilon)
            #subconjuntos = [[transiciones epsilon del primer recorrido], [transiciones segundo recorrido]....]
            #subconjuntos[0] = transiciones primer recorrido
            #for subconjuntos[0] (recorrer todos los estados que se encuentran en esa lista)
            #otro for para recorrer los estados de cada uno de los estados en subconjuntos[0]
        while len(stack) != 0:
            #afn -> estado actual en el que se está
            afn = stack.pop()
            
            #Transiciones del estado actual
            transiciones = afn.transitions.items()

            for key, value in transiciones:
                if afn not in visited:
                    stack.append(key)
                    if afn.name in trans.keys():
                        trans[afn.name] = {value: [key.name, anterior]}
                        
                    #Transiiciones
                    #Trans = transiciones
                    #trans[afn.name] = {nombre del estado actual: {simobolo: estado al que va}}
                    
                    else:
                        trans[afn.name] = {value: key.name}
                anterior = key.name
                    
            visited.append(afn)
                
        return trans
        pass
            
    
    
    
