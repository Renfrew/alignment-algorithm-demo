"""Alignment Demo

This is a demo program testing an aliment algorithm

Created by Liang Chen (Renfrew) on 2021-02-10.

"""

# import sys
import pygame
from pygame.constants import K_ESCAPE
# from pygame.locals import {

# }

# Start the screen
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (800, 600)
FPS = 30


class Rectangle(pygame.Rect):
    """This is the object that can align to other objects"""

    # The screen used to draw itself
    screen = None

    def __init__(self,_x, _y, width, height):
        super().__init__(_x, _y, width, height)

    def move_horiontally(self, distance):
        """A method that calculates the alignment status horizontally with other nodes"""

    def move_vertically(self, distance):
        """A method that calculates the alignment status vertically with other nodes"""

    def draw(self):
        """A method that draw this object into the screen"""
        pygame.draw.rect(screen, (255, 0, 0), self)


def main():
    """This is the main function of the demo"""

    clock = pygame.time.Clock()
    nodes = []

    # Initial the Rectangle
    Rectangle.screen = screen

    # Create a triangle
    nodes.append(Rectangle(100, 200, 80, 40))

    is_draging = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = (click_x, click_y) = event.pos
                print(click_x)
                print(click_y)

                # Check if a node is clicked
                for node in nodes:
                    if node.collidepoint(position):
                        print('collision')
                        is_draging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                is_draging = False
                print('up')

            # if the user click the window close button.
            elif event.type == pygame.QUIT:
                running = False

        # Refresh screen with white color
        screen.fill((255, 255, 255))

        # Draw all rectangles
        for node in nodes:
            node.draw()

        # Update the screen
        pygame.display.flip()

        # - constant game speed / FPS -
        clock.tick(FPS)


# Initial the screen
pygame.init()
pygame.display.set_caption("Alignment Deme")
screen = pygame.display.set_mode(SCREEN_SIZE)

main()
