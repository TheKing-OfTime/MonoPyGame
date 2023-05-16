import pygame

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

	def __init__(self, scene, players):
		super().__init__(scene)
		self.state = "DEFAULT"

		self.player_cards = []
		i = 0
		for player in players:
			self.player_cards.append(PlayerCard(scene, i))
			i+=1

	def render(self, state="DEFAULT", player=None, players=None):
		if state == "DEFAULT":

			for player_card in self.player_cards:
				player_card.render(players[player_card.pid], player)



class PlayerCard(Displayable):

	def __init__(self, scene, pid):
		super().__init__(scene)
		self.pid = pid
		self.colour = (204, 227, 198)
		self.border_radius = 10
		self.pos.height = 150
		self.pos.length = 250
		self.pos.x = 5
		self.pos.y = 5 + ((self.pos.height + 5) * pid)

		self.player_name_text = DisplayableText(scene, "Name", color=(0, 0, 0))
		self.player_money_text = DisplayableText(scene, "Money", color=(0, 0, 0))

		self.highlighted = False

	def render(self, player, curr_pl):
		if player == curr_pl:
			pygame.draw.rect(self.scene, (255, 255, 255),
							 (self.pos.x - 4, self.pos.y - 4, self.pos.length + 8, self.pos.height + 8),
							 border_radius=self.border_radius + 4)

			pygame.draw.rect(self.scene, (50, 50, 50),
							 (self.pos.x - 2, self.pos.y - 2, self.pos.length + 4, self.pos.height + 4),
							 border_radius=self.border_radius + 2)

			self.highlighted = True
		else:
			self.highlighted = False

		pygame.draw.rect(self.scene, self.colour, self.pos.get_rect(), border_radius=self.border_radius)

		self.player_name_text.change_text(player.name)
		self.player_name_text.pos.move_to(self.pos.x + ((self.pos.length - self.player_name_text.pos.length) / 2),
										  self.pos.y + self.pos.height - self.player_name_text.pos.height - 5)
		self.player_name_text.render()

		self.player_money_text.change_text(str(player.money) + '$')
		self.player_money_text.pos.move_to(
			self.pos.x + self.pos.length - self.player_money_text.pos.length,
			self.pos.y + 5)
		self.player_money_text.render()

		self.scene.blit(pygame.transform.smoothscale_by(player.core_assets[player._id], 0.2), (self.pos.x + 5, self.pos.y + 5))
