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
		self.current_overlay = None
		self.state = "DEFAULT"
		self.player_cards = []
		self.buttons = []
		self.overlays = []
		self.game_title = None
		self.play_button = None
		self.next_turn_button = None
		self.buy_card_button = None
		self.request_trade_button = None
		self.pc_2 = None
		self.pc_3 = None
		self.pc_4 = None

	def init_default(self, players, game):
		i = 0
		for player in players:
			self.player_cards.append(PlayerCard(self.scene, self, i))
			i+=1
		self.next_turn_button = Button(self.scene, self, 'regular_next_turn', text='Бросить кости', gab=(250, 50, 10),
									   text_size=30)
		self.buy_card_button = Button(self.scene, self, 'regular_buy_card', text='Нельзя купить', gab=(250, 50, 10),
									   text_size=30)
		self.request_trade_button = Button(self.scene, self, 'request_trade_turn', text='Предложить обмен', gab=(250, 50, 10),
									   text_size=30)
		self.next_turn_button.show()
		self.buy_card_button.show()
		self.buy_card_button.disabled = True
		self.request_trade_button.show()
		self.request_trade_button.disabled = True
		self.buttons = [self.next_turn_button, self.buy_card_button, self.request_trade_button]
		self.overlays = [
			Modal(self.scene,
				  self,
				  'Выпало:',
				  y_btn=Button(self.scene, self, 'regular_modal_dice-notice_got-it', text='Окей')
				  ),
			Modal(self.scene,
				  self,
				  'Купить карту?',
				  y_btn=Button(self.scene, self, 'regular_modal_buy_card_yes', text='Да'),
				  n_btn=Button(self.scene, self, 'regular_modal_buy_card_no', text='Отмена')
				  )
		]
		self.current_overlay = self.overlays[0]
		self.repos(game=game)

	def init_main_menu(self):
		self.play_button = Button(self.scene, self, 'regular_play', 'assets/BUTT.png', 'Play', (200, 100, 10), text_size=50, icon_size=75)
		self.play_button.show()

		self.pc_2 = Button(self.scene, self, 'radio_pc_2', 'assets/pieces/dices/Dices_2.png', gab=(60, 60, 10))
		self.pc_2.show()

		self.pc_3 = Button(self.scene, self, 'radio_pc_3', 'assets/pieces/dices/Dices_3.png', gab=(60, 60, 10))
		self.pc_3.show()

		self.pc_4 = Button(self.scene, self, 'radio_pc_4', 'assets/pieces/dices/Dices_4.png', gab=(60, 60, 10))
		self.pc_4.show()
		self.pc_4.highlighted = True

		self.game_title = Displayable(self.scene)
		self.game_title.show()
		self.game_title.load_asset('assets/LOGO.png')
		self.game_title.rescale_asset_by(0.5)

		self.repos("MAIN_MENU")
		self.buttons = []
		self.buttons.append(self.play_button)
		self.buttons.append(self.pc_2)
		self.buttons.append(self.pc_3)
		self.buttons.append(self.pc_4)


	def render(self, state="DEFAULT", player=None, players=None):

		if state == "DEFAULT":
			self.render_player_cards(player, players)
			self.render_buttons()
			self.render_overlays()


		elif state == "LOADING":
			self.show_loading()

		elif state == "MAIN_MENU":
			self.render_buttons()
			self.game_title.draw()

	def render_player_cards(self, player, players):
		for player_card in self.player_cards:
			player_card.render(players[player_card.pid], player)

	def render_buttons(self):
		for btn in self.buttons:
			if btn._show:
				btn.render()

	def render_overlays(self):
		for overlay in self.overlays:
			overlay.render()

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

	def repos(self, state="DEFAULT", game=None):
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

			self.game_title.pos.move_to(
				(self.scene.get_width() - self.game_title.pos.length) / 2,
				(self.scene.get_height() / 4) - (self.game_title.pos.height / 2)
			)

		elif state == "DEFAULT":

			self.next_turn_button.pos.move_to(
				5,
				self.scene.get_height() - self.next_turn_button.pos.height - 5
			)

			self.request_trade_button.pos.move_to(
				self.scene.get_width() - self.request_trade_button.pos.length - 5,
				self.next_turn_button.pos.y
			)

			if self.request_trade_button.pos.length + 5 + self.buy_card_button.pos.length < self.scene.get_width() - game.bg.pos.x - game.bg.pos.length:
				self.buy_card_button.pos.move_to(self.request_trade_button.pos.x - self.buy_card_button.pos.length - 10, self.request_trade_button.pos.y)
			else:
				self.buy_card_button.pos.move_to(self.request_trade_button.pos.x,
												 self.request_trade_button.pos.y - self.buy_card_button.pos.height - 10)

			for btn in self.buttons:
				btn.repos()
			for overlay in self.overlays:
				overlay.repos()


class UIElement(Displayable):

	def __init__(self, scene, HUD):
		super().__init__(scene)
		self.colour = (204, 227, 198)
		self.HUD = HUD
		self.border_radius = 0
		self.highlighted = False
		self.darkened = False
		self.disabled = False

	def render_highlighted(self):
		if self.highlighted and not self.disabled:
			pygame.draw.rect(self.scene, (255, 255, 255),
							 (self.pos.x - 4, self.pos.y - 4, self.pos.length + 8, self.pos.height + 8),
							 border_radius=self.border_radius + 4)

			pygame.draw.rect(self.scene, (50, 50, 50),
							 (self.pos.x - 2, self.pos.y - 2, self.pos.length + 4, self.pos.height + 4),
							 border_radius=self.border_radius + 2)

	def render_base(self):
		color = np.array(self.colour) - (np.array((50, 50, 50)) * int(self.darkened)) - (np.array((100, 100, 100)) * int(self.disabled))
		pygame.draw.rect(self.scene, color, self.pos.get_rect(), border_radius=self.border_radius)

	def render(self):
		self.render_base()

	def repos(self):
		pass

	def handle_animation(self):
		pass

class Button(UIElement):

	def __init__(self, scene, HUD, type, asset_path=None, text=None, gab=(200, 100, 20), text_size=40, icon_size=50):
		super().__init__(scene, HUD)
		self.type = type

		if not asset_path and not text:
			text = 'Test'

		self.label = None
		if text:
			self.label = DisplayableText(scene, text, size=text_size, color=(0, 0, 0))

		self.icon = None
		if asset_path:
			self.icon = Displayable(scene)
			self.icon.load_asset(asset_path)
			self.icon.rescale_asset(icon_size, icon_size)
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

	def show(self):
		super().show()
		if self.label:
			self.label.show()
		if self.icon:
			self.icon.show()

	def hide(self):
		super().hide()
		if self.label:
			self.label.hide()
		if self.icon:
			self.icon.hide()


# class PlayButton(Button):
# 	def __init__(self, scene, type, asset_path, gab=(200, 100, 20)):
# 		super().__init__(scene, type, asset_path, None, gab)
# 		self.icon.rescale_asset_by(4)
#
# 	def repos(self):
# 		self.icon.pos.move_to(self.pos.x, self.pos.y)
#
# 	def render_highlighted(self):
# 		if self.highlighted:
# 			pygame.Rect(self.scene, (255, 255, 255),
# 							 (self.pos.x - 4, self.pos.y - 4, self.pos.length + 8, self.pos.height + 8),
# 							 border_radius=self.border_radius + 4)
#
# 			pygame.draw.rect(self.scene, (50, 50, 50),
# 							 (self.pos.x - 2, self.pos.y - 2, self.pos.length + 4, self.pos.height + 4),
# 							 border_radius=self.border_radius + 2)
# 	def render(self):
# 		self.render_highlighted()
#
# 		self.icon.draw()


class PlayerCard(UIElement):

	def __init__(self, scene, HUD, pid):
		super().__init__(scene, HUD)
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


class Overlay(UIElement):
	def __init__(self, scene, HUD):
		super().__init__(scene, HUD)
		self.ui_elements = []
		self.surface = pygame.Surface((self.pos.length,self.pos.height))
		self.colour = (0, 0, 0)
		self.alpha = 0
		self.animation_speed = 8
		self.target_alpha = 150
		self.border_radius = 0

	def appear(self):
		if self.animation_state == "DEFAULT":
			self.animation_state = "APPEARING"

	def disappear(self):
		if self.animation_state == "DEFAULT":
			self.animation_state = "DISAPPEARING"

	def handle_animation(self):
		if self.animation_state == "APPEARING":
			self.alpha += self.animation_speed
			if self.alpha >= self.target_alpha:
				self.alpha = self.target_alpha
				self.animation_state = "DEFAULT"
				for el in self.ui_elements:
					el.show()

		elif self.animation_state == "DISAPPEARING":
			self.alpha -= self.animation_speed
			if self.alpha <= 0:
				self.alpha = 0
				self.animation_state = "DEFAULT"
				self.hide()
				for el in self.ui_elements:
					el.hide()


		# for el in self.ui_elements:
		# 	el.handle_animation()

	def render_base(self):
		self.surface.fill(self.colour)
		self.surface.set_alpha(self.alpha)
		self.scene.blit(self.surface, (0, 0))

	def render(self):
		if self.animation_state != "DEFAULT":
			self.handle_animation()
		self.render_base()

	def base_repos(self):
		self.pos.height = self.scene.get_height()
		self.pos.length = self.scene.get_width()
		self.surface = pygame.Surface((self.pos.length, self.pos.height))

class Modal(Overlay):
	def __init__(self, scene, HUD, title, y_btn, description=None, n_btn=None, additional_elements=None):
		super().__init__(scene, HUD)
		self.hide()
		self.bg = ModalBG(scene, HUD)
		self.title = DisplayableText(scene, title, size=50)
		self.title.hide()

		self.addons = additional_elements

		self.y_btn = y_btn
		self.n_btn = n_btn
		self.y_btn.hide()
		self.HUD.buttons.append(self.y_btn)

		self.ui_elements = [
			self.bg,
			self.title,
			self.y_btn
		]

		if self.n_btn is not None:
			self.y_btn.hide()
			self.ui_elements.append(self.n_btn)
			self.HUD.buttons.append(self.n_btn)

		self.repos()

	def render(self):
		if self.animation_state != "DEFAULT":
			self.handle_animation()
		self.render_base()

		for el in self.ui_elements:
			if el.animation_state != "DEFAULT":
				el.handle_animation()
			if el._show:
				el.render()
		if self.addons and self.animation_state == "DEFAULT":
			for el in self.addons:
				if el.animation_state != "DEFAULT":
					el.handle_animation()
				if el._show:
					el.render()

	def appear(self):
		super().appear()
		self.show()

		#for el in self.ui_elements:
		el = self.ui_elements[0]
		el.animation_state = 'APPEARING'

		if self.addons:
			for el in self.addons:
				el.show()

	def disappear(self):
		super().disappear()
		self.hide()
		#for el in self.ui_elements:
		el = self.ui_elements[0]
		el.animation_state = 'DISAPPEARING'

		if self.addons:
			for el in self.addons:
				el.hide()

	def handle_animation(self):
		super().handle_animation()
		self.repos()

	def repos(self):
		self.base_repos()
		self.bg.repos()
		self.title.pos.move_to(self.bg.pos.x + 10, self.bg.pos.y + 10)
		self.y_btn.pos.move_to(
			self.bg.pos.x + self.bg.pos.length - self.y_btn.pos.length - 10,
			self.bg.pos.y + self.bg.pos.height - self.y_btn.pos.height - 10
		)
		self.y_btn.pos.height = 50
		self.y_btn.pos.length = 150
		self.y_btn.border_radius = 5
		self.y_btn.repos()

		if self.n_btn:
			self.n_btn.pos.move_to(
				self.y_btn.pos.x - self.n_btn.pos.length - 10,
				self.y_btn.pos.y
			)
			self.n_btn.pos.height = 50
			self.n_btn.pos.length = 150
			self.n_btn.border_radius = 5
			self.n_btn.repos()

		if self.addons:
			for el in self.addons:
				el.repos()


class ModalBG(UIElement):
	def __init__(self, scene, HUD):
		super().__init__(scene, HUD)
		self.colour = (50, 50, 50)
		self.target_gap = np.array([500, 400])
		self.offset_gap = np.array([125, 100])
		self.animation_speed = 12
		self.pos.length = self.target_gap[0] + self.offset_gap[0]
		self.pos.height = self.target_gap[1] + self.offset_gap[1]
		self.border_radius = 10

	def handle_animation(self):
		if self.animation_state == "APPEARING":
			self.show()
			self.pos.length -= self.offset_gap[0] / self.animation_speed
			self.pos.height -= self.offset_gap[1] / self.animation_speed
			if self.pos.length <= self.target_gap[0]:
				self.pos.length = self.target_gap[0]
				self.pos.height = self.target_gap[1]
				self.animation_state = "DEFAULT"
			self.repos()

		elif self.animation_state == "DISAPPEARING":
			self.pos.length += self.offset_gap[0] / self.animation_speed
			self.pos.height += self.offset_gap[1] / self.animation_speed
			if self.pos.length >= (self.target_gap + self.offset_gap)[0]:
				self.pos.length = (self.target_gap + self.offset_gap)[0]
				self.pos.height = (self.target_gap + self.offset_gap)[1]
				self.animation_state = "DEFAULT"
				self.hide()
			self.repos()
	def repos(self):
		self.pos.move_to(
			(self.scene.get_width()  - self.pos.length) / 2,
			(self.scene.get_height() - self.pos.height) / 2)

class Toast(Overlay):
	def __init__(self, scene, HUD):
		super().__init__(scene, HUD)


