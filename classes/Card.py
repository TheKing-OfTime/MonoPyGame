from classes.Displayable import Animated


class Card(Animated):

    def __init__(self, scene):
        super().__init__(scene)
        self.deposited = False
        self.price = 0
        self.one_home_price = 0
        self.two_home_price = 0
        self.three_home_price = 0
        self.four_home_price = 0
        self.hostel_price = 0
        self.load_asset('assets/tiles/green_1')

    def deposit(self):
        self.deposited = not self.deposited
