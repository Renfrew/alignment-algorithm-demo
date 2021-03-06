"""Rectangle

This is a custom rectangle which is auto align to other rectangle or window.

Created by Liang Chen (Renfrew) on 2021-02-11.

"""


from __future__ import annotations
import sys
import typing
import pygame

# Settings
THRESHOLD = 3
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (800, 600)


class AlignPoint:
    """Align Point is a essencial class of Rectangle

    This is actually a doubly linked list item

    idx: which is a number indicating a position
    position: the position of the edge. Ex
            'left', 'center', 'right' or
            'top', 'center', 'bottom'
    node: which is the reference of the Rectangle or string 'window'
    """

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
        if self.idx <= another.idx and self._next is None:
            self._next = another
            another.set__prew(self)

        # the new node should add to my next
        elif self.idx <= another.idx <= self._next.idx:
            another.set__prew(self)
            another.set__next(self._next)
            another.get__next().set__prew(another)
            self._next = another

        # the new node should go behind my next
        elif self.idx <= another.idx:
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
        self.idx += distance

        # Move self to the left side of the linked list
        if distance < 0 and self._prew is not None and self._prew.idx > self.idx:
            # Find the new location which can keep the list sorted
            __prew = self._prew
            while __prew.get__prew() is not None and \
                    __prew.get__prew().idx > self.idx:

                __prew = __prew.get__prew()

            # Connect the prew and the next node of self (old location)
            if self._prew is not None:
                self._prew.set__next(self._next)
            if self._next is not None:
                self._next.set__prew(self._prew)

            # Add self to the new location
            # Prew side
            if __prew.get__prew() is not None:
                __prew.get__prew().set__next(self)
            self._prew = __prew.get__prew()
            # Next side
            self._next = __prew
            __prew.set__prew(self)

        elif distance > 0 and self._next is not None and self._next.idx < self.idx:
            # Find the new location which can keep the list sorted
            __next = self._next
            while __next.get__next() is not None and \
                    __next.get__next().idx < self.idx:

                __next = __next.get__next()

            # Connect the prew and the next node of self (old location)
            if self._prew is not None:
                self._prew.set__next(self._next)
            if self._next is not None:
                self._next.set__prew(self._prew)

            # Add self to the new location
            # Next side
            if __next.get__next() is not None:
                __next.get__next().set__prew(self)
            self._next = __next.get__next()
            # Prew side
            self._prew = __next
            __next.set__next(self)

    def get_coincident_point(self) -> typing.List[AlignPoint]:
        """Find all the points in the linked list that has the same idx"""

        result = []

        # Find all coincident points on the left side
        __prew = self._prew
        while __prew is not None and \
                self.idx - THRESHOLD <= __prew.idx <= self.idx + THRESHOLD:
            result.append(__prew)
            __prew = __prew.get__prew()

        # Find all coincident points on the right side
        __next = self._next
        while __next is not None and \
                self.idx - THRESHOLD <= __next.idx <= self.idx + THRESHOLD:
            result.append(__next)
            __next = __next.get__next()

        return result

    def get_center_coincident_point(self) -> typing.List[AlignPoint]:
        """Find all the center points in the linked list that has the same idx"""

        temp_result = self.get_coincident_point()
        result = []

        for point in temp_result:
            if point.position == 'center':
                result.append(point)

        return result

    def get_side_coincident_point(self) -> typing.List[AlignPoint]:
        """Find all the side points in the linked list that has the same idx"""

        temp_result = self.get_coincident_point()
        result = []

        for point in temp_result:
            if point.position != 'center':
                result.append(point)

        return result

    def print_all(self):
        """The function to print the entired linked list"""
        if self._prew is not None:
            self._prew.print_all()
        else:
            self.print_next()

    def print_next(self):
        """The function to print all the next node in the linked list"""
        self.print_self()
        if self._next is not None:
            self._next.print_next()

    def print_self(self):
        """The function tto print the self"""
        print("Index: ", self.idx, " Position: ",
              self.position, " Node: ", self.node)


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

        # Create AlignPoints for the node
        self._left = AlignPoint(_x, 'left', self)
        self._center_horizontal = AlignPoint(
            int(_x + _width / 2), 'center', self)
        self._right = AlignPoint(_x + _width, 'right', self)
        self._top = AlignPoint(_y, 'top', self)
        self._center_vertical = AlignPoint(
            int(_y + _height / 2), 'center', self)
        self._bottom = AlignPoint(_y + _height, 'bottom', self)

        # Add all align point to the list
        if Rectangle.horizontal is None:
            Rectangle.horizontal = self._left
        else:
            Rectangle.horizontal.add(self._left)

        if Rectangle.vertical is None:
            Rectangle.vertical = self._top
        else:
            Rectangle.vertical.add(self._top)

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

    def get_top_point(self):
        """return the _top"""
        return self._top

    def get_bottom_point(self):
        """return the _bottom"""
        return self._bottom

    def get_left_point(self):
        """return the _left"""
        return self._left

    def get_right_point(self):
        """return the _right"""
        return self._right

    def move_horiontally(self, distance) -> AlignPoint:
        """A method that calculates the alignment status horizontally with other nodes"""

        # Check if this move would touch the left edge
        if self.get_left_idx() + distance - THRESHOLD <= 0:
            self.move_ip(-self.get_left_idx(), 0)
            self.update()
            return AlignPoint(0, 'left', 'window')

        # Check if this move would touch the right edge
        if self.get_right_idx() + distance + THRESHOLD >= SCREEN_WIDTH:
            self.move_ip(SCREEN_WIDTH - 1 - self.get_right_idx(), 0)
            self.update()
            return AlignPoint(SCREEN_WIDTH - 1, 'right', 'window')

        # This move is safe, update the position of myself
        self.move_ip(distance, 0)
        self.update()

        # Check if it is aligned with the center of viewpoint (horizontal)
        left_idx = self.get_center_horizontal_idx() - THRESHOLD
        right_idx = self.get_center_horizontal_idx() + THRESHOLD
        if left_idx <= int(SCREEN_WIDTH / 2) <= right_idx:
            adjust_distance = int(SCREEN_WIDTH / 2) - \
                self.get_center_horizontal_idx()
            self.move_ip(adjust_distance, 0)
            self.update()
            return AlignPoint(int(SCREEN_WIDTH / 2), 'center', 'window')

        # Check if it is aligned to the center of other nodes
        closest_node = None
        closest_distance = 0
        # Search all nodes that are aligned with self
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

        # Return the node that is aligned with the center of self, if exists
        if closest_node is not None:
            adjust_distance = closest_node.idx - self.get_center_horizontal_idx()
            self.move_ip(adjust_distance, 0)
            self.update()
            return closest_node

        # Return the node that is aligned with the edge of self
        return self.move_horiontally_helper()

    def move_horiontally_helper(self) -> AlignPoint:
        """This is the helper function of move_horiontally

            The function will find the closest node with a edge aligned with self
        """
        # Find the nodes that is aligned with the edge of self
        nodes_aligned_with_left_edge = self._left.get_side_coincident_point()
        nodes_aligned_with_right_edge = self._right.get_side_coincident_point()

        (closest_node_to_left_on_top,
         closest_distance_to_left_on_top,
         closest_node_to_left_on_bottom,
         closest_distance_to_left_on_bottom
         ) = self.find_aligned_points(nodes_aligned_with_left_edge)

        (closest_node_to_right_on_top,
         closest_distance_to_right_on_top,
         closest_node_to_right_on_bottom,
         closest_distance_to_right_on_bottom
         ) = self.find_aligned_points(nodes_aligned_with_right_edge)

        # Remove aligned nodes which may be blocked by other nodes
        if closest_node_to_left_on_top is not None and \
            self.find_blocking_point(
                self.get_left_point(),
                closest_node_to_left_on_top.node,
                self,
                'horizontal'):
            closest_node_to_left_on_top = None
            closest_distance_to_left_on_top = sys.maxsize

        if closest_node_to_right_on_top is not None and \
            self.find_blocking_point(
                self.get_right_point(),
                closest_node_to_right_on_top.node,
                self,
                'horizontal'):
            closest_node_to_right_on_top = None
            closest_distance_to_right_on_top = sys.maxsize

        if closest_node_to_left_on_bottom is not None and \
            self.find_blocking_point(
                self.get_left_point(),
                self,
                closest_node_to_left_on_bottom.node,
                'horizontal'):
            closest_node_to_left_on_bottom = None
            closest_distance_to_left_on_bottom = sys.maxsize

        if closest_node_to_right_on_bottom is not None and \
            self.find_blocking_point(
                self.get_right_point(),
                self,
                closest_node_to_right_on_bottom.node,
                'horizontal'):
            closest_node_to_right_on_bottom = None
            closest_distance_to_right_on_bottom = sys.maxsize

        # Output the result, which is the closest node to the moving node
        top_left = closest_distance_to_left_on_top
        top_right = closest_distance_to_right_on_top
        bottom_left = closest_distance_to_left_on_bottom
        bottom_right = closest_distance_to_right_on_bottom

        if closest_node_to_left_on_top is not None and \
                top_left < top_right and \
                top_left < bottom_left and \
                top_left < bottom_right:
            adjust_distance = closest_node_to_left_on_top.idx - \
                self.get_left_idx()
            self.move_ip(adjust_distance, 0)
            self.update()
            return closest_node_to_left_on_top

        if closest_node_to_right_on_top is not None and \
                top_right < top_left and \
                top_right < bottom_left and \
                top_right < bottom_right:
            adjust_distance = closest_node_to_right_on_top.idx - \
                self.get_right_idx()
            self.move_ip(adjust_distance, 0)
            self.update()
            return closest_node_to_right_on_top

        if closest_node_to_left_on_bottom is not None and \
                bottom_left < top_left and \
                bottom_left < top_right and \
                bottom_left < bottom_right:
            adjust_distance = closest_node_to_left_on_bottom.idx - \
                self.get_left_idx()
            self.move_ip(adjust_distance, 0)
            self.update()
            return closest_node_to_left_on_bottom

        if closest_distance_to_right_on_bottom is not None and \
                bottom_right < top_left and \
                bottom_right < top_right and \
                bottom_right < bottom_left:
            adjust_distance = closest_node_to_right_on_bottom.idx - \
                self.get_right_idx()
            self.move_ip(adjust_distance, 0)
            self.update()
            return closest_node_to_right_on_bottom

        return None

    def move_vertically(self, distance):
        """A method that calculates the alignment status vertically with other nodes"""

        # Check if this move would touch the top edge
        if self.get_top_idx() + distance - THRESHOLD <= 0:
            self.move_ip(0, -self.get_top_idx())
            self.update()
            return AlignPoint(0, 'top', 'window')

        # Check if this move would touch the bottom edge
        if self.get_bottom_idx() + distance + THRESHOLD >= SCREEN_HEIGHT:
            self.move_ip(0, SCREEN_HEIGHT - 1 - self.get_bottom_idx())
            self.update()
            return AlignPoint(SCREEN_HEIGHT - 1, 'bottom', "window")

        # This move is safe, update the position of myself
        self.move_ip(0, distance)
        self.update()

        # Check if it is aligned with the center of the viewpoint (vertical)
        top_idx = self.get_center_vertical_idx() - THRESHOLD
        bottom_idx = self.get_center_vertical_idx() + THRESHOLD
        if top_idx <= int(SCREEN_HEIGHT / 2) <= bottom_idx:
            adjust_distance = int(SCREEN_HEIGHT / 2) - \
                self.get_center_vertical_idx()
            self.move_ip(0, adjust_distance)
            self.update()
            return AlignPoint(int(SCREEN_HEIGHT / 2), 'center', 'window')

        # Check if it is aligned to the center of other nodes
        closest_node = None
        closest_distance = 0
        # Search all nodes that are aligned with self
        for _point in self._center_vertical.get_center_coincident_point():
            left_distance = self.get_left_idx() - _point.node.get_right_idx()
            right_distance = _point.node.get_left_idx() - self.get_right_idx()

            # Check if node ha the smallest distance to self
            update1 = closest_node is None
            update2 = 0 < left_distance < closest_distance
            update3 = 0 < right_distance < closest_distance
            if update1 or update2 or update3:
                closest_node = _point
                if left_distance > 0:
                    closest_distance = left_distance
                else:
                    closest_distance = right_distance

        # Return the node that is aligned with the center of self, if exists
        if closest_node is not None:
            adjust_distance = closest_node.idx - self.get_center_vertical_idx()
            self.move_ip(0, adjust_distance)
            self.update()
            return closest_node

        # Return the node that is aligned with the edge of self
        return self.move_vertically_helper()

    def move_vertically_helper(self) -> AlignPoint:
        """This is the helper function of move_vertically

            The function will find the closest node with a edge aligned with self
        """
        # Find the nodes that is aligned with the edge of self
        nodes_aligned_with_top_edge = self._top.get_side_coincident_point()
        nodes_aligned_with_bottom_edge = self._bottom.get_side_coincident_point()

        (closest_node_to_top_on_left,
         closest_distance_to_top_on_left,
         closest_node_to_top_on_right,
         closest_distance_to_top_on_right
         ) = self.find_aligned_points(nodes_aligned_with_top_edge, 'vertical')

        (closest_node_to_bottom_on_left,
         closest_distance_to_bottom_on_left,
         closest_node_to_bottom_on_right,
         closest_distance_to_bottom_on_right
         ) = self.find_aligned_points(nodes_aligned_with_bottom_edge, 'vertical')

        # Remove aligned nodes which may be blocked by other nodes
        if closest_node_to_top_on_left is not None and \
                self.find_blocking_point(
                    self.get_top_point(),
                    closest_node_to_top_on_left.node,
                    self,
                    'vertical'
                ):
            closest_node_to_top_on_left = None
            closest_distance_to_top_on_left = sys.maxsize

        if closest_node_to_bottom_on_left is not None and \
                self.find_blocking_point(
                    self.get_bottom_point(),
                    closest_node_to_bottom_on_left.node,
                    self,
                    'vertical'
                ):
            closest_node_to_bottom_on_left = None
            closest_distance_to_bottom_on_left = sys.maxsize

        if closest_node_to_top_on_right is not None and \
                self.find_blocking_point(
                    self.get_top_point(),
                    self,
                    closest_node_to_top_on_right.node,
                    'vertical'
                ):
            closest_node_to_top_on_right = None
            closest_distance_to_top_on_right = sys.maxsize

        if closest_node_to_bottom_on_right is not None and \
                self.find_blocking_point(
                    self.get_bottom_point(),
                    self,
                    closest_node_to_bottom_on_right.node,
                    'vertical'
                ):
            closest_node_to_bottom_on_right = None
            closest_distance_to_bottom_on_right = sys.maxsize

        # Output the result, which is the closest node to the moving node
        left_top = closest_distance_to_top_on_left
        left_bottom = closest_distance_to_bottom_on_left
        right_top = closest_distance_to_top_on_right
        right_bottom = closest_distance_to_bottom_on_right

        if closest_node_to_top_on_left is not None and \
                left_top < left_bottom and \
                left_top < right_top and \
                left_top < right_bottom:
            adjust_distance = closest_node_to_top_on_left.idx - \
                self.get_top_idx()
            self.move_ip(0, adjust_distance)
            self.update()
            return closest_node_to_top_on_left

        if closest_node_to_top_on_right is not None and \
                right_top < left_top and \
                right_top < left_bottom and \
                right_top < right_bottom:
            adjust_distance = closest_node_to_top_on_right.idx - \
                self.get_top_idx()
            self.move_ip(0, adjust_distance)
            self.update()
            return closest_node_to_top_on_right

        if closest_node_to_bottom_on_left is not None and \
                left_bottom < left_top and \
                left_bottom < right_top and \
                left_bottom < right_bottom:
            adjust_distance = closest_node_to_bottom_on_left.idx - \
                self.get_bottom_idx()
            self.move_ip(0, adjust_distance)
            self.update()
            return closest_node_to_bottom_on_left

        if closest_node_to_bottom_on_right is not None and \
                right_bottom < left_top and \
                right_bottom < right_top and \
                right_bottom < left_bottom:
            adjust_distance = closest_node_to_bottom_on_right.idx - \
                self.get_bottom_idx()
            self.move_ip(0, adjust_distance)
            self.update()
            return closest_node_to_bottom_on_right

        return None

    def find_aligned_points(
            self,
            points: typing.List[AlignPoint],
            direction='horizontal'):
        """Find the closest aligned point of a given edge

            Each direction would have one
        """

        # Variables used to determine the final result
        first_closest_node = None
        first_closest_distance = sys.maxsize
        second_closest_node = None
        second_closest_distance = sys.maxsize

        for __point in points:
            # Variables used to store temporary value
            first_distance = 0
            second_distance = 0
            if direction == 'horizontal':
                first_distance = self.get_top_idx() \
                    - __point.node.get_bottom_idx()
                second_distance = __point.node.get_top_idx() \
                    - self.get_bottom_idx()
            else:
                first_distance = self.get_left_idx() \
                    - __point.node.get_right_idx()
                second_distance = __point.node.get_left_idx() \
                    - self.get_right_idx()

            if first_distance > 0 and first_closest_node is None:
                first_closest_node = __point
                first_closest_distance = first_distance
            elif 0 < first_distance < first_closest_distance:
                first_closest_node = __point
                first_closest_distance = first_distance
            elif second_distance > 0 and second_closest_node is None:
                second_closest_node = __point
                second_closest_distance = second_distance
            elif 0 < second_distance < second_closest_distance:
                second_closest_node = __point
                second_closest_distance = second_distance

        return (first_closest_node,
                first_closest_distance,
                second_closest_node,
                second_closest_distance)

    def find_blocking_point(
            self,
            line: AlignPoint,
            start: Rectangle,
            end: Rectangle,
            direction='horizontal'):
        """Find if there is a node between begin and end position cut the line

            Return true is the line is blocking, otherwise false
        """

        if start is None or end is None:
            return True

        if direction == 'horizontal':
            __start_point = start.get_bottom_point()
            __end_point = end.get_top_point()

            while __start_point.idx != __end_point.idx:
                if __start_point.node.get_left_idx() < \
                        line.idx < __start_point.node.get_right_idx():
                    return True
                __start_point = __start_point.get__next()

        else:
            __start_point = start.get_right_point()
            __end_point = end.get_left_point()

            while __start_point.idx != __end_point.idx:
                if __start_point.node.get_top_idx() < \
                        line.idx < __start_point.node.get_bottom_idx():
                    return True
                __start_point = __start_point.get__next()

        return False

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
        pygame.draw.rect(self.screen, (0, 191, 255), self)
