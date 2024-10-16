import os
import pygame
import random
import yaml
from pygame import mixer

with open(os.path.join("SnakeSoul", "config.yml"), "r") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

mixer.init()

mixer.Channel(1).set_volume(0.5)
mixer.Channel(2).set_volume(0.5)
mixer.Channel(3).set_volume(0.5)
mixer.Channel(4).set_volume(0.5)

asset_path = os.path.join("SnakeSoul", "assets")
audio_path = os.path.join("SnakeSoul", "audio")

# Colors
red = (255, 0, 0)
green = (0, 255, 0)
lime = (50, 205, 50)
black = (0, 0, 0)
white = (255, 255, 255)
dark_yellow = (182, 143, 64)
gray = (128, 128, 128)
dark_green = (21, 54, 19)
purple = (128, 0, 128)
orange = (255, 165, 0)
gold = (255, 215, 0)

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
        super().__init__(x, y, red, "apple")
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
        self._color = gold
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
        self._color = gray
        self._type = "poison_apple"

class Bar:
    """
    Class for Bar object.
    """
    def __init__(self, x, y, w, h, color, bg_color, max_val):
        """
        Initializes the Bar object.

        Parameters:
            x (int): the x position of the Bar on the screen.
            y (int): the y position of the Bar on the screen.
            w (int): the width of the Bar (in pixels).
            h (int): the height of the Bar (in pixels).
            color (tuple): RGB color code of the Bar.
            bg_color (tuple): RGB color code for the background of the Bar.
            max_val (int): the value in which the Bar is full.
        """
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__color = color
        self.__bg_color = bg_color
        self.__max_val = max_val
        self.__val = max_val

    def set_val(self, val):
        """
        Sets the current value of the Bar.

        Parameters:
            val (int): value to be set.
        """
        self.__val = val

    def draw(self, screen):
        """
        Draws the bar to the screen.

        Parameters:
            screen (pygame.Surface): the surface in which the Bar is drawn.
        """
        pygame.draw.rect(screen, self.__bg_color, [self.__x, self.__y, self.__w, self.__h])
        pygame.draw.rect(screen, self.__color, [self.__x, self.__y, self.__w*self.__val/self.__max_val, self.__h])
        pygame.draw.rect(screen, "black", [self.__x, self.__y, self.__w, self.__h], 1)

class Button():
    """
    Class for the Button object.
    """
    def __init__(self, pos, text_input, font, base_color, hovering_color):
        """
        Initializes the Button object.

        Parameters:
            pos (tuple): the (x, y) position on which the Button is drawn.
            text_input (string): the text of the Button.
            font (pygame.Font): the font of text_input.
            base_color (tuple): RGB color code for the text when the Button is not hovered.
            hovering_color (tuple): RGB color code for the text when the Button is hovered.
        """
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Draws the Button to the screen.

        Parameters:
            screen (pygame.Surface): the Surface on which the Button is drawn.
        """
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """
        Returns True if the mouse position is in the button box.

        Parameters:
            position (tuple): (x, y) position of the mouse.
        """
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            return True
        return False

    def changeColor(self, position):
        """
        Changes to hovering_color if the mouse position is in the button box, else changes to base_color.

        Parameters:
            position (tuple): (x, y) position of the mouse.
        """
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

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
        super().__init__(x, y, dir, purple, 5)

class Cell:
    """
    Class for Cell object.
    """
    def __init__(self, type, color, text=None):
        """
        Initializes the Cell object.

        Parameters:
            type (string): type of the Cell.
            color (tuple): RGB color code of the Cell.
            text (string): the text to be displayed on top of the Cell (if not None). Default=None.
        """
        self.__type = type
        self.__color = color
        self.__text = text

    def get_type(self):
        """
        Returns type of the Cell.
        """
        return self.__type

    def set_type(self, type):
        """
        Assigns type of the Cell to a different value.

        Parameters:
            type (string): new string for the type of the Cell.
        """
        self.__type = type
    
    def get_color(self):
        """
        Returns the RGB color code of the Cell.
        """
        return self.__color
    
    def set_color(self, color):
        """
        Assigns color of the Cell to a different value.

        Parameters:
            color (tuple): new RGB color code for the color of the Cell.
        """
        self.__color = color

    def get_text(self):
        """
        Returns the text that is drawn on top of the Cell.
        """
        return self.__text

    def set_text(self, text):
        """
        Assigns text of the Cell to a different value.

        Parameters:
            text (string): new string for the text of the Cell.
        """
        self.__text = text

class Grid:
    """
    Class for Grid object.
    """
    def __init__(self, x_offset, y_offset, width, height, dim, font):
        """
        Initializes the Grid object.

        Parameters:
            x_offset (int): the x position on the screen (in pixels) on which the Grid begins to be drawn.
            y_offset (int): the y position on the screen (in pixels) on which the Grid begins to be drawn.
            width (int): 
        """
        self.__x_offset = x_offset
        self.__y_offset = y_offset
        self.__cellWidth = (width-x_offset)/dim[0]
        self.__cellHeight = (height-y_offset)/dim[1]
        self.__dim = dim
        self.__cells = []
        self.__font = font

        for _ in range(dim[0]):
            temp = []
            for _ in range(dim[1]):
                cell = Cell("none", None)
                temp.append(cell)
            self.__cells.append(temp)

    def draw(self, screen):
        """
        Draws the Grid to the screen.

        Parameters:
            screen (pygame.Surface): the surface to be drawn on.
        """
        for i in range(self.__dim[0]):
            for j in range(self.__dim[1]):
                x = self.__x_offset + i*self.__cellWidth
                y = self.__y_offset + j*self.__cellHeight
                cell_color = self.__cells[i][j].get_color()
                cell_text = self.__cells[i][j].get_text()
                if cell_color:
                    pygame.draw.rect(screen, self.__cells[i][j].get_color(), [x, y, self.__cellWidth, self.__cellHeight])
                pygame.draw.rect(screen, gray, [x, y, self.__cellWidth, self.__cellHeight], 1)
                if cell_text:
                    cell_text = self.__font.render(cell_text, True, white)
                    screen.blit(cell_text, cell_text.get_rect(center=(x + self.__cellWidth/2, y + self.__cellHeight/2)))

    def addObject(self, x, y, type, color, text=None):
        """
        Add an object to a Cell on the Grid.

        Parameters:
            x (int): the x position on the Grid.
            y (int): the y position on the Grid.
            type (string): the type of the object.
            color (tuple): RGB color code of the object.
            text (string): the text to be drawn on top of the Cell. Default=None.
        """
        self.__cells[x][y].set_type(type)
        self.__cells[x][y].set_color(color)
        self.__cells[x][y].set_text(text)

    def getShape(self):
        """
        Returns the shape of the Grid (number of Cell rows, number of Cell columns).
        """
        return self.__dim

    def reset(self):
        """
        Resets all the Cells (deletes all objects on the Grid).
        """
        for i in range(self.__dim[0]):
            for j in range(self.__dim[1]):
                self.__cells[i][j].set_type("none")
                self.__cells[i][j].set_color(None)
                self.__cells[i][j].set_text(None)

    def checkBounderies(self, pos):
        """
        Checks if the position is out of the Grid.

        Parameters:
            pos (tuple): xy position to be checked.
        """
        return True if pos[0] >= self.__dim[0] or pos[0] < 0 or pos[1] >= self.__dim[1] or pos[1] < 0 else False

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
        super().__init__(x, y, dir=1, color=green, speed=2)
        self.__snake = [Object(x, y, green, "snake")]
        self.__lives = lives

    def move(self):
        """
        Updates the segments of the Snake.
        """
        self.__snake[0].set_color(green)
        self.__snake.pop()
        self.__snake.insert(0, Object(self._x, self._y, lime, "snake"))

    def grow(self):
        """
        Increase the number of Snake's segments by 1.
        """
        self.__snake[0].set_color(green)
        self.__snake.insert(0, Object(self._x, self._y, lime, "snake"))
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
            del self.__snake[1:]
            self.__update_speed()
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
        index = self.collide(self.get_segments_pos()[1:-1])
        if index != -1:
            self.decay(index+1)
            self.move()
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

# pygame setup
pygame.init()
WIDTH, HEIGHT = int(config["width"]), int(config["height"])
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SnakeSoul")
clock = pygame.time.Clock()

def timer(t):
    min = t//60
    sec = t%60
    return f"{(min//10)%10}{min%10}:{(sec//10)%10}{sec%10}"

def gaussian_blur(surface, radius):
    scaled_surface = pygame.transform.smoothscale(surface, (surface.get_width() // radius, surface.get_height() // radius))
    scaled_surface = pygame.transform.smoothscale(scaled_surface, (surface.get_width(), surface.get_height()))
    return scaled_surface

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(os.path.join(asset_path, "vinque.otf"), size)

def display_text(surface, text, pos, font, color):
    collection = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    x,y = pos
    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)
            word_width , word_height = word_surface.get_size()
            if x + word_width >= WIDTH:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x,y))
            x += word_width + space
        x = pos[0]
        y += word_height

def tutorial():
    click_sound = mixer.Sound(os.path.join(audio_path, "click.mp3"))

    TUTORIAL_TEXT = "Welcome to SnakeSoul!\n\n"\
                    "Your goal is to defeat the Magic Hawk before it defeats you!\n\n"\
                    "How to play:\n"\
                    "- Use WASD to move the snake\n"\
                    "- There are 3 types of apples:\n"\
                    "   + NormalApples(Red): Gain length and damage the Magic Hawk\n"\
                    "   + GoldenApples(Yellow): Gain length, lives and cause severe damage to the Magic Hawk\n"\
                    "   + PoisonApples(Gray): Shorten the snake and heal the Magic Hawk\n\n"\
                    "Sometimes the Magic Hawk will shoot Fireball(Purple). If they touch you, you will decay and the Magic Hawk will heal up.\n\n"\
                    "At night, there will be more Fireballs and there are no GoldenApples.\n\n"\
                    "You have 3 lives. You will lose a live if you run into a Fireball, run out of border or run into yourself.\n"\
                    "If you are out of lives, the game will be over.\n"
    font = get_font(30)

    QUIT_BUTTON = Button(pos=(WIDTH//2, 1000), text_input="MAIN MENU", font=get_font(75), base_color=white, hovering_color=gray)
    
    instruction = 3
    running = True
    while running:
        screen.fill(black)

        display_text(screen, TUTORIAL_TEXT, (20, 20), font, white)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.Channel(1).play(click_sound)
                    instruction = 0
                    running = False

        pygame.display.update()

    return instruction



def victory(game_time):
    click_sound = mixer.Sound(os.path.join(audio_path, "click.mp3"))
    victory_sound = mixer.Sound(os.path.join(audio_path, "victory.mp3"))

    mixer.Channel(0).play(victory_sound)

    MENU_TEXT = get_font(75).render("VICTORY", True, dark_yellow)
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, 400))

    TIME_TEXT = get_font(50).render(f"Time taken: {game_time}", True, white)
    TIME_RECT = TIME_TEXT.get_rect(center=(WIDTH//2, 600))

    QUIT_BUTTON = Button(pos=(WIDTH//2, 800), text_input="MAIN MENU", font=get_font(75), base_color=white, hovering_color=dark_green)

    instruction = 2
    running = True
    while running:
        screen.fill(black)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(TIME_TEXT, TIME_RECT)

        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.Channel(0).play(click_sound)
                    instruction = 0
                    running = False
        pygame.display.update()

    return instruction

def game_over():
    click_sound = mixer.Sound(os.path.join(audio_path, "click.mp3"))
    oof = mixer.Sound(os.path.join(audio_path, "oof.mp3"))
    
    mixer.Channel(0).play(oof)

    MENU_TEXT = get_font(80).render("GAME OVER", True, dark_yellow)
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, 400))

    QUIT_BUTTON = Button(pos=(WIDTH//2, 600), text_input="MAIN MENU", font=get_font(75), base_color=white, hovering_color=dark_green)

    instruction = 2
    running = True
    while running:
        screen.fill(black)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(MENU_TEXT, MENU_RECT)

        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.Channel(1).play(click_sound)
                    instruction = 0
                    running = False
        pygame.display.update()

    return instruction

def pause():
    click_sound = mixer.Sound(os.path.join(audio_path, "click.mp3"))

    mixer.Channel(0).pause()
    mixer.Channel(1).play(click_sound)

    MENU_TEXT = get_font(80).render("SnakeSoul", True, dark_yellow)
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, 400))

    RESUME_BUTTON = Button(pos=(WIDTH//2, 600), text_input="RESUME", font=get_font(75), base_color=white, hovering_color=gray)
    QUIT_BUTTON = Button(pos=(WIDTH//2, 800), text_input="MAIN MENU", font=get_font(75), base_color=white, hovering_color=gray)

    instruction = 0
    running = True
    while running:
        screen.fill(black)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [RESUME_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.Channel(1).play(click_sound)
                    mixer.Channel(0).unpause()
                    instruction = 0
                    running = False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.Channel(1).play(click_sound)
                    instruction = 1
                    running = False
        pygame.display.update()

    return instruction

def menu():
    bg_music = mixer.Sound(os.path.join(audio_path, "dark_soul.mp3"))
    click_sound = mixer.Sound(os.path.join(audio_path, "click.mp3"))
    
    mixer.Channel(0).play(bg_music, loops=-1)
    


    img_file = f"bg{random.randint(1,3)}.jpg"
    bg = pygame.transform.scale(pygame.image.load(os.path.join(asset_path, img_file)), (WIDTH, HEIGHT))

    instruction = 0
    running = True
    while running:
        screen.fill(black)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("SnakeSoul", True, dark_yellow)
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, 200))

        PLAY_BUTTON = Button(pos=(WIDTH//2, 400), text_input="PLAY", font=get_font(75), base_color=white, hovering_color=gray)
        OPTIONS_BUTTON = Button(pos=(WIDTH//2, 600), text_input="TUTORIAL", font=get_font(75), base_color=white, hovering_color=gray)
        QUIT_BUTTON = Button(pos=(WIDTH//2, 800), text_input="QUIT", font=get_font(75), base_color=white, hovering_color=gray)

        screen.blit(gaussian_blur(bg, 5), (0, 0))
        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.Channel(1).play(click_sound)
                    instruction = 1
                    running = False
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.Channel(1).play(click_sound)
                    instruction = 3
                    running = False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.Channel(1).play(click_sound)
                    instruction = -1
                    running = False
        pygame.display.update()
    return instruction


def play():
    fs_index = 1
    
    bg_music = mixer.Sound(os.path.join(audio_path, "c418.mp3"))
    fireball = mixer.Sound(os.path.join(audio_path, "enemy_chaser.mp3"))
    damage = mixer.Sound(os.path.join(audio_path, "damage.mp3"))
    coin = mixer.Sound(os.path.join(audio_path, "coin.mp3"))

    mixer.Channel(0).play(bg_music, loops=-1)

    dt = 0
    prev_game_time = 0
    game_time = 0
    updated_time = 0
    clock.tick(60)

    DAYTIME = 60
    is_day = True

    day = pygame.transform.scale(pygame.image.load(os.path.join(asset_path, "day_sky.jpg")), (WIDTH, 360))
    night = pygame.transform.scale(pygame.image.load(os.path.join(asset_path, "night_sky.jpg")), (WIDTH, 360))
    grass = pygame.transform.scale(pygame.image.load(os.path.join(asset_path, "grass.jpg")), (WIDTH, HEIGHT-360))
    grass2 = pygame.transform.scale(pygame.image.load(os.path.join(asset_path, "grass2.jpg")), (WIDTH, HEIGHT-360))
    hawk_img = pygame.transform.scale(pygame.image.load(os.path.join(asset_path, "hawk.png")).convert_alpha(), (200, 210))
    full_heart = pygame.transform.scale(pygame.image.load(os.path.join(asset_path, "full_heart.png")).convert_alpha(), (50, 50))
    empty_heart = pygame.transform.scale(pygame.image.load(os.path.join(asset_path, "empty_heart.png")).convert_alpha(), (50, 50))


    font = get_font(60)
    game_title = font.render("SnakeSoul", True, dark_yellow)
    title_rect = game_title.get_rect(center=(150, 50))

    SHAPE = [18, 18]
    grid = Grid(0, 360, WIDTH, HEIGHT, SHAPE, get_font(30))

    snake = Snake(SHAPE[0]//2, SHAPE[1]//2, 3)
    dir = snake.getDirection()
    isDirUpdated = False

    hawk = Hawk(grid.getShape())
    hawk.spawn_apple("apple", snake.get_segments_pos(), game_time)
    
    health_bar = Bar(200, 300, 500, 30, red, gray, hawk.MAX_HEALTH)

    instruction = 1
    while True:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            response = pause()
            if response:
                instruction = 0
                break
            clock.tick(60)

        if not isDirUpdated:
            newDir = dir
            if keys[pygame.K_w]:
                newDir = -2
            elif keys[pygame.K_s]:
                newDir = 2
            elif keys[pygame.K_a]:
                newDir = -1
            elif keys[pygame.K_d]:
                newDir = 1
            if newDir != dir:
                isDirUpdated = True
                dir = newDir

        # Day-time switch
        if int(game_time) % DAYTIME == 0 and updated_time:
            is_day = not is_day

        # Game events
        if updated_time:
            if is_day:
                if game_time >= 15 and int(game_time) % 15 in range(5):
                    mixer.Channel(1).play(fireball)
                    hawk.spawn_fireball()
                if game_time >= 30 and int(game_time) % 30 == 0:
                    hawk.spawn_apple("golden_apple", snake.get_segments_pos(), game_time)
            else:
                if game_time >= 15 and int(game_time) % 15 in range(10):
                    mixer.Channel(1).play(fireball)
                    hawk.spawn_fireball()
            if game_time >= 20 and int(game_time) % 20 in range(10):
                hawk.spawn_apple("poison_apple", snake.get_segments_pos(), game_time)
            for apple in hawk.get_apples():
                if apple.get_type() in ["golden_apple", "poison_apple"]:
                    if apple.is_timeup(game_time):
                        hawk.remove_apple(apple)

        # Snake movement
        if snake.is_move(dt):
            mixer.Channel(2).play(mixer.Sound(os.path.join(audio_path, f"footstep{fs_index}.mp3")))
            fs_index += 1
            if fs_index > 4:
                fs_index = 1
            snake.update_pos(dir)
            index = snake.collide(hawk.get_apple_pos())
            if index != -1:
                type = hawk.pop_apple(index)
                if type == "apple":
                    mixer.Channel(4).play(coin)
                    snake.grow()
                    hawk.damage(100)
                    hawk.spawn_apple("apple", snake.get_segments_pos(), game_time)
                elif type == "golden_apple":
                    mixer.Channel(4).play(coin)
                    snake.gain_live()
                    hawk.damage(500)
                    snake.move()
                else:
                    mixer.Channel(3).play(damage)
                    hawk.heal(20)
                    snake.decay(-1)
                    snake.move()
            elif grid.checkBounderies(snake.get_head()):
                snake = Snake(SHAPE[0]//2, SHAPE[1]//2, snake.get_lives()-1)
                hawk.reset_mob()
            elif snake.self_collide():
                snake.lose_live()
            else:
                snake.move()
            isDirUpdated = False


        # Mobs movement
        hawk.update(dt)
        for mob in hawk.get_mobs():
            if grid.checkBounderies(mob.get_pos()):
                hawk.remove_mob(mob)
            index = mob.collide(snake.get_segments_pos())
            if index != -1:
                mixer.Channel(3).play(damage)
                l = snake.decay(index)
                hawk.heal(50*l)
                hawk.remove_mob(mob)

        # End game
        if snake.is_dead():
            instruction = 2
            break
        if hawk.is_dead():
            victory(timer(int(game_time)))
            instruction = 0
            break

        # Adding to grid
        grid.reset()
        for s in snake.getSegments():
            grid.addObject(s.get_x(), s.get_y(), s.get_type(), s.get_color())
        for a in hawk.get_apples():
            grid.addObject(a.get_x(), a.get_y(), a.get_type(), a.get_color(), a.get_time(game_time))
        for mob in hawk.get_mobs():
            grid.addObject(mob.get_x(), mob.get_y(), mob.get_type(), mob.get_color())

        # Updating UI
        timer_str = font.render(timer(int(game_time)), True, white)
        timer_rect = timer_str.get_rect(center=(WIDTH-100, 50))

        health_bar.set_val(hawk.get_health())

        # Drawing
        screen.fill(black)
        if is_day:
            screen.blit(day, (0, 0))
            screen.blit(grass, (0, 360))
        else:
            screen.blit(night, (0, 0))
            screen.blit(grass2, (0, 360))
        grid.draw(screen)
        screen.blit(game_title, title_rect)
        screen.blit(timer_str, timer_rect)
        screen.blit(hawk_img, (0, 160))

        health_bar.draw(screen)

        for i in range(3, 0, -1):
            screen.blit((full_heart if i <= snake.get_lives() else empty_heart), (WIDTH-20-50*i, 100))

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-independent physics.
        dt = clock.tick(60) / 1000
        game_time += dt
        updated_time = int(game_time) - int(prev_game_time)
        prev_game_time = game_time

    return instruction

def main():
    instruction = 0
    while instruction != -1:
        if instruction == 0:
            instruction = menu()
        elif instruction == 1:
            instruction = play()
        elif instruction == 2:
            instruction = game_over()
        elif instruction == 3:
            instruction = tutorial()
    pygame.quit()

main()
