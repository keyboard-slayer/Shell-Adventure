#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import os

from game.script.Interpreter import Interpreter
from game.mechanics.term.Term import Term

if __name__ == "__main__":
    pygame.init()
    os.chdir("../")
    term = Term("test-user", "localhost", (800, 800))
    inter = Interpreter(term)
    while True:
        code = input("> ")
        inter.evaluate(code)