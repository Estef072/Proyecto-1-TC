
class Graph:
    def __init__(self, alphabet: list, states: int or list, isAFND: bool = False, epsilon: bool = False,
                 initial_state: str or int = None, final_states:list = None) -> None:

        self.initial = initial_state
        self.final = final_states or []


        # States
        if isinstance(states, int):
            self.states = [x for x in range(states)]
        else:
            self.states = states



        if epsilon and not isAFND:
            raise ValueError("Un AFD no puede tener transiciones Epsilon")

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
        if self.initial:
            print(f"Ya existe un estado inicial: {self.initial}")
            if input("Sobreescribir? (y/n)").upper() != "Y":
                return None
        if self.checkState(state):
            self.initial = state

    def addFinal(self, state:int or str):
        if self.checkState(state):
            self.final.append(state) if state not in self.final else None




def main():
    x = Graph([0, 1], 3)


if __name__ == "__main__":
    main()
