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

    pila = [mapa_claus[AFNDE.initial]]

    tt = {}

    while pila:
        print(pila)
        beta = pila.pop()
        print(pila, beta)
        ma = {}
        for letra in AFNDE.alphabet:
            ma.update({letra: []})
            for x in beta:
                try:
                    state = AFNDE.table[x][letra]
                except KeyError:
                    continue
                ma[letra] += (mapa_claus[state])
            ma[letra] = list(set(ma[letra]))
            if str(ma[letra]) not in tt and ma[letra] != beta:
                pila.append(ma[letra])
        tt.update({str(beta):ma})

    alfabeto = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    matriz_final = {}

    for x, y in tt.items():
        print(alfabeto[list(tt.keys()).index(x)])
        mamei = {}
        for z, w in y.items():
            mamei.update({z: alfabeto[list(tt.keys()).index(str(w))]})
        matriz_final.update({alfabeto[list(tt.keys()).index(x)]: mamei})

    inicial = "A"




if __name__ == '__main__':
    main()


def pruebas():
    AFD = Graph([0, 1], 5, initial_state=0, final_states=[3,4],
                transition_table={0: {0: 1, 1: 2}, 1: {0: 2, 1: 3}, 2: {0: 2, 1: 4}, 3: {0: 3, 1: 3}, 4: {0: 4, 1: 4}})

    AFD = Graph([0, 1], 5, initial_state=0, final_states=4,
                transition_table={0: {0: 1, 1: 2}, 1: {0: 1, 1: 3}, 2: {0: 1, 1: 2}, 3: {0: 1, 1: 4}, 4: {0: 1, 1: 2}})

    AFN = Graph([0, 1], 3, True, False, 0, 2, transition_table={0: {0: [0, 1], 1: [0]}, 1: {1: 2}})




