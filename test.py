import pygame
import sys
import math

pygame.init()

# Set up the display
WIDTH, HEIGHT = 640, 480
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotated Ellipse")

# Define colors
white = (255, 255, 255)
ellipse_color = (0, 0, 255)  # Blue

# Create an ellipse surface
ellipse_width = 100
ellipse_height = 50
ellipse_surface = pygame.Surface((ellipse_width, ellipse_height), pygame.SRCALPHA)

# Draw the ellipse on the surface
pygame.draw.ellipse(ellipse_surface, ellipse_color, (0, 0, ellipse_width, ellipse_height))

# Define the rotation angle in degrees
angle_degrees = 45

# Rotate the ellipse surface
rotated_ellipse_surface = pygame.transform.rotate(ellipse_surface, angle_degrees)

# Get the rectangle that encloses the rotated ellipse
rotated_ellipse_rect = rotated_ellipse_surface.get_rect()

# Calculate the position to center the rotated ellipse on the screen
x = (WIDTH - rotated_ellipse_rect.width) // 2
y = (HEIGHT - rotated_ellipse_rect.height) // 2

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    SCREEN.fill(white)

    # Draw the rotated ellipse
    SCREEN.blit(rotated_ellipse_surface, (x, y))

    pygame.display.flip()

pygame.quit()
sys.exit()
