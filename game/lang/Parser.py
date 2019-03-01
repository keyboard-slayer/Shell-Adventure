#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from sly import Parser

from game.lang.Lexer import SAdvLexer
from string import hexdigits

class SAdvParser(Parser):
    tokens = SAdvLexer.tokens

    def __init__(self, rpg):
        self.env = {"loop": {}}
        self.obj = []
        self.func = ""
        self.rpg = rpg

    @_('', 'COMMENT')
    def statement(self, p):
        pass

    @_('CLEAR')
    def statement(self, p):
        return [('PYTHON', 'self.term.clear()')]
    
    @_('LOADSCRIPT STRING')
    def statement(self, p):
        return [('LOADSCRIPT', p.STRING)]

    @_('SAY STRING')
    def statement(self, p):
        return [('PYTHON', f'self.term.add_to_display(self.parseString(\"{p.STRING}\"))')]

    @_('SAY NAME')
    def statement(self, p):
        return [('PYTHON', f'self.term.add_to_display(self.variable[\"{p.NAME}\"])')]

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

    @_('INPUT NAME')
    def statement(self, p):
        return [('INPUT', p.NAME)]

    @_('INPUT NAME STRING')
    def statement(self, p):
        return [('INPUT', p.NAME, p.STRING)]

    
    @_('LOOP NUM TIMES')
    def statement(self, p):
        identity = ''.join([random.choice(hexdigits) for _ in range(16)])
        self.env["loop"][f"{identity}@{p.NUM}"] = []


    @_('WAIT TIME')
    def statement(self, p):
        return [('WAIT', p.TIME)]

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
    
    @_('ENABLE GAMEPART')
    def statement(self, p):
        return [("ENABLE", p.GAMEPART.lower())]

    @_('DISABLE TERMPART')
    def statement(self, p):
        return [("PYTHON", f"self.term.disable_{p.TERMPART.lower()}()")]

    @_('ENABLE TERMPART')
    def statement(self, p):
        return [("PYTHON", f"self.term.enable_{p.TERMPART.lower()}()")]
        

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
        return [("READFILE", p.STRING)]
    
    @_('TYPEFILE TIME STRING')
    def statement(self, p):
        return [("TYPEFILE", p.TIME, p.STRING)]
    
    @_('TYPESTRING TIME STRING')
    def statement(self, p):
        return [("TYPESTRING", p.TIME, p.STRING)]

    @_('TYPESTRING TIME NAME')
    def statement(self, p):
        return [("PYTHON", f"self.evaluate([(\"TYPESTRING\", \"{p.TIME}\", self.variable[\"{p.NAME}\"])])")]

    @_('SETUSERNAME STRING')
    def statement(self, p):
        return [("PYTHON", f"self.term.set_env('USER', \"{p.STRING}\")")]

    @_('SETUSERNAME NAME')
    def statement(self, p):
        return [("PYTHON", f"self.term.set_env('USER', self.variable[\"{p.NAME}\"])")]

    @_('SETMACHINENAME STRING')
    def statement(self, p):
        return [("PYTHON", f"self.term.set_env('HOST', \"{p.STRING}\")")]
    
    @_('LOADSPRITE NAME STRING NUM NUM NUM NUM NUM NUM HEXCOLOR NUM NUM')
    def statement(self, p):
        return [(
            "LOADSPRITE",
            p.NAME,
            p.STRING, 
            p.NUM0,
            p.NUM1,
            p.NUM2,
            p.NUM3,
            p.NUM4,
            p.NUM5,
            p.HEXCOLOR,
            p.NUM6,
            p.NUM7
        )]
    
    @_('GO POS NAME NUM SPEED')
    def statement(self, p):
        return [("GO", p.POS, p.NAME, p.NUM, p.SPEED)]

    @_('DIALOG STRING STRING')
    def statement(self, p):
        return [("DIALOG", p.STRING0, p.STRING1)]