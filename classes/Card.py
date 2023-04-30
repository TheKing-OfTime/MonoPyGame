import pygame

from classes.Displayable import Animated


class Card(Animated):

    def __init__(self, scene, street_data):
        super().__init__(scene)
        self.deposited = False
        self.colour = street_data["colour"]
        self.name = street_data["name"]
        self.price = street_data["price"]
        self.rent_price = street_data["rent_price"]
        self.combo_rent_price = street_data["combo_rent_price"]
        self.one_house_rent_price = street_data["one_house_rent_price"]
        self.two_house_rent_price = street_data["two_house_rent_price"]
        self.three_house_rent_price = street_data["three_house_rent_price"]
        self.four_house_rent_price = street_data["four_house_rent_price"]
        self.hostel_rent_price = street_data["hostel_rent_price"]
        self.house_price = street_data["house_price"]
        self.hostel_price = street_data["hostel_price"]
        self.load_asset(street_data["assets_path"])
        self.rescale_assets(200, 300)
        self.pos.move_to_random()

    def deposit(self):
        self.deposited = not self.deposited
