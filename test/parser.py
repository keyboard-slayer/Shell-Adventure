#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Used 
# https://github.com/dabeaz/sly
# https://stackoverflow.com/questions/500864/case-insensitive-python-regular-expression-without-re-compile

from game.script.Lexer import SAdvLexer as Lexer
from game.script.Parser import SAdvParser as Parser
# from game.script.Executer import SAdvExec as Executer 

if __name__ == "__main__":
    lexer = Lexer()

    while True:
        text = input("> ")
        lex = Lexer()
        parser = Parser()
        tree = parser.parse(lexer.tokenize(text))
        print(tree)
        