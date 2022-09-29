from grafo import Graph

def minimizar(AFD:Graph) -> Graph:

    map = {}
    for x in AFD.alphabet:
        map.update({x: []})

    for x in AFD.table.values():
        for y, w in x.items():
            map[y].append(w)

    combinations = lambda list1, list2: [(x, y) for x in list1 for y in list2]

    lista = []
    m = combinations(AFD.states, AFD.states)

    matrix = []
    [matrix.append(x) for x in [tuple(sorted(y)) for y in m] if x not in matrix]

    states = AFD.states

    for x in zip(states, states):
        matrix.remove(x)

    for x in combinations(AFD.final, [x for x in AFD.states if x not in AFD.final]):
        lista.append(x)

    everyindex = lambda list, value: [i for i, x in enumerate(list) if x == value]

    variables = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

    while lista:
        x, y = lista.pop(0)
        for transitions in map.values():
            if x in transitions or y in transitions:
                tx = everyindex(transitions, x)
                ty = everyindex(transitions, y)

                comb = combinations(tx, ty)

                if (x, y) in comb:
                    comb.remove((x, y))

                lista += comb

            print(x,y)
            vert = tuple(sorted((x, y)))

            if vert in matrix:
                matrix.remove(vert)

    newstates = []

    for x in AFD.states:
        for y in matrix:
            if x not in y:
                newstates.append(x)

    newstates += matrix

    mapa = []

    for a, x in map.items():
        for y in range(len(x)):
            for i, z in enumerate(matrix):
                if x[y] in z:
                    x[y] = variables[i]
        map.update({a: x})
        mapa.append(x)

    for x in range(len(states)):
        for i, y in enumerate(matrix):
            if states[x] in y:
                states[x] = variables[i]

    initial = AFD.initial
    for i, x in enumerate(matrix):
        if initial in x:
            initial = variables[i]

    final = AFD.final
    for x in range(len(final)):
        for i, y in enumerate(matrix):
            if final[x] in y:
                final[x] = variables[i]
    final = list(set(final))

    tt = {}
    for x in range(len(states)):
        tt.update({states[x]: {AFD.alphabet[0]: mapa[0][x], AFD.alphabet[1]: mapa[1][x]}})

    return Graph(AFD.alphabet, list(set(states)), initial_state=initial, final_states=final, transition_table=tt)