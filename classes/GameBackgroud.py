import pygame
from classes.Displayable import Displayable, Position


class GameBackground(Displayable):

	def __init__(self, scene):
		super().__init__(scene)
		self.load_asset()
