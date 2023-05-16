import pygame
import numpy as np
from classes.Displayable import Displayable


class Player(Displayable):

    action_types = [
        "MOVE",
        "ROLL_DICES",
        "STREET_ACTION",
        "CARD_EXCHANGE_REQUEST"
    ]

    animation_states = [
        "DEFAULT",
        "BEFORE_HALF",
        "AFTER_HALF",
        "START"
    ]

    def __init__(self, scene, id):
        super().__init__(scene)
        self.load_asset('assets\\pieces\\playable\\Car.png')
        self.asset = pygame.transform.smoothscale(self.asset, (32, 32))
        self._id = id
        self.name = "TheKingOfTime"
        self.tile = self.curr_tile = 0
        self.memory = {}
        self.money = 1500
        self.owned = []
        self.chance_cards = []
        self.comm_ch_cards = []
        self.pos.move_to(322, 41)
        self.show()

    def move_to_tile(self, number):
        self.curr_tile = self.tile
        self.tile += number
        if self.tile > 39:
            self.tile -= 40
            self.money += 2000

    def get_target_pos(self, number=1):
        target = 0
        pos = np.array([self.pos.x, self.pos.y])
        tile = self.curr_tile
        tile_target = tile + number
        if tile_target >= 40:
            tile_target -= 40
        while tile != tile_target:
            if tile == 0 or tile == 9:
                target = pos + np.array([73, 0])
            elif 0 < tile < 9:
                target = pos + np.array([57, 0])
            elif tile == 10 or tile == 19:
                target = pos + np.array([0, 73])
            elif 10 < tile < 19:
                target = pos + np.array([0, 57])
            elif tile == 20 or tile == 29:
                target = pos + np.array([-73, 0])
            elif 20 < tile < 29:
                target = pos + np.array([-57, 0])
            elif tile == 30 or tile == 39:
                target = pos + np.array([0, -73])
            elif 30 < tile < 39:
                target = pos + np.array([0, -57])
            tile += 1
            if tile >= 40:
                tile -= 40

        return target
