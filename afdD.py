import ply.lex as lex
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
import matplotlib.pyplot as plt

# Tokens
tokens = (
    'OPEN_P',
    'CLOSED_P',
    'OR',
    'STAR',
    'CONCAT',
    'LETTER',
    'LAMBDA'
)

# reglas
t_OPEN_P = r'\('
t_CLOSED_P = r'\)'
t_OR = r'\+'
t_STAR = r'\*'
t_CONCAT = r'\.'
t_LETTER = r'[a-zA-Z]'
t_LAMBDA = r'\&'

# si no existe el caracter
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# leyendo el input
def _getContent(filename):
    file = open(filename, 'r')
    content = file.read()
    file.close()

    return content


class RegexLexer:
    lexer = lex.lex()
    # Contenedro de los tokens descritos
    parts = []

    def __init__(self, filename=None):
        if filename is not None:
            self.filename = filename
            self.content = _getContent(filename)
            self.content = '(' + self.content + ')&'
            self.tokenize()
        else:
            print("The file name was empty")

    # separación de tokens con lexer
    def tokenize(self):
        self.lexer.input(self.content)
        while True:
            token = self.lexer.token()
            if not token:
                break
            self.parts.append(token)

    def printTokens(self):
        for part in self.parts:
            print(part)

    # le agrega la concatenación con un punto
    def dotConcat(self):
        possibleConcat = False
        concatMessage = ''
        index = 0

        for part in self.parts:
            if part.type in ['LETTER', 'LAMBDA']:
                if possibleConcat is True:
                    concatMessage = concatMessage + '.'
                else:
                    possibleConcat = True
            elif part.type in ['STAR', 'CLOSED_P']:
                possibleConcat = True
            elif (part.type == 'OPEN_P') & (self.parts[index - 1].type in ['LETTER', 'STAR']):
                concatMessage = concatMessage + '.'
            else:
                possibleConcat = False
            concatMessage = concatMessage + part.value
            index = index + 1

        self.content = concatMessage
        self.parts.clear()
        self.tokenize()

    # función para pasar a postfix
    def postfix(self, permanent=False):
        if self.content[len(self.content) - 1] == '.':
            print("Already in postfix notation")
            return

        # Hay que pasarla a postfox
        operator_stack = []
        last_index = -1
        rpn_regex = ''

        for part in self.parts:
            if part.type in ['LETTER', 'STAR', 'LAMBDA']:
                rpn_regex = rpn_regex + part.value
                continue

            if part.type == 'OPEN_P':
                operator_stack.append(part)
                last_index += 1
                continue

            if part.type == 'CLOSED_P':
                while operator_stack[last_index].type != 'OPEN_P':
                    rpn_regex += operator_stack[last_index].value
                    operator_stack.pop()
                    last_index -= 1
                # Otro pop para el último paréntesis
                operator_stack.pop()
                last_index -= 1
                continue

            if part.type in ['OR', 'CONCAT']:
                if last_index >= 0:
                    if operator_stack[last_index].type not in ['OPEN_P', 'CLOSED_P']:
                        rpn_regex += operator_stack[last_index].value
                        operator_stack.pop()
                        operator_stack.append(part)
                    else:
                        operator_stack.append(part)
                        last_index += 1
                else:
                    operator_stack.append(part)
                    last_index += 1
                continue

        # limpiando la pilaaa
        while len(operator_stack) != 0:
            rpn_regex += operator_stack[last_index].value
            operator_stack.pop()

        if permanent is True:
            self.parts.clear()
            self.content = rpn_regex
            self.tokenize()

        return rpn_regex

    # árbol para proceder con el firstpos, lastpos y followpos
    def makeAST(self):
        self.dotConcat()
        # print("\nRegex after adding concatenations: " + self.content + '\n')
        # self.printTokens()

        print("\nRegex written postfix: " + self.postfix(permanent=True) + '\n')

        AST = nx.DiGraph()
        node_stack = []
        last_index = -1

        for part in self.parts:
            if part.type in ['LETTER', 'LAMBDA']:
                AST.add_node(part, val=part.value)
                node_stack.append(part)
                last_index += 1
            elif part.type in ['OR', 'CONCAT']:
                AST.add_node(part, val=part.value)
                for i in range(1, 2):
                    AST.add_edge(part, node_stack[last_index])
                    node_stack.pop()
                    last_index -= 1
                node_stack.append(part)
                last_index += 1
            elif part.type == 'STAR':
                AST.add_node(part, val=part.value)
                AST.add_edge(part, node_stack[last_index])
                node_stack.pop()
                node_stack.append(part)

        return AST

    def printAST(self):
        AST = self.makeAST()
        
def _makeNodeLabel(node):
    label = 0
    for pos in node:
        label = label * 10 + pos

    return label


class Converter:
    FirstPos = []
    LastPos = []
    FollowPos = []

    DFA = nx.MultiDiGraph()

    def __init__(self, rpn_tokens: list):
        
        self.rpn_tokens = rpn_tokens
        self._makeFirstPos()
        self._makeLastPos()
        self._makeFollowPos()

    def _makeFirstPos(self):
        
        index = 0  # Used to copy positions from previous nodes
        letter_no = 1  # Each letter in the regex is associated a number in the order of appearance
        nullable = []

        for token in self.rpn_tokens:
            if token.type in ['LETTER', 'LAMBDA']:
                newpos = [letter_no]
                letter_no += 1
                index += 1
                self.FirstPos.append(newpos)
                if token.type == 'LAMBDA':
                    if token.lexpos == len(self.rpn_tokens) - 2:
                        nullable.append(False)
                    else:
                        nullable.append(True)
                else:
                    nullable.append(False)

            elif token.type == 'OR':
                newpos = self.FirstPos[index - 2].copy() + self.FirstPos[index - 1].copy()
                self.FirstPos.append(newpos)
                index += 1
                if nullable[index - 3] | nullable[index - 2]:
                    nullable.append(True)
                else:
                    nullable.append(False)

            elif token.type == 'STAR':
                newpos = self.FirstPos[index - 1].copy()
                self.FirstPos.append(newpos)
                nullable.append(True)
                index += 1

            elif token.type == 'CONCAT':

                if self.rpn_tokens[index - 1].type == 'STAR':
                    nb = index - 2
                    while True:
                        if self.rpn_tokens[nb].type in ['CONCAT', 'OR']:
                            nb -= 2
                        else:
                            nb -= 1
                            break
                    newpos = self.FirstPos[nb].copy()
                    self.FirstPos.append(newpos)
                    index += 1

                    if nullable[nb]:
                        newpos = self.FirstPos[index - 2].copy()
                        self.FirstPos[index - 1] += newpos
                    if nullable[nb] & nullable[index - 2]:
                        nullable.append(True)
                    else:
                        nullable.append(False)
                else:
                    newpos = self.FirstPos[index - 2].copy()
                    self.FirstPos.append(newpos)
                    index += 1

                    if nullable[index - 3]:
                        newpos = self.FirstPos[index - 2].copy()
                        self.FirstPos[index - 1] += newpos
                    if nullable[index - 3] & nullable[index - 2]:
                        nullable.append(True)
                    else:
                        nullable.append(False)

    def _makeLastPos(self):
        index = 0  # posiciones de los nodos pasados
        letter_no = 1  # cada letra en el regex esta asociada con un número
        nullable = []

        for token in self.rpn_tokens:
            if token.type in ['LETTER', 'LAMBDA']:
                newpos = [letter_no]
                letter_no += 1
                index += 1
                self.LastPos.append(newpos)
                if token.type == 'LAMBDA':
                    if token.lexpos == len(self.rpn_tokens) - 2:
                        nullable.append(False)
                    else:
                        nullable.append(True)
                else:
                    nullable.append(False)

            elif token.type == 'OR':
                newpos = self.LastPos[index - 2].copy() + self.LastPos[index - 1].copy()
                self.LastPos.append(newpos)
                index += 1
                if nullable[index - 3] | nullable[index - 2]:
                    nullable.append(True)
                else:
                    nullable.append(False)

            elif token.type == 'STAR':
                newpos = self.LastPos[index - 1].copy()
                self.LastPos.append(newpos)
                nullable.append(True)
                index += 1

            elif token.type == 'CONCAT':
                newpos = self.LastPos[index - 1].copy()
                self.LastPos.append(newpos)
                index += 1

                if self.rpn_tokens[index - 2].type == 'STAR':
                    nb = index - 3
                    while True:
                        if self.rpn_tokens[nb].type in ['CONCAT', 'OR']:
                            nb -= 2
                        else:
                            nb -= 1
                            break

                    if nullable[index - 2]:
                        newpos = self.LastPos[nb].copy()
                        self.LastPos[index - 1] += newpos

                    if nullable[nb] & nullable[index - 2]:
                        nullable.append(True)
                    else:
                        nullable.append(False)
                else:
                    if nullable[index - 2]:
                        newpos = self.LastPos[index - 3].copy()
                        self.LastPos[index - 1] += newpos
                    if nullable[index - 3] & nullable[index - 2]:
                        nullable.append(True)
                    else:
                        nullable.append(False)

    def _makeFollowPos(self):
        index = 0
        number_nop = 0

    
        for token in self.rpn_tokens:
            if token.type in ['LETTER', 'LAMBDA']:
                number_nop += 1

        self.FollowPos = [[] for _ in range(number_nop)]

        for token in self.rpn_tokens:
            if token.type == 'STAR':
                for pos in self.LastPos[index]:
                    newpos = self.FirstPos[index].copy()
                    self.FollowPos[pos - 1] += newpos
                index += 1
            elif token.type == 'CONCAT':
                if self.rpn_tokens[index - 1].type == 'STAR':
                    nb = index - 2
                    while True:
                        if self.rpn_tokens[nb].type in ['CONCAT', 'OR']:
                            nb -= 2
                        else:
                            nb -= 1
                            break
                    for pos in self.LastPos[nb]:
                        self.FollowPos[pos - 1] += self.FirstPos[index - 1].copy()
                else:
                    for pos in self.LastPos[index - 2]:
                        self.FollowPos[pos - 1] += self.FirstPos[index - 1].copy()
                index += 1
            else:
                index += 1

       s
        for collection in self.FollowPos:
            if collection is not None:
                collection = set(collection)

    def _createNodes(self, used_nodes, first_node, index, letters, letter_groups, first_pos_groups):
        for group in first_pos_groups:
            newNode = []
            for pos in group:
                newNode += self.FollowPos[pos - 1]
            newNode = list(set(newNode))

            newLabel = _makeNodeLabel(newNode)

            if newLabel == 0:
                continue

            if newLabel not in used_nodes:
                self.DFA.add_node(newLabel)
                if len(letters) in newNode:
                    self.DFA.add_edge(first_node, newLabel, letter=letters[group[0] - 1], final=True)
                else:
                    self.DFA.add_edge(first_node, newLabel, letter=letters[group[0] - 1])
                used_nodes.add(newLabel)
                index += 1

                new_pos_groups = [[] for _ in range(len(letter_groups))]
                for pos in newNode:
                    i = 0
                    for letter in letter_groups:
                        if letter == letters[pos - 1]:
                            new_pos_groups[i].append(pos)
                            break
                        else:
                            i += 1

                self._createNodes(used_nodes, newLabel, index, letters, letter_groups, new_pos_groups)
            else:
                if (first_node, newLabel) in self.DFA.edges():
                    continue
                if len(letters) in newNode:
                    self.DFA.add_edge(first_node, newLabel, letter=letters[group[0] - 1], final=True)
                else:
                    self.DFA.add_edge(first_node, newLabel, letter=letters[group[0] - 1])

    def convertToDFA(self):
        used_nodes = set()
        index = -1

        startNode = "START"
        self.DFA.add_node(startNode)
        firstNode = self.FirstPos[len(self.FirstPos) - 1]
        self.DFA.add_node(_makeNodeLabel(firstNode))
        used_nodes.add(_makeNodeLabel(firstNode))
        index += 1

        self.DFA.add_edge(startNode, _makeNodeLabel(firstNode))

        letters = []
        for token in self.rpn_tokens:
            if token.type in ['LETTER', 'LAMBDA']:
                letters.append(token.value)

        letter_groups = set(letters)

        first_pos_groups = [[] for _ in range(len(letter_groups))]
        for pos in firstNode:
            i = 0
            for group in letter_groups:
                if group == letters[pos - 1]:
                    first_pos_groups[i].append(pos)
                    break
                else:
                    i += 1

        self._createNodes(used_nodes, _makeNodeLabel(firstNode), index, letters, letter_groups, first_pos_groups)

if __name__ == '__main__':
    regexlexer = RegexLexer("input.txt")

    # regular expresion
    print("Original regex: " + regexlexer.content + '\n')
    regexlexer.printTokens()

    print(regexlexer.printAST())

    converter = Converter(regexlexer.parts)

    print("FirstPos:")
    print(converter.FirstPos)
    print("\nLastPos:")
    print(converter.LastPos)
    print("\nFollowPos:")
    print(converter.FollowPos)

    converter.convertToDFA()