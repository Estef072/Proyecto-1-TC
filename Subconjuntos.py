from grafo import Graph

def subconjuntos(AFNDE):

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
        beta = pila.pop()
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

    alfabeto = ["0","1","2","3","4","5","6","7","8","9"]

    matriz_final = {}

    for x, y in tt.items():
        print(alfabeto[list(tt.keys()).index(x)])
        mamei = {}
        for z, w in y.items():
            mamei.update({z: alfabeto[list(tt.keys()).index(str(w))]})
        matriz_final.update({alfabeto[list(tt.keys()).index(x)]: mamei})

    inicial = "0"

    final_states = []
    real_final_states = []

    for st in tt.keys():
        for ef in AFNDE.final:
            if str(ef) in st:
                final_states.append(st)

    for x in final_states:
        real_final_states.append((alfabeto[list(tt.keys()).index(str(x))]))

    tt = matriz_final
    ti = inicial
    tf = real_final_states
    talpha = AFNDE.alphabet
    tstates = list(matriz_final.keys())

    SB = Graph(talpha, tstates, False, False, ti, tf, tt)

    return SB
