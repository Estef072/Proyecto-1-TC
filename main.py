from grafo import Graph
from minimization import minimizar
from Thompson import Thompson, InfixPostfix
from itertools import cycle
import time


def main():
    AFNDE = Graph(["a", "b"], 23, True, True, 6, [22], transition_table={0: {"#":[1,2]},
                                                                     1: {"a": 3},
                                                                     2: {"b": 4},
                                                                     3: {"#": 5},
                                                                     4: {"#": 5},
                                                                     5: {"#": [0,7]},
                                                                     6: {"#": [0,7]},
                                                                     7: {"#": [8,15]},
                                                                     8: {"a": 9},
                                                                     9: {"b": 10},
                                                                     10: {"b": 11},
                                                                     11: {"#": [12,14]},
                                                                     12: {"a": 13},
                                                                     13: {"#": [12,14]},
                                                                     14: {"#": 22},
                                                                     15: {"#": [16,19]},
                                                                     16: {"a": 17},
                                                                     17: {"b": 18},
                                                                     18: {"#": [16,19]},
                                                                     19: {"b": 20},
                                                                     20: {"a": 21},
                                                                     21: {"#": 22},
                                                                     })

    def clausura(estado) -> list:

        lista = [estado]
        marca = []

        while lista:
            estado = lista.pop()
            marca.append(estado) # Marcamos el estado

            try:
                states = AFNDE.table[estado]['#']
            except KeyError:
                continue

            if not isinstance(states, list or tuple):
                states = [states]
            for x in states:
                if x not in marca:
                    lista.append(x)
            lista = list(set(lista))

        return list(set(marca))


    mapa_claus = {}
    for x in AFNDE.states:
        mapa_claus.update({x:clausura(x)})


    tt = {}

    beta = mapa_claus[AFNDE.initial]




if __name__ == '__main__':
    main()


def pruebas():
    AFD = Graph([0, 1], 5, initial_state=0, final_states=[3,4],
                transition_table={0: {0: 1, 1: 2}, 1: {0: 2, 1: 3}, 2: {0: 2, 1: 4}, 3: {0: 3, 1: 3}, 4: {0: 4, 1: 4}})

    AFD = Graph([0, 1], 5, initial_state=0, final_states=4,
                transition_table={0: {0: 1, 1: 2}, 1: {0: 1, 1: 3}, 2: {0: 1, 1: 2}, 3: {0: 1, 1: 4}, 4: {0: 1, 1: 2}})

    AFN = Graph([0, 1], 3, True, False, 0, 2, transition_table={0: {0: [0, 1], 1: [0]}, 1: {1: 2}})




