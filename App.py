import pygame
import numpy as np
from random import randint

# Initialize Pygame
pygame.init()

screen_info = pygame.display.Info()
winSize = (screen_info.current_w, screen_info.current_h)
win = pygame.display.set_mode(winSize, pygame.FULLSCREEN)

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  # Sun
BLUE = (0, 0, 255)  # Planet

# Constants for simulation
AU_to_pixels = 15  # Scale: 1 AU = 300 pixels
center_x, center_y = winSize[0] // 2, winSize[1] // 2  # Center screen

# Planetary Data (Example: Earth)
a_AU = 1.0  # Semi-major axis in AU
e = 0.017  # Eccentricity

sun_radius = 6.95700e8

stars = [((randint(150, 200), randint(150, 200), randint(150, 200)), (randint(1, winSize[0]), randint(1, winSize[1])), randint(1, 2)) for _ in range(250)]
def draw_stars():
    for star in stars:
        pygame.draw.circle(win, star[0], star[1], star[2])


solar_system_data = {
    "Mercury": {
        "colour": (169, 169, 169),
        "Mass_kg": 3.301e23,
        "Radius_m": 2.4397e6,
        "Semi_Major_Axis_m": 5.79e10,
        "a_AU": 0.387,
        "e": 0.206,
        "Orbital_Period_s": 7.60e6,
        "Orbital_Velocity_m_s": 4.788e4,
        "GM_m3_s2": 2.2032e13
    },
    "Venus": {
        "colour": (255, 165, 0),
        "Mass_kg": 4.867e24,
        "Radius_m": 6.0518e6,
        "Semi_Major_Axis_m": 1.08e11,
        "a_AU": 0.723,
        "e": 0.007,
        "Orbital_Period_s": 1.94e7,
        "Orbital_Velocity_m_s": 3.503e4,
        "GM_m3_s2": 3.2486e14
    },
    "Earth": {
        "colour": (0, 0, 255),
        "Mass_kg": 5.972e24,
        "Radius_m": 6.371e6,
        "Semi_Major_Axis_m": 1.50e11,
        "a_AU": 1.000,
        "e": 0.017,
        "Orbital_Period_s": 3.16e7,
        "Orbital_Velocity_m_s": 2.979e4,
        "GM_m3_s2": 3.986e14
    },
    "Mars": {
        "colour": (0, 0, 255),
        "Mass_kg": 6.417e23,
        "Radius_m": 3.3895e6,
        "Semi_Major_Axis_m": 2.28e11,
        "a_AU": 1.524,
        "e": 0.093,
        "Orbital_Period_s": 5.93e7,
        "Orbital_Velocity_m_s": 2.413e4,
        "GM_m3_s2": 4.2828e13
    },
    "Jupiter": {
        "colour": (255, 0, 0),
        "Mass_kg": 1.898e27,
        "Radius_m": 6.9911e7,
        "Semi_Major_Axis_m": 7.78e11,
        "a_AU": 5.204,
        "e": 0.049,
        "Orbital_Period_s": 3.74e8,
        "Orbital_Velocity_m_s": 1.306e4,
        "GM_m3_s2": 1.2669e17
    },
    "Saturn": {
        "colour": (210, 180, 140),
        "Mass_kg": 5.683e26,
        "Radius_m": 5.8232e7,
        "Semi_Major_Axis_m": 1.43e12,
        "a_AU": 9.582,
        "e": 0.056,
        "Orbital_Period_s": 9.29e8,
        "Orbital_Velocity_m_s": 9.645e3,
        "GM_m3_s2": 3.7931e16
    },
    "Uranus": {
        "colour": (0, 255, 255),
        "Mass_kg": 8.681e25,
        "Radius_m": 2.5362e7,
        "Semi_Major_Axis_m": 2.87e12,
        "a_AU": 19.201,
        "e": 0.046,
        "Orbital_Period_s": 2.65e9,
        "Orbital_Velocity_m_s": 6.800e3,
        "GM_m3_s2": 5.7939e15
    },
    "Neptune": {
        "colour": (0, 0, 139),
        "Mass_kg": 1.024e26,
        "Radius_m": 2.4622e7,
        "Semi_Major_Axis_m": 4.50e12,
        "a_AU": 30.070,
        "e": 0.010,
        "Orbital_Period_s": 5.20e9,
        "Orbital_Velocity_m_s": 5.432e3,
        "GM_m3_s2": 6.8365e15
    }
}

# Find the maximum planet radius from the data
max_radius = max(data["Radius_m"] for data in solar_system_data.values())

# Define the desired maximum planet radius on the screen (e.g., 30 pixels)
desired_max_radius = 100

# Calculate the scaling factor
scaling_factor = desired_max_radius / (sun_radius / 1e6)  # Convert meters to kilometers and scale
print(scaling_factor)

# Function to calculate orbit position
def get_orbit_position(theta, a, e):
    """Compute (x, y) position for given true anomaly theta."""
    r = (a * (1 - e**2)) / (1 + e * np.cos(theta))  # Orbital equation
    x = r * np.cos(theta)  # Convert to Cartesian
    y = r * np.sin(theta)
    return int(center_x + x), int(center_y - y)  # Translate to screen center

# Generate orbit paths for all planets
orbit_paths = {}
for planet, data in solar_system_data.items():
    a_pixels = (data["Semi_Major_Axis_m"] / 1.50e11) * AU_to_pixels  # Normalize based on Earth's semi-major axis
    e = data["e"]
    
    num_points = 360
    theta_vals = np.linspace(0, 2 * np.pi, num_points)
    orbit_paths[planet] = [get_orbit_position(theta, a_pixels, e) for theta in theta_vals]

# Simulation loop
running = True
theta_values = {planet: 0 for planet in solar_system_data}  # Start position for each planet
clock = pygame.time.Clock()

zoom_factor = 1.0  # Initial zoom level

while running:
    win.fill((0, 0, 0))  # Clear screen

    draw_stars()

    SUN_RELATIVE_SIZE = 0.2 
    sun_scaled_radius = max(10, SUN_RELATIVE_SIZE * AU_to_pixels * zoom_factor)


    # Draw the Sun
    pygame.draw.circle(win, YELLOW, (center_x, center_y), int(sun_scaled_radius))

    for planet, data in solar_system_data.items():
        a_pixels = data["a_AU"] * AU_to_pixels * zoom_factor  # Apply zoom factor to orbit
        e = data["e"]
        orbital_period = data["Orbital_Period_s"]

        orbit_scaled = [
            get_orbit_position(theta, a_pixels, e)  # Now recalculating with zoom
            for theta in np.linspace(0, 2 * np.pi, 360)
        ]
        pygame.draw.aalines(win, WHITE, True, orbit_scaled, 1)

        # Update planet position
        theta_values[planet] += 0.002 * (3.16e7 / orbital_period)  # Adjust speed based on Planet's period
        theta_values[planet] %= 2 * np.pi  # Keep within range

        # Compute new planet position using **zoomed orbit parameters**
        planet_x, planet_y = get_orbit_position(theta_values[planet], a_pixels, e)

        # **Fix 2: Correct planet scaling**
        scaled_radius = data["Radius_m"] / 1e6 * scaling_factor * zoom_factor
        pygame.draw.circle(win, data["colour"], (planet_x, planet_y), int(scaled_radius))

    # Refresh display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Zoom in
                zoom_factor *= 1.1
            if event.key == pygame.K_DOWN:  # Zoom out
                zoom_factor /= 1.1


pygame.quit()
