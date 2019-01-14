#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

# from game.mechanics.term.Nano import Nano

def execute(cmd: str, term):
    commands = cmd.split(' && ')
    homepath = term.getenv()["HOME"]
    os.chdir(homepath)
    for command in commands:
        if not command.replace(' ', ''):
            return 0

        if command == "exit":
            exit()
            return 0

        elif command == "history":
            with open(os.path.join(homepath, '.bash_history'), 'r') as history:
                for index, line in enumerate(history.readlines()):
                    term.add_to_display(f"{index+1: 4}  {line[:-1]}")

        elif command == "clear":
            term.clear()
            return 0

        elif command == "philosophy":
            execute("python -m this", term)
            return 0

        elif command == "sayHi":
            art = f"""
     ____{(len({term.getenv()["USER"]})*9)*'_'}
    < Hi {term.getenv()["USER"]} >
     ------{(len({term.getenv()["USER"]})*8)*'-'}
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\\
                    ||----w |
                    ||     ||
    """
            for line in art.split('\n'):
                term.add_to_display(line)
            return 0

        else:
            cmdWArg = command.split(' ')

            if cmdWArg[0] == "nano":
                term.add_to_display("Pas encore dispo")
                return 0
            elif cmdWArg[0] == "cd":
                pwd = term.getenv()["PWD"].split('/')
                directory = cmdWArg[1].split('/')
                if not directory[0]:
                    term.add_to_display("Le chemain absolu sont interdit :p")
                    return 1

                for dir in directory:
                    if dir == "..":
                        pwd = pwd[:-1]
                    elif dir == ".":
                        continue
                    else:
                        pwd.append(dir)

                pwd = '/'.join(pwd) + '/'
                if not pwd[:len(term.getenv()["HOME"])] == term.getenv()["HOME"]:
                    term.add_to_display("Tu ne peux pas quitter le bac à sable")
                    return 1

                elif not os.path.isdir(pwd):
                    term.add_to_display(f"bash: cd: {pwd}: Aucun fichier ou dossier de ce type")
                    return 1

                term.setenv("PWD", pwd)


            else:
                command = "ls -F" if command == "ls" else command
                try:
                    out = subprocess.Popen(filter(None, cmdWArg),\
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

                    output = out[1].decode("utf-8") if out[1] else out[0].decode("utf-8")

                except FileNotFoundError:
                    term.add_to_display(f"{cmdWArg[0]}: commande introuvable")
                    return 1


                for line in output.split('\n')[:-1]: 
                    term.add_to_display(line)
                return 0
