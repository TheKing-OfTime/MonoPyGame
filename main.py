import pygame
from classes.Game import Game

pygame.init()
scr = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption('Monopoly')

game = Game(scr)

game.run_loop()