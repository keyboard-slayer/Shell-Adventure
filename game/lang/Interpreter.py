from game.lang.Lexer import SAdvLexer as Lexer
from game.lang.Parser import SAdvParser as Parser
from game.mechanics.rpg.sprite import Sprite
from game.mechanics.rpg.dialog import Dialog

from game.mechanics.term.executor import *

from typing import Tuple

import os
import datetime

def hexConvert(hexColor: str) -> Tuple[int, int, int]:
    hexColor = hexColor[1:]
    decimalColor = []
    for index in range(0, 6, 2):
        decimalColor.append(int(hexColor[index:index+2], 16))
    return tuple(decimalColor) 


class Interpreter:
    def __init__(self, gameDir: str, term: object, quest: object, rpg: object):
        self.gameDir = gameDir
        self.term = term 
        self.quest = quest 
        self.rpg = rpg 

        self.lexer = Lexer()
        self.parser = Parser(self.rpg)


        self.codeTree = []

        self.mainPath = False 
        self.evaluated = True

        self.string = (0, [], 0)
        self.timing = 0
        self.typeBuffer = ""

        self.buffer = {
            'FILE': ([], os.path.isfile),
            'DIR' : ([], os.path.isdir),
            'DELFILE': ({}, lambda fichier: not os.path.isfile(fichier)),
            'DELDIR': ({}, lambda dossier: not os.path.isdir(dossier)) 
        }
        self.spriteMove = []
        self.sprites = {}
        self.pos = {'term': (1420, 0), 'quest': (1420, 540), 'rpg': (0, 0)}
        self.backPos = {'term': (1420, 0), 'quest': (1420, 540), 'rpg': (0, 0)}


    def parse(self, line):
        lex = self.lexer.tokenize(line)
        return self.parser.parse(lex)

    def parseString(self, string: str):
        resultat = []
        for index, word in enumerate(string.split(' ')):
            if word[0] == '$':
                varName = word[1:].replace(',', '')
                if varName in globals():
                    resultat.append(globals()[varname])
                else:
                    raise NameError(f"name {varName} is undefined")
            else:
                resultat.append(word)

        return ' '.join(resultat)
                   
    def evaluate(self, code):        
        if code[0] == "PYTHON":
            exec(code[1])
            
        if code[0] == "DISABLE":
            exec(f"self.{code[1]}.resize((0, 0))")
            self.pos[code[1]] = (6666, 6666)
        
        if code[0] == "ENABLE":
            size = "500, 540" if code[1] != "rpg" else "1420, 1080"
            exec(f"self.{code[1]}.resize(({size}))")
            self.pos[code[1]] = self.backPos[code[1]]
            
        if code[0] == "INPUT":
            if len(code) == 3:
                self.term.set_custom_prompt(code[2])
                
            self.term.getInput()
            self.inputVar = code[1]
            self.evaluated = False

        if code[0] == "LOADSCRIPT":
            self.execute(code[1])

        if code[0] == "TYPESTRING":
            self.term.add_to_display(" ")
            nextTiming = datetime.datetime.now() + datetime.timedelta(0, float(code[1][:-1]))
            self.string = (nextTiming, self.parseString(code[2]), float(code[1][:-1]))
            self.evaluated = False
        
        if code[0] == "WAIT":
            self.timing = datetime.datetime.now() + datetime.timedelta(0, float(code[1][:-1]))
            self.evaluated = False

        if code[0] == "SETPATH":
            if os.path.isdir(os.path.join(self.gameDir, code[1])):
                self.mainPath = code[1]
            else:
                raise Exception(f"The directory {os.path.join(self.gameDir, code[1])} is not found")

        if code[0] == "LOADSPRITE":
            color = hexConvert(code[-3])
            self.sprites[code[1]] =  Sprite(
                os.path.join(self.mainPath, code[2]), 
                color, 
                (int(code[3]), int(code[4])),
                (int(code[5]), int(code[6])), 
                int(code[7]), 
                int(code[8]),
                (int(code[-1]), int(code[-2]))
            )
            self.rpg.add_to_surface(code[1], self.sprites[code[1]])

        if code[0] == "GO":

            goto = ["UP", "RIGHT", "LEFT", "DOWN"].index(code[1])
            speed = 0.5 if code[-1] == "WALK" else 0.2
            self.spriteMove.append(
                [datetime.datetime.now() + datetime.timedelta(0, speed), self.sprites[code[2]], goto, int(code[3]), speed]
            )
            
        if code[0] == "DIALOG":
            # ('DIALOG', 'dialog-sci.png', '20', '20', '#3cff00', 'Coucou')
            self.rpg.add_to_surface('dialog', Dialog(icon=os.path.join(self.mainPath, code[1]), txt=[5], color=hexConvert(code[4])))



    def execute(self, filename: str):
        with open(f"{self.gameDir}/game/script/{filename}", 'r') as script:
            for line in script.readlines():
                tree = self.parse(line)
                if tree is not None:
                    self.codeTree.append(tree)

    def mainloop(self):
        if self.spriteMove:
            if datetime.datetime.now() > self.spriteMove[0][0]:
                if self.spriteMove[0][-2] > 0:
                    self.spriteMove[0][1].move(self.spriteMove[0][2])
                    self.spriteMove[0][0] = datetime.datetime.now() + datetime.timedelta(0, self.spriteMove[0][-1])
                    self.spriteMove[0][-2] -= 1
                    self.rpg.update()
                else:
                    self.spriteMove[0][1].stop(self.spriteMove[0][2])
                    self.spriteMove.remove(self.spriteMove[0])
        if self.codeTree:
            if self.evaluated:
                self.evaluate(self.codeTree[0])

            if self.timing and self.timing < datetime.datetime.now():
                self.timing = 0
                self.evaluated = True 

            if self.term.get_env("LASTINPUT"):
                if self.inputVar != '_':
                    globals()[self.inputVar] = self.term.get_env("LASTINPUT")
                
                self.term.set_env("LASTINPUT", "")
                self.inputVar = ""
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