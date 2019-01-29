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
        self.instructNotFinished = False
        self.mainPath = None
        self.string = ""
        self.currentTyping = ""
        self.inputVar = ""

        self.variable = {}

        self.buffer = {
            'INPUT': [],
            'FILE': ({}, os.path.isfile), 
            'DIR': ({},  os.path.isdir),
            'TIME': ({}, lambda time: datetime.datetime.now() > time),
            'DELFILE': ({}, lambda fichier: not os.path.isfile(fichier)),
            'DELDIR': ({}, lambda dossier: not os.path.isdir(dossier)) 
        }

        self.waitIter = []

        self.pos = {'term': (1420, 0), 'quest': (1420, 540), 'rpg': (0, 0)}

    def parse(self, command):
        lex = self.lexer.tokenize(command)
        return self.parser.parse(lex)

    def nextChar(self, time):
        try:
            self.term.removeLine()
            self.currentTyping += next(self.string)
            self.term.add_to_display(self.currentTyping)

            if not self.term.collideFont():
                self.term.add_to_display(" ")
                self.currentTyping = ""

            self.buffer["TIME"][0][datetime.datetime.now() + datetime.timedelta(0, time)] = [("PYTHON", f"self.nextChar({time})")]
        except StopIteration:
            self.term.add_to_display(self.currentTyping)

            try:
                self.evaluate(self.waitIter[0])
                self.waitIter = self.waitIter[1:]
            except IndexError:
                pass

            self.currentTyping = ""
            return 1

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
                    
                if code[0] == "INPUT":
                    self.term.getInput()
                    self.inputVar = code[1]


                if code[0] == "WAIT":
                    if code[1] == "INPUT":
                       self.buffer['INPUT'] = code[2]

                    if code[1] == "STRING":
                        self.waitIter.append(code[2])
                    
                    if code[1][-1] == 's':
                        self.buffer['TIME'][0][datetime.datetime.now() + datetime.timedelta(0, float(code[1][:-1]))] = code[2]
                    
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
                    if self.mainPath is None:
                        raise Exception("the mainPath is undefined")
                    else:
                        if not os.path.isfile(os.path.join(self.mainPath, code[1])):
                            raise Exception(f"Le fichier {os.path.join(self.mainPath, code[1])} est introuvable")
                        else:
                            execute_and_out(f"cat {os.path.join(self.mainPath, code[1])}", self.term)


                if code[0] == "TYPESTRING":
                    self.term.add_to_display(" ")
                    self.string = iter(code[2])
                    self.buffer['TIME'][0][datetime.datetime.now() + datetime.timedelta(0, float(code[1][:-1]))] = [("PYTHON", f"self.nextChar(float({code[1][:-1]}))")]

                if code[0] == "TYPEFILE":
                    if self.mainPath is None:
                        raise Exception("the mainPath is undefined")
                    else:
                        if not os.path.isfile(os.path.join(self.mainPath, code[2])):
                            raise Exception(f"Le fichier {os.path.join(self.mainPath, code[2])} est introuvable")
                        else:
                            with open(os.path.join(self.mainPath, code[2]), 'r') as file:
                                self.string = iter(file.read().replace("\n", ""))
                                self.term.add_to_display(" ")
                                self.buffer['TIME'][0][datetime.datetime.now() + datetime.timedelta(0, float(code[1][:-1]))] = [('PYTHON', f'self.nextChar(float({code[1][:-1]}))')]
                            
                            
            return 0
        except TypeError:
            return 1



    def mainloop(self):
        for wait in list(self.buffer.keys())[1:]:
            loop = 0
            check = self.buffer[wait][1]
            while len(self.buffer[wait][0]) > loop:
                if check(list(self.buffer[wait][0].keys())[loop]):
                    self.evaluate(self.buffer[wait][0][list(self.buffer[wait][0].keys())[loop]])
                    del self.buffer[wait][0][list(self.buffer[wait][0].keys())[loop]]
                loop += 1
            
            if self.term.get_env("LASTINPUT"):
                self.variable[self.inputVar] = self.term.get_env("LASTINPUT")
                self.term.set_env("LASTINPUT", "")
                self.inputVar = ""
                if self.buffer["INPUT"]:
                    self.evaluate(self.buffer["INPUT"])
                    self.buffer["INPUT"] = []
                

        return list(self.pos.values())

    def execute(self, file):
        with open(f"{self.gameDir}/game/script/{file}", 'r') as script:
            for line in script.readlines():
                tree = self.parse(line)
                self.evaluate(tree)

                while self.instructNotFinished:
                    continue



    def get_tree(self):
        return self.tree
