
class Graph:
    def __init__(self, alphabet: list, states: int or list, isAFND: bool = False, epsilon: bool = False,
                 initial_state: str or int = None, final_states:list = None) -> None:

        self.alphabet = alphabet
        self.initial = initial_state
        self.final = final_states or []

        # States
        if isinstance(states, int):
            self.states = [x for x in range(states)]
        else:
            self.states = states

        if epsilon and not isAFND:
            raise ValueError("Un AFD no puede tener transiciones Epsilon")

        self.table = {}
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
            self.final.append(state) if state not in self.final else None

    def resetFinal(self) -> None:
        """
        Erases all current final states.
        """
        self.final = []

    def __str__(self) -> str:

        string = ""

        divisor = len(str(self.initial)) + 2

        formato = lambda x: str(x).center(divisor, " ")

        header = formato("")

        for x in self.alphabet:
            header += "|" + formato(x)
        header += "\n"

        string += header

        for x in self.table:
            line = ""
            line += formato(x)
            for y in self.table[x].values():
                line += "|" + formato(y)
            string += line + "\n"

        return string

    def setTransition(self,initial_state, transition, final_state) -> None:
        self.table[initial_state][transition] = final_state

def main():
    x = Graph([0, 1], 3)


if __name__ == "__main__":
    main()
