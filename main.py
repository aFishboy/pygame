import pygame, random
pygame.init()

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

class Ant:
    def __init__(self, screen_width, screen_height):
        self.x_pos = random.randint(0, screen_width)
        self.y_pos = random.randint(0, screen_height)
        self.antWidth = 3
        self.antHeight = 10

    def draw(self, screen):
        # Draw the ant as an ellipse
        pygame.draw.ellipse(screen, COLORS["black"], (self.x_pos, self.y_pos, self.antWidth, self.antHeight))

    def update(self):
        # Implement logic to update the ant's position here
        self.x_pos += random.randint(-5, 5)
        self.y_pos += random.randint(-5, 5)

def main():
    WIDTH, HEIGHT = 640, 480
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ant Sim")

    ants = [Ant(WIDTH, HEIGHT) for _ in range(10)]  # Create a list of ant objects

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.fill(COLORS["default"])

        # Draw and update ants
        for ant in ants:
            ant.draw(SCREEN)
            ant.update()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()