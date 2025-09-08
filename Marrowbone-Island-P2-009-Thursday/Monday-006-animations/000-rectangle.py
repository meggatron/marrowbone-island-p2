import pygame, sys  # import graphics/game library + system exit

pygame.init()  # initialize pygame

# window setup
W, H = 640, 360  # window width and height in pixels
screen = pygame.display.set_mode((W, H))  # create the screen
pygame.display.set_caption("single rectangle")  # window title

# colors
BLACK = (0, 0, 0)  # rgb black
RED = (255, 0, 0)  # rgb red

# rectangle setup
rect_w, rect_h = 100, 160  # rectangle width and height
rect = pygame.Rect(0, 0, rect_w, rect_h)  # create rectangle at (0,0)
rect.center = (W // 2, H // 2)  # move rectangle to center of screen

clock = pygame.time.Clock()  # limit fps

# main loop
while True:
    # check events
    for e in pygame.event.get(): # e is a variable for events
        if e.type == pygame.QUIT:  # if close button clicked
            pygame.quit()  # shut down pygame
            sys.exit()  # quit program

    # fill screen and draw rectangle
    screen.fill(BLACK)  # fill background black
    pygame.draw.rect(screen, RED, rect)  # draw red rectangle
    pygame.display.flip()  # update screen

    clock.tick(60)  # run loop at 60 fps
