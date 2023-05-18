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


class Game(BaseClass):
    GAME_STATES = [
        "LOADING"
        "PAUSED"
        "DEFAULT"
        "MAIN_MENU"
        "CONNECTING"
    ]

    TURN_STATES = [
        'ROLL',
        'MOVE',
        'OPTIONAL_ACTIONS',
        'NEXT_PLAYER'
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
        self.p_pos_shifted = np.array([0, 0])
        self.bg = GameBackground(scene)
        self.cards = []
        self.dice_glass = GlassDice(scene)
        self.cards_in_move = []
        self.players = []
        self.current_player = None
        self.current_turn = self.TURN_STATES[0]
        self.current_player_id = 0

        self.HUD.init_main_menu()

        self.game_state = "MAIN_MENU"
        print("loaded in: ", round((time.time() - start_time) * 1000), 'ms', sep='')

    def run_loop(self):
        while not self.done:
            frame_time = time.time()
            self.handle_events()

            if self.game_state == 'DEFAULT':

                self.bg.draw()

                #self.handle_cards()

                self.handle_players()

                self.handle_dices()

            self.handle_HUD()

            pygame.display.flip()
            pygame.time.wait(max(10 - round((time.time() - frame_time) * 1000), 0))
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
            p = self.load_player(i)
            p.pos.move(*self.p_pos_shifted)
            self.players.append(p)
        self.HUD.init_default(self.players)
        self.current_player = self.players[0]

    def load_player(self, id):
        return Player(self.scene, id, "TheKingOfTime" + str(id))

    def create_street(self, street_data) -> Card:
        return Card(self.scene, street_data)

    def init_game(self):
        self.load_cards()
        self.load_players()

    def handle_cards(self):
        self.handle_cards_animation()
        for card in self.cards:
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
                    if not self.HUD.next_turn_button.disabled:
                        self.HUD.next_turn_button.darkened = False
                        self.next_turn()
                # elif event.key == pygame.K_d:
                #     if self.cards[0].animation_state == "DEFAULT":
                #         self.cards[0].animation_state = "IN_DEPOSIT"
                #         self.cards_in_move.append(self.cards[0])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_state == 'DEFAULT':
                    if not self.HUD.next_turn_button.disabled:
                        self.HUD.next_turn_button.darkened = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.game_state == "DEFAULT":
                        for card in reversed(self.cards):
                            if not card._show:
                                continue
                            collide = card.get_rect().collidepoint(pygame.mouse.get_pos())
                            if collide:
                                if card.animation_state == "DEFAULT":
                                    card.animation_state = "IN_DEPOSIT"
                                    self.cards_in_move.append(card)
                                break

                    for btn in self.HUD.buttons:
                        btn.darkened = False
                        if btn.disabled:
                            continue
                        collide = btn.get_rect().collidepoint(pygame.mouse.get_pos())
                        if collide:
                            if self.game_state == "MAIN_MENU":
                                if btn.type == 'regular_play':
                                    self.game_state = "LOADING"
                                    self.HUD.show_loading()
                                    self.init_game()
                                    self.game_state = "DEFAULT"
                                elif btn.type.startswith('radio'):
                                    btn.highlighted = True
                                    self.p_count = int(btn.type.split('_')[2])
                                    for rbtn in self.HUD.buttons:
                                        if rbtn.type == btn.type:
                                            continue
                                        rbtn.highlighted = False

                            elif self.game_state == 'DEFAULT':
                                if btn.type == 'regular_next_turn':
                                    self.next_turn()


            elif event.type == pygame.MOUSEMOTION:
                for btn in self.HUD.buttons:
                    if btn.type.startswith('radio') or btn.disabled:
                        continue
                    collide = btn.get_rect().collidepoint(pygame.mouse.get_pos())
                    if collide:
                        btn.highlighted = True
                        break
                    else:
                        btn.highlighted = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.HUD.buttons:
                    if btn.disabled:
                        continue
                    collide = btn.get_rect().collidepoint(pygame.mouse.get_pos())
                    if collide:
                        btn.darkened = True

            elif event.type == pygame.WINDOWRESIZED:
                self.handle_window_resize()

    def next_turn(self):
        next_turn = self.TURN_STATES[(self.TURN_STATES.index(self.current_turn) + 1) % len(self.TURN_STATES)]
        target_turn = next_turn

        if self.current_turn == self.TURN_STATES[0]:
            self.dice_glass.roll_dices()
            self.HUD.next_turn_button.change_text('Двигать фишку')
        elif self.current_turn == self.TURN_STATES[1]:
            target_turn = self.current_turn
            self.HUD.next_turn_button.disabled = True
            if self.current_player.animation_state == "DEFAULT":
                self.current_player.animation_state = "START"
                self.current_player.move_to_tile(self.dice_glass.get_value())
            elif self.current_player.animation_state == "END":
                target_turn = next_turn
                self.current_player.animation_state = "DEFAULT"
                self.HUD.overlays[0].appear()
                self.HUD.next_turn_button.change_text('Пропустить')
                self.HUD.next_turn_button.disabled = False
        elif self.current_turn == self.TURN_STATES[2]:
            self.HUD.overlays[0].disappear()
            txt = 'Передать ход'
            if self.dice_glass.first_dice.value == self.dice_glass.second_dice.value:
                txt = "Продолжить ход"
            self.HUD.next_turn_button.change_text(txt)
        elif self.current_turn == self.TURN_STATES[3]:
            target = (self.current_player_id + 1) % len(self.players)
            if self.dice_glass.first_dice.value == self.dice_glass.second_dice.value:
                target = self.current_player_id
            self.current_player = self.players[target]
            self.current_player_id = target
            self.HUD.next_turn_button.change_text('Бросить кости')

        self.current_turn = target_turn

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
                self.current_player.animation_state = "END"
                self.next_turn()
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
        self.p_pos_shifted = np.array(self.bg.update_pos())
        for player in self.players:
            player.pos.move(*self.p_pos_shifted)

        self.dice_glass.update_pos()
        self.HUD.repos(self.game_state)
