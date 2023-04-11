import pygame
from classes.BaseClass import BaseClass
from classes.Displayable import Displayable, Animated
from classes.GameBackgroud import GameBackground

class Game(BaseClass):

	GAME_STATES = [
		"LOADING"
		"PAUSED"
		"DEFAULT"
		"MAIN_MENU"
		"CONNECTING"
	]
	def __init__(self, scene):
		super().__init__(scene)
		self.done = False
		self.game_state = "LOADING"
		self.test_displayable = Animated(scene)
		self.bg = GameBackground(scene)
		self.test_displayable.load_asset('assets/tiles/green_1')
		self.game_state = "DEFAULT"


	def run_loop(self):
		while not self.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True
			self.bg.draw()
			self.test_displayable.draw()
			self.test_displayable.pos.move_to(100, 100)
			if not self.test_displayable._show:
				self.test_displayable.show()
			pygame.display.flip()
			pygame.time.wait(10)
			self.scene.fill(color=[0, 0, 0])

