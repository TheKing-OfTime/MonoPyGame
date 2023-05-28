import pygame
import time
from classes.Game import Game

start_time = time.time()
print("loading...")
pygame.init()
scr = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption('Monopygame')

game = Game(scr, start_time)

game.run_loop()