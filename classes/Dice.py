from classes.Displayable import Displayable, Animated
from random import randint


class Dice(Animated):
    def __init__(self, scene):
        super().__init__(scene)
        self.value = 0
        self.show()
        self.load_asset('assets\\pieces\\dices')
        self.rescale_assets_by(0.1)

    def roll(self):
        self.value = randint(1, 6)
        self.frame = self.value - 1
        return self.value


class GlassDice(Displayable):
    def __init__(self, scene):
        super().__init__(scene)
        self.first_dice = Dice(scene)
        self.second_dice = Dice(scene)
        self.update_pos()

    def roll_dices(self):
        result = self.first_dice.roll() + self.second_dice.roll()
        return result

    def update_pos(self):
        shift = 5
        w = self.scene.get_width()
        self.first_dice.pos.move_to(w - shift - self.first_dice.pos.length - 60, 5)
        self.second_dice.pos.move_to(w - shift - self.second_dice.pos.length, 5)
