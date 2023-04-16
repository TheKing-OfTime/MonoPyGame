import pygame
from classes.Displayable import Displayable, Position


class GameBackground(Displayable):

	width = 700
	height = 700

	def __init__(self, scene):
		super().__init__(scene)
		self.load_asset('assets/Board/monopolyFirst.jpg')
		self.show()
		self.asset = pygame.transform.scale(self.asset, (self.width, self.height))
		self.pos.x = (self.scene.get_width()/2) - (self.width/2)
		self.pos.y = (self.scene.get_height()/2) - (self.height/2)
