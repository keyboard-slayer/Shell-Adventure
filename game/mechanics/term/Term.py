#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import pygame

from typing import (
    Tuple,
    Dict
)
from string import ascii_lowercase
from game.mechanics.term.executor import execute


class Term:
    def __init__(self, username: str, host: str, size: Tuple[int, int]):
        self.surface = pygame.Surface(size)
        self.mono = pygame.font.Font("font/monospace.ttf", 22)
        self.visualLine = []
        self.currentTyping = ""

        if not os.path.isdir(os.path.join(os.environ["HOME"], ".shelladv")):
            os.mkdir(os.path.join(os.environ["HOME"], ".shelladv"))
        if not os.path.isdir(os.path.join(os.path.join(os.environ["HOME"], ".shelladv"), username)):
            os.mkdir(os.path.join(os.path.join(os.environ["HOME"], ".shelladv"), username))

        self.env = {
            "HOME": os.path.join(os.path.join(os.environ["HOME"], ".shelladv"), username),
            "PWD": os.path.join(os.path.join(os.environ["HOME"], ".shelladv"), username),
            "USER": username,
            "HOST": host
        }

        if self.env["PWD"][:len(self.env["HOME"])] == self.env["HOME"]:
            path = f"~{self.env['PWD'].split(self.env['HOME'])[1]}"
        else:
            path = self.env["PWD"]

        self.prompt = f"{self.env['USER']}@{self.env['HOST']} {path}: $"
        self.tick = time.time()

    def add_to_display(self, output: str):
        self.visualLine.append(f">{output}")

    def clear(self):
        self.visualLine = []

    def getenv(self) -> Dict[str, str]:
        return self.env

    def draw(self):
        for lineIndex, line in enumerate(self.visualLine):
            toshow = f"{self.prompt} {line}" if line[0] != '>' else line[1:]
            self.surface.blit(
                self.mono.render(
                    toshow,
                    True,
                    (255, 255, 255)
                ),
                (0, lineIndex * 22)
            )

        self.surface.blit(
            self.mono.render(
                f"{self.prompt} {self.currentTyping}",
                True,
                (255, 255, 255)
            ),
            (0, len(self.visualLine) * 22)
        )

    def keydown(self, keycode: int):
        keyName = pygame.key.name(keycode)
        print(keyName)

        if keyName == "backspace":
            self.currentTyping = self.currentTyping[:-1]

        if keyName == "return":
            self.visualLine.append(self.currentTyping)
            execute(self.currentTyping, self)
            self.currentTyping = ""

        if keyName == "space":
            self.currentTyping += ' '

        if keyName == "c" and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.visualLine.append(self.currentTyping)
            self.visualLine.append("^C")
            self.currentTyping = ""

        elif keyName in ascii_lowercase and pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.currentTyping += keyName.upper()

        elif keyName in ascii_lowercase or keyName in ['&']:
            self.currentTyping += keyName

    def update(self):
        self.surface.fill((0, 0, 0))

        if 0.3 < time.time() - self.tick < 0.8:
            pygame.draw.rect(
                self.surface,
                (255, 255, 255),
                ((len(self.prompt) + len(self.currentTyping)) * 11.5,
                    2 + len(self.visualLine) * 22,
                    12,
                    20)
            )
        if time.time() - self.tick > 0.8:
            self.tick = time.time()

        self.draw()

    def get_surface(self) -> pygame.Surface:
        self.update()
        return self.surface






