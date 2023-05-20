import pygame
import numpy as np
import json
import time
from classes.BaseClass import BaseClass
from classes.Player import Player
from classes.GameBackgroud import GameBackground
from classes.Card import Card
from classes.HUD import HUD, Button
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

                self.handle_cards_animation()

                self.handle_players()

                #self.handle_dices()

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
            card = self.create_street(tile['data'])
            card.set_id(tile['id'])
            self.cards.append(card)

    def load_players(self):
        for i in range(self.p_count):
            p = self.load_player(i)
            p.pos.move(*self.p_pos_shifted)
            self.players.append(p)
        self.current_player = self.players[0]
        self.HUD.init_default(self.players, self)

    def load_player(self, id):
        return Player(self.scene, id, "Player" + str(id))

    def create_street(self, street_data) -> Card:
        return Card(self.scene, street_data, self)

    def init_game(self):
        self.load_cards()
        self.load_players()

    def handle_cards(self):
        self.handle_cards_animation()
        for card in self.cards:
            card.draw()

    def handle_cards_animation(self):
        for card in self.cards_in_move:
            card.handle_animation()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYUP:

                if self.HUD.text_input:
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.HUD.current_overlay.addons[0].text) > 0:
                            self.HUD.current_overlay.addons[0].change_text(self.HUD.current_overlay.addons[0].text[:-1])
                            self.HUD.current_overlay.addons[0].repos()
                    else:
                        if len(self.HUD.current_overlay.addons[0].text) < 16:
                            self.HUD.current_overlay.addons[0].change_text(self.HUD.current_overlay.addons[0].text + event.unicode)
                            self.HUD.current_overlay.addons[0].repos()

                    if len(self.HUD.current_overlay.addons[0].text) == 0:
                        self.HUD.current_overlay.y_btn.disabled = True
                    else:
                        self.HUD.current_overlay.y_btn.disabled = False
                    self.HUD.current_overlay.y_btn.custom_id \
                        = self.HUD.current_overlay.y_btn.custom_id.split('|')[0] \
                          + '|' \
                          + self.HUD.current_overlay.addons[0].text

                else:
                    if event.key == pygame.K_SPACE and self.game_state == 'DEFAULT':
                        if not self.HUD.next_turn_button.disabled:
                            self.HUD.next_turn_button.darkened = False
                            self.next_turn()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_state == 'DEFAULT':
                    if not self.HUD.next_turn_button.disabled:
                        self.HUD.next_turn_button.darkened = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.game_state == "DEFAULT":
                        if self.HUD.context_menu._show:
                            self.HUD.context_menu.disappear()
                    els = self.HUD.buttons
                    if self.HUD.context_menu:
                        if self.HUD.context_menu._show:
                            els = self.HUD.context_menu.ui_elements
                    for btn in els:
                        btn.darkened = False
                        if btn.disabled or (not btn._show and 'ctx-menu_deposit' in btn.type):
                            continue
                        if self.HUD.current_overlay:
                            if (self.HUD.current_overlay._show) and not ('modal' in btn.type) or not self.HUD.current_overlay._show and ('modal' in btn.type):
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

                                elif btn.type == 'regular_ctx-menu_deposit':
                                    card = self.get_card_by_tile(btn.custom_id)
                                    if card.animation_state == "DEFAULT":
                                        card.animation_state = "IN_DEPOSIT"
                                        self.cards_in_move.append(card)

                                elif btn.type == 'regular_ctx-menu_change-name':
                                    self.HUD.current_overlay = self.HUD.overlays[2]
                                    self.HUD.text_input = True
                                    name = self.players[btn.custom_id].name
                                    self.HUD.current_overlay.addons = [DisplayableText(self.scene, text=name, size=50)]
                                    self.HUD.current_overlay.y_btn.custom_id = str(btn.custom_id) + '|' + self.players[btn.custom_id].name
                                    self.HUD.current_overlay.appear()

                                elif btn.type == 'regular_ctx-menu_demolish':
                                    card = self.get_card_by_tile(btn.custom_id)
                                    if card.buildings > 0:
                                        if card.buildings == 5:
                                            card.owned_by.money += card.hostel_price
                                        else:
                                            card.owned_by.money += card.house_price
                                        card.buildings -= 1


                                elif btn.type == 'regular_ctx-menu_build':
                                    card = self.get_card_by_tile(btn.custom_id)
                                    if card.buildings < 5:
                                        card.buildings += 1
                                        if card.buildings == 5:
                                            card.owned_by.money -= card.hostel_price
                                        else:
                                            card.owned_by.money -= card.house_price

                                elif btn.type == 'regular_modal_change-name_yes':
                                    self.HUD.text_input = False
                                    self.HUD.current_overlay.disappear()
                                    data = btn.custom_id.split('|')
                                    self.players[int(data[0])].name = data[1]
                                    self.HUD.current_overlay.disappear()

                                elif btn.type == 'regular_buy_card':
                                    self.HUD.current_overlay = self.HUD.overlays[1]
                                    card = self.get_card_by_tile(self.current_player.tile)
                                    self.HUD.current_overlay.addons = [card]
                                    self.HUD.current_overlay.title.change_text(
                                        self.HUD.current_overlay.title_text + ' ' + str(card.price) + '$'
                                    )
                                    self.HUD.current_overlay.appear()

                                elif btn.type == 'regular_request_trade':
                                    self.HUD.current_overlay = self.HUD.overlays[3]
                                    self.HUD.current_overlay.appear()

                                elif btn.type == "regular_modal_buy_card_yes":
                                    card = self.get_card_by_tile(self.current_player.tile)
                                    card.owned_by = self.current_player
                                    self.current_player.owned.append(card)
                                    self.current_player.money -= card.price
                                    self.HUD.buy_card_button.change_text('Куплена')
                                    self.HUD.buy_card_button.disabled = True
                                    self.HUD.current_overlay.disappear()

                                elif btn.type.startswith('regular_modal'):
                                    self.HUD.current_overlay.disappear()

                elif event.button == 3:
                    if self.game_state == 'DEFAULT':
                        collide = None
                        for plcrds in self.HUD.player_cards:
                            collide = plcrds.get_rect().collidepoint(pygame.mouse.get_pos())
                            if collide:
                                self.HUD.context_menu.pos.move_to(*pygame.mouse.get_pos())
                                self.HUD.context_menu.alpha = 0
                                self.HUD.context_menu.hide()
                                self.HUD.context_menu.change_ui_elements([
                                    Button(
                                        self.scene,
                                        self.HUD,
                                        'regular_ctx-menu_change-name',
                                        text='Изменить имя',
                                        gab=(200, 50, 10),
                                        text_size=30,
                                        highlight_type=2,
                                        text_colour=(255, 255, 255),
                                        custom_id=plcrds.pid
                                    )
                                ])
                                self.HUD.context_menu.appear()
                                break
                        if not collide:
                            for card in self.current_player.owned:
                                if not card._show:
                                    continue
                                collide = card.get_rect().collidepoint(pygame.mouse.get_pos())
                                if collide:
                                    self.HUD.context_menu.pos.move_to(*pygame.mouse.get_pos())
                                    self.HUD.context_menu.alpha = 0
                                    self.HUD.context_menu.hide()

                                    self.HUD.context_menu.change_ui_elements([
                                        Button(
                                            self.scene,
                                            self.HUD,
                                            'regular_ctx-menu_deposit',
                                            text=('Выкупить' if card.deposited else 'Заложить'),
                                            gab=(200, 50, 10),
                                            text_size=30,
                                            highlight_type=2,
                                            text_colour=(255, 255, 255),
                                            custom_id=card._id,
                                            disabled=((card.owned_by.money - card.price * 0.6) < 0 and card.deposited) or card.buildings > 0,
                                            disabled_color=(60, 60, 60)
                                        )
                                    ])

                                    if card.buildings < 5:
                                        check = card.buildings + 1
                                        chk_money = 0
                                        if check == 5:
                                            chk_money = card.owned_by.money - card.hostel_price
                                        else:
                                            chk_money = card.owned_by.money - card.house_price
                                        self.HUD.context_menu.ui_elements.append(
                                        Button(
                                            self.scene,
                                            self.HUD,
                                            'regular_ctx-menu_build',
                                            text='Построить ' + (f'{card.buildings + 1}-й дом' if card.buildings < 4 else 'отель'),
                                            gab=(250, 50, 10),
                                            text_size=30,
                                            highlight_type=2,
                                            text_colour=(255, 255, 255),
                                            custom_id=card._id,
                                            disabled_color=(60, 60, 60),
                                            disabled=chk_money < 0
                                        ))

                                    if card.buildings > 0:
                                        self.HUD.context_menu.ui_elements.append(
                                        Button(
                                            self.scene,
                                            self.HUD,
                                            'regular_ctx-menu_demolish',
                                            text=f'Снести ' + (f'{card.buildings}-й дом' if card.buildings <= 4 else 'отель'),
                                            gab=(250, 50, 10),
                                            text_size=30,
                                            highlight_type=2,
                                            text_colour=(255, 255, 255),
                                            custom_id=card._id,
                                            disabled_color=(60, 60, 60)
                                        ))

                                    self.HUD.context_menu.repos()

                                    if self.HUD.context_menu.pos.x + self.HUD.context_menu.pos.length > self.scene.get_width() - 5:
                                        self.HUD.context_menu.pos.move(
                                            -(self.HUD.context_menu.pos.x + self.HUD.context_menu.pos.length - self.scene.get_width() + 5),
                                            0
                                        )
                                    if self.HUD.context_menu.pos.y + self.HUD.context_menu.pos.height > self.scene.get_height() - 5:
                                        self.HUD.context_menu.pos.move(
                                            0,
                                            -(self.HUD.context_menu.pos.y + self.HUD.context_menu.pos.height - self.scene.get_height() + 5)
                                        )
                                    self.HUD.context_menu.repos()
                                    self.HUD.context_menu.appear()
                                    break


            elif event.type == pygame.MOUSEMOTION:
                els = self.HUD.buttons
                if self.HUD.context_menu:
                    if self.HUD.context_menu._show:
                        els = self.HUD.context_menu.ui_elements
                for btn in els:
                    if btn.type.startswith('radio') or btn.disabled or not btn._show:
                        continue

                    if self.HUD.current_overlay:
                        if self.HUD.current_overlay._show and not ('modal' in btn.type) or not self.HUD.current_overlay._show and ('modal' in btn.type):
                            continue
                    collide = btn.get_rect().collidepoint(pygame.mouse.get_pos())
                    if collide:
                        btn.highlighted = True
                        break
                    else:
                        btn.highlighted = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    els = self.HUD.buttons
                    if self.HUD.context_menu:
                        if self.HUD.context_menu._show:
                            els = self.HUD.context_menu.ui_elements
                    for btn in els:
                        if btn.disabled or not btn._show:
                            continue
                        if self.HUD.current_overlay:
                            if self.HUD.current_overlay._show and not ('modal' in btn.type) or not self.HUD.current_overlay._show and ('modal' in btn.type):
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
            self.HUD.current_overlay = self.HUD.overlays[0]
            self.HUD.current_overlay.addons = [self.dice_glass]
            self.dice_glass.roll_dices()
            self.HUD.current_overlay.appear()
            self.HUD.next_turn_button.change_text('Двигать фишку')


        elif self.current_turn == self.TURN_STATES[1]:
            self.HUD.current_overlay.disappear()
            target_turn = self.current_turn
            self.HUD.next_turn_button.disabled = True
            if self.current_player.animation_state == "DEFAULT":
                self.current_player.animation_state = "START"
                self.current_player.move_to_tile(self.dice_glass.get_value())
            elif self.current_player.animation_state == "END":
                target_turn = next_turn
                self.current_player.animation_state = "DEFAULT"
                self.HUD.next_turn_button.change_text('Пропустить')
                self.HUD.next_turn_button.disabled = False
                self.HUD.request_trade_button.disabled = False
                card = self.get_card_by_tile(self.current_player.tile)
                self.HUD.buy_card_button.disabled = True
                self.current_player.handle_current_tile(self)
                if card is None:
                    self.HUD.buy_card_button.change_text('Нельзя купить')
                elif card.owned_by == self.current_player:
                    self.HUD.buy_card_button.change_text('Куплена')
                elif card.owned_by != self.current_player and card.owned_by is not None:
                    self.HUD.buy_card_button.change_text('Чужая карта')
                elif self.current_player.money - card.price < 0:
                    self.HUD.buy_card_button.change_text('Слишком дорого')
                else:
                    self.HUD.buy_card_button.disabled = False
                    self.HUD.buy_card_button.change_text('Купить карту')

        elif self.current_turn == self.TURN_STATES[2]:
            if self.current_player.money < 0:
                self.current_player.bankrupt = True
            self.HUD.request_trade_button.disabled = True
            self.HUD.buy_card_button.disabled = True
            txt = 'Передать ход'
            if self.dice_glass.first_dice.value == self.dice_glass.second_dice.value:
                txt = "Продолжить ход"
            self.HUD.next_turn_button.change_text(txt)


        elif self.current_turn == self.TURN_STATES[3]:
            self.next_player()

            self.HUD.next_turn_button.change_text('Бросить кости')

        self.current_turn = target_turn

    def next_player(self):
        target = (self.current_player_id + 1) % len(self.players)
        if self.dice_glass.first_dice.value == self.dice_glass.second_dice.value:
            target = self.current_player_id
        self.current_player = self.players[target]
        self.current_player_id = target
        if self.current_player.bankrupt:
            self.next_player()

    def handle_players(self):
        for player in self.players:
            self.handle_player(player)
        self.handle_player_animation()

    def handle_player(self, player):
        player.draw()

    def handle_player_animation(self):
        self.current_player.handle_animations(self)


    def handle_HUD(self):
        self.HUD.render(self, self.game_state, self.current_player, self.players)

    def handle_dices(self):
        self.dice_glass.first_dice.draw()
        self.dice_glass.second_dice.draw()

    def get_card_by_tile(self, tile):
        for card in self.cards:
            if card.get_id() == tile:
                return card
        return None

    def handle_window_resize(self):
        self.p_pos_shifted = np.array(self.bg.update_pos())
        for player in self.players:
            player.pos.move(*self.p_pos_shifted)

        self.dice_glass.repos()
        self.HUD.repos(self.game_state, self)
