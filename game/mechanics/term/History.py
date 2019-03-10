#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

class History:
    def __init__(self, home: str):
        self.home = home
        if not os.path.isfile(os.path.join(self.home, ".bash_history")):
            open(os.path.join(self.home, ".bash_history"), 'w').close()
        self.hist = None

    def __del__(self):
        try:
            self.hist.close()
        except AttributeError:
            pass 
    def __getitem__(self, index: int) -> str:
        self.openFile()
        return self.hist.readlines()[index][:-1]

    def append(self, line: str):
        self.openFile()
        self.hist.write(f"{line}\n")
        self.hist.close()


    def openFile(self):
        self.hist = open(os.path.join(self.home, ".bash_history"), 'a+')
