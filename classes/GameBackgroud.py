import pygame, os, sys
import numpy as np
from classes.Displayable import Displayable


class GameBackground(Displayable):

	width = 700
	height = 700

	def __init__(self, scene):
		super().__init__(scene)
		self.load_asset('assets/Board/monopolyFirst_logo.png')
		self.convert_asset()
		self.show()
		self.asset = pygame.transform.smoothscale(pygame.transform.rotate(self.asset, 90), (self.width, self.height))
		self.pos.length = self.width
		self.pos.height = self.height
		self.update_pos()

	def update_pos(self):
		old_pos = np.array([self.pos.x, self.pos.y])
		self.pos.x = (self.scene.get_width() / 2) - (self.width / 2)
		self.pos.y = (self.scene.get_height() / 2) - (self.height / 2)
		return np.array([self.pos.x, self.pos.y]) - old_pos

	def draw(self):
		self.scene.blit(self.asset, (self.pos.x, self.pos.y))
