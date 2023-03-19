from classes.Displayable import Displayable
from random import randint


class Dice(Displayable):
    def __init__(self, scene):
        super().__init__(scene)
        self.value = 0

    def roll(self):
        self.value = randint(1, 6)
