import math
import pygame
from random import randint, uniform
pygame.init()

vec = pygame.math.Vector2

COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203),
    "brown": (165, 42, 42),
    "gray": (128, 128, 128),
    "light_gray": (211, 211, 211),
    "dark_gray": (169, 169, 169),
    "default": (29, 34, 27),
}

FPS = 30
WIDTH, HEIGHT = 640, 480
MAX_SPEED = 10
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
APPROACH_RADIUS = 120
FONT = pygame.font.Font(None, 20)


class Ant:
    def __init__(self, screen_width, screen_height):
        self.pos = vec(randint(0, WIDTH), randint(0, HEIGHT))
        self.vel =vec(MAX_SPEED,0).rotate(uniform(0, 360))
        self.acc = vec(0,0)
        self.antWidth = 3
        self.antHeight = 10

    def follow_mouse(self):
        mpos = pygame.mouse.get_pos()
        self.acc = (mpos - self.pos).normalize() * 0.5
    
    def ant_color(self):
        red_value = int(140 - (((self.vel.x + self.vel.y) // 2) * 14))
        if red_value > 255:
            red_value = 255
        if red_value < 0:
            red_value = 0
        color = (red_value, 0 , 0)
        return color

    def draw(self, screen):
        # Create an ellipse Surface
        ellipse_surface = pygame.Surface((self.antWidth, self.antHeight), pygame.SRCALPHA)
        pygame.draw.ellipse(ellipse_surface, self.ant_color(), (0, 0, self.antWidth, self.antHeight))
        # Rotate the ellipse
        angle = math.degrees(math.atan2(self.vel.y, self.vel.x))
        rotated_surface = pygame.transform.rotate(ellipse_surface, angle + 90)

        # Get the rect of the rotated ellipse
        rotated_rect = rotated_surface.get_rect()
        rotated_rect.center = self.pos  # Set the center of the rotated ellipse
        
        # Draw the rotated ellipse onto the screen
        screen.blit(rotated_surface, rotated_rect.topleft)

    def update(self):
        #equations of motion
        self.follow_mouse()
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        if self.pos.x < 0 or self.pos.x > WIDTH or self.pos.y < 0 or self.pos.y > HEIGHT:
            self.pos.x = min(WIDTH - 1, max(0, self.pos.x))
            self.pos.y = min(HEIGHT - 1, max(0, self.pos.y))
    
    def draw_vectors(self):
        scale = 3
        # vel
        pygame.draw.line(SCREEN, COLORS["green"], self.pos, (self.pos + self.vel * scale), 4)
        # desired
        pygame.draw.line(SCREEN, COLORS["red"], self.pos, (self.pos + vec(1,1) * scale), 4)
        # approach radius
        pygame.draw.circle(SCREEN, COLORS["white"], pygame.mouse.get_pos(), APPROACH_RADIUS, 1)


def main():
    
    pygame.display.set_caption("Ant Sim")

    ants = [Ant(WIDTH, HEIGHT) for _ in range(2000)]  # Create a list of ant objects

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.fill(COLORS["light_gray"])
        # Calculate FPS
        current_fps = int(clock.get_fps())
        # Render the FPS text
        fps_text = FONT.render(f"FPS: {current_fps}", True, (255, 255, 255))
        # Draw the FPS text on the screen at position (10, 10)
        SCREEN.blit(fps_text, (10, 10))

        # Draw and update ants
        for ant in ants:
            ant.draw(SCREEN)
            ant.update()
            ant.draw_vectors()          

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()