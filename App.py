import math
import tkinter as tk
import turtle
import time

g = 6.67430e-11

def forRadius(g, m, v):
    return g * m / v ** 2

def forVelocity(m, r, g):
    return math.sqrt(g * m / r)

def forMass(v, r, g):
    return v ** 2 * r / g

# Global animation and zoom parameters
angle = 0
step_time = 20  # Milliseconds per frame
zoom_scale = 1.0  # Zoom level (1.0 = default)
offset_x, offset_y = 0, 0  # Viewport offset
panning = False  # Track if panning is active
pan_start_x, pan_start_y = 0, 0  # Start position of panning
velocity = 0  # Global variable to store velocity
actual_radius = 0  # Global variable to store the actual radius

def submit():
    global velocity, actual_radius, r1, r2  # Make actual_radius a global variable
    mass_input = mass_entry.get()
    radius_input = radius_entry.get()
    velocity_input = velocity_entry.get()
    r1 = radius_inOrbit_entry.get()
    r2 = radius_NotinOrbit_entry.get()

    check = False
    r = None  # Ensure r is defined here

    try:
        r1 = float(r1)
        r2 = float(r2)

        try:
            m = float(mass_input)
        except ValueError:
            try:
                v = float(velocity_input)
                r = float(radius_input)
                m = forMass(v, r, g)
                check = True
            except ValueError:
                print("Invalid input.")

        if not check:
            try:
                v = float(velocity_input)
            except ValueError:
                try:
                    m = float(mass_input)
                    r = float(radius_input)
                    v = forVelocity(m, r, g)
                    check = True
                except ValueError:
                    print("Invalid input.")

        if not check:
            try:
                r = float(radius_input)
            except ValueError:
                try:
                    m = float(mass_input)
                    v = float(velocity_input)
                    r = forRadius(g, m, v)
                    check = True
                except ValueError:
                    print("Invalid input.")      
    except ValueError:
            print("Invalid input.") 

    # Ensure r is assigned a value
    if r is not None:
        velocity = v  # Store the calculated or provided velocity globally
        actual_radius = r  # Store the actual radius globally
        Graphics(r, velocity)
    else:
        print("Please provide valid input for radius, mass, or velocity.")



    velocity = v  # Store the calculated or provided velocity globally
    actual_radius = r  # Store the actual radius globally
    Graphics(r, velocity)

def update_position():
    global angle, planet, scaled_radius, angle_step

    # Calculate new position with zoom and pan offset
    x = offset_x + (scaled_radius * zoom_scale) * math.cos(math.radians(angle))
    y = offset_y + (scaled_radius * zoom_scale) * math.sin(math.radians(angle))
    planet.goto(x, y)

    angle += angle_step
    if angle >= 360:
        angle -= 360  # Keep angle in range

    turtle.update()
    turtle.ontimer(update_position, step_time)

def redraw_orbit():
    global orbit_drawer, text_turtle, scaled_radius, velocity, actual_radius, scaling_factor, planet

    # Ensure scaling_factor is calculated before use
    if 'scaling_factor' not in globals():
        scaling_factor = actual_radius / scaled_radius  # Default scaling factor if not calculated before

    # Clear previous drawings
    orbit_drawer.clear()
    text_turtle.clear()

    # Clear the planet (if it exists) before redrawing it
    if planet:
        planet.clear()

    # Draw the orbit (affected by zoom)
    orbit_drawer.penup()
    orbit_drawer.goto(offset_x, offset_y - (scaled_radius * zoom_scale))
    orbit_drawer.pendown()
    orbit_drawer.circle(scaled_radius * zoom_scale)
    orbit_drawer.penup()

    # Draw the planet at the center (scaled according to r2 and scaling_factor)
    planet_radius = r2 * scaling_factor  # Scale the planet radius
    planet = turtle.Turtle()  # Create a new planet turtle each time
    planet.shape("circle")
    planet.color("blue")
    planet.shapesize(planet_radius / 10)  # Scale the planet size
    planet.penup()
    planet.goto(offset_x, offset_y)  # Place it at the center of the orbit
    planet.stamp()  # Stamp the planet shape at the center of the orbit

    # Display velocity and scaling factor at fixed positions
    text_turtle.penup()
    text_turtle.goto(-350, 335)
    text_turtle.write(f"Velocity: {velocity:.2f} m/s", align="left", font=("Arial", 12, "normal"))

    text_turtle.goto(-350, 350)
    text_turtle.write(f"Scale: 1:{scaling_factor:.2f}", align="left", font=("Arial", 12, "normal"))

    turtle.update()

def zoom(factor):
    global zoom_scale, scaled_radius, offset_x, offset_y, planet

    # Get the current planet position
    planet_x, planet_y = planet.xcor(), planet.ycor()

    # Apply zoom factor to zoom scale
    old_zoom = zoom_scale
    zoom_scale *= factor

    print(f"Zooming: {old_zoom} -> {zoom_scale}")  # Debugging output

    # Calculate the new offset to keep the planet centered during zoom
    offset_x = planet_x - planet_x * factor
    offset_y = planet_y - planet_y * factor

    # Recalculate scaled radius based on new zoom scale
    redraw_orbit()


def zoom_in():
    zoom(1.1)  # Zoom in by increasing scale

def zoom_out():
    zoom(0.9)  # Zoom out by decreasing scale

def move_left():
    global offset_x
    offset_x += 20
    redraw_orbit()

def move_right():
    global offset_x
    offset_x -= 20
    redraw_orbit()

def move_up():
    global offset_y
    offset_y -= 20
    redraw_orbit()

def move_down():
    global offset_y
    offset_y += 20
    redraw_orbit()

turtle.listen()
turtle.onkeypress(zoom_in, "equal")  # Use 'equal' for the '+' key
turtle.onkeypress(zoom_out, "minus")  # Use 'minus' for the '-' key
turtle.onkeypress(move_left, "Left")
turtle.onkeypress(move_right, "Right")
turtle.onkeypress(move_up, "Up")
turtle.onkeypress(move_down, "Down")


def Graphics(radius, velocity):
    global planet, scaled_radius, angle_step, orbit_drawer, text_turtle, scaling_factor

    # Ensure scaling_factor is set here
    max_display_radius = 400 * 0.4
    scaling_factor = max_display_radius / radius if radius > max_display_radius else 1
    scaled_radius = radius * scaling_factor

    orbit_drawer = turtle.Turtle()
    orbit_drawer.speed(0)
    orbit_drawer.hideturtle()

    text_turtle = turtle.Turtle()
    text_turtle.hideturtle()

    # Create planet object
    radius_planet = r1 * scaling_factor / 10  # Scale the radius of the orbiting planet
    planet = turtle.Turtle()
    planet.shape("circle")
    planet.color("blue")
    planet.shapesize(radius_planet)  # Set the scaled size of the orbiting planet
    planet.penup()

    orbital_circumference = 2 * math.pi * radius
    time_per_orbit = orbital_circumference / velocity
    angle_step = (360 / time_per_orbit) * (step_time / 1000) * 5000

    redraw_orbit()
    update_position()
    turtle.mainloop()

UserInput = tk.Tk()
UserInput.title("Orbit Calculator")

label = tk.Label(UserInput, text="Enter your data (you can leave one blank and it will be calculated)")
label.pack()

label = tk.Label(UserInput, text="Mass of Planet (kg):")
label.pack()

mass_entry = tk.Entry(UserInput)
mass_entry.pack()

label = tk.Label(UserInput, text="Velocity of object in orbit (m/s):")
label.pack()

velocity_entry = tk.Entry(UserInput)
velocity_entry.pack()

label = tk.Label(UserInput, text="Radius of orbit (M):")
label.pack()

radius_entry = tk.Entry(UserInput)
radius_entry.pack()

label = tk.Label(UserInput, text="Radius of planet in orbit (M):")
label.pack()

radius_inOrbit_entry = tk.Entry(UserInput)
radius_inOrbit_entry.pack()

label = tk.Label(UserInput, text="Radius of main planet (M):")
label.pack()

radius_NotinOrbit_entry = tk.Entry(UserInput)
radius_NotinOrbit_entry.pack()

submit_button = tk.Button(UserInput, text="Submit", command=submit)
submit_button.pack()

UserInput.mainloop()
