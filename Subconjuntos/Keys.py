from anld import *

class Keys :
    """
    Conjunto de variables claves del analizador
    """

    VACIO = "Ɛ"
    OR = "|"
    PLUS = "+"
    STAR = "*"
    CONCAT = "."
    NONE_OR_ONE = "?"
    COPY_LABEL ="B" 
    DIGITOS = "0123456789"
    ALFABETO = "abcdefghijklmnopqrstuvwxyz"
    

    def __init__ (self, alfabeto=None) :
        self.operadores_binarios = "|."
        self.operadores_unarios = "+*?"
        self.agrupadores = "()"
        self.operadores =  self.operadores_binarios + \
                           self.operadores_unarios + \
                           self.agrupadores
        if alfabeto != None:
            self.alfabeto = alfabeto
        else :
            self.alfabeto = Keys.ALFABETO + Keys.DIGITOS
            
        self.definicion_regular = "$"
        self.tabla_simbolos = {}
        self.tabla = {}
        self.j = 0
    
    def get_tabla_simbolos_value_at(self, def_regular):
     
        if self.tabla_simbolos.has_key(def_regular) :
            return self.tabla_simbolos[def_regular]
        return None
        
    def set_tabla_simbolos_value_at(self, def_regular, value):
      
        analizar_def_reg = anld(value, self)
        
        analizar_def_reg.start()
        
        self.tabla_simbolos[def_regular] = analizar_def_reg.postfija
        
        t = def_regular + "->" + value
        
        self.tabla[self.j] = t
        
        self.j += 1
    
    def print_tabla_simbolos(valor):
        
        i = 0 
        while (i<len(valor)):
            print (valor[i])
            i += 1
        return valor

Valorx = Keys.print_tabla_simbolos("((ab)*)b")
print(Valorx)