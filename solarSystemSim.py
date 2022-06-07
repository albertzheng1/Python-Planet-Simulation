# All values are real and accurate astronomical units except for radii
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/

import pygame
import math
pygame.init() # initialize pygame module

WIDTH, HEIGHT = 1250, 800 # Declares 2 variables in one line
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Set up a window that takes in coordinates for the size of the window
pygame.display.set_caption("Solar system simulation") # Sets caption (title) of window

# RGB values for colors
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
LIGHT_GREY = (199, 205, 214)
WHITE = (255,255,255)
BLACK = (0, 0, 0)
ORANGE = (168, 86, 13)
LIGHT_YELLOW = (219, 205, 81)
LIGHT_BLUE = (145, 186, 227)
DARK_BLUE = (9, 15, 179)

FONT = pygame.font.SysFont("arial", 12)

FPS = 60

# Template for creating planets
class Planet:
    # Class variables
    AU = 149.6e6 * 1000 # (in m) 1 AU = distance from earth to sun
    G = 6.67428e-11 # Gravitational constant
    SCALE = 20 / AU # 250 / AU -> 1 AU = 100 pixels
    TIMESTEP = 3600 * 24 * 10 # Time it takes to update frame = 10 days

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius # (in pixels)
        self.color = color
        self.mass = mass # (in kg)

        self.orbit = [] # List of all the points that a planet has traveled along
        self.sun = False # Whether or not the "planet" is a sun
        self.distance_to_sun = 0 # Each planet has a unique distance to sun

        self.x_vel = 0
        self.y_vel = 0

    # Draws planet on screen
    def draw(self, win):
        # Shifts reference frame so origin is at center of window
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # Gets list of all updated points to scale
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 1)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        # Create and draw text object
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / (10 * 10**9), 1)}Gm", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    # Returns the x and y components of the gravitational force between two masses
    def attraction(self, other):
        # Calculates the distance (r) between the two masses
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        # Calculates force using Newton's law of gravity
        force = (self.G * self.mass * other.mass) / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        return force_x, force_y

    # Continuously call this function to update position every TIMESTEP (every "day")
    def update_position(self, planets):
        total_fx = total_fy = 0

        # Sums up total forces exerted on planet from other masses
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Updates x and y component of velocity using Newton's second law
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Updates x and y position using velocity
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        # Adds current position to list to allow for drawing the orbit
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    # Create planets
    sun = Planet(0, 0, 5, YELLOW, 1.98892 * 10**30)
    sun.sun = True
    mercury = Planet(0.387 * Planet.AU, 0, 4, DARK_GREY, 0.33 * 10**24)
    mercury.y_vel = -47.4 * 1000  # (in m/s)
    venus = Planet(0.723 * Planet.AU, 0, 7, LIGHT_GREY, 4.87 * 10**24)
    venus.y_vel = -35 * 1000  # (in m/s)
    earth = Planet(1 * Planet.AU, 0, 8, BLUE, 5.97 * 10**24)
    earth.y_vel = -29.8 * 1000 # (in m/s)
    mars = Planet(1.524 * Planet.AU, 0, 6, RED, 0.642 * 10**24)
    mars.y_vel = -24.1 * 1000 # (in m/s)
    jupiter = Planet(5.204 * Planet.AU, 0, 20, ORANGE, 1898 * 10**24)
    jupiter.y_vel = -13.1 * 1000 # (in m/s)
    saturn = Planet(9.572 * Planet.AU, 0, 16, LIGHT_YELLOW, 568 * 10**24)
    saturn.y_vel = -9.7 * 1000 # (in m/s)
    uranus = Planet(19.165 * Planet.AU, 0, 10, LIGHT_BLUE, 86.8 * 10**24)
    uranus.y_vel = -6.8 * 1000 # (in m/s)
    neptune = Planet(30.181 * Planet.AU, 0, 12, DARK_BLUE, 102 * 10**24)
    neptune.y_vel = -5.4 * 1000 # (in m/s)
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    # Pygame event loop that runs while the simulation is going on
    while run:
        clock.tick(FPS)
        WIN.fill(BLACK)

        # Traverses list of all the events that occur
        for event in pygame.event.get():
            # Checks if user has clicked exit button
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    # Quits simulation
    pygame.quit()

# Begin simulation
main()
