from game.lang.Lexer import SAdvLexer as Lexer
from game.lang.Parser import SAdvParser as Parser

from game.mechanics.term.executor import *

import os
import datetime

class Interpreter:
    def __init__(self, gameDir: str, term: object, quest: object, rpg: object):
        self.gameDir = gameDir
        self.term = term 
        self.quest = quest 
        self.rpg = rpg 

        self.lexer = Lexer()
        self.parser = Parser()


        self.codeTree = []

        self.mainPath = False 
        self.evaluated = True
        self.variable = {}

        self.string = (0, [], 0)
        self.timing = 0
        self.typeBuffer = ""

        self.buffer = {
            'FILE': ([], os.path.isfile),
            'DIR' : ([], os.path.isdir),
            'DELFILE': ({}, lambda fichier: not os.path.isfile(fichier)),
            'DELDIR': ({}, lambda dossier: not os.path.isdir(dossier)) 
        }

        self.pos = {'term': (1420, 0), 'quest': (1420, 540), 'rpg': (0, 0)}


    def parse(self, line):
        lex = self.lexer.tokenize(line)
        return self.parser.parse(lex)


    def evaluate(self, tree):
        for code in tree:
            if code[0] == "PYTHON":
                exec(code[1])

            if code[0] == "DISABLE":
                exec(f"self.{code[1]}.resize((0, 0))")
                self.pos[code[1]] = (6666, 6666)

            if code[0] == "TYPESTRING":
                self.term.add_to_display(" ")
                nextTiming = datetime.datetime.now() + datetime.timedelta(0, float(code[1][:-1]))
                self.string = (nextTiming, code[2], float(code[1][:-1]))
                self.evaluated = False
            
            if code[0] == "WAIT":
                self.timing = datetime.datetime.now() + datetime.timedelta(0, float(code[1][:-1]))
                self.evaluated = False

            if code[0] == "SETPATH":
                if os.path.isdir(os.path.join(self.gameDir, code[1])):
                    self.mainPath = code[1]
                else:
                    raise Exception(f"The directory {os.path.join(self.gameDir, code[1])} is not found")


    def execute(self, filename: str):
        with open(f"{self.gameDir}/game/script/{filename}", 'r') as script:
            for line in script.readlines():
                tree = self.parse(line)
                if tree is not None:
                    self.codeTree.append(tree)

    def mainloop(self):
        if self.codeTree:
            if self.evaluated:
                self.evaluate(self.codeTree[0])

            if self.timing and self.timing < datetime.datetime.now():
                self.timing = 0
                self.evaluated = True        
            
            if self.string[1] and self.string[0] < datetime.datetime.now():
                self.term.removeLine()
                self.typeBuffer += self.string[1][0]
                nextTiming = datetime.datetime.now() + datetime.timedelta(0, self.string[2])
                self.string = (nextTiming, self.string[1][1:], self.string[2])
                self.term.add_to_display(self.typeBuffer)
            
            elif self.string[0] and not self.string[1]:
                self.typeBuffer = ""
                self.string = (0, [], 0)
                self.evaluated = True

            if self.evaluated:    
                self.codeTree = self.codeTree[1:]
        
        return list(self.pos.values())

                    
                            
                            
                
        