import pygame
import numpy as np

from classes.BaseClass import BaseClass
from classes.Displayable import DisplayableText, Displayable

class HUD(BaseClass):

	HUD_states = [
        "LOADING"
        "PAUSED"
        "DEFAULT"
        "MAIN_MENU"
        "CONNECTING"
    ]

	def __init__(self, scene):
		super().__init__(scene)
		self.state = "DEFAULT"
		self.player_cards = []
		self.buttons = []
		self.play_button = None
		self.pc_2 = None
		self.pc_3 = None
		self.pc_4 = None

	def init_p_cards(self, players):
		i = 0
		for player in players:
			self.player_cards.append(PlayerCard(self.scene, i))
			i+=1

	def init_main_menu_buttons(self):
		self.play_button = Button(self.scene, 'play', 'assets/pieces/dices/Dices_1.png', 'Play', (200, 100, 10))
		self.play_button.icon.show()

		self.pc_2 = Button(self.scene, 'radio_pc_2', 'assets/pieces/dices/Dices_2.png', gab=(60, 60, 10))
		self.pc_2.icon.show()

		self.pc_3 = Button(self.scene, 'radio_pc_3', 'assets/pieces/dices/Dices_3.png', gab=(60, 60, 10))
		self.pc_3.icon.show()

		self.pc_4 = Button(self.scene, 'radio_pc_4', 'assets/pieces/dices/Dices_4.png', gab=(60, 60, 10))
		self.pc_4.icon.show()

		self.repos("MAIN_MENU")
		self.buttons.append(self.play_button)
		self.buttons.append(self.pc_2)
		self.buttons.append(self.pc_3)
		self.buttons.append(self.pc_4)



	def render(self, state="DEFAULT", player=None, players=None):

		if state == "DEFAULT":
			for player_card in self.player_cards:
				player_card.render(players[player_card.pid], player)

		elif state == "LOADING":
			self.show_loading()

		elif state == "MAIN_MENU":
			self.play_button.render()
			self.pc_2.render()
			self.pc_3.render()
			self.pc_4.render()

	def show_loading(self):
		self.scene.fill(color=[50, 50, 50])
		loading_text = DisplayableText(self.scene, 'Loading...', size=60)
		loading_text.pos.move_to(
			(self.scene.get_width() - loading_text.pos.length) / 2,
			(self.scene.get_height() - loading_text.pos.height) / 2
		)
		loading_text.show()
		loading_text.render()
		pygame.display.flip()

	def repos(self, state="DEFAULT"):
		if state == "MAIN_MENU":
			self.play_button.pos.x = (self.scene.get_width() / 2) - (self.play_button.pos.length / 2)
			self.play_button.pos.y = (self.scene.get_height() / 2) - (self.play_button.pos.height / 2)
			self.play_button.repos()

			pc_row_y = self.play_button.pos.y + self.play_button.pos.height + 10

			self.pc_2.pos.move_to(self.play_button.pos.x, pc_row_y)
			self.pc_2.repos()
			self.pc_3.pos.move_to(self.pc_2.pos.x + self.pc_2.pos.length + 10, pc_row_y)
			self.pc_3.repos()
			self.pc_4.pos.move_to(self.pc_3.pos.x + self.pc_2.pos.length + 10, pc_row_y)
			self.pc_4.repos()

class UIElement(Displayable):

	def __init__(self, scene):
		super().__init__(scene)
		self.colour = (204, 227, 198)
		self.border_radius = 0
		self.highlighted = False
		self.darkened = False

	def render_highlighted(self):
		if self.highlighted:
			pygame.draw.rect(self.scene, (255, 255, 255),
							 (self.pos.x - 4, self.pos.y - 4, self.pos.length + 8, self.pos.height + 8),
							 border_radius=self.border_radius + 4)

			pygame.draw.rect(self.scene, (50, 50, 50),
							 (self.pos.x - 2, self.pos.y - 2, self.pos.length + 4, self.pos.height + 4),
							 border_radius=self.border_radius + 2)

	def render_base(self):
		color = np.array(self.colour) - (np.array((50, 50, 50)) * int(self.darkened))
		pygame.draw.rect(self.scene, color, self.pos.get_rect(), border_radius=self.border_radius)

class Button(UIElement):

	def __init__(self, scene, type, asset_path=None, text=None, gab=(200, 100, 20)):
		super().__init__(scene)
		self.type = type

		if not asset_path and not text:
			text = 'Test'

		self.label = None
		if text:
			self.label = DisplayableText(scene, text, size=40, color=(0, 0, 0))

		self.icon = None
		if asset_path:
			self.icon = Displayable(scene)
			self.icon.load_asset(asset_path)
			self.icon.rescale_asset(50, 50)
		self.pos.length = gab[0]
		self.pos.height = gab[1]
		self.border_radius = gab[2]

		self.repos()

	def repos(self):
		if self.label and self.icon:
			full_length = self.icon.pos.length + 10 + self.label.pos.length
			self.icon.pos.move_to(
				self.pos.x + (self.pos.length - full_length) / 2,
				self.pos.y + (self.pos.height - self.icon.pos.height) / 2)

			self.label.pos.move_to(
				(self.pos.x + (self.pos.length - full_length) / 2) + self.icon.pos.length + 10,
				self.pos.y + (self.pos.height - self.label.pos.height) / 2)
		elif self.icon:
			self.icon.pos.move_to(
				self.pos.x + (self.pos.length - self.icon.pos.length) / 2,
				self.pos.y + (self.pos.height - self.icon.pos.height) / 2)

		elif self.label:
			self.label.pos.move_to(
				self.pos.x + (self.pos.length - self.label.pos.length) / 2,
				self.pos.y + (self.pos.height - self.label.pos.height) / 2)

	def change_text(self, text):
		self.label.change_text(text)
		self.repos()
	def render(self):
		self.render_highlighted()
		self.render_base()

		if self.label:
			self.label.render()
		if self.icon:
			self.icon.draw()

class PlayerCard(UIElement):

	def __init__(self, scene, pid):
		super().__init__(scene)
		self.pid = pid
		self.border_radius = 10
		self.pos.height = 150
		self.pos.length = 250
		self.pos.x = 5
		self.pos.y = 5 + ((self.pos.height + 5) * pid)

		self.player_name_text = DisplayableText(scene, "Name", color=(0, 0, 0))
		self.player_money_text = DisplayableText(scene, "Money", color=(0, 0, 0))

	def render(self, player, curr_pl):

		self.highlighted = (curr_pl == player)
		self.render_highlighted()

		self.render_base()

		self.player_name_text.change_text(player.name)
		self.player_name_text.pos.move_to(self.pos.x + ((self.pos.length - self.player_name_text.pos.length) / 2),
										  self.pos.y + self.pos.height - self.player_name_text.pos.height - 5)
		self.player_name_text.render()

		self.player_money_text.change_text(str(player.money) + '$')
		self.player_money_text.pos.move_to(
			self.pos.x + self.pos.length - self.player_money_text.pos.length,
			self.pos.y + 5)
		self.player_money_text.render()

		self.scene.blit(pygame.transform.smoothscale_by(player.core_assets[player.frame], 0.2), (self.pos.x + 5, self.pos.y + 5))
