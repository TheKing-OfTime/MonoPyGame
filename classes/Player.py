import pygame
from classes.Displayable import Displayable


class Player(Displayable):

    action_types = [
        "MOVE",
        "ROLL_DICES",
        "STREET_ACTION",
        "CARD_EXCHANGE_REQUEST"
    ]

    def __init__(self, scene, id):
        super().__init__(scene)
        self.load_asset('assets\\pieces\\playable\\Car.png')
        self.asset = pygame.transform.smoothscale(self.asset, (32, 32))
        self._id = id
        self.name = "TheKingOfTime"
        self.tile = 0
        self.money = 1500
        self.owned = []
        self.chance_cards = []
        self.comm_ch_cards = []
        self.pos.move_to(322, 41)
        self.show()

    def move_to_tile(self, number):
        curr_tile = self.tile
        self.tile += number
        if self.tile > 39:
            self.tile -= 40
            self.money += 2000
        while curr_tile != self.tile:
            if curr_tile == 0 or curr_tile == 9:
                self.pos.move(73, 0)
            elif 0 < curr_tile < 9:
                self.pos.move(57, 0)
            elif curr_tile == 10 or curr_tile == 19:
                self.pos.move(0, 73)
            elif 10 < curr_tile < 19:
                self.pos.move(0, 57)
            elif curr_tile == 20 or curr_tile == 29:
                self.pos.move(-73, 0)
            elif 20 < curr_tile < 29:
                self.pos.move(-57, 0)
            elif curr_tile == 30 or curr_tile == 39:
                self.pos.move(0, -73)
            elif 30 < curr_tile < 39:
                self.pos.move(0, -57)

            curr_tile += 1
            if curr_tile > 39:
                curr_tile -= 40



