import pygame
import json, random
import time
from classes.BaseClass import BaseClass
from classes.Player import Player
from classes.GameBackgroud import GameBackground
from classes.Card import Card


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
        self.players = []
        self.init_game()
        self.game_state = "DEFAULT"
        print("loaded in: ", round((time.time() - start_time) * 1000), 'ms', sep='')

    def run_loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
            self.bg.draw()
            for card in self.cards:
                card.draw(1)
                if not card._show:
                    card.show()
            for player in self.players:
                player.draw()
                if not player._show:
                    player.show()
            pygame.display.flip()
            pygame.time.wait(10)
            self.scene.fill(color=[0, 0, 0])

    def load_cards(self):
        with open('config.json', 'r') as rf:
            data = json.load(rf)
        for street in data["streets"]:
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
