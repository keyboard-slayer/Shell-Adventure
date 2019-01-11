#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

# from game.mechanics.term.Nano import Nano

def execute(cmd: str, term):
    commands = cmd.split(' && ')
    os.chdir(term.getenv()["HOME"])
    for command in commands:
        if not command.replace(' ', ''):
            return 0

        if command == "exit":
            exit()

        elif command == "clear":
            term.clear()

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

        else:
            cmdWArg = command.split(' ')

            if cmdWArg[0] == "nano":
                term.add_to_display("Pas encore dispo")
            elif cmdWArg[0] == "cd":
                pwd = term.getenv()["PWD"].split('/')
                directory = cmdWArg[1].split('/')
                if not directory[0]:
                    term.add_to_display("Le chemain absolu sont interdit :p")

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

                elif not os.path.isdir(pwd):
                    term.add_to_display(f"bash: cd: {pwd}: Aucun fichier ou dossier de ce type")

                term.setenv("PWD", pwd)




            else:
                command = "ls -F" if command == "ls" else command
                out = subprocess.Popen(filter(None, cmdWArg),\
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

                output = out[1].decode("utf-8") if out[1] else out[0].decode("utf-8")

                for line in output.split('\n')[:-1]:
                    term.add_to_display(line)
