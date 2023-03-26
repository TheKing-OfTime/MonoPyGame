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
	test_displayable.pos.move(1, 1)
	if not test_displayable._show:
		test_displayable.show()
	pygame.display.flip()
	pygame.time.wait(10)
	scr.fill(color=[0, 0, 0])
