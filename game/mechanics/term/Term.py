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

from game.mechanics.term.executor import execute_and_out
from game.mechanics.term.History import History



class Term:
    def __init__(self, username: str, host: str, size: Tuple[int, int]):
        self.surface = pygame.Surface(size)
        self.mono = pygame.font.Font("font/monospace.ttf", 22)
        self.visualLine = []
        self.lineRect = None
        self.blinkRect = None
        self.sessionHistory = []
        self.currentTyping = ""
        self.blinkX = 0

        if not os.path.isdir(os.path.join(os.environ["HOME"], ".shelladv")):
            os.mkdir(os.path.join(os.environ["HOME"], ".shelladv"))

        if not os.path.isdir(
            os.path.join(
                os.path.join(os.environ["HOME"], ".shelladv"),
            username)
        ):

            os.mkdir(
                os.path.join(
                    os.path.join(os.environ["HOME"], ".shelladv"),
                username)
            )

        self.history = History(
            os.path.join(
                os.path.join(os.environ["HOME"], ".shelladv"),
            username)
        )


        self.env = {
            "HOME": os.path.join(os.path.join(os.environ["HOME"], ".shelladv"), username),
            "PWD": os.path.join(os.path.join(os.environ["HOME"], ".shelladv"), username),
            "USER": username,
            "HOST": host
        }
        
        os.chdir(self.env["HOME"])
        self.tick = time.time()
        self.updatePrompt()

    def updatePrompt(self):
        if self.env["PWD"][:len(self.env["HOME"])] == self.env["HOME"]:
            path = f"~{self.env['PWD'].split(self.env['HOME'])[1]}"
        else:
            path = self.env["PWD"]

        self.prompt = f"{self.env['USER']}@{self.env['HOST']} {path}: $"

    def add_to_display(self, output: str):
        self.visualLine.append((self.prompt, f">{output}"))

    def clear(self):
        self.visualLine = []

    def getenv(self) -> Dict[str, str]:
        return self.env

    def setenv(self, var, value):
        self.env[var] = value
        self.blinkX = 0

    def draw(self):
        for lineIndex, line in enumerate(self.visualLine):
            toshow = line[1][1:] if len(line[1]) > 1 and line[1][0] == '>' else f"{line[0]} {line[1]}"
            
            self.surface.blit(
                self.mono.render(
                    toshow,
                    True,
                    (255, 255, 255)
                ),
                (0, lineIndex * 22)
            )

        self.lineRect = self.surface.blit(
            self.mono.render(
                f"{self.prompt} {self.currentTyping}",
                True,
                (255, 255, 255)
            ),
            (0, len(self.visualLine) * 22)
        )

    def keydown(self, keycode: int):
        keyName = pygame.key.name(keycode)

        if keyName == "<" \
            and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.currentTyping += '>'

        elif keyName == "&" and pygame.key.get_mods() & pygame.KMOD_MODE:
            self.currentTyping += '|'

        elif keyName == "[.]" or keyName == ';'\
            and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.currentTyping += '.'

        elif keyName == "[/]" or keyName == ':'\
            and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.currentTyping += '/'

        elif keyName == "-" and pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.currentTyping += '_'


        elif keyName == "[-]":
            self.currentTyping += '-'

        elif keyName == "backspace":
            self.currentTyping = self.currentTyping[:-1]
            self.blinkX = 0

        elif keyName == "return":
            self.visualLine.append((self.prompt, self.currentTyping))
            self.history.append(self.currentTyping)
            execute_and_out(self.currentTyping, self)
            self.currentTyping = ""
            self.blinkX = 0

        elif keyName == "space":
            self.currentTyping += ' '

        elif keyName == "c" and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.visualLine.append((self.prompt, self.currentTyping+"^C"))
            self.currentTyping = ""
            self.blinkX = 0

        elif keyName in ascii_lowercase and pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.currentTyping += keyName.upper()

        elif keyName in ascii_lowercase or keyName in ['&', '-', '=', '$', ';', '<', '\'', '\"', '(', ')', '!']:
            self.currentTyping += keyName

    def drawBlink(self):
        self.blinkRect = pygame.draw.rect(
            self.surface,
            (255, 255, 255),
            (self.blinkX,
                2 + len(self.visualLine) * 22,
                12,
                20)
        )

    def update(self):
        self.surface.fill((0, 0, 0))
        self.draw()
        self.updatePrompt()
        if 0.3 < time.time() - self.tick < 0.8:
            self.drawBlink()
            while self.blinkRect is None or \
                self.lineRect.colliderect(self.blinkRect):

                self.drawBlink()
                self.blinkX += 1
                done = True
        if time.time() - self.tick > 0.8:
            self.tick = time.time()

    def get_surface(self) -> pygame.Surface:
        self.update()
        return self.surface
