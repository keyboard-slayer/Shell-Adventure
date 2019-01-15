#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sly import Parser

from game.script.Lexer import SAdvLexer

class SAdvParser(Parser):
    tokens = SAdvLexer.tokens

    def __init__(self):
        self.env = {}

    @_('', 'COMMENT')
    def statement(self, p):
        pass 
    
    @_('SAY STRING')
    def statement(self, p):
        return ('PYTHON', f'term.add_to_display({p.STRING})')

    @_('OBJECTIF STRING')
    def statement(self, p):
        return ('PYTHON', f'quest.add({p.STRING})')

    @_('WAIT FILE STRING THEN statement')
    def statement(self, p):
        return ('WAIT', 'FILE', p.STRING, p.statement)
    
    @_('WAIT DIR STRING THEN statement')
    def statement(self, p):
        return ('WAIT', 'DIR', p.STRING, p.statement)

    
    @_('BEGIN')
    def statement(self, p):
        return ('START')

    @_('END')
    def statement(self, p):
        return ('END')

    @_('EXEC STRING')
    def statement(self, p):
        return ('exec', p.STRING)