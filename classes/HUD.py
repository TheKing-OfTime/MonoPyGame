from classes.BaseClass import BaseClass
from classes.Displayable import DisplayableText

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

		self.player_name_text = DisplayableText(scene, "Test")
		self.player_name_text.pos.move_to(0, 30)

		self.player_money_text = DisplayableText(scene, "Test")
		self.player_money_text.pos.move_to(scene.get_width() - self.player_money_text.pos.length, 30)

	def render(self, state="DEFAULT", player=None):
		if state == "DEFAULT":
			if player is None:
				print('Failed render HUD: Player not found!')
				return -1

			self.player_name_text.change_text(player.name)
			self.player_name_text.render()

			self.player_money_text.change_text(str(player.money) + '$')
			self.player_money_text.pos.move_to(0, 60)
			self.player_money_text.render()
