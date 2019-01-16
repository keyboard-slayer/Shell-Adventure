from game.script.Lexer import SAdvLexer as Lexer
from game.script.Parser import SAdvParser as Parser

class Interpreter:
    def __init__(self, term: object): # TODO: add quest object later
        self.term = term 
        self.lexer = Lexer()
        self.parser = Parser()

    def evaluate(self, command):
        lex = self.lexer.tokenize(command)
        tree = self.parser.parse(lex)

        if tree[0] == "PYTHON":
            print(tree[1])
