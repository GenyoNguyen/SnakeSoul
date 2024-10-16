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
