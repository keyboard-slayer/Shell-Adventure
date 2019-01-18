from game.lang.Lexer import SAdvLexer as Lexer
from game.lang.Parser import SAdvParser as Parser

from game.mechanics.term.executor import *

import os
import datetime

class Interpreter:
    def __init__(self, term: object, quest: object):
        self.term = term
        self.quest = quest
        self.lexer = Lexer()
        self.parser = Parser()
        self.buffer = {'FILE': {}, 'DIR': {}, 'TIME': {}}

    def parse(self, command):
        lex = self.lexer.tokenize(command)
        return self.parser.parse(lex)

    def evaluate(self, tree):
        try:
            for code in tree:
                if type(code) == list:
                    code = code[0]
                if code[0] == "PYTHON":
                    exec(code[1])
                    
                if code[0] == "WAIT":
                    # print(code[1])
                    if code[1][-1] == 's':
                        self.buffer['TIME'][datetime.datetime.now() + datetime.timedelta(0, int(code[1][:-1]))] = code[2]
                        print(self.buffer['TIME'])
                    if code[1] == 'DIR':
                        self.buffer['DIR'][code[2]] = code[3]
                    
                    if code[1] == "FILE":
                        self.buffer['FILE'][code[2]] = code[3]

            return 0
        except TypeError:
            return 1


    def mainloop(self):
        if self.buffer['TIME']:
            time = list(self.buffer['TIME'].keys())[0]
            if datetime.datetime.now() > time:
                self.evaluate(self.buffer['TIME'][time])
                del self.buffer['TIME'][time]
        
        if self.buffer['FILE']:
            fichier = list(self.buffer['FILE'].keys())[0]
            if os.path.isfile(fichier):
                self.evaluate(self.buffer['FILE'][fichier])
                del self.buffer['FILE'][fichier]
        
        if self.buffer['DIR']:
            dossier = list(self.buffer['DIR'].keys())[0]
            if os.path.isdir(dossier):
                self.evaluate(self.buffer['DIR'][dossier])
                del self.buffer['DIR'][dossier]


    def execute(self, file):
        with open(f"./game/script/{file}", 'r') as script:
            for line in script.readlines():
                tree = self.parse(line)
                self.evaluate(tree)



    def get_tree(self):
        return self.tree
