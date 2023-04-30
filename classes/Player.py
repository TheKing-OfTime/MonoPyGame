from classes.Displayable import Displayable
from classes.Dice import Dice


class Player(Displayable):
    def __init__(self, scene, id):
        super().__init__(scene)
        self.load_asset('assets\\pieces\\playable\\Car.png')
        self._id = id
        self.tile = 0
        self.money = 1500
        self.owned = []
        self.chance_cards = []
        self.comm_ch_cards = []

    def check(self):
        if self.tile >= 40:
            self.money += 2000  # Деньги за прохождение поля
            self.tile = self.tile - 40

    def roll_dices(self):
        dice1, dice2 = Dice(self.scene), Dice(self.scene)
        dice1.roll()
        dice2.roll()
        self.tile += dice1.value + dice2.value
