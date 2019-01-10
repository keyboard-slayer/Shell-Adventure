#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys


def launch(file: str):
    os.system(
            "/bin/bash -c 'chmod +x venv/bin/* && source venv/bin/activate && cd game/ && PYTHONPATH=\"{}\"" \
            " python3 -O {}'" .format(os.path.abspath("./"), os.path.abspath(f"./test/{file}")))


if __name__ == "__main__":
    header = "\n".join([files for files in os.listdir("./test/") \
                        if files != "__init__.py" and files.split('.')[-1] == "py"])

    if len(sys.argv) == 2 and sys.argv[1] == "--dev":
        print(f"""
*******************
*Fichier de tests *
*******************
{header}""")
        filename = input("Tappez le nom du fichier: ")
        launch(filename)

    elif len(sys.argv) == 3 and sys.argv[1] == "--dev":
        launch(sys.argv[2])
