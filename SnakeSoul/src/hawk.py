import random
from entity import Fireball
from apples import Apple, GoldenApple, PoisonApple

class Hawk:
    """
    The enemy of Snake. It has the ability to spawn Fireballs and spawn Apples in the game.
    """
    MAX_HEALTH = 3000
    def __init__(self, grid_size):
        """
        Initializes the Hawk object.

        Parameters:
            grid_size (tuple): the Shape of the Grid (number of Cell rows, number of Cell columns).
        """
        self.__health = Hawk.MAX_HEALTH
        self.__mobs = []
        self.__apples = []
        self.__grid_size = grid_size

    def update(self, dt):
        """
        Updates all the Mobs spawned on the Grid.

        Parameters:
            dt (float): the time between function calls (in seconds).
        """
        for m in self.__mobs:
            if m.is_move(dt):
                m.update_pos()

    def spawn_fireball(self):
        """
        Spawns a Fireball randomly on the Grid.
        """
        choice = random.randrange(4)
        if choice == 0:
            self.__mobs.append(Fireball(0, random.randrange(self.__grid_size[1]), 1))
        elif choice == 1:
            self.__mobs.append(Fireball(self.__grid_size[0]-1, random.randrange(self.__grid_size[1]), -1))
        elif choice == 2:
            self.__mobs.append(Fireball(random.randrange(self.__grid_size[0]), 0, 2))
        elif choice == 3:
            self.__mobs.append(Fireball(random.randrange(self.__grid_size[0]), self.__grid_size[1]-1, -2))

    def __spawn_apple(self, type, init_time):
        if type == "apple":
            return Apple(random.randint(0, self.__grid_size[0]-1), random.randint(0, self.__grid_size[1]-1))
        if type == "golden_apple":
            return GoldenApple(random.randint(0, self.__grid_size[0]-1), random.randint(0, self.__grid_size[1]-1), 5, init_time)
        return PoisonApple(random.randint(0, self.__grid_size[0]-1), random.randint(0, self.__grid_size[1]-1), 5, init_time)

    def spawn_apple(self, type, banned_pos, init_time):
        """
        Spawns an Apple with a desired type randomly on the Grid.

        Parameters:
            type (string): the type of the Apple (apple, golden_apple, poison_apple).
            banned_pos (list): a list of xy positions that the Apple cannot be spawned on.
            init_time (float): the game time at which the function is called.
        """
        apple = self.__spawn_apple(type, init_time)
        while apple.get_pos() in banned_pos+[a.get_pos() for a in self.__apples]:
            apple = self.__spawn_apple(type, init_time)
        self.__apples.append(apple)

    def reset_mob(self):
        """
        Deletes all Mobs on the Grid.
        """
        self.__mobs = []

    def heal(self, value):
        """
        Heals the Hawk with a specified amount.

        Parameters:
            value (int): the amount of health to be healed.
        """
        self.__health = min(self.__health + value, Hawk.MAX_HEALTH)

    def damage(self, value):
        """
        Reduces the Hawk's health.

        Parameters:
            value (int): the amount of health to be reduced.
        """
        self.__health = max(self.__health - value, 0)

    def is_dead(self):
        """
        Returns True if Hawk's health dropped to 0, else False.
        """
        return self.__health == 0

    def get_health(self):
        """
        Returns Hawk's current health.
        """
        return self.__health

    def get_mobs(self):
        """
        Returns a list of Mobs currently on the Grid.
        """
        return self.__mobs

    def get_apples(self):
        """
        Returns a list of Apples currently on the Grid.
        """
        return self.__apples

    def get_apple_pos(self):
        """
        Returns a list of Apples' xy position currently on the Grid.
        """
        return [a.get_pos() for a in self.__apples]

    def get_mob_pos(self):
        """
        Returns a list of Mobs' xy position currently on the Grid.
        """
        return [m.get_pos() for m in self.__mobs]
    
    def remove_mob(self, m):
        """
        Removes a specified Mob from the Grid.

        Parameters:
            m (Mob): the Mob to be removed.
        """
        self.__mobs.remove(m)

    def remove_apple(self, a):
        """
        Removes a specified Apple from the Grid.

        Parameters:
            a (Apple): the Apple to be removed.
        """
        self.__apples.remove(a)

    def pop_apple(self, index):
        """
        Removes an Apple from the Grid with a specified index.

        Parameters:
            index (Apple): the index of the Apple to be removed.

        Returns:
            type (string): the type of the Apple.
        """
        type = self.__apples[index].get_type()
        self.__apples.pop(index)
        return type
