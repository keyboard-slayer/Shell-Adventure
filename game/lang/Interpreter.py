from game.lang.Lexer import SAdvLexer as Lexer
from game.lang.Parser import SAdvParser as Parser

from game.mechanics.term.executor import *

import os
import datetime

class Interpreter:
    def __init__(self, gameDir: str, term: object, quest: object, rpg: object):
        self.term = term
        self.quest = quest
        self.rpg = rpg
        self.lexer = Lexer()
        self.parser = Parser()
        self.gameDir = gameDir
        self.mainPath = None
        self.buffer = {
            'FILE': ({}, os.path.isfile), 
            'DIR': ({},  os.path.isdir),
            'TIME': ({}, lambda time: datetime.datetime.now() > time),
            'DELFILE': ({}, lambda fichier: not os.path.isfile(fichier)),
            'DELDIR': ({}, lambda dossier: not os.path.isdir(dossier)) 
        }

        self.pos = {'term': (1420, 0), 'quest': (1420, 540), 'rpg': (0, 0)}

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

                if code[0] == "REPEAT":
                    for _ in range(int(code[1])):
                        self.evaluate(code[2])
                    
                if code[0] == "WAIT":
                    if code[1][-1] == 's':
                        self.buffer['TIME'][0][datetime.datetime.now() + datetime.timedelta(0, int(code[1][:-1]))] = code[2]
                    
                    if code[1] in self.buffer.keys():
                        self.buffer[code[1]][0][code[2]] = code[3]
                
                if code[0] == "EXIST":
                    if os.path.isfile(code[1]) or os.path.isdir(code[1]):
                        self.evaluate(code[2])

                if code[0] == "DISABLE":
                    exec(f"self.{code[1]}.resize((0, 0))")
                    self.pos[code[1]] = (6666, 6666)

                if code[0] == "SETPATH":
                    if os.path.isdir(os.path.join(self.gameDir, code[1])):
                        self.mainPath = code[1]
                    else:
                        raise Exception(f"The directory {os.path.join(self.gameDir, code[1])} is not found")

                if code[0] == "READFILE":
                    print(True)
                    if self.mainPath is None:
                        raise Exception("the mainPath is undefined")
                    else:
                        if not os.path.isfile(os.path.join(self.mainPath, code[1])):
                            raise Exception(f"Le fichier {os.path.join(self.mainPath, code[1])} est introuvable")
                        else:
                            execute_and_out(f"cat {os.path.join(self.mainPath, code[1])}", self.term)
            
            return 0
        except TypeError:
            return 1


    def mainloop(self):
        for wait in self.buffer.keys():
            loop = 0
            check = self.buffer[wait][1]
            while len(self.buffer[wait][0]) > loop:
                if check(list(self.buffer[wait][0].keys())[loop]):
                    self.evaluate(self.buffer[wait][0][list(self.buffer[wait][0].keys())[loop]])
                    del self.buffer[wait][0][list(self.buffer[wait][0].keys())[loop]]
                loop += 1

        return list(self.pos.values())

    def execute(self, file):
        with open(f"{self.gameDir}/game/script/{file}", 'r') as script:
            for line in script.readlines():
                tree = self.parse(line)
                self.evaluate(tree)



    def get_tree(self):
        return self.tree
