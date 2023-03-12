import pygame
from random import randint

class Dice():
    def __init__(self):
        self.value = 0
    def roll(self):
        self.value = randint(1, 6)

class Player():
    def __init__(self, id):
        self.id = id
        self.place = 0
        self.money = 1500
        self.owned = {}
        self.chance_cards = {}
        self.comm_ch_cards = {}
    def check(self):
        if self.place >= 40:
            self.money += 2000 #Деньги за прохождение поля !!!!!!!!!
            self.place = self.place - 40
    def add_owned(self):
        pass
    def add_cards(self):
        pass

class Board():
    def __init__(self):
        self.owned = {}
        self.chance_cards = {}
        self.community_chest_cards = {}

def play(dice1, dice2, player):
    dice1.roll()
    dice2.roll()
    player.place += dice1.value + dice2.value



def main():
    is_game = True
    n_players = int(input())
    while n_players > 4 or n_players < 2:
        print("Illegal amount of players (Allowed range: 2-4)")
        n_players = int(input())

    list_of_players = []
    for i in range(1, n_players+1):
        play = Player(id = i)
        list_of_players.append(play)
    dice1, dice2 = Dice(), Dice()

    while is_game:
        for i in range(list_of_players):
            play(list_of_players[i])






if __name__ == "__main__":
    main()