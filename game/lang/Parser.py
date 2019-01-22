#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from sly import Parser

from game.lang.Lexer import SAdvLexer
from string import hexdigits

class SAdvParser(Parser):
    tokens = SAdvLexer.tokens

    def __init__(self):
        self.env = {"loop": {}}
        self.obj = []
        self.func = ""

    @_('', 'COMMENT')
    def statement(self, p):
        pass

    @_('SAY STRING')
    def statement(self, p):
        return [('PYTHON', f'self.term.add_to_display(\"{p.STRING}\")')]

    @_('OBJECTIF NAME STRING')
    def statement(self, p):
        self.obj.append(p.NAME)
        return [('PYTHON', f'self.quest.add(\"{p.NAME}\", \"{p.STRING}\")')]

    @_('DONE NAME')
    def statement(self, p):
        return [('PYTHON', f'self.quest.done(\"{p.NAME}\")')]

    @_('WAIT FILE STRING THEN statement')
    def statement(self, p):
        return [('WAIT', 'FILE', p.STRING, p.statement)]

    @_('WAIT DIR STRING THEN statement')
    def statement(self, p):
        return [('WAIT', 'DIR', p.STRING, p.statement)]
    
    @_('LOOP NUM TIMES')
    def statement(self, p):
        identity = ''.join([random.choice(hexdigits) for _ in range(16)])
        print(self.env["loop"])
        self.env["loop"][f"{identity}@{p.NUM}"] = []


    @_('WAIT TIME THEN statement')
    def statement(self, p):
        return [('WAIT', p.TIME, p.statement)]

    @_('WAIT DELFILE STRING THEN statement')
    def statement(self, p):
        return [('WAIT', 'DELFILE', p.STRING, p.statement)]
    
    @_('WAIT DELDIR STRING THEN statement')
    def statement(self, p):
        return [('WAIT', 'DELDIR', p.STRING, p.statement)]

    @_('EXIT')
    def statement(self, p):
        return [('PYTHON', 'exit()')]

    @_('EXEC STRING')
    def statement(self, p):
        return [("PYTHON", f'execute_and_out(\"{p.STRING}\", self.term)')]

    @_('RUN STRING')
    def statement(self, p):
        return [("PYTHON", f'file_and_out(self.gameDir+\"/game/script/{p.STRING}\", self.term)')]

    @_('FUN NAME')
    def statement(self, p):
        if not self.func:
            self.env[p.NAME] = []
            self.func = p.NAME
        
        else:
            raise Exception("Doesn't work like that :(")

    @_('CALL NAME')
    def statement(self, p):
        return self.env[p.NAME]

    @_('TAB statement')
    def statement(self, p):
        if self.func:
            self.env[self.func].append(p.statement)

        else:
           raise IndentationError("unexpected indent")

    @_('SPACE statement')
    def statement(self, p):
        if self.func:
            self.env[self.func].append(p.statement)
        
        elif self.env["loop"]:
            if p.statement is not None:
                self.env["loop"][list(self.env["loop"].keys())[-1]].append(p.statement)

        else:
           raise IndentationError("unexpected indent")

    @_('END FUN')
    def statement(self, p):
        if not self.func:
            raise SyntaxError()
        else:
            self.func = ""

    @_('END LOOP')
    def statement(self, p):
        if not self.env["loop"]:
            raise SyntaxError()
        else:
            toreturn = self.env["loop"][list(self.env["loop"].keys())[-1]]
            time = list(self.env["loop"].keys())[-1].split('@')[-1]
            del self.env["loop"][list(self.env["loop"].keys())[-1]]
            return [("REPEAT", time, toreturn)]

    @_('IFEXIST STRING THEN statement')
    def statement(self, p):
        return [("EXIST", p.STRING, p.statement)]
    
    @_('DISABLE GAMEPART')
    def statement(self, p):
        return [("DISABLE", p.GAMEPART.lower())]

    @_('SETPOS GAMEPART NUM NUM')
    def statement(self, p):
        return [("PYTHON", f"self.pos[\"{p.GAMEPART.lower()}\"] = ({p.NUM0}, {p.NUM1})")]

    @_('SETSIZE GAMEPART NUM NUM')
    def statement(self, p):
        return [("PYTHON", f"self.{p.GAMEPART.lower()}.resize(({p.NUM0}, {p.NUM1}))")]
    
    @_('LOADPATH STRING')
    def statement(self, p):
        return [("SETPATH", p.STRING)]

    @_('READFILE STRING')
    def statement(self, p):
        print(True)
        return [("READFILE", p.STRING)]