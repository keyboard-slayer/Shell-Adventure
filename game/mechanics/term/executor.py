#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def execute(cmd: str, term):
    commands = cmd.split(' && ')
    print(commands)
    for command in commands:
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
