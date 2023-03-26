import pygame
from classes.Displayable import Displayable, Animated

pygame.init()
scr = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Monopoly')
done = False
test_displayable = Animated(scr)
test_displayable.load_asset('assets/tiles/green_1')
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	test_displayable.draw_next()
	test_displayable.pos.move(10, 0)
	if not test_displayable._show:
		test_displayable.show()
	pygame.display.flip()
	pygame.time.wait(10)
	scr.fill(color=[0, 0, 0])
