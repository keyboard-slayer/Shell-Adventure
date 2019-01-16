#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import os

from game.script.Interpreter import Interpreter
from game.mechanics.term.Term import Term

if __name__ == "__main__":
    pygame.init()
    fichier = open("essais.adv", 'r')
    os.chdir("../")
    term = Term("test-user", "localhost", (800, 800))
    inter = Interpreter(term)
    

    for line in fichier.readlines():
        inter.evaluate(line)
        a = inter.get_tree()
        if a is not None:
            print(f"OUTPUT {a}")