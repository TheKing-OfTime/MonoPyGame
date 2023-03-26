import pygame
from classes.Displayable import Displayable, Animated
from classes.GameBackgroud import GameBackground

pygame.init()
scr = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Monopoly')
done = False
test_displayable = Animated(scr)
bg = GameBackground(scr)
test_displayable.load_asset('assets/tiles/green_1')
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	bg.draw()
	test_displayable.draw(1)
	test_displayable.pos.move_to(100, 100)
	if not test_displayable._show:
		test_displayable.show()
	pygame.display.flip()
	pygame.time.wait(10)
	scr.fill(color=[0, 0, 0])
