import colors
from object import Object
from entity import Entity

class Snake(Entity):
    """
    The protagonist, inherits the Entity class.
    """
    MAX_SPEED = 10
    def __init__(self, x, y, lives):
        """
        Initializes the Snake object.

        Parameters:
            x (int): the x position on the Grid.
            y (int): the y position on the Grid.
            lives (int): the number of lives.
        """
        super().__init__(x, y, dir=1, color=colors.green, speed=2)
        self.__snake = [Object(x, y, colors.green, "snake")]
        self.__lives = lives

    def move(self):
        """
        Updates the segments of the Snake.
        """
        self.__snake[0].set_color(colors.green)
        self.__snake.pop()
        self.__snake.insert(0, Object(self._x, self._y, colors.lime, "snake"))

    def grow(self):
        """
        Increase the number of Snake's segments by 1.
        """
        self.__snake[0].set_color(colors.green)
        self.__snake.insert(0, Object(self._x, self._y, colors.lime, "snake"))
        self.__update_speed()

    def decay(self, index):
        """
        Decreases the Snake's segments from the specified index to the end.

        Parameters:
            index (int): the index from which the segments are deleted.
        """
        if index == -1:
            index += len(self.__snake)
        if index == 0:
            self.__lives -= 1
            return len(self.__snake)
        else:
            deleted = len(self.__snake) - index
            del self.__snake[index:]
            self.__update_speed()
            return deleted

    def gain_live(self):
        """
        Increases Snake's lives by 1.
        """
        self.__lives = min(self.__lives + 1, 3)

    def lose_live(self):
        """
        Decreases Snake's lives by 1.
        """
        self.__lives -= 1

    def self_collide(self):
        """
        Returns True if the position of the first segment is the same with the position of any of other segments, else False.
        """
        index = self.collide(self.get_segments_pos()[1:])
        if index != -1:
            self.decay(index)
            return True
        return False

    def is_dead(self):
        """
        Returns True if the number of Snake's lives is 0, else False.
        """
        return self.__lives == 0

    def __update_speed(self):
        self._speed = min(2*(len(self.__snake)//5) + 2, Snake.MAX_SPEED)

    def getSegments(self):
        """
        Returns a list of Snake's segments.
        """
        return self.__snake

    def getDirection(self):
        """
        Returns the current direction of the Snake.
        """
        return self._direction

    def get_segments_pos(self):
        """
        Returns a list of positions of the Snake's segments.
        """
        return [(s._x, s._y) for s in self.__snake]

    def get_head(self):
        """
        Returns the position of the first segment.
        """
        return self._x, self._y

    def get_lives(self):
        """
        Returns the number of lives.
        """
        return self.__lives
