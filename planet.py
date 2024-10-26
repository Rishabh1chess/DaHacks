import pygame
import sys
import math
import random
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Black Hole Absorption Simulation")

# Constants
WINDOW_SIZE = (1820, 1050)
G = 6.67408e-11  # Gravitational Constant
MASS_AREA_RATIO = 2e9  # mass in kilograms to area in pixels

# Screen setup
screen = pygame.display.set_mode(WINDOW_SIZE)

# Global variables
planets = []
planet_id = 0
mouse_down = False
mx, my = WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2  # Default mouse position

class Planet:
    def __init__(self, x, y, radius, mass, planet_id):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.planet_id = planet_id
        self.velocity = (0, 0)
        self.last_pos = (x, y)
        self.doneCreating = False
        self.color = random.choice([
            (236, 37, 37), (236, 151, 37), (247, 219, 41),
            (41, 247, 72), (46, 231, 208), (46, 63, 231),
            (221, 53, 232), (255, 84, 180), (255, 165, 0),
            (138, 43, 226), (60, 179, 113), (0, 255, 255),
            (255, 105, 180), (34, 139, 34), (0, 191, 255),
            (255, 215, 0), (139, 0, 139), (255, 69, 0),
            (218, 112, 214), (173, 255, 47)
        ])
        self.trail = []  # List to store trail positions

    def draw(self):
        # Draw a neon-like trail
        if len(self.trail) > 1:
            for i in range(len(self.trail) - 1):
                start_pos = (int(self.trail[i][0]), int(self.trail[i][1]))
                end_pos = (int(self.trail[i + 1][0]), int(self.trail[i + 1][1]))
                
                # Calculate opacity based on trail segment's position (older segments are dimmer)
                opacity = max(30, 255 - (i * 10))  # Gradually decrease opacity
                trail_color = (*self.color, opacity)

                # Draw a glow effect by layering circles with reduced opacity
                for j in range(6):  # Number of glow layers for intensity
                    glow_radius = int(self.radius - j + 4)
                    glow_opacity = max(0, opacity - j * 30)  # Fades with each layer
                    glow_color = (*self.color, glow_opacity)

                    pygame.draw.circle(screen, glow_color, start_pos, glow_radius)

            # Draw a thick, solid neon line along the trail path
            pygame.draw.lines(screen, self.color, False, [(int(tx), int(ty)) for tx, ty in self.trail], 5)

        # Draw the planet with a slightly larger neon outline for more glow
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), int(self.radius + 5), 3)  # Outer glow
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

    def update(self, black_hole):
        self.get_velocity()
        self.collision()
        self.apply_damping_and_pull(black_hole)  # Distance and time-based damping effect
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.mass = math.pi * (self.radius ** 2) * MASS_AREA_RATIO

        # Update trail to appear as a thin line
        if self.doneCreating:  # Only leave a trail after release
            self.trail.append((self.x, self.y))
            if len(self.trail) > 20:  # Limit trail length to keep it thin
                self.trail.pop(0)

        if not self.doneCreating:
            self.create()

    def create(self):
        if self.radius <= 200:
            self.radius += 0.35
        self.x, self.y = mx, my  # Follow mouse position
        self.mass = math.pi * (self.radius ** 2) * MASS_AREA_RATIO

    def get_velocity(self):
        if not self.doneCreating:
            current_pos = [mx, my]
            dpos = [
                (current_pos[0] - self.last_pos[0]) / 2,
                (current_pos[1] - self.last_pos[1]) / 2,
            ]
            self.last_pos = current_pos
            self.velocity = dpos

    def apply_damping_and_pull(self, black_hole):
        # Calculate distance to the black hole
        dx = black_hole.x - self.x
        dy = black_hole.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Stronger damping effect as the planet gets closer to the black hole
        if distance < black_hole.accretion_disk_radius:
            damping_factor = 0.95 - (distance / black_hole.accretion_disk_radius) * 0.3
        else:
            damping_factor = 0.98  # Slow down slightly in outer layers
        
        # Accelerate when close to event horizon for absorption
        if distance < black_hole.radius * 2:
            damping_factor = max(0.8, damping_factor)  # Increase damping inside event horizon
        
        self.velocity = (
            self.velocity[0] * damping_factor,
            self.velocity[1] * damping_factor
        )

    def collision(self):
        # Placeholder for collision detection
        pass

    def draw(self):
        # Draw the trail as a line
        if len(self.trail) > 1:
            pygame.draw.lines(screen, self.color, False, [(int(tx), int(ty)) for tx, ty in self.trail], 1)

        # Draw the planet
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

class BlackHole:
    def __init__(self, x, y, radius, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = (0, 0, 0)
        self.accretion_disk_radius = 3 * self.radius  # Initial accretion disk size

    def draw(self):
        # Draw the black hole
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

        # Draw the accretion disk
        pygame.draw.circle(screen, (150, 150, 150), (int(self.x), int(self.y)), int(self.accretion_disk_radius), 1)

    def update(self, planets):
        for planet in planets:
            dx = self.x - planet.x
            dy = self.y - planet.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            # Prevent division by zero near the center
            if distance < 1:
                distance = 1

            # Determine gravitational force with multi-layer scaling
            pull_strength = self.get_pull_strength(distance)
            force_magnitude = (G * self.mass * planet.mass / (distance ** 2)) * pull_strength
            angle = math.atan2(dy, dx)

            # Calculate gravitational acceleration and apply to planet velocity
            acceleration_x = (math.cos(angle) * force_magnitude) / planet.mass
            acceleration_y = (math.sin(angle) * force_magnitude) / planet.mass
            planet.velocity = (
                planet.velocity[0] + acceleration_x,
                planet.velocity[1] + acceleration_y
            )

            # Immediate absorption if within visual radius of the black hole
            absorption_radius = 1.2 * self.radius
            if distance < absorption_radius + planet.radius:
                planets.remove(planet)  # Absorb planet immediately
                self.grow()  # Increase black hole size and accretion disk

    def get_pull_strength(self, distance):
        # Define gravitational layers with a new innermost "super event horizon" layer
        layer_radii = [100 * self.radius, 200 * self.radius, 400 * self.radius, 600 * self.radius]
        
        # Stronger pull near the event horizon with an added innermost layer
        LAYER_MULTIPLIERS = [0.5, 0.8, 1.0, 1.3]

        if distance <= layer_radii[0]:  # Closest to the black hole (super event horizon)
            return LAYER_MULTIPLIERS[3]  # Strongest pull in super event horizon
        elif layer_radii[0] < distance <= layer_radii[1]:  # Event horizon
            return LAYER_MULTIPLIERS[2]  # Very strong pull near event horizon
        elif layer_radii[1] < distance <= layer_radii[2]:  # Middle layer
            return LAYER_MULTIPLIERS[1]  # Moderate pull
        elif layer_radii[2] < distance <= layer_radii[3]:  # Outermost layer
            return LAYER_MULTIPLIERS[0]  # Weak pull
        else:
            return 0  # No pull beyond the fourth layer

    def grow(self):
        # Increase the black hole's radius and mass by 0.9%
        growth_factor = 1.009
        self.radius *= growth_factor
        self.mass *= growth_factor
        self.accretion_disk_radius = 3 * self.radius  # Adjust accretion disk size to match growth

# Initialize the black hole at the center of the screen
black_hole = BlackHole(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2, 15, 1e15)

def draw():
    screen.fill((25, 25, 25))  # Fill the background
    for planet in planets:
        planet.draw()
    black_hole.draw()
    pygame.display.update()

def main():
    global mx, my, mouse_down, planet_id
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_down = True
                if event.button == 1:  # Left mouse button
                    planets.append(
                        Planet(
                            event.pos[0],
                            event.pos[1],
                            10,
                            math.pi * (10 ** 2) * MASS_AREA_RATIO,
                            planet_id,
                        )
                    )
                    planet_id += 1
            elif event.type == MOUSEBUTTONUP:
                mouse_down = False
                for planet in planets:
                    planet.doneCreating = True
            elif event.type == MOUSEMOTION:
                mx, my = event.pos

        for planet in planets:
            planet.update(black_hole)

        black_hole.update(planets)

        draw()
        clock.tick(60)

if __name__ == "__main__":
    main()
