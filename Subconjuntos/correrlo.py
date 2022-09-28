
from Keys import *
from Subconjuntos import *
class App:

    def __init_automata_params__(self):
        """
        Este método inicializa las variables que seran utilizadas por
        los algorimtos
        """
        self.keys = Keys()
        self.afn = None
        self.afn_svg = "images/afn.svg"
        self.afd_svg = "images/afd.svg"
        self.afd_min_svg = "images/afd_min.svg"
        self.afd = None
        self.afd_min = None
        self.bnf = None

    def __ejecutar_subconjutos(self):
        """
        Este método se encarga de ejecutar el algoritmo de subconjuntos
        """
        subconjuntos = Subconjuntos(self.afn, self.keys)
        self.afd = subconjuntos.start_subconjutos()
        for arco in self.afd.arcos :
            self.subconjuntos_store.append([str(arco)])
        return (subconjuntos)


if __name__ == "__main__":

    try:
        a = App()
        
    except KeyboardInterrupt:
        pass