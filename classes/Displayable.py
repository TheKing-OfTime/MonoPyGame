import pygame
import random
import os
import sys
from classes.BaseClass import BaseClass


class Displayable(BaseClass):
	asset = None
	pos = None
	_show: bool = False

	def __init__(self, scene, show=False):
		super().__init__(scene)
		self.pos = Position(scene, length=100, height=100)
		self._show = show

	def load_asset(self, asset_path):
		self.asset = pygame.image.load(os.path.abspath(sys.argv[0]).replace('main.py', '') + asset_path)

	# noinspection PyTypeChecker
	def draw(self):
		if not self._show:
			return
		if self.asset is None:
			pygame.draw.rect(self.scene, self.pos.color, self.pos.get_rect())
		else:
			self.scene.blit(self.asset, (self.pos.x, self.pos.y))

	def show(self):
		self._show = True

	def hide(self):
		self._show = False


class Position(BaseClass):
	x = 0
	y = 0
	length = 0
	height = 0

	def __init__(self, scene, x=100, y=100, length=10, height=10):
		super().__init__(scene)
		self.x = x
		self.y = y
		self.length = length
		self.height = height
		self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

	def get_rect(self):
		print(self.x, self.y, self.length, self.height)
		return self.x, self.y, self.length, self.height

	def move(self, x, y):
		self.x += x
		self.y += y

	def move_to(self, x, y):
		self.x = x
		self.y = y


class Animated(Displayable):
	assets = []
	frame = 0

	def __init__(self, scene):
		super().__init__(scene)
		self.pos = Position(scene, length=20, height=20)

	def load_asset(self, asset_dir_path):
		for asset in os.listdir(asset_dir_path):
			self.assets.append(
				pygame.image.load(os.path.abspath(sys.argv[0]).replace('main.py', '') + asset_dir_path + '/' + asset)
			)

	def draw(self, asset_number=None):
		if asset_number is not None:
			self.frame = asset_number
		if self.assets is None:
			pygame.draw.rect(self.scene, self.pos.color, self.pos.get_rect())
		else:
			self.scene.blit(self.assets[self.frame], (self.pos.x, self.pos.y))

	def draw_next(self):
		if self.frame < len(self.assets) - 1:
			self.frame += 1
		else:
			self.frame = 0
		print(self.frame)
		self.draw()
