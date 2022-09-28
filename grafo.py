import graphviz
import time

class Graph:
    def __init__(self, alphabet: list, states: int or list, isAFND: bool = False, epsilon: bool = False,
                 initial_state: str or int = None, final_states: list = [], transition_table: dict = None) -> None:
        """
        Initiates the graph for the automata.\n
        :param alphabet: The name of the transitions. Ej. [0,1]
        :param states: Given an int it generates the states from 0 to the given number. Otherwise, it can accept a list [Q1,Q2,Q3]
        :param isAFND: True if the automata is non deterministic.
        :param epsilon: True if the automata has empty (epsilon) transitions.
        :param initial_state: The initial state of the automata, can only be string or int.
        :param final_states: A list with the final states, can be string, int or list.
        :param transition_table: Dictionary containing the transitions of the table: {"state":{"tranition":"end_state",...},...}
        """

        self.alphabet = alphabet
        self.initial = initial_state
        self.hasEpsilon = epsilon

        if isinstance(final_states, int or str):
            self.final = [final_states]
        else:
            self.final = final_states or []

        # States
        if isinstance(states, int):
            self.states = [x for x in range(states)]
        else:
            self.states = states

        if epsilon and not isAFND:
            raise ValueError("Un AFD no puede tener transiciones Epsilon")

        self.table = transition_table or {}
        if not self.table:
            transitions = {letter: "" for letter in alphabet}
            for state in self.states:
                self.table.update({state: transitions.copy()})

    def checkState(self, state: str or int) -> bool:
        """
        Checks if a given state is on the graph.\n
        :param state: {str or int} The given state
        :return: True if the state exists. False otherwise.
        """
        if state not in self.states:
            print(f"El estado {state} no existe. Estados: [{self.states}]")
            return False
        return True

    def setInitial(self, state: str or int) -> None:
        """
        Sets a new initial state for the graph. There can only be one Initial state.\n
        :param state: {str or int} The specified state, which ought to be on the list already.
        """
        if self.initial:
            print(f"Ya existe un estado inicial: {self.initial}")
            if input("Sobreescribir? (y/n)").upper() != "Y":
                return None
        if self.checkState(state):
            self.initial = state

    def addFinal(self, state: int or str) -> None:
        """
        Adds a new final state for the graph.\n
        :param state: {str or int} The specified state, which ought to be on the list already.
        """
        if self.checkState(state):
            self.final.append(str(state)) if state not in self.final else None

    def resetFinal(self) -> None:
        """
        Erases all current final states.
        """
        self.final = []

    def __str__(self) -> str:
        """
        Gives the correct format for displaying the graph with a relation table.
        :return: Formatted string
        """
        string = ""
        header_list = self.alphabet + (["e"] if self.hasEpsilon else [])

        divisor = len(str(self.initial)) + 2

        def text_format(text, filler = " "):
            return str(text).center(divisor, filler)

        header = text_format("", "_")

        for x in header_list:
            header += "|" + text_format(x,"_")

        string += header + "\n"

        for x in self.states:
            line = ""
            line += (str ("*" if x in list(self.final) else ">" if x == self.initial else "") + str(x)).rjust(divisor, " ")

            valores = self.table[x] if x in self.table else []

            for y in header_list:
                line += "|" + text_format(valores[y] if y in valores else " ")
            string += line + "\n"

        return string

    def setTransition(self, initial_state, transition, final_state) -> None:
        """
        Sets a especific transition, can overwrite current data.\n
        :param initial_state: The initial state.
        :param transition: The name of the transition, it should be part of the alphabet.
        :param final_state: The destination after the transition.
        """

        if not {initial_state, *final_state}.issubset(self.states):
            raise ValueError("The given states cant be outside of the states of the graph.")

        if transition not in self.alphabet:
            raise ValueError("The transition should be in the alphabet for the graph.")

        self.table[initial_state][transition] = final_state

    def export(self, filename="output"):
        """
        Creates a text file with the data of the automata and a graph of the automata
        :param filename: the name of the files without extension
        :return: Three files with the given name: <output>.gv,<output>.gv.png,<output>.txt
        """

        with open(filename.join(("", ".gv")), "w") as file:
            file.write("digraph finite_state_machine {\n    rankdir=LR;\n\n\t")

            file.write("node [shape = point]; Start;\n\t")
            print(str(self.final).replace("[", "").replace("]", "").replace("'",""))
            file.write("node [shape = doublecircle]; " + str(self.final).replace("[", "").replace("]", "").replace("'","") + ";\n\t")
            file.write("node [shape = circle];\n\n\t")

            file.write(f"Start -> {self.initial}\n\n")

            for state, t_tbl in self.table.items():
                for trans, dest in t_tbl.items():
                    for single in dest if isinstance(dest, list) else [dest]:
                        file.write(f'\t{state} -> "{single}" [ label = "{trans}" ]\n')

            file.write("}")

        graphviz.render(engine="dot", format="png", filepath=filename.join(("",".gv")))

        with open(filename.join(("",".txt")), "w") as file:
            file.write(f"Estados: {self.states}\n")
            file.write(f"Simbolos: {self.alphabet}\n")
            file.write(f"Inicio: {self.initial}\n")
            file.write(f"Aceptacion: {self.final}\n")
            file.write(f"Transiciones:\n")
            file.write(str(self))

    def simular(self, cadena: str) -> None:

        for y in cadena:
            if (int(y) if isinstance(self.alphabet[0], int) else y) not in self.alphabet:
                print(f"Un valor {y} no se encuentra en el alfabeto {self.alphabet}")
                return None

        current_state = self.initial

        initial_time = time.time()

        string = ""

        def inner_simular(inner_cadena, current_state, string):
            for y in range(len(inner_cadena)):
                trans = inner_cadena[y]

                string += (f"{current_state} --[{trans}]-> ")

                try:
                    current_state = self.table[current_state][int(trans) if isinstance(self.alphabet[0], int) else trans]
                except:
                    print(f"{string}Fin del camino.")
                    return None

                if isinstance(current_state, list or tuple):
                    temp = []
                    for state in current_state:
                        temp += [inner_simular(inner_cadena[y + 1:], state, string)]
                    if True in temp:
                        return True
                    else:
                        return False

            string += f"{current_state}"
            print(string, end=" ")
            if current_state in self.final:
                print("Aceptado")
                return True
            else:
                print("No Aceptado")
                return False

        if inner_simular(cadena, current_state, string):
            print("La cadena es aceptada")
        else:
            print("La cadena no es aceptada")
        final_time = time.time()
        print(f"Tiempo de simulacion: {final_time - initial_time}")




def main():
    AFD = Graph([0, 1], 5, initial_state=0, final_states=4, transition_table={0: {0: 1, 1: 2}, 1: {0: 1, 1: 3}, 2: {0: 1, 1: 2}, 3: {0: 1, 1: 4}, 4: {0: 1, 1: 2}})

    AFNDE = Graph(["a", "b"], 3, True, True, 0, 1, transition_table={0: {"a": 1}, 1: {"b": 2}, 2: {"e": 0}})
    AFN = Graph([0,1], 3, True, False, 0, 2, transition_table={0: {0: 1, 1:[0,1]}, 1: {1: 2}})

if __name__ == "__main__":
    main()
