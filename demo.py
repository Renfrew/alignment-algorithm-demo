"""Alignment Demo

This is a demo program testing an aliment algorithm

Created by Liang Chen (Renfrew) on 2021-02-10.

"""

from __future__ import annotations
import typing
import pygame
from pygame.constants import K_ESCAPE
import rectangle as rt

# Settings
FPS = 30

DEFAULT_COLOR = (199, 21, 133)
HIGHTLIGHT_COLOR = (199, 21, 133)


def draw_line(point: rt.AlignPoint, shape: rt.Rectangle, direction='horizontal'):
    """ Draw a line between two rectangle"""
    if direction == 'horizontal' and shape is not None:
        pygame.draw.line(screen,
                         HIGHTLIGHT_COLOR,
                         (point.idx, point.node.get_bottom_idx()),
                         (point.idx, shape.get_bottom_idx()))
    elif direction == 'horizontal':
        pygame.draw.line(screen,
                         HIGHTLIGHT_COLOR,
                         (point.idx, 0),
                         (point.idx, rt.SCREEN_HEIGHT))
    elif shape is not None:
        pygame.draw.line(screen,
                         HIGHTLIGHT_COLOR,
                         (point.node.get_right_idx(), point.idx),
                         (shape.get_right_idx(), point.idx))
    else:
        pygame.draw.line(screen,
                         HIGHTLIGHT_COLOR,
                         (0, point.idx),
                         (rt.SCREEN_WIDTH, point.idx))


def main():
    """This is the main function of the demo"""

    clock = pygame.time.Clock()

    # list of all nodes
    nodes: typing.List[rt.Rectangle] = []

    # variables used in handling drag event
    mouse_x = 0
    mouse_y = 0
    _node: rt.Rectangle = None
    horizontal_aligned_node: rt.AlignPoint = None
    vertical_aligned_node: rt.AlignPoint = None

    # Create a triangle
    nodes.append(rt.Rectangle(200, 100, 60, 40))
    nodes.append(rt.Rectangle(300, 400, 80, 40))
    nodes.append(rt.Rectangle(170, 300, 80, 80))
    nodes.append(rt.Rectangle(600, 200, 100, 100))

    # Initial the Rectangle
    rt.Rectangle.screen = screen
    rt.Rectangle.nodes = nodes

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
                _node = None
                horizontal_aligned_node = None
                vertical_aligned_node = None

            elif event.type == pygame.MOUSEMOTION:
                if is_draging:
                    (click_x, click_y) = event.pos
                    horizontal_aligned_node = \
                        _node.move_horiontally(click_x - mouse_x)
                    vertical_aligned_node = \
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

        # If two nodes are aligned, hightlight them and draw the line
        if _node is not None:
            # Horizontal direction
            if horizontal_aligned_node is not None:
                pygame.draw.rect(screen, HIGHTLIGHT_COLOR, _node)
                if horizontal_aligned_node.node != "window":
                    pygame.draw.rect(screen,
                                     HIGHTLIGHT_COLOR,
                                     horizontal_aligned_node.node)
                    draw_line(horizontal_aligned_node, _node)
                else:
                    draw_line(horizontal_aligned_node, None)
            # Vertical direction
            if vertical_aligned_node is not None:
                pygame.draw.rect(screen, HIGHTLIGHT_COLOR, _node)
                if vertical_aligned_node.node != "window":
                    pygame.draw.rect(screen,
                                     HIGHTLIGHT_COLOR,
                                     vertical_aligned_node.node)
                    draw_line(vertical_aligned_node, _node, 'vertical')
                else:
                    draw_line(vertical_aligned_node, None, 'vertical')

        # Update the screen
        pygame.display.flip()

        # - constant game speed / FPS
        clock.tick(FPS)

        # Initial the screen
pygame.init()
pygame.display.set_caption("Alignment Demo")
screen = pygame.display.set_mode(rt.SCREEN_SIZE)

main()
