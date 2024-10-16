import colors
from object import Object

class Entity(Object):
    """
    Class for Entity object, inherits the Object class.
    """
    def __init__(self, x, y, dir, color, speed):
        """
        Initializes the Entity object.

        Parameters:
            x (int): the x position on the Grid.
            y (int): the y position on the Grid.
            dir (int): the direction the Entity faces (top: -2, right: 1, down: 2, left: -1).
            color (tuple): RGB color code for the Entity's color.
            speed (int): the movement speed of the Entity (cells per second).
        """
        super().__init__(x, y, color, "mob")
        self._speed = speed
        self._direction = dir    # top: -2, right: 1, down: 2, left: -1
        self._current_time = 0

    def update_pos(self, key=None):
        """
        Updates the Entity's position (and direction) based on key input.

        Parameters:
            key (int): one of the position's valid value (-2, 1, 2, -1). If key is None or the new direction is opposite with the current direction, direction will not be updated. Default=None.
        """
        if key:
            if self._direction + key != 0:
                self._direction = key

        self._x += self._direction if abs(self._direction) == 1 else 0
        if self._direction == 2:
            self._y += 1
        elif self._direction == -2:
            self._y -= 1

    def is_move(self, dt):
        """
        Returns True if the snake hasn't moved after 1/speed (seconds). 

        Parameters:
            dt (float): the amount of time (in seconds) between function calls.
        """
        self._current_time += dt
        if self._current_time > (1/self._speed):
            self._current_time = 0
            return True
        return False

class Fireball(Entity):
    """
    Class for Fireball object, inherits Entity class.
    """
    def __init__(self, x, y, dir):
        """
        Initializes Fireball object.

        Parameters:
            x (int): the x position on the Grid.
            y (int): the y position on the Grid.
            dir (int): the direction the Fireball faces (top: -2, right: 1, down: 2, left: -1).
        """
        super().__init__(x, y, dir, colors.purple, 5)
