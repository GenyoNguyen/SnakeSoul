import colors
from object import Object

class Apple(Object):
    """
    Class for Apple object, inherits Object class.
    """
    def __init__(self, x, y, duration=None, init_time=None):
        """
        Initializes the Apple object.
        
        Parameters:
            x (int): the x position on grid.
            y (int): the y position on grid.
            duration (int): the amount of time (in seconds) in which the apple stays on the screen. If None, it stays forever. Default=None.
            init_time (float): the game time (in seconds) in which the apple is created. Default=None.
        """
        super().__init__(x, y, colors.red, "apple")
        self.__duration = duration
        self.__init_time = int(init_time) if init_time else None

    def is_timeup(self, time):
        """
        Returns True if the duration the apple stays on screen greater than the initialized duration. If init_time or duration is None, returns None.

        Parameters:
            time (float): the game time (in seconds) in which the function is called.
        """
        if self.__init_time and self.__duration:
            return int(time) - self.__init_time >= self.__duration
        return None

    def get_time(self, time):
        """
        Returns the amount of time left (in seconds) before the Apple disappears. If init_time or duration is None, returns None

        Parameters:
            time (float): the game time (in seconds) in which the function is called.
        """
        if self.__init_time and self.__duration:
            return str(self.__duration - int(time) + self.__init_time)
        return None

class GoldenApple(Apple):
    """
    Class for GoldenApple object, inherits Apple class.
    """
    def __init__(self, x, y, duration, init_time):
        """
        Initializes the GoldenApple object.

        Parameters:
            x (int): the x position on grid.
            y (int): the y position on grid.
            duration (int): the amount of time (in seconds) in which the apple stays on the screen. If None, it stays forever.
            init_time (float): the game time (in seconds) in which the apple is created.
        """
        super().__init__(x, y, duration, init_time)
        self._color = colors.gold
        self._type = "golden_apple"

class PoisonApple(Apple):
    """
    Class for PoisonApple object, inherits Apple class.
    """
    def __init__(self, x, y, duration, init_time):
        """
        Initializes the PoisonApple object.

        Parameters:
            x (int): the x position on grid.
            y (int): the y position on grid.
            duration (int): the amount of time (in seconds) in which the apple stays on the screen. If None, it stays forever.
            init_time (float): the game time (in seconds) in which the apple is created.
        """
        super().__init__(x, y, duration, init_time)
        self._color = colors.gray
        self._type = "poison_apple"
