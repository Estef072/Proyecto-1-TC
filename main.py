from grafo import Graph
from minimization import minimizar
from Thompson import Thompson, InfixPostfix
from itertools import cycle
import time


def main():
    AFN = Graph([0, 1], 3, True, False, 0, 2, transition_table={0: {0: [0,1], 1: [0]}, 1: {1: 2}})

    AFN.simular("100")

    AFD = Graph([0, 1], 5, initial_state=0, final_states=[3, 4],
                transition_table={0: {0: 1, 1: 2}, 1: {0: 2, 1: 3}, 2: {0: 2, 1: 4}, 3: {0: 3, 1: 3}, 4: {0: 4, 1: 4}})

    print(AFD)
    AFD = minimizar(AFD)

    print(AFD)

    tta = Thompson(InfixPostfix("((ab)*)b"))
    tt = tta.Transiciones()
    ti = tta.start.name
    tf = tta.final.name
    regex = "aa+b*".replace("*","").replace("+","").replace("(","").replace(")","")
    talpha = list(set(list(regex)))
    tstates = list(tt.keys()) + list([tf] if tf not in tt else "")

    TEST = Graph(talpha,tstates,True,True,ti,[tf],tt)
    TEST.export("a")

    


if __name__ == '__main__':
    main()


def pruebas():
    AFD = Graph([0, 1], 5, initial_state=0, final_states=[3,4],
                transition_table={0: {0: 1, 1: 2}, 1: {0: 2, 1: 3}, 2: {0: 2, 1: 4}, 3: {0: 3, 1: 3}, 4: {0: 4, 1: 4}})

    AFD = Graph([0, 1], 5, initial_state=0, final_states=4,
                transition_table={0: {0: 1, 1: 2}, 1: {0: 1, 1: 3}, 2: {0: 1, 1: 2}, 3: {0: 1, 1: 4}, 4: {0: 1, 1: 2}})

    AFN = Graph([0, 1], 3, True, False, 0, 2, transition_table={0: {0: [0, 1], 1: [0]}, 1: {1: 2}})




