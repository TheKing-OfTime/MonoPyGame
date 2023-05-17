import pygame
import numpy as np
import json
import time
from classes.BaseClass import BaseClass
from classes.Player import Player
from classes.GameBackgroud import GameBackground
from classes.Card import Card
from classes.HUD import HUD
from classes.Dice import GlassDice
from classes.Displayable import DisplayableText


class Game(BaseClass):
    GAME_STATES = [
        "LOADING"
        "PAUSED"
        "DEFAULT"
        "MAIN_MENU"
        "CONNECTING"
    ]

    def __init__(self, scene, player_count=4):
        super().__init__(scene)
        start_time = time.time()
        self.done = False
        self.game_state = "LOADING"
        self.HUD = HUD(scene)
        self.HUD.show_loading()
        print("loading...")

        self.p_count = player_count
        self.bg = GameBackground(scene)
        self.cards = []
        self.dice_glass = GlassDice(scene)
        self.cards_in_move = []
        self.players = []
        self.current_player = None
        self.current_player_id = 0

        self.init_game()

        self.game_state = "MAIN_MENU"
        print("loaded in: ", round((time.time() - start_time) * 1000), 'ms', sep='')

    def run_loop(self):
        while not self.done:

            self.handle_events()

            if self.game_state == 'DEFAULT':

                self.bg.draw()

                #self.handle_cards()

                self.handle_players()

                self.handle_dices()

            self.handle_HUD()

            pygame.display.flip()
            pygame.time.wait(10)
            self.scene.fill(color=[50, 50, 50])

    def load_cards(self):
        with open('config.json', 'r', encoding='UTF-8') as rf:
            data = json.load(rf)
        for tile in data["tiles"]:
            if tile['type'] != 'street':
                continue
            if not tile['data']['assets_path']:
                print(tile['name'] + ' assets_path not found. Skipping!')
                continue

            self.cards.append(self.create_street(tile['data']))

    def load_players(self):
        for i in range(self.p_count):
            self.players.append(self.load_player(i))
        self.HUD.init_p_cards(self.players)
        self.current_player = self.players[0]

    def load_player(self, id):
        return Player(self.scene, id, "TheKingOfTime" + str(id))

    def create_street(self, street_data) -> Card:
        return Card(self.scene, street_data)

    def init_game(self):
        self.load_cards()
        self.load_players()
        self.HUD.init_main_menu_buttons()

    def handle_cards(self):
        self.handle_cards_animation()
        #for card in self.cards:
        card = self.cards[0]
        card.draw()

        if not card._show:
            card.show()

    def handle_cards_animation(self):
        for card in self.cards_in_move:

            if card.animation_state == "IN_DEPOSIT":
                target = card.pos.length - 20
                if target <= 0:
                    card.rescale_assets(width=0)
                    card.pos.move((-card.pos.length / 2), 0)
                    card.draw_next()
                    card.animation_state = "OUT_DEPOSIT"
                else:
                    card.rescale_assets(target)
                    card.pos.move(10, 0)

            elif card.animation_state == "OUT_DEPOSIT":
                target = card.pos.length + 20
                if target >= card.pos.default_length:
                    card.rescale_assets(width=card.pos.default_length)
                    card.pos.move(((card.pos.default_length - card.pos.length) / 2), 0)
                    card.animation_state = "DEFAULT"
                    card.deposit()
                    self.cards_in_move.remove(card)
                else:
                    card.rescale_assets(width=target)
                    card.pos.move(-10, 0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and self.game_state == 'DEFAULT':
                    if self.current_player.animation_state == "DEFAULT":
                        self.current_player.animation_state = "START"
                        res = self.dice_glass.roll_dices()
                        self.current_player.move_to_tile(res)
                elif event.key == pygame.K_d:
                    if self.cards[0].animation_state == "DEFAULT":
                        self.cards[0].animation_state = "IN_DEPOSIT"
                        self.cards_in_move.append(self.cards[0])
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # for card in reversed(self.cards):
                    #     if not card._show:
                    #         continue
                    #     collide = card.get_rect().collidepoint(pygame.mouse.get_pos())
                    #     if collide:
                    #         if card.animation_state == "DEFAULT":
                    #             card.animation_state = "IN_DEPOSIT"
                    #             self.cards_in_move.append(card)
                    #         break
                    collide = self.HUD.play_button.get_rect().collidepoint(pygame.mouse.get_pos())
                    if collide:
                        self.game_state = "DEFAULT"

            elif event.type == pygame.MOUSEMOTION:
                collide = self.HUD.play_button.get_rect().collidepoint(pygame.mouse.get_pos())
                if collide:
                    self.HUD.play_button.highlighted = True
                else:
                    self.HUD.play_button.highlighted = False

            elif event.type == pygame.WINDOWRESIZED:
                self.handle_window_resize()


    def handle_players(self):
        for player in self.players:
            self.handle_player(player)
        self.handle_player_animation()

    def handle_player(self, player):
        player.draw()

    def handle_player_animation(self):
        A = 5
        player = self.current_player

        if player.animation_state == 'MOVE':
            target_pos = np.array(player.animation_memory['target_pos'])
            player_pos_g = np.array(player.animation_memory['player_pos'])
            player_pos = np.array([player.pos.x, player.pos.y])
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
                player.animation_state = 'START'
                res = target_pos
                self.current_player.curr_tile += 1
                if self.current_player.curr_tile > 39:
                    self.current_player.curr_tile -= 40
                    self.current_player.money += 2000
            player.pos.move_to(*res)

        if player.animation_state == 'START':
            if player.curr_tile == player.tile:
                self.current_player.animation_state = "DEFAULT"
                target = (self.current_player_id + 1) % 4
                self.current_player = self.players[target]
                self.current_player_id = target
                return

            target_pos = player.get_target_pos()
            player.animation_memory = {"target_pos":target_pos, "player_pos": np.array([player.pos.x, player.pos.y])}
            player.animation_state = 'MOVE'

    def handle_HUD(self):
        self.HUD.render(self.game_state, self.current_player, self.players)

    def handle_dices(self):
        self.dice_glass.first_dice.draw()
        self.dice_glass.second_dice.draw()

    def handle_window_resize(self):
        shifted = self.bg.update_pos()
        for player in self.players:
            player.pos.move(*shifted)

        self.dice_glass.update_pos()
