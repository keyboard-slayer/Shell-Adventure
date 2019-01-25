#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sly import Lexer

class SAdvLexer(Lexer):
    tokens = {
        COMMENT,
        SAY,
        OBJECTIF,
        WAIT,
        FILE,
        DIR,
        THEN,
        STRING,
        EXEC,
        RUN,
        EXIT,
        FUN,
        NAME,
        END,
        TAB,
        SPACE,
        CALL,
        DONE,
        TIME,
        DELFILE,
        DELDIR,
        IFEXIST,
        DISABLE,
        GAMEPART,
        SETPOS,
        SETSIZE,
        NUM,
        LOOP, 
        TIMES,
        LOADPATH,
        READFILE,
        TYPEFILE
    }

    ignore = '\n'

    TYPEFILE = r'(?i)TYPEFILE'
    READFILE = r'(?i)READFILE'
    LOADPATH = r'(?i)LOADPATH'
    GAMEPART = r'(?i)(TERM|QUEST|RPG)'
    DISABLE = r'(?i)DISABLE'
    SAY = r'(?i)SAY'
    DONE = r'(?i)DONE'
    OBJECTIF = r'(?i)OBJECTIF'
    WAIT = r'(?i)WAIT'
    RUN = r'(?i)RUN'
    FILE = r'(?i)FILE'
    DIR = r'(?i)DIR'
    THEN = r'(?i)THEN'
    EXIT = r'(?i)EXIT'
    EXEC = r'(?i)EXEC'
    FUN = r'(?i)FUN'
    END = r'(?i)END'
    CALL = r'(?i)CALL'
    DELFILE = r'(?i)DELFILE'
    DELDIR = r'(?i)DELDIR'
    IFEXIST = r'(?i)IFEXIST'
    SETPOS = r'(?i)SETPOS'
    SETSIZE = r'(?i)SETSIZE'
    LOOP = r'(?i)LOOP'
    TIMES = r'(?i)TIME'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    TAB = r'\t'
    TIME = r'[+-]?([0-9]*[.])?[0-9]+s'
    NUM = r'\d{1,10}'
    SPACE = r'    '


    ignore_newline = r'\n'

    @_(r';.*')
    def COMMENT(self, t):
        pass

    @_(r'("([^"]|"")*")')
    def STRING(self, t):
        t.value = t.value.replace('\"', '')
        return t

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        self.index += 1
