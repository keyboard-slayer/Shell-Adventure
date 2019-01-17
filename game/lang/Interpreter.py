from game.lang.Lexer import SAdvLexer as Lexer
from game.lang.Parser import SAdvParser as Parser

from game.mechanics.term.executor import *

import os

class Interpreter:
    def __init__(self, term: object, quest: object):
        self.term = term
        self.quest = quest
        self.lexer = Lexer()
        self.parser = Parser()
        self.tree = None

    def evaluate(self, command):
        lex = self.lexer.tokenize(command)
        self.tree = self.parser.parse(lex)
        try:
            for code in self.tree:
                if type(code) == list:
                    code = code[0]
                if code[0] == "PYTHON":
                    print(code[1])
                    exec(code[1])

            return 0
        except TypeError:
            return 1

    def execute(self, file):
        with open(f"./game/script/{file}", 'r') as script:
            for line in script.readlines():
                self.evaluate(line)



    def get_tree(self):
        return self.tree
