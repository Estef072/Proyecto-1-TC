from string_tokenizer import *

DEBUG = False

class anld:
 
    def __init__ (self, expr_reg, keys):
        self.tokens = StringTokenizer (expr_reg, keys)
        self.token = self.tokens.get_next_token()
        self.index = 0
        self.keys = keys
        self.operadores_binarios = keys.operadores_binarios
        self.operadores_unarios = keys.operadores_unarios
        self.alfabeto = keys.alfabeto
        self.definicion_regular = keys.definicion_regular
        self.postfija = []

    def start(self):
       
        self.exp_reg()
        return True

    def exp_reg(self):
        
        if DEBUG:
            print ("exp_reg -> Token = ", self.token)

        self.term()
        self.sub_exp_reg()
        
    def sub_exp_reg(self):
        if DEBUG:
            print ("sub_exp_reg -> Token = ", self.token)

        if self.token != "|":
            return

        self.match('|')
        self.term()
        self.postfija.append("|")
        self.sub_exp_reg()

    def term (self):
        if DEBUG:
            print ("term -> Token = "), self.token

        self.factor()
        self.sub_term()

    def sub_term (self):
        if DEBUG:
            print ("sub_term-> Token = "), self.token

        if self.token != ".":
            return

        self.match(".")
        self.factor()
        self.postfija.append(".")
        self.sub_term()


    def factor(self):
        if DEBUG:
            print ("factor -> Token = "), self.token

        if self.token.find(self.definicion_regular) >= 0:
            if DEBUG:
                print ("def_reg -> Token = "), self.token
          
            self.token = self.token[1:]
           
            def_reg_value = self.keys.get_tabla_simbolos_value_at(self.token)
            
            if def_reg_value == None :
                raise Exception( \
                    "ERROR DE SINTAXIS, La definición regular '" + \
                        self.token + "' no se encuentra en la tabal de \
                        simbolos."
                )
             
            self.postfija += def_reg_value
            
            self.match(self.token)

        elif self.alfabeto.find(self.token) >= 0:
            if DEBUG:
                print ("alfabeto -> Token = "), self.token

            self.postfija.append(self.token)
            self.match(self.token)

        else:
            self.match("(")
            self.exp_reg()
            self.match(")")

        if self.operadores_unarios.find(self.token) >= 0:
            self.oper_una()

    def oper_una(self):
    

        if DEBUG:
            print ("oper_una-> Token = ", self.token)

        if self.operadores_unarios.find(self.token) < 0:
            raise Exception( "ERROR DE SINTAXIS, se esperaba un operador unario")
            #exit();

        self.postfija.append(self.token)
        self.match(self.token)

    def match (self, t):

        if self.token == t:
            self.index += 1
            if  self.index < self.tokens.len():
                self.token = self.tokens.get_next_token()

            if DEBUG:
                print ("MATCH ('" + t + "') -> NEXT('" + self.token + "')\n")

            return

        else:
            raise Exception("ERROR DE SINTAXIS, inesperado '", t, "' se esperaba '"\
                , self.token, "'" )
            #exit()
