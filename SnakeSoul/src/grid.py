import pygame
import colors

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
                pygame.draw.rect(screen, colors.gray, [x, y, self.__cellWidth, self.__cellHeight], 1)
                if cell_text:
                    cell_text = self.__font.render(cell_text, True, colors.white)
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
        
