from classes.Displayable import Displayable, Animated
from random import randint


class Dice(Animated):
    def __init__(self, scene):
        super().__init__(scene)
        self.value = 0
        self.show()
        self.load_asset('assets\\pieces\\dices')
        self.rescale_assets_by(0.3)

    def roll(self):
        self.value = randint(1, 6)
        self.frame = self.value - 1
        return self.value


class GlassDice(Displayable):
    def __init__(self, scene):
        super().__init__(scene)
        self.first_dice = Dice(scene)
        self.second_dice = Dice(scene)
        self.repos()
        self.hide()

    def roll_dices(self):
        result = self.first_dice.roll() + self.second_dice.roll()
        return result

    def get_value(self):
        return self.first_dice.value + self.second_dice.value

    def repos(self):
        shift = self.first_dice.pos.length + 5
        w = self.scene.get_width()
        h = self.scene.get_height()
        self.first_dice.pos.move_to(w / 2 - shift, (h - self.first_dice.pos.height)/2)
        self.second_dice.pos.move_to(w / 2 + 5, (h - self.second_dice.pos.height)/2)

    def hide(self):
        super().hide()
        self.first_dice.hide()
        self.second_dice.hide()

    def show(self):
        super().show()
        self.first_dice.show()
        self.second_dice.show()

    def render(self):
        self.first_dice.draw()
        self.second_dice.draw()
