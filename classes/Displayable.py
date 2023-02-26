import pygame
import random
from classes.BaseClass import BaseClass


class Displayable(BaseClass):
	asset = None
	pos = None

	def __init__(self, scene):
		super().__init__(scene)
		self.pos = Position(scene, length=10, height=10)

	def load_asset(self, asset_path):
		self.asset = pygame.image.load(asset_path)

	# noinspection PyTypeChecker
	def draw(self):
		if self.asset is None:
			pygame.draw.rect(self.scene, self.pos.color, self.pos.get_rect())
		else:
			self.scene.blit(self.asset, (self.pos.x, self.pos.y))


class Position(BaseClass):
	x = 0
	y = 0
	length = 0
	height = 0

	def __init__(self, scene, x=100, y=100, length=1, height=1):
		super().__init__(scene)
		self.x = x
		self.y = y
		self.length = length
		self.height = height
		self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

	def get_rect(self):
		return ((self.x - (self.length / 2)), (self.y - (self.height / 2)), (self.x + (self.length / 2)),
				(self.y + (self.height / 2)))
