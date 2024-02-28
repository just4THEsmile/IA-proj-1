import pygame
import sys
import math

# Define hexagon properties
hex_size = 40
horizontal_distance = hex_size * math.sqrt(3)
vertical_distance = hex_size * 1.5
WIDTH, HEIGHT =1920, 1080
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ABOYNE  !!!!")

# Define colors
WHITE = (255, 255, 255)
BLACK = (50, 50, 50)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

def draw_hexagon(x, y, size, color):
    """
    Draw a hexagon on the Pygame window.
    """
    points = []
    for i in range(6):
        angle_deg = 60 * i + 30
        angle_rad = math.radians(angle_deg)
        points.append((x + size * math.cos(angle_rad),
                       y + size * math.sin(angle_rad)))
    pygame.draw.polygon(WINDOW, color, points)
    pygame.draw.polygon(WINDOW, WHITE, points, 1)

def draw_circle(x, y, size, color):
    """
    Draw a circle on the Pygame window.
    """
    pygame.draw.circle(WINDOW, color, (x, y), 10)

def draw_board(board):
    """
    Draw the hexagonal board grid.
    """
    WINDOW.fill(WHITE)
    for position, stone in board.items():
        if stone:
            stone.draw()
        else:
            x, y = position
            draw_hexagon(x, y, hex_size, BLACK)


    def draw(self):
        # Draw stone on the board
        x, y = self.position
        draw_hexagon(x, y, hex_size, BLACK)
        draw_circle(x, y, hex_size, self.color,)                  

