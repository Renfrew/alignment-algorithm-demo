"""Alignment Demo

This is a demo program testing an aliment algorithm

Created by Liang Chen (Renfrew) on 2021-02-10.

"""

import pygame
from pygame.constants import K_ESCAPE

# Settings
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (800, 600)
FPS = 30


class AlignPoint:
    """This is the doubly linked list class"""

    def __init__(self, idx, position, node):
        self.idx = idx
        self.position = position
        self.node = node
        self.prew = None
        self.next = None

    def add(self, node):
        pass


class Rectangle(pygame.Rect):
    """This is the object that can align to other objects"""

    # The screen used to draw itself and the list of all rectangles
    screen = None
    nodes = []

    # The doubly linked list storing all points that can be used to auto-aligned
    horizontal = None
    vertical = None

    def __init__(self, _x, _y, _width, _height):
        super().__init__(_x, _y, _width, _height)

        self._left = AlignPoint(_x, 'left', self)
        self._center_horizontal = AlignPoint(_x + _width / 2, 'center', self)
        self._right = AlignPoint(_x + _width, 'right', self)
        self._top = AlignPoint(_y, 'top', self)
        self._center_vertical = AlignPoint(_y + _height / 2, 'center', self)
        self._bottom = AlignPoint(_y + _height, 'bottom', self)

        # Add all align point to the list
        if Rectangle.horizontal is None:
            Rectangle.horizontal = self._left

        if Rectangle.vertical is None:
            Rectangle.vertical = self._top

        Rectangle.horizontal.add(self._center_horizontal)
        Rectangle.horizontal.add(self._right)
        Rectangle.vertical.add(self._center_vertical)
        Rectangle.vertical.add(self._bottom)

    def get_horizontal_midpoint(self):
        """Get the midpoint of the width"""
        return self.width / 2

    def get_vertical_midpoint(self):
        """Get the midpoint of the height"""
        return self.height / 2

    def move_horiontally(self, distance):
        """A method that calculates the alignment status horizontally with other nodes"""

        self.move_ip(distance, 0)

    def move_vertically(self, distance):
        """A method that calculates the alignment status vertically with other nodes"""

        self.move_ip(0, distance)

    def draw(self):
        """A method that draw this object into the screen"""
        pygame.draw.rect(screen, (255, 0, 0), self)


def main():
    """This is the main function of the demo"""

    clock = pygame.time.Clock()

    # list of all nodes
    nodes = []

    # variables used in handling drag event
    mouse_x = 0
    mouse_y = 0
    _node = None

    # Create a triangle
    nodes.append(Rectangle(100, 200, 80, 40))

    # Initial the Rectangle
    Rectangle.screen = screen
    Rectangle.nodes = nodes

    is_draging = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = (click_x, click_y) = event.pos

                # Check if a node is clicked
                for node in nodes:
                    if node.collidepoint(position):
                        is_draging = True
                        mouse_x = click_x
                        mouse_y = click_y
                        _node = node
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                is_draging = False

            elif event.type == pygame.MOUSEMOTION:
                if is_draging:
                    (click_x, click_y) = event.pos
                    _node.move_horiontally(click_x - mouse_x)
                    _node.move_vertically(click_y - mouse_y)
                    mouse_x = click_x
                    mouse_y = click_y

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

        # - constant game speed / FPS
        clock.tick(FPS)


# Initial the screen
pygame.init()
pygame.display.set_caption("Alignment Deme")
screen = pygame.display.set_mode(SCREEN_SIZE)

main()
