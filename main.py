import pygame
from classes.Displayable import Displayable

pygame.init()
scr = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Monopoly')
done = False
test_displayable = Displayable(scr)
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	test_displayable.draw()
	pygame.display.update()
	pygame.time.wait(10)
