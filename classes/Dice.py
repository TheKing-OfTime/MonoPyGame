from classes.Displayable import Displayable
from random import randint

# TODO: переписать
class Dice(Animated):
    def __init__(self, scene):
        super().__init__(scene)
        self.value = 0

    def roll(self):
        self.value = randint(1, 6)
        

def GlassDice(Displayable):
    def __init__(self, scene):
        super().__init__(scene)
        self.first_dice = Dice(scene, True)
        self.second_dice = Dice(scene, True)
    def roll_dices(self):
        self.first_dice.roll()
        self.second_dice.roll()
        while (self.first_dice.value == self.second_dice.value):
            self.first_dice.roll()
            self.second_dice.roll()
        result = self.first_dice.value+self.second_dice.value
        self.first_dice.value, self.second_dice.value = 0
        return result
        
