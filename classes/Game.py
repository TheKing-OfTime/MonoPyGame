import pygame
import json
import time
from classes.BaseClass import BaseClass
from classes.Player import Player
from classes.GameBackgroud import GameBackground
from classes.Card import Card
from classes.HUD import HUD


class Game(BaseClass):
    GAME_STATES = [
        "LOADING"
        "PAUSED"
        "DEFAULT"
        "MAIN_MENU"
        "CONNECTING"
    ]

    def __init__(self, scene):
        super().__init__(scene)
        start_time = time.time()
        self.done = False
        self.game_state = "LOADING"
        print("loading...")
        self.bg = GameBackground(scene)
        self.cards = []
        self.cards_in_move = []
        self.players = []
        self.HUD = HUD(scene)
        self.init_game()
        self.game_state = "DEFAULT"
        print("loaded in: ", round((time.time() - start_time) * 1000), 'ms', sep='')

    def run_loop(self):
        while not self.done:

            self.handle_events()

            self.bg.draw()

            self.handle_cards()

            self.handle_players()

            self.handle_HUD()

            pygame.display.flip()
            pygame.time.wait(10)
            self.scene.fill(color=[50, 50, 50])

    def load_cards(self):
        with open('config.json', 'r', encoding='UTF-8') as rf:
            data = json.load(rf)
        for street in data["streets"]:
            if not street['assets_path']:
                print(street['name'] + ' assets_path not found. Skipping!')
                continue
            self.cards.append(self.create_street(street))

    def load_players(self):
        self.load_player()

    def load_player(self):
        self.players.append(Player(self.scene, 0))

    def create_street(self, street_data) -> Card:
        return Card(self.scene, street_data)

    def init_game(self):
        self.load_cards()
        self.load_players()

    def handle_cards(self):
        self.handle_cards_animation()
        # for card in self.cards:
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
                if event.key == pygame.K_UP:
                    self.players[0].pos.move(0, -1)
                    print(self.players[0].pos.y)
                elif event.key == pygame.K_DOWN:
                    self.players[0].pos.move(0, 1)
                    print(self.players[0].pos.y)
                elif event.key == pygame.K_LEFT:
                    self.players[0].pos.move(-1, 0)
                    print(self.players[0].pos.x)
                elif event.key == pygame.K_RIGHT:
                    self.players[0].pos.move(1, 0)
                    print(self.players[0].pos.x)
                elif event.key == pygame.K_SPACE:
                    self.players[0].move(1)
                elif event.key == pygame.K_d:
                    if self.cards[0].animation_state == "DEFAULT":
                        self.cards[0].animation_state = "IN_DEPOSIT"
                        self.cards_in_move.append(self.cards[0])

    def handle_players(self):
        for player in self.players:
            self.handle_player(player)

    def handle_player(self, player):
        player.draw()


    def handle_HUD(self, state="DEFAULT"):
        self.HUD.render(state, self.players[0])

