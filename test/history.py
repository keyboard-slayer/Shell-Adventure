#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from game.mechanics.term.History import History

if __name__ == "__main__":
    os.mkdir(os.path.join(os.getcwd(), "../test/historyTesting/"))
    history = History(os.path.join(os.getcwd(), "../test/historyTesting/"))
    for nbr in range(11):
        history.append(str(nbr))

    for line in range(10, 0, -1):
        print(history[line])

    os.system(f"rm -rf {os.path.join(os.getcwd(), "../test/historyTesting/")}")
