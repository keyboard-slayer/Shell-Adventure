#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

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
            command = "ls -F" if command == "ls" else command
            out = subprocess.Popen(filter(None, command.split(' ')),\
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

            output = out[1].decode("utf-8") if out[1] else out[0].decode("utf-8")

            for line in output.split('\n')[:-1]:
                term.add_to_display(line)
