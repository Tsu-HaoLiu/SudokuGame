import pygame
import time



# set width/height of game
WIDTH, HEIGHT = 480, 800
surface = pygame.display.set_mode((WIDTH, HEIGHT))
print(surface)

# internal clock
clock = pygame.time.Clock()

# global colors
color_white = (255, 255, 255)
safety_base_color = pygame.Color('#383B35')
safety_base_inverse = pygame.Color(255-safety_base_color.r, 255-safety_base_color.b, 255-safety_base_color.g)
safety_secondary_color = pygame.Color('#AEC99E')
safety_secondary_inverse = pygame.Color(255-safety_secondary_color.r, 255-safety_secondary_color.b, 255-safety_secondary_color.g)
hardsolved_circles = pygame.Color('#646762')  # Grey

