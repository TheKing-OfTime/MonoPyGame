import pygame
import random
import os
import sys

from classes.BaseClass import BaseClass


class Displayable(BaseClass):

    def __init__(self, scene, show=False):
        super().__init__(scene)
        self.asset = None
        self.core_asset = None
        self.pos = None
        self._show: bool = False
        self.pos = Position(scene, length=100, height=100)
        self._show = show
        self.animation_state = 'DEFAULT'
        self.animation_memory = {}

    def load_asset(self, asset_path):
        img = pygame.image.load(os.path.abspath(sys.argv[0]).replace('main.py', '') + asset_path)
        self.asset = self.core_asset = img
        self.pos.length = img.get_width()
        self.pos.height = img.get_height()

    # noinspection PyTypeChecker
    def draw(self):
        if not self._show:
            return
        if self.asset is None:
            pygame.draw.rect(self.scene, self.pos.color, self.pos.get_rect())
        else:
            self.scene.blit(self.asset, (self.pos.x, self.pos.y))
    def get_rect(self):
        return pygame.Rect(self.pos.get_rect())

    def show(self):
        self._show = True

    def hide(self):
        self._show = False

    def rescale_asset(self, width=None, height=None):
        if width is not None:
            self.pos.length = width
        if height is not None:
            self.pos.height = height

        self.asset = pygame.transform.smoothscale(self.core_asset, (self.pos.length, self.pos.height))
        return self.asset

    def rescale_asset_by(self, factor):
        if isinstance(factor, tuple):
            factor_l = factor[0]
            factor_h = factor[1]
        else:
            factor_l = factor_h = factor
        self.pos.length = self.pos.length * factor_l
        self.pos.height = self.pos.height * factor_h
        self.asset = pygame.transform.smoothscale_by(self.core_asset, factor)
        return self.asset


class Position(BaseClass):

    def __init__(self, scene, x=100, y=100, length=10, height=10):
        super().__init__(scene)
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.default_length = length
        self.default_height = height
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def get_rect(self):
        return self.x, self.y, self.length, self.height

    def move(self, x, y):
        self.x += x
        self.y += y

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def move_to_random(self):
        self.x = random.randint(50, round(self.scene.get_width() / 1.5))
        self.y = random.randint(50, round(self.scene.get_height() / 1.5))


class Animated(Displayable):

    def __init__(self, scene):
        super().__init__(scene)
        self.pos = Position(scene, length=20, height=20)
        self.assets = []
        self.core_assets = []
        self.frame = 0

    def load_asset(self, asset_dir_path):
        for asset in os.listdir(asset_dir_path):
            img = pygame.image.load(os.path.abspath(sys.argv[0]).replace('main.py', '') + asset_dir_path + '\\' + asset)
            if not asset.endswith('.png'):
                img = img.convert()
            self.assets.append(img)
            self.pos.length = img.get_width()
            self.pos.height = img.get_height()
            self.core_assets.append(img)

    def rescale_assets(self, width=None, height=None):
        new_assets = []
        if width is not None:
            self.pos.length = width
        if height is not None:
            self.pos.height = height
        for asset in self.core_assets:
            new_assets.append(pygame.transform.smoothscale(asset, (self.pos.length, self.pos.height)))
        self.assets = new_assets
        return self.assets


    def rescale_assets_by(self, factor):
        new_assets = []
        if isinstance(factor, tuple):
            factor_l = factor[0]
            factor_h = factor[1]
        else:
            factor_l = factor_h = factor
        self.pos.length = self.pos.length * factor_l
        self.pos.height = self.pos.height * factor_h
        for asset in self.core_assets:
            new_assets.append(pygame.transform.smoothscale_by(asset, factor))
        self.assets = new_assets
        return self.assets

    def draw(self, asset_number=None):
        if not self._show:
            return
        if asset_number is not None:
            self.frame = asset_number
        if self.assets:
            self.scene.blit(self.assets[self.frame], (self.pos.x, self.pos.y))

    def draw_next(self):
        if self.frame < len(self.assets) - 1:
            self.frame += 1
        else:
            self.frame = 0
        self.draw()


class DisplayableText(Displayable):

    def __init__(self, scene, text, color=(255, 255, 255), size=30, pos=(0, 0)):
        super().__init__(scene)
        self.text = text
        self.font = pygame.font.Font(os.path.abspath(sys.argv[0]).replace('main.py', '') + 'fonts/Myriad Pro/MyriadPro-Light.otf', size) #pygame.font.SysFont('Consolas', size)
        self.color = color
        self.surface = self.font.render(self.text, True, self.color)
        self.pos.length = self.pos.default_length = self.surface.get_width()
        self.pos.height = self.pos.default_height = self.surface.get_height()
        self.pos.x = pos[0]
        self.pos.y = pos[1]
        self._show = True

    def render(self):
        if self._show:
            self.scene.blit(self.surface, (self.pos.x, self.pos.y))

    def change_text(self, text):
        if text == self.text:
            return
        self.text = text
        self.surface = self.font.render(self.text, True, self.color)
        self.pos.length = self.pos.default_length = self.surface.get_width()
        self.pos.height = self.pos.default_height = self.surface.get_height()