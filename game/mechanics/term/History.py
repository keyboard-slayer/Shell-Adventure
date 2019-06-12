#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


class History:
    def __init__(self, path: str):
        self.path = os.path.join(path, ".bash_history")
        if not os.path.isfile(self.path):
            open(self.path, 'w').close()
        self.cursor = self.get_size()

    def append(self, line: str):
        with open(self.path, 'a') as hist:
            hist.write(f"{line}\n")

    def __getitem__(self, index: int) -> str:
        with open(self.path, 'r') as hist:
            self.line = hist.readlines()
            self.line = [line for line in self.line if line[:-1]]
            print(self.line, index, self.line[index])
            return self.line[index][:-1]

    def get_size(self) -> int:
        with open(self.path, 'r') as hist:
            return len([line[:-1] for line in hist.readlines() if line[:-1]])

    def get_previous(self) -> str:
        if self.cursor > -1:
            self.cursor -= 1
            return self.__getitem__(self.cursor)

    def get_next(self) -> str:
        if self.cursor < self.get_size()-1:
            self.cursor += 1
            return self.__getitem__(self.cursor)
        else:
            return ""
