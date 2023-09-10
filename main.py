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
WIDTH, HEIGHT = 1280, 960
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 25)

ANT_COUNT = 2000
ANT_WIDTH = 3
ANT_HEIGHT = 10

ACCEL = 0.5 # Only used with follow mouse function

MAX_SPEED = 10
SEEK_FORCE = 0.3
APPROACH_RADIUS = 500

WANDER_RING_RADIUS = 200
WANDER_RING_DISTANCE = 50

def normalizeSafe(vec):
    if vec.length() == 0:
            vec = pygame.Vector2(1, 0)
    else:
        vec = vec.normalize()
    return vec

class Ant:
    def __init__(self, screen_width, screen_height):
        self.pos = pygame.Vector2(randint(0, WIDTH), randint(0, HEIGHT))
        self.vel = pygame.Vector2(0,0).rotate(uniform(0, 360))
        self.acc = pygame.Vector2(0,0)
        self.antWidth = ANT_WIDTH
        self.antHeight = ANT_HEIGHT
        self.target = pygame.Vector2(randint(0,WIDTH), randint(0,HEIGHT))
        self.last_target = 0
        self.displacement = pygame.Vector2(0, 0)
    
    def ant_color(self):
        red_value = int(150 - ((abs((self.vel.x + self.vel.y)) // 2) * 16))
        if red_value > 255:
            red_value = 255
        if red_value < 0:
            red_value = 0
        color = (red_value, 0 , 0)
        return color

    def follow_mouse(self):
        mpos = pygame.mouse.get_pos()
        vec_to_normalize = mpos - self.pos
        if vec_to_normalize.length() == 0:
            vec_to_normalize = pygame.Vector2(1, 0)
        self.acc = vec_to_normalize.normalize() * ACCEL
    
    def seek(self, target):
        vec_to_normalize = target - self.pos
        vec_to_normalize = normalizeSafe(vec_to_normalize)
        self.desired = vec_to_normalize * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > SEEK_FORCE:
            steer.scale_to_length(SEEK_FORCE)
        return steer
    
    def flee(self, target):
        vec_to_normalize = self.pos - target
        distance = vec_to_normalize.length()
        vec_to_normalize = normalizeSafe(vec_to_normalize)
        
        if distance < APPROACH_RADIUS:
            self.desired = vec_to_normalize * MAX_SPEED
        else:
            self.desired = pygame.Vector2(0,0)

        steer = (self.desired - self.vel)
        if steer.length() > SEEK_FORCE:
            steer.scale_to_length(SEEK_FORCE)
        return steer
    
    def wander(self):
        now = pygame.time.get_ticks()
        if now - self.last_target > 500:
            self.last_target = now
            self.target = pygame.Vector2(randint(0,WIDTH), randint(0,HEIGHT))
        return self.seek(self.target)
    
    def wander_improved(self):
        if self.vel.length() == 0:
            self.vel = pygame.Vector2(1, 0)
        circle_pos = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        target = circle_pos + pygame.Vector2(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
        self.displacement = target
        return self.seek(target)

    
    def seek_with_approach(self, target):
        vec_to_normalize = target - self.pos
        distance = vec_to_normalize.length()
        
        # Handle the case where the vector to normalize is zero
        if vec_to_normalize.length() == 0:
            vec_to_normalize = pygame.Vector2(1, 0)

        vec_to_normalize.normalize_ip()
        self.desired = vec_to_normalize

        if distance < APPROACH_RADIUS:
            self.desired *= distance / APPROACH_RADIUS * MAX_SPEED
        else:
            self.desired *= MAX_SPEED

        steer = self.desired - self.vel

        if steer.length() > SEEK_FORCE:
            steer.scale_to_length(SEEK_FORCE)

        return steer

    def update(self, mode):
        #equations of motion
        #self.follow_mouse()
        if mode == "Flee":
            self.acc = self.flee(pygame.mouse.get_pos())
        elif mode == "Wander":
            self.acc = self.wander_improved()
        else:
            self.acc = self.seek(pygame.mouse.get_pos())

        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        if self.pos.x < 0 or self.pos.x > WIDTH or self.pos.y < 0 or self.pos.y > HEIGHT:
            self.pos.x = min(WIDTH - 1, max(0, self.pos.x))
            self.pos.y = min(HEIGHT - 1, max(0, self.pos.y))
    
    def draw(self, screen):
        # Create an ellipse Surface
        ellipse_surface = pygame.Surface((self.antWidth, self.antHeight), pygame.SRCALPHA)
        pygame.draw.ellipse(ellipse_surface, self.ant_color(), (0, 0, self.antWidth, self.antHeight))
        # Rotate the ellipse
        angle = math.degrees(math.atan2(self.vel.y, self.vel.x))
        rotated_surface = pygame.transform.rotate(ellipse_surface, -angle - 90)

        # Get the rect of the rotated ellipse
        rotated_rect = rotated_surface.get_rect()
        rotated_rect.center = self.pos  # Set the center of the rotated ellipse
        
        # Draw the rotated ellipse onto the screen
        screen.blit(rotated_surface, rotated_rect)

    def draw_vectors(self):
        scale = 4
        # vel
        pygame.draw.line(SCREEN, COLORS["green"], self.pos, (self.pos + self.vel * scale), 4)
        # desired
        pygame.draw.line(SCREEN, COLORS["red"], self.pos, (self.pos + self.desired * scale), 4)
        # target
        center = self.pos + normalizeSafe(self.vel) * WANDER_RING_DISTANCE
        pygame.draw.circle(SCREEN, COLORS["white"], (int(center.x), int(center.y)), WANDER_RING_RADIUS, 1)
        pygame.draw.line(SCREEN, COLORS["cyan"], center, self.displacement, 5)


def main():
    pygame.display.set_caption("Ant Sim")

    ants = [Ant(WIDTH, HEIGHT) for _ in range(ANT_COUNT)]  # Create a list of ant objects
    show_vectors = False
    paused = False
    current_mode = "Seek"

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    show_vectors = not show_vectors
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if current_mode == "Seek":
                        current_mode = "Flee"
                    elif current_mode == "Flee":
                        current_mode = "Wander"
                    elif current_mode == "Wander":
                        current_mode = "Seek"
                if event.key == pygame.K_p:
                    paused = not paused
        SCREEN.fill(COLORS["light_gray"])
        # Calculate FPS
        current_fps = int(clock.get_fps())
        # Render the FPS text
        fps_text = FONT.render(f"FPS: {current_fps}", True, (255, 255, 255))
        mode_text = FONT.render(f"Mode: {current_mode}", True, (255, 255, 255))
        # Draw the FPS text on the screen at position (10, 10)
        SCREEN.blit(fps_text, (10, 10))
        SCREEN.blit(mode_text, (10, 50))


        if not paused:
            # Draw and update ants
            for ant in ants:
                ant.draw(SCREEN)
                ant.update(current_mode)
                if show_vectors:
                    ant.draw_vectors()          

            pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()