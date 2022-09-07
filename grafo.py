
class Graph:
    def __init__(self, alphabet: list, states: int or list, isAFND: bool = False, epsilon: bool = False,
                 initial_state: str or int = None, final_states:list = [], transition_table:dict = None) -> None:
        """
        Initiates the graph for the automata.\n
        :param alphabet:
        :param states:
        :param isAFND:
        :param epsilon:
        :param initial_state:
        :param final_states: A list or integer of the final states, can be string, int or list.
        :param transition_table: Dictionary containing the transitions of the table: {"state":{"tranition":"end_state",...},...}
        """

        self.alphabet = alphabet
        self.initial = initial_state

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
            transitions = {letter:"" for letter in alphabet}
            for state in self.states:
                self.table.update({state:transitions.copy()})




    def checkState(self, state:str or int) -> bool:
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

    def addFinal(self, state:int or str) -> None:
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

        string = ""

        divisor = len(str(self.initial)) + 2

        formato = lambda x: str(x).center(divisor, " ")

        header = "\033[1;4m"+ formato("")

        for x in self.alphabet:
            header += "|" + formato(x)
        header += "\033[0m\n"

        string += header

        for x in self.table:
            line = ""
            line += (str("*" if x in list(self.final) else ">" if x == self.initial else "") + str(x)).rjust(divisor," ")
            for y in self.table[x].values():
                line += "|" + formato(y)
            string += line + "\n"

        return string

    def setTransition(self,initial_state, transition, final_state) -> None:
        self.table[initial_state][transition] = final_state

    def export(self,filename="output"):
        with open(filename.join(("",".gv")), "w") as file:
            file.write("digraph finite_state_machine {\n    rankdir=LR;\n\n\t")

            file.write("node [shape = point]; Start;\n\t")
            file.write("node [shape = doublecircle]; "+str(self.final).replace("[","").replace("]","")+";\n\t")
            file.write("node [shape = circle];\n\n\t")

            file.write(f"Start -> {self.initial}\n\n")

            for state, t_tbl in self.table.items():
                for trans, dest in t_tbl.items():
                    file.write(f'\t{state} -> {dest} [ label = "{trans}" ]\n')

            file.write("}")



def main():
    x = Graph([0,1],5,initial_state=0,final_states=4,transition_table={0:{0:1,1:2},1:{0:1,1:3},2:{0:1,1:2},3:{0:1,1:4},4:{0:1,1:2}})


if __name__ == "__main__":
    main()
