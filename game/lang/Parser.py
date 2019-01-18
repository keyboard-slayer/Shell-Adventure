#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sly import Parser

from game.lang.Lexer import SAdvLexer

class SAdvParser(Parser):
    tokens = SAdvLexer.tokens

    def __init__(self):
        self.env = {}
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
        if p.NAME in self.obj:
            return [('PYTHON', f'self.quest.done(\"{p.NAME}\")')]
        else:
            raise NameError(f"{p.NAME} is not declared")

    @_('WAIT FILE STRING THEN statement')
    def statement(self, p):
        return [('WAIT', 'FILE', p.STRING, p.statement)]

    @_('WAIT DIR STRING THEN statement')
    def statement(self, p):
        return [('WAIT', 'DIR', p.STRING, p.statement)]


    @_('WAIT TIME THEN statement')
    def statement(self, p):
        return [('WAIT', p.TIME, p.statement)]

    @_('EXIT')
    def statement(self, p):
        return [('PYTHON', 'exit()')]

    @_('RUN STRING')
    def statement(self, p):
        return [("PYTHON", f'execute_and_out(\"{p.STRING}\", self.term)')]

    @_('EXEC STRING')
    def statement(self, p):
        return [("PYTHON", f'file_and_out(\"{p.STRING}\", self.term)')]

    @_('FUN NAME')
    def statement(self, p):
        self.env[p.NAME] = []
        self.func = p.NAME

    @_('CALL NAME')
    def statement(self, p):
        return self.env[p.NAME]

    @_('TAB statement')
    def statement(self, p):
        if not self.func:
           raise IndentationError("unexpected indent")
        else:
            self.env[self.func].append(p.statement)

    @_('SPACE statement')
    def statement(self, p):
        if not self.func:
           raise IndentationError("unexpected indent")
        else:
            if p.statement is not None:
                self.env[self.func].append(p.statement)

    @_('END FUN')
    def statement(self, p):
        if not self.func:
            raise SyntaxError()
        else:
            self.func = ""
