from ast import Pass
from State import State
from Automata import Automata


def Thompson(expression:str):
    stack = []
    # "#" representa epsilon
    for i in expression:
        
        #UNION
        #Forma:
        #con epsilon: S0 (inicio) -> s1 done
        #con epsilon: S0 (inicio) -> s2
        #con char1: S1 -> S3
        #con char2: S2 -> S4
        #con espsilon: S3 -> S5 (final)
        #con espsilon: S4 -> S5 (final)

        if i == "+":
            inicio = State()
            end = State()
            afn1 = stack.pop()
            afn2 = stack.pop()
            inicio.AddTransition(afn1.start, "#") #S0 (inicio) -> S1
            inicio.AddTransition(afn2.start, "#") #S0 (inicio) -> S2
            afn1.final.AddTransition(end, "#")    #S3 -> S5 (final)
            afn2.final.AddTransition(end, "#")    #S4 -> S5 (final)
            afn = Automata(inicio, end)
            stack.append(afn)
            pass
        
        #CONCATENACIÓN
        #Forma:
        #con char1: S0 (inicio) -> S1
        #con char2: S1 -> S2 (final)
        elif i == "?":
            afn1 = stack.pop()
            afn2 = stack.pop()
            afn2.end.transitions = afn1.start.transitions
            afn = Automata(afn2.start, afn1.end)
            stack.append(afn)
            
        elif i == "*":
            pass
        else:
            inicio = State()
            end = State()
            inicio.AddTransition(end, i)
            
            #forma:
            #con char: start -> fin
            afn = Automata(start = inicio, final = end)
            stack.append(afn)
            
    print(stack)
        
Thompson("000")
    
    
