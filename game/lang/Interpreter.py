from game.lang.Lexer import SAdvLexer as Lexer
from game.lang.Parser import SAdvParser as Parser
from game.mechanics.rpg.sprite import Sprite
from game.mechanics.rpg.dialog import Dialog

from game.mechanics.term.executor import *

from typing import Tuple

import os
import datetime

def hex_convert(hexColor: str) -> Tuple[int, int, int]:
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
            'FILE': ({}, os.path.isfile),
            'DIR': ({}, os.path.isdir),
            'DELFILE': ({}, lambda fichier: not os.path.isfile(fichier)),
            'DELDIR': ({}, lambda dossier: not os.path.isdir(dossier))
        }

        self.dialog_buffer = []
        self.end_dialog = []
        self.spriteMove = []
        self.sprites = {}
        self.pos = {'term': (1420, 0), 'quest': (1420, 540), 'rpg': (0, 0)}
        self.backPos = {'term': (1420, 0), 'quest': (1420, 540), 'rpg': (0, 0)}

    def parse(self, line):
        lex = self.lexer.tokenize(line)
        return self.parser.parse(lex)

    def parse_string(self, string: str):
        resultat = []
        for word in [txt for txt in string.split(' ') if txt]:
            if word[0] == '$':
                varName = word[1:].replace(',', '')
                if varName in globals():
                    resultat.append(globals()[varName])
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

        if code[0] == "EXIST":
            if os.path.isfile(code[1]) or os.path.isdir(code[1]):
                self.evaluate(code[2])

        if code[0] == "INPUT":
            if len(code) == 3:
                self.term.set_custom_prompt(self.parse_string(code[2]))

            self.term.getInput()
            self.inputVar = code[1]

            self.evaluated = False

        if code[0] == "LOADSCRIPT":
            self.execute(code[1])

        if code[0] == "REPEAT":
            for _ in range(int(code[1])):
                for statement in code[2]:
                    self.evaluate(statement)

        if code[0] == "TYPESTRING":
            self.term.add_to_display(" ")
            current_timing = datetime.datetime.now()
            nextTiming = current_timing + datetime.timedelta(0, float(code[1][:-1]))
            self.string = (nextTiming, self.parse_string(code[2]), float(code[1][:-1]))
            self.evaluated = False

        if code[0] == "WAIT":
            if code[1] in self.buffer.keys():
                self.buffer[code[1]][0][code[2]] = code[3]
                print(self.buffer[code[1]][0])
            else:
                self.timing = datetime.datetime.now() + datetime.timedelta(0, float(code[1][:-1]))
                self.evaluated = False

        if code[0] == "SETPATH":
            if os.path.isdir(os.path.join(self.gameDir, code[1])):
                self.mainPath = code[1]
            else:
                raise Exception(f"The directory {os.path.join(self.gameDir, code[1])} is not found")

        if code[0] == "LOADSPRITE":
            spriteFolder = os.path.join(self.mainPath, "sprite")
            color = hex_convert(code[-3])
            self.sprites[code[1]] = Sprite(
                os.path.join(spriteFolder, code[2]),
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
                [datetime.datetime.now() + datetime.timedelta(0, speed),
                 self.sprites[code[2]], goto, int(code[3]), speed]
            )

        if code[0] == "IF":
            if globals()[code[1]] == code[2]:
                self.evaluate(code[3])


        if code[0] == "DIALOG":
            spriteFolder = os.path.join(self.mainPath, "sprite")
            sprite = os.path.join(spriteFolder, code[1])
            color = hex_convert(code[2])
            boolean = True if code[4].lower() == "true" else False
            if "dialog" not in self.rpg.in_surface():
                self.rpg.add_to_surface("dialog",
                                        Dialog(icon=sprite, color=color, txt=code[3], haveToContinue=boolean,
                                               font="./font/monospace.ttf", screenSize=self.rpg.get_size())
                                        )
            else:
                self.dialog_buffer.append(Dialog(icon=sprite, color=color, txt=code[3],
                                                 haveToContinue=boolean, font="./font/monospace.ttf",
                                                 screenSize=self.rpg.get_size())
                                          )
            # TODO: Stop instructions

    def execute(self, filename: str):
        with open(f"{self.gameDir}/game/script/{filename}", 'r') as script:
            for line in script.readlines():
                tree = self.parse(line)
                if tree is not None:
                    self.codeTree.append(tree)

    def mainloop(self):
        # ~ self.evaluated = self.rpg.get_interruption()

        for key in self.buffer.keys():
            tofind = list(self.buffer[key][0])
            if tofind:
                if self.buffer[key][1](tofind[0]):
                    self.evaluate(self.buffer[key][0][tofind[0]])
                    del self.buffer[key][0][tofind[0]]


        if self.dialog_buffer:
            if "dialog" not in self.rpg.in_surface():
                self.rpg.add_to_surface("dialog", self.dialog_buffer[0])
                self.dialog_buffer = self.dialog_buffer[1:]

        if not self.dialog_buffer and self.end_dialog and "dialog" not in self.rpg.in_surface():
            self.codeTree += self.end_dialog[0]
            self.end_dialog = self.end_dialog[1:]

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

        if self.string[1] and self.string[0] < datetime.datetime.now():
            self.term.removeLine()
            self.typeBuffer += self.string[1][0]
            nextTiming = datetime.datetime.now() + datetime.timedelta(0, self.string[2])
            self.string = (nextTiming, self.string[1][1:], self.string[2])
            self.term.add_to_display(self.typeBuffer)

        if self.codeTree:
            #print(self.codeTree)
            if self.evaluated:
                if type(self.codeTree[0]) == tuple:
                    self.evaluate(self.codeTree[0])
                else:
                    for code in self.codeTree[0]:
                        self.evaluate(code)

            if self.timing and self.timing < datetime.datetime.now():
                self.timing = 0
                self.evaluated = True

            if self.term.get_env("LASTINPUT"):
                if self.inputVar != '_':
                    globals()[self.inputVar] = self.term.get_env("LASTINPUT")

                self.term.set_env("LASTINPUT", "")
                self.inputVar = ""
                self.evaluated = True

            elif self.string[0] and not self.string[1]:
                self.typeBuffer = ""
                self.string = (0, [], 0)
                self.evaluated = True

            if self.evaluated:
                self.codeTree = self.codeTree[1:]

        return list(self.pos.values())
