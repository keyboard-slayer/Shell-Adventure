#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sly import Parser

from game.script.Lexer import SAdvLexer

class SAdvParser(Parser):
    tokens = SAdvLexer.tokens

    def __init__(self):
        self.env = {}
        self.func = ""

    @_('', 'COMMENT')
    def statement(self, p):
        pass 
    
    @_('SAY STRING')
    def statement(self, p):
        return ('PYTHON', f'self.term.add_to_display(\"{p.STRING}\")')

    @_('OBJECTIF STRING')
    def statement(self, p):
        return ('PYTHON', f'self.quest.add(\"{p.STRING}\")')

    @_('WAIT FILE STRING THEN statement')
    def statement(self, p):
        return ('WAIT', 'FILE', p.STRING, p.statement)
    
    @_('WAIT DIR STRING THEN statement')
    def statement(self, p):
        return ('WAIT', 'DIR', p.STRING, p.statement)

    @_('EXIT')
    def statement(self, p):
        return ('PYTHON', 'exit()')

    @_('RUN STRING')
    def statement(self, p):
        return ("PYTHON", f'self.term.exec_sh(\"{p.STRING}\")') # TODO
    
    @_('EXEC STRING')
    def statement(self, p):
        return ("PYTHON", f'self.term.exec(\"{p.STRING}\")') # TODO

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

    @_('END')
    def statement(self, p):
        if not self.func:
            raise SyntaxError()
        else:
            self.func = ""