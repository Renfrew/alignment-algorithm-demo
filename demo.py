"""Alignment Demo

This is a demo program testing an aliment algorithm

Created by Liang Chen (Renfrew) on 2021-02-10.

"""


from __future__ import annotations
import typing
import pygame
from pygame.constants import K_ESCAPE

# Settings
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (800, 600)
FPS = 30


class AlignPoint:
    """This is the doubly linked list class storing data for alignment module"""

    def __init__(self, idx, position, node):
        self.idx = idx
        self.position = position
        self.node: Rectangle = node
        self._prew: AlignPoint = None
        self._next: AlignPoint = None

    def get__prew(self) -> AlignPoint:
        """getter of _prew"""
        return self._prew

    def set__prew(self, another: AlignPoint) -> None:
        """setter of _prew"""
        self._prew = another

    def get__next(self) -> AlignPoint:
        """getter of _next"""
        return self._next

    def set__next(self, another: AlignPoint) -> None:
        """setter of _next"""
        self._next = another

    def add(self, another: AlignPoint):
        """Add another alignPoint into the linked list"""

        # My next is None
        if another.idx >= self.idx and self._next is None:
            self._next = another
            another.set__prew(self)

        # the new node should add to my next
        elif another.idx >= self.idx and another.idx <= self._next.idx:
            another.set__prew(self)
            another.set__next(self._next)
            another.get__next().set__prew(another)
            self._next = another

        # the new node should go behind my next
        elif another.idx >= self.idx:
            self._next.add(another)

        # My prew is None
        elif self._prew is None:
            self._prew = another
            another.set__next(self)

        # the new node is my prew
        elif self._prew.idx <= another.idx:
            another.set__prew(self._prew)
            another.set__next(self)
            self._prew.set__next(another)
            self._prew = another

        # the new node should go infront of my prew
        else:
            self._prew.add(another)

    def relocate(self, distance):
        """Relocated self to another postion so the linked list are sorted"""

    def get_coincident_point(self) -> typing.List[AlignPoint]:
        """Find all the points in the linked list that has the same idx"""

        result = []

        # Find all coincident points on the left side
        __prew = self._prew
        while __prew is not None and __prew.idx == self.idx:
            result.append(__prew)
            __prew = __prew.get__prew()

        # Find all coincident points on the right side
        __next = self._next
        while __next is not None and __next.idx == self.idx:
            result.append(__next)
            __next = __next.get__next()

        return result

    def get_center_coincident_point(self) -> typing.List[AlignPoint]:
        """Find all the points in the linked list that has the same idx"""

        temp_result = self.get_coincident_point()
        result = []

        for point in temp_result:
            if point.position == 'center':
                result.append(point)

        return result


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

    def get_left_idx(self):
        """return the left idx"""
        return self._left.idx

    def get_center_horizontal_idx(self):
        """return the center horizontal idx"""
        return self._center_horizontal.idx

    def get_right_idx(self):
        """return the right idx"""
        return self._right.idx

    def get_top_idx(self):
        """return the top idx"""
        return self._top.idx

    def get_center_vertical_idx(self):
        """return the center vertical idx"""
        return self._center_vertical.idx

    def get_bottom_idx(self):
        """return the bottom idx"""
        return self._bottom.idx

    def move_horiontally(self, distance) -> AlignPoint:
        """A method that calculates the alignment status horizontally with other nodes"""

        # Check if this move would touch the left edge
        if self._left.idx + distance <= 0:
            self.move_ip(-self._left.idx, 0)
            self.update()
            return AlignPoint(0, 'left', 'window')

        # Check if this move would touch the right edge
        if self.get_right_idx() + distance >= SCREEN_WIDTH:
            self.move_ip(SCREEN_WIDTH - 1 - self.get_right_idx(), 0)
            self.update()
            return AlignPoint(SCREEN_WIDTH - 1, 'right', 'window')

        # This move is safe, update the position of myself
        self.move_ip(distance, 0)
        self.update()

        # Check if it is aligned to the center of viewpoint
        if self.get_center_horizontal_idx() == SCREEN_WIDTH / 2:
            return AlignPoint(SCREEN_WIDTH / 2, 'center', 'window')

        # Check if it is aligned to the center of other nodes
        closest_node = None
        closest_distance = 0
        # Search all nodess that are aligned with self
        for _point in self._center_horizontal.get_center_coincident_point():
            top_distance = self.get_top_idx() - _point.node.get_bottom_idx()
            bottom_distance = _point.node.get_top_idx() - self.get_bottom_idx()

            # Check if the node has the smallest distance to self
            update1 = closest_node is None
            update2 = 0 < top_distance < closest_distance
            update3 = 0 < bottom_distance < closest_distance
            if update1 or update2 or update3:
                closest_node = _point
                if top_distance > 0:
                    closest_distance = top_distance
                else:
                    closest_distance = bottom_distance

        # Return the node that is aligned to self, if exists
        if closest_node is not None:
            return closest_node

        return None

    def move_vertically(self, distance):
        """A method that calculates the alignment status vertically with other nodes"""

        self.move_ip(0, distance)

    def update(self):
        """Update the position on the linked list if self had moved"""
        horizontal_diff = self.x - self._left.idx
        vertical_diff = self.y - self._top.idx

        # Update horizontal align point
        if horizontal_diff != 0:
            self._left.relocate(horizontal_diff)
            self._center_horizontal.relocate(horizontal_diff)
            self._right.relocate(horizontal_diff)

        if vertical_diff != 0:
            self._top.relocate(vertical_diff)
            self._center_vertical.relocate(vertical_diff)
            self._bottom.relocate(vertical_diff)

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
