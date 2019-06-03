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

    @_('', 'COMMENT')  # DONE
    def statement(self, p):
        pass

    @_('CLEAR GAMEPART')  # TESTED TODO
    def statement(self, p):
        return ('PYTHON', f'self.{p.GAMEPART.lower()}.clear()')

    @_('LOADSCRIPT STRING')
    def statement(self, p):
        return ('LOADSCRIPT', p.STRING)

    @_('SAY STRING')  # DONE
    def statement(self, p):
        return ('PYTHON', f'self.term.add_to_display(self.parse_string(\"{p.STRING}\"))')

    @_('CHECK COPY STRING STRING ELSE statement')
    def statement(self, p):
        return ('CHECK', p.STRING0, p.STRING1, p.statement)

    @_('SAY NAME')  # DONE
    def statement(self, p):
        return ('PYTHON', f'self.term.add_to_display(globals()[\"{p.NAME}\"])')

    @_('OBJECTIF NAME STRING')  # TESTED TODO
    def statement(self, p):
        self.obj.append(p.NAME)
        return ('PYTHON', f'self.quest.add(\"{p.NAME}\", \"{p.STRING}\")')

    @_('DONE NAME')  # TESTED TODO
    def statement(self, p):
        return ('QUEST', p.NAME)

    @_('WAIT FILE STRING THEN statement')  # DONE
    def statement(self, p):
        return ('WAIT', 'FILE', p.STRING, p.statement)

    @_('WAIT DIR STRING THEN statement')  # DONE
    def statement(self, p):
        return ('WAIT', 'DIR', p.STRING, p.statement)

    @_('INPUT NAME')  # DONE
    def statement(self, p):
        return ('INPUT', p.NAME)

    @_('INPUT NAME STRING')  # DONE
    def statement(self, p):
        return ('INPUT', p.NAME, p.STRING)

    @_('LOOP NUM TIMES')  # TESTED TODO
    def statement(self, p):
        identity = ''.join([random.choice(hexdigits) for _ in range(16)])
        self.env["loop"][f"{identity}@{p.NUM}"] = []

    @_('WAIT TIME')  # DONE
    def statement(self, p):
        return ('WAIT', p.TIME)

    @_('WAIT DELFILE STRING THEN statement')  # DONE
    def statement(self, p):
        return ('WAIT', 'DELFILE', p.STRING, p.statement)

    @_('WAIT DELDIR STRING THEN statement')  # DONE
    def statement(self, p):
        return ('WAIT', 'DELDIR', p.STRING, p.statement)

    @_('EXIT')  # TESTED TODO
    def statement(self, p):
        return ('PYTHON', 'exit()')

    @_('EXEC STRING')  # TESTED TODO
    def statement(self, p):
        return ("PYTHON", f'execute_and_out(\"{p.STRING}\", self.term)')

    @_('RUN STRING')  # TESTED TODO
    def statement(self, p):
        return ("PYTHON", f'file_and_out(self.gameDir+\"/game/script/{p.STRING}\", self.term)')

    @_('FUN NAME')  # TESTED TODO
    def statement(self, p):
        if not self.func:
            self.env[p.NAME] = []
            self.func = p.NAME

        else:
            raise Exception("Doesn't work like that :(")

    @_('CALL NAME')  # TESTED TODO
    def statement(self, p):
        return self.env[p.NAME]

    @_('TAB statement')  # TESTED
    def statement(self, p):
        if self.func:
            self.env[self.func].append(p.statement)

        else:
            raise IndentationError("unexpected indent")

    @_('SPACE statement')  # TESTED
    def statement(self, p):
        if self.func:
            self.env[self.func].append(p.statement)

        elif self.env["loop"]:
            if p.statement is not None:
                self.env["loop"][list(self.env["loop"].keys())[-1]].append(p.statement)

        else:
            raise IndentationError("unexpected indent")

    @_('END FUN')  # TESTED TODO
    def statement(self, p):
        if not self.func:
            raise SyntaxError()
        else:
            self.func = ""
        

    @_('END LOOP')  # TODO Google docs
    def statement(self, p):
        if not self.env["loop"]:
            raise SyntaxError()
        else:
            toreturn = self.env["loop"][list(self.env["loop"].keys())[-1]]
            time = list(self.env["loop"].keys())[-1].split('@')[-1]
            del self.env["loop"][list(self.env["loop"].keys())[-1]]
            return ("REPEAT", time, toreturn)

    @_('IFEXIST STRING THEN statement')  # TODO Google Docs
    def statement(self, p):
        return ("EXIST", p.STRING, p.statement)

    @_('DISABLE GAMEPART')  # TODO Google Docs
    def statement(self, p):
        return ("DISABLE", p.GAMEPART.lower())

    @_('ENABLE GAMEPART')  # TODO Google Docs
    def statement(self, p):
        return ("ENABLE", p.GAMEPART.lower())

    @_('RESET GAMEPART')
    def statement(self, p):
        return ("ENABLE", p.GAMEPART.lower())

    @_('RESET NAME')
    def statement(self, p):
        return ("GO", "DOWN", p.NAME, 0, "RUN")

    @_('DISABLE TERMPART')  # TODO Google Docs
    def statement(self, p):
        return ("PYTHON", f"self.term.disable_{p.TERMPART.lower()}()")

    @_('ENABLE TERMPART')  # TODO Google Docs
    def statement(self, p):
        return ("PYTHON", f"self.term.enable_{p.TERMPART.lower()}()")

    @_('SETPOS GAMEPART NUM NUM')  # TODO Google Docs
    def statement(self, p):
        return ("PYTHON", f"self.pos[\"{p.GAMEPART.lower()}\"] = ({p.NUM0}, {p.NUM1})")

    @_('SETSIZE GAMEPART NUM NUM')  # TODO Google Docs
    def statement(self, p):
        return ("PYTHON", f"self.{p.GAMEPART.lower()}.resize(({p.NUM0}, {p.NUM1}))")

    @_('LOADPATH STRING')  # TODO Google Docs
    def statement(self, p):
        return ("SETPATH", p.STRING)

    @_('TYPESTRING TIME STRING')  # TODO Google Docs
    def statement(self, p):
        return ("TYPESTRING", p.TIME, p.STRING)

    @_('TYPESTRING TIME NAME')
    def statement(self, p):
        return ("PYTHON", f"self.evaluate([(\"TYPESTRING\", \"{p.TIME}\", globals()[\"{p.NAME}\"]))")

    @_('SETUSERNAME STRING')
    def statement(self, p):
        return ("PYTHON", f"self.term.set_env('USER', \"{p.STRING}\")")

    @_('SETUSERNAME NAME')
    def statement(self, p):
        return ("PYTHON", f"self.term.set_env('USER', globals()[\"{p.NAME}\"])")

    @_('SETMACHINENAME STRING')
    def statement(self, p):
        return ("PYTHON", f"self.term.set_env('HOST', \"{p.STRING}\")")

    @_('SETMACHINENAME NAME')
    def statement(self, p):
        return("PYTHON", f"self.term.set_env('HOST', globals()[\"{p.NAME}\"])")

    @_('LOADSPRITE NAME STRING NUM NUM NUM NUM NUM NUM HEXCOLOR NUM NUM')
    def statement(self, p):
        return (
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
        )

    @_('GO POS NAME NUM SPEED')  # TOFIX
    def statement(self, p):
        return ("GO", p.POS, p.NAME, p.NUM, p.SPEED)

    @_('DIALOG STRING HEXCOLOR STRING BOOL')  # TODO
    def statement(self, p):
        return ("DIALOG", p.STRING0, p.HEXCOLOR, p.STRING1, p.BOOL)

    @_('WAIT END DIALOG THEN statement')  # DONE
    def statement(self, p):
        return ("PYTHON", f"self.end_dialog.append({p.statement})")

    @_('IF NAME EQ STRING THEN statement')
    def statement(self, p):
        return ("IF", p.NAME, p.STRING, p.statement)
