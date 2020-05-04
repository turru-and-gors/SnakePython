import pygame
import numpy as np

from player import player, body_element, coordinate
import constants


class game():
    def __init__(self):
        """
            Create a new instance of the game.
        """
        # Initialize pygame
        pygame.init()
        
        # Create screen
        self.window = pygame.display.set_mode( (constants.screen_width, constants.screen_height) )
        pygame.display.set_caption("Snake")
        icon = pygame.image.load("res/snake-icon.png")
        pygame.display.set_icon(icon)
        
        # Font
        self.font = pygame.font.Font("res/Arcade.ttf", 40)
        self.text = self.font.render('Snake', True, (221,220,255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (constants.screen_width*0.7, 30)
        
        # Clock
        self.clock = pygame.time.Clock()
        
        # Player
        self.snake = player()
        
        # Food
        self.food = body_element(color=(26,255,213))
        self.__add_new_food__()
        
        self.score = 0
        
    
    def restart(self):
        """
            Restart game.
        """
        self.snake.reset()
        self.score = 0
        
        
    def run(self):
        """
            Main controller for the game.
        """
        running = True
        while running:
            self.clock.tick(5)
            
            running, direction = self.handle_events()
            
            self.snake.set_direction(direction)
            self.snake.move()
            if self.snake.eat(self.food.position):
                self.__add_new_food__()
                self.score += 10
            self.render()
           
        # Closing window before exiting the game
        pygame.display.quit()
        pygame.quit()

        
    def render(self):
        """
            Re-drawing the scene. This methond handles all the rendering,
            including the grid, player and food.
        """
        self.window.fill((0,0,0))
        self.__draw_grid__()
        self.snake.draw(self.window)
        self.food.draw(self.window)
        self.__draw_text__()
        pygame.display.update()
        
        
    def handle_events(self):
        """
            Event handling. An event occurs whe the user presses a key or a
            button in the window. 
        """
        running = True 
        direction = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                if event.key == pygame.K_RIGHT:
                    direction = 'right'
                if event.key == pygame.K_UP:
                    direction = 'up'
                if event.key == pygame.K_DOWN:
                    direction = 'down'
                if event.key == pygame.K_ESCAPE:
                    running = False
                if self.snake.lose:
                    self.restart()
                    
        return running, direction
    
    
    def __draw_grid__(self):
        """
            Draw the grid inside the game window, the grid is just a visual
            hint for controlling the player.
        """
        dw = constants.screen_width // constants.num_rows
        dh = constants.screen_height // constants.num_rows
        grid_color = (128,128,128)
           
        x = 0
        y = 0
        for i in range(constants.num_rows):
            x += dw
            y += dh
               
            pygame.draw.line(self.window, grid_color, (x,0), (x,constants.screen_height))
            pygame.draw.line(self.window, grid_color, (0,y), (constants.screen_width,y))
    
    
    def __draw_text__(self):
        """
            Draw current score when the user is playing, and a placeholder
            text at the beginning and end of the game.
        """
        font_color = (221,220,255)
        if not self.snake.playing and not self.snake.lose:
            self.text = self.font.render('Snake', True, font_color)
        elif self.snake.playing and not self.snake.lose:
            self.text = self.font.render('Score: '+str(self.score), True, font_color)
        else:
            self.text = self.font.render('You lost!', True, font_color)
        self.window.blit(self.text, self.text_rect)
        
    
    def __add_new_food__(self):
        """
            Makes the food appear in a new valid position.
        """
        while True:
            food_pos = coordinate(x=np.random.randint(constants.num_rows),
                              y=np.random.randint(constants.num_rows))
            if not self.snake.in_body(food_pos):
                self.food.set_position(x=food_pos.x, y=food_pos.y)
                return