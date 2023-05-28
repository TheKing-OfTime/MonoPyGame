import pygame

from classes.Displayable import Animated


class Card(Animated):

    ANIMATION_STATES = [
        "IN_DEPOSIT"
        "OUT_DEPOSIT"
        "DEFAULT"
    ]

    def __init__(self, scene, street_data, game):
        super().__init__(scene)
        self.deposited = False
        self.owned_by = None
        self.frame = 1
        self.buildings = 0
        self.colour = street_data["colour"]
        self.name = street_data["name"]
        self.price = street_data["price"]
        self.rent_price = street_data["rent_price"]
        self.combo_rent_price = self.rent_price * 2
        self.one_house_rent_price = street_data["one_house_rent_price"]
        self.two_house_rent_price = street_data["two_house_rent_price"]
        self.three_house_rent_price = street_data["three_house_rent_price"]
        self.four_house_rent_price = street_data["four_house_rent_price"]
        self.hostel_rent_price = street_data["hostel_rent_price"]
        self.house_price = street_data["house_price"]
        self.hostel_price = street_data["hostel_price"]
        self.load_asset(street_data["assets_path"])
        self.convert_assets()
        self.rescale_assets_by(0.2)
        self.pos.default_length = self.pos.length
        self.pos.default_height = self.pos.height
        self.hide()
        self.game = game

    def deposit(self):
        self.deposited = not self.deposited
        self.owned_by.money += int(((self.price * 0.5) if self.deposited else (self.price * -0.6)))

    def repos(self):
        self.pos.move_to(
            (self.scene.get_width() - self.pos.length) / 2,
            (self.scene.get_height() - self.pos.height) / 2
        )

    def handle_animation(self):
        if self.animation_state == "IN_DEPOSIT":
            target = self.pos.length - 20
            if target <= 0:
                self.rescale_assets(width=0)
                self.pos.move((-self.pos.length / 2), 0)
                self.draw_next()
                self.animation_state = "OUT_DEPOSIT"
            else:
                self.rescale_assets(target)
                self.pos.move(10, 0)

        elif self.animation_state == "OUT_DEPOSIT":
            target = self.pos.length + 20
            if target >= self.pos.default_length:
                self.rescale_assets(width=self.pos.default_length)
                self.pos.move(((self.pos.default_length - self.pos.length) / 2), 0)
                self.animation_state = "DEFAULT"
                self.deposit()
                self.game.cards_in_move.remove(self)
            else:
                self.rescale_assets(width=target)
                self.pos.move(-10, 0)

    def render(self):
        self.draw()

    def get_rent_price(self):
        if self.buildings == 0:
            return self.rent_price
        elif self.buildings == 1:
            return self.one_house_rent_price
        elif self.buildings == 2:
            return self.two_house_rent_price
        elif self.buildings == 3:
            return self.three_house_rent_price
        elif self.buildings == 4:
            return self.four_house_rent_price
        elif self.buildings == 5:
            return self.hostel_rent_price