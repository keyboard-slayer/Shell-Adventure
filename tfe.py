#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys


from typing import List
from game.game import launch_game


def launch(file: str):
    os.system(
            "cd game/ && PYTHONPATH=\"{}\""
            " python3 -O {}" .format(os.path.abspath("./"), os.path.abspath(f"./test/{file}")))


def dev_menu():
    print(f"""
*******************
*Fichier de tests *
*******************
{header}""")
    filename = input("Tappez le nom du fichier: ")
    launch(filename)


if __name__ == "__main__":
    if os.path.isdir("./text"):
        header = "\n".join([files for files in os.listdir("./test/")
                            if files != "__init__.py" and files.split('.')[-1] == "py"])

    if len(sys.argv) == 2 and sys.argv[1] == "--dev":
        dev_menu()
    elif len(sys.argv) == 3 and sys.argv[1] == "--dev":
        launch(sys.argv[2])
    else:
        launch_game()
