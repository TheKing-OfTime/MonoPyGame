import pygame
import numpy as np
from classes.Displayable import Displayable, Position


class GameBackground(Displayable):

	width = 700
	height = 700

	def __init__(self, scene):
		super().__init__(scene)
		self.load_asset('assets/Board/monopolyFirst.jpg')
		self.show()
		self.asset = pygame.transform.smoothscale(self.asset, (self.width, self.height))
		self.update_pos()

	def update_pos(self):
		old_pos = np.array([self.pos.x, self.pos.y])
		self.pos.x = (self.scene.get_width() / 2) - (self.width / 2)
		self.pos.y = (self.scene.get_height() / 2) - (self.height / 2)
		return np.array([self.pos.x, self.pos.y]) - old_pos
