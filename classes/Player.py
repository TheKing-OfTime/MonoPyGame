import pygame
import numpy as np
from classes.Displayable import Animated


class Player(Animated):

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

    def __init__(self, scene, id, name="TheKingOfTime"):
        super().__init__(scene)
        self.bankrupt = False
        self.frame = id % 5
        self.load_asset('assets\\pieces\\playable\\highlighted')
        self.rescale_assets(35, 35)
        self.icon = pygame.transform.smoothscale_by(self.core_assets[self.frame], 0.2)
        self._id = id
        self.name = name
        self.tile = self.curr_tile = 0
        self.memory = {}
        self.money = 15000
        self.owned = []
        self.chance_cards = []
        self.comm_ch_cards = []
        self.pos.move_to(
            (self.scene.get_width()/2) - 318,
            (self.scene.get_height()/2) - 319)
        self.show()

    def move_to_tile(self, number):
        self.curr_tile = self.tile
        self.tile += number
        if self.tile > 39:
            self.tile -= 40
            
    def handle_animations(self, game):
        A = 5
        
        if self.animation_state == 'MOVE':
            target_pos = np.array(self.animation_memory['target_pos'])
            player_pos_g = np.array(self.animation_memory['player_pos'])
            player_pos = np.array([self.pos.x, self.pos.y])
            direction = target_pos - player_pos_g
            direction_x = 0
            direction_y = 0
            if direction[0] != 0:
                direction_x = direction[0]/abs(direction[0])
            if direction[1] != 0:
                direction_y = direction[1]/abs(direction[1])

            res = np.array([direction_x * A, direction_y * A]) + player_pos
            check = (target_pos - res) * np.array([-direction_x, -direction_y])
            if check[0] > 0 or check[1] > 0:
                self.animation_state = 'START'
                res = target_pos
                game.current_player.curr_tile += 1
                if game.current_player.curr_tile > 39:
                    game.current_player.curr_tile -= 40
                    game.current_player.money += 2000
            self.pos.move_to(*res)

        if self.animation_state == 'START':
            if self.curr_tile == self.tile:
                game.current_player.animation_state = "END"
                game.next_turn()
                return

            target_pos = self.get_target_pos()
            self.animation_memory = {"target_pos":target_pos, "player_pos": np.array([self.pos.x, self.pos.y])}
            self.animation_state = 'MOVE'

    def handle_current_tile(self, game):
        card = game.get_card_by_tile(self.tile)
        if card:
            if card.owned_by:
                m = card.get_rent_price()
                card.owned_by.money += m
                self.money -= m

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
