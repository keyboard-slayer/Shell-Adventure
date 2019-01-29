#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess


def execute(cmd: str, term: object) -> str:
    commands = cmd.split(' && ')
    homepath = term.get_env()["HOME"]

    for command in commands:
        if not command.replace(' ', ''):
            return ""

        if command == "exit":
            exit()

        elif command == "ls":
            return execute("ls -F", term)

        elif command == "history":
            with open(os.path.join(homepath, '.bash_history'), 'r') as history:
                output = ""
                for index, line in enumerate(history.readlines()):
                    output += f"{index+1: 4}  {line[:-1]}\n"
                return output

        elif command == "clear":
            term.clear()
            return ""

        elif command == "pwd":
            return f"~{term.get_env()['PWD'].split(term.get_env()['HOME'])[-1]}"

        elif command == "philosophy":
            return execute("python -m this", term)

        elif command == "sayHi":
            return f"""
     ____{(len({term.get_env()["USER"]})*9)*'_'}
    < Hi {term.get_env()["USER"]} >
     ------{(len({term.get_env()["USER"]})*8)*'-'}
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\\
                    ||----w |
                    ||     ||
    """

        else:
            cmdWArg = command.split(' ')

            if cmdWArg[0] == "nano":
                return "Pas encore dispo"

            elif cmdWArg[0] == "cd":
                pwd = term.get_env()["PWD"].split('/')
                directory = cmdWArg[1].split('/')
                if not directory[0]:
                    return "Le chemain absolu sont interdit :p"

                for dir in directory:
                    if dir == "..":
                        pwd = pwd[:-1]
                    elif dir == ".":
                        continue
                    else:
                        pwd.append(dir)


                pwd = '/'.join(pwd)

                if not pwd[:len(term.get_env()["HOME"])] == term.get_env()["HOME"]:
                    return "Tu ne peux pas quitter le bac à sable"

                elif not os.path.isdir(pwd):
                    return f"bash: cd: ~{pwd.split(term.get_env()['HOME'])[-1]}: Aucun fichier ou dossier de ce type"

                term.setenv("PWD", pwd)
                os.chdir(pwd)

            else:
                try:
                    out = subprocess.Popen(filter(None, cmdWArg),\
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

                    output = out[1].decode("utf-8") if out[1] else out[0].decode("utf-8")

                except FileNotFoundError as e:
                    return f"{cmdWArg[0]}: commande introuvable"

                return output


def execute_and_out(cmd: str, term: object):
    result = execute(cmd, term)

    if result:
        for out in [word for word in result.split('\n') if word]:
            term.add_to_display(out)

def file_and_out(filename: str, term:object):
    with open(filename, 'r') as bash:
        writeBuffer = []
        cat = False
        eof = False
        for line in bash.readlines():
            print(f"eof: {eof} cat: {cat}")
            print(line.encode("utf-8"))
            eof = line == "EOF"
        
            if line[:-1] == "cat << EOF" and not cat:
                cat = True 
                continue

            if not cat:
                execute_and_out(line, term)
            elif not eof and cat:
                writeBuffer.append(line)
            if eof and cat:
                cat = False 
                eof = False 
                print(True)
                for towrite in writeBuffer:
                    execute_and_out(f"echo {towrite}", term)
                writeBuffer = []

