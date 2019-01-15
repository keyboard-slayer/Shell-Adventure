#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sly import Lexer

class SAdvLexer(Lexer):
    tokens = {
        COMMENT, 
        BEGIN, 
        SAY,
        OBJECTIF,
        WAIT,
        FILE,
        DIR,
        THEN,
        STRING,
        EXEC,
        END
    }

    ignore = ' \t'

    BEGIN = r'(?i)BEGIN'
    EXEC = r'(?i)EXEC'
    SAY = r'(?i)SAY'
    OBEJCTIF = r'(?i)OBEJCTIF'
    WAIT = r'(?i)WAIT'
    FILE = r'(?i)FILE'
    DIR = r'(?i)DIR'
    THEN = r'(?i)THEN'

    @_(r';.*')
    def COMMENT(self, t):
        pass

    @_(r'("([^"]|"")*")')
    def STRING(self, t):
        t.value = t.value.replace('\"', '')
        return t 


