class Object:
    """
    Represents an Object on the Grid (Snake's segment, Apple, Fireball,...).
    """
    def __init__(self, x, y, color, type):
        """
        Initializes the Object object.

        Parameters:
            x (int): the x position on the Grid.
            y (int): the y position on the Grid.
            color (tuple): RGB color code for the Object.
            type (string): the type of the Object.
        """
        self._x = x
        self._y = y
        self._color = color
        self._type = type

    def get_x(self):
        """
        Returns the x position on the Grid.
        """
        return self._x
    
    def get_y(self):
        """
        Returns the y position on the Grid.
        """
        return self._y
    
    def get_pos(self):
        """
        Returns the xy position on the Grid (in tuple).
        """
        return self._x, self._y

    def get_color(self):
        """
        Returns RGB color code of the Object (in tuple).
        """
        return self._color

    def set_color(self, color):
        """
        Changes the color of the Object.

        Parameters:
            color (tuple): new RGB color code to change to.
        """
        self._color = color

    def get_type(self):
        """
        Returns the type of the Object.
        """
        return self._type
    
    def collide(self, poses):
        """
        Returns True if the xy position of the Object is the same with any of the given positions, else False.

        Parameters:
            poses (list): a list of xy positions on the Grid to be checked.
        """
        for i in range(len(poses)):
            if (self._x, self._y) == poses[i]:
                return i
        return -1
