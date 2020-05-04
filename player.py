import pygame
import constants


class coordinate:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = x
    


class body_element:
    def __init__(self, color=(123, 131, 255)):
        """
            Each element forming the body of the snake.
            
            :param color: RGB color of the body element. Values must be in range [0,255].
            :type color: (integer, integer, integer)
        """
        self.color = color
        self.position = coordinate()
        self.step = coordinate(x = constants.screen_width/constants.num_rows,
                               y = constants.screen_height/constants.num_rows)
        
        
    def set_position(self, x, y):
        """
            Set current position of this body element.
            
            :param x: Horizontal coordinate, in range [0, constants.num_rows].
            :type x: integer
            
            :param y: Vertical coordinate, in range [0, constants.num_rows].
            :type y: integer
        """
        self.position.x = x
        self.position.y = y
            
        
    def draw(self, surface):
        """
            Draw the body element in the current position.
            
            :param surface: Pygame surface where the rendering will be performed.
            :type surface: Pygame display.
        """
        x = self.position.x * self.step.x
        y = self.position.y * self.step.y
        
        pygame.draw.rect(surface, self.color, (x, y, self.step.x, self.step.y))
        
    

class player:
    def __init__(self, color=(125, 131, 255)):
        """
            Snake player.
        """
        self.color = color
        self.speed = coordinate()
        
        self.body = []
        self.head = None
        self.direction = None
        self.playing = None
        self.lose = None
        self.reset()
        
    
    def reset(self):
        """
            Restart game
        """
        self.body.clear()
        self.head = body_element(self.color)
        self.head.set_position(x=constants.num_rows//2, 
                               y=constants.num_rows//2)
        self.body.append(self.head)
        
        self.direction = None
        self.playing = False
        self.lose = False
        
        
    def set_direction(self, direction=None):
        """
            Set the direction at which the head moves.
            
            :param direction: 'right', 'left', 'up' or 'down'
            :type direction: string
        """
        if direction == None:
            return
        
        # If current direction is equal to new direction, ignore
        if self.direction == direction:
            return
        # If attempting to go in opposite direction, ignore
        if self.direction == "right" and direction == "left" or \
            self.direction == "left" and direction == "right":
                return
        if self.direction == "up" and direction == "down" or \
            self.direction == "down" and direction == "up":
                return
        
        self.direction = direction
        if direction == 'right':
            self.speed.x = 1
            self.speed.y = 0
        elif direction == 'left':
            self.speed.x = -1
            self.speed.y = 0
        elif direction == 'up':
            self.speed.x = 0
            self.speed.y = -1
        else:
            self.speed.x = 0
            self.speed.y = 1 
            
        if not self.playing:
            self.playing = True
        
            
    def __move_head__(self):
        """
            Update the position of the head, according to the stated direction.
            If the head goes beyond the limit of the grid, it reappears
            on the opposite border.
        """
        self.head.position.x += self.speed.x
        if self.head.position.x >= constants.num_rows:
            self.head.position.x = 0
        elif self.head.position.x < 0:
            self.head.position.x = constants.num_rows-abs(self.speed.x)
            
        self.head.position.y += self.speed.y
        if self.head.position.y >= constants.num_rows:
            self.head.position.y = 0
        elif self.head.position.y < 0:
            self.head.position.y = constants.num_rows-abs(self.speed.y)
            
    
    def __collision_detected__(self):
        """
            Check if the body collided with itself.
            
            :return: True if there was collision (lose game), False otherwise.
        """
        for i in range(len(self.body)-1, 0, -1):
            if self.head.position.x == self.body[i].position.x and \
                self.head.position.y == self.body[i].position.y:
                    return True
        return False
        
        
    def move(self):
        """
            Moves the body of the snake to the next position.
        """
        if not self.playing or self.lose:
            return 
        
        for i in range(len(self.body)-1, 0, -1):
            self.body[i].position.x = self.body[i-1].position.x
            self.body[i].position.y = self.body[i-1].position.y
        self.__move_head__()
        if self.__collision_detected__():
            self.lose = True
        
        
    def draw(self, surface):
        """
            Redraws the player.
            
            :param surface: Pygame surface where the rendering will be performed.
            :type surface: Pygame display.
        """
        for elem in self.body:
            elem.draw(surface)
            
            
    def eat(self, position):
        """
           Add a new body element. 
           
           :param position: Position of the food to take.
           :type position: player.coordinate
           
           :return: True if the player could eat the food, False otherwise.
           :rtype: boolean.
        """
        if self.head.position.x == position.x and \
            self.head.position.y == position.y:
                new_elem = body_element(self.color)
                self.body.append(new_elem)
                return True
        return False
        
        
    def in_body(self, position):
        """
            Check if the given position is being used by one element in the body.
            
            :param position: Position to check.
            :type position: player.coordinate
        """
        for elem in self.body:
            if position.x == elem.position.x and \
                position.y == elem.position.y:
                    return True
        return False
                