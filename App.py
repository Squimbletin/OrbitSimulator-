import math
import tkinter as tk
import turtle
import time

g = 6.67430e-11

def forRadius(g, m, v):
    solution = g * m / v ** 2
    return solution

def forVelocity(m, r, g):
    solution = math.sqrt(g * m / r)
    return solution

def forMass(v, r, g):
    solution = v ** 2 * r / g
    return solution

def submit():
    # Get the input from each entry widget
    mass_input = mass_entry.get()
    radius_input = radius_entry.get()
    velocity_input = velocity_entry.get()
    
    # Print the user input
    print(f"Mass: {mass_input}")
    print(f"Radius: {radius_input}")
    print(f"Velocity: {velocity_input}")
    
    try:
        m = float(mass_input)
    except ValueError:
        print("Calculating Mass...")
        try:
            v = float(velocity_input)
            r = float(radius_input)
            m = forMass(v, r, g)  # Make sure m is defined inside this block
            print("Mass calculated...")
            print("The calculated Mass is: " + str(m))  # Convert float to string
            check = True;
        except ValueError:
            print("One of your inputs is not a valid number...")

    if(check != True): 
        try:
            v = float(velocity_input)
        except ValueError:
            print("Calculating Velocity...")
            try:
                m = float(mass_input)
                r = float(radius_input)
                v = forVelocity(v, r, g)  
                print("Velocity calculated...")
                print("The calculated Velocity is: " + str(v))  
                check = True;
            except  ValueError:
                print("one of your inputs is not a valid Number...")

    if(check != True): 
        try:
            r = float(radius_input)
        except ValueError:
            print("Calculating Radius...")
            try:
                m = float(mass_input)
                v = float(velocity_input)
                r = forVelocity(g, m, v)  
                print("radius calculated...")
                print("The calculated radius is: " + str(r))  
                check = True;
            except  ValueError:
                print("one of your inputs is not a valid Number...")
    
    Graphics(r, v)

angle = 0
step_time = 20  # Milliseconds per frame

def update_position():
    global angle, planet, scaled_radius, angle_step

    # Calculate new position
    x = scaled_radius * math.cos(math.radians(angle))
    y = scaled_radius * math.sin(math.radians(angle))
    planet.goto(x, y)

    # Update angle for next frame
    angle += angle_step
    if angle >= 360:
        angle -= 360  # Keep angle in range

    # Schedule the next update
    turtle.update()
    turtle.ontimer(update_position, step_time)

def Graphics(radius, velocity):
    global planet, scaled_radius, angle_step

    screen_size = 400  # Define screen size
    turtle.setup(screen_size * 2, screen_size * 2)  
    turtle.tracer(0, 0)  # Disable auto-updating for smooth animation

    # Define max display radius (40% of screen size)
    max_display_radius = screen_size * 0.4  

    # Compute scaling factor (only scale if too large)
    scaling_factor = max_display_radius / radius if radius > max_display_radius else 1
    scaled_radius = radius * scaling_factor  

    # Draw the orbit
    orbit_drawer = turtle.Turtle()
    orbit_drawer.speed(0)
    orbit_drawer.penup()
    orbit_drawer.goto(0, -scaled_radius)
    orbit_drawer.pendown()
    orbit_drawer.circle(scaled_radius)
    orbit_drawer.penup()
    orbit_drawer.hideturtle()

    # Display velocity text
    text_turtle = turtle.Turtle()
    text_turtle.hideturtle()
    text_turtle.penup()
    text_turtle.goto(scaled_radius + 20, 0)  # Position text outside the orbit
    text_turtle.write(f"Velocity: {velocity:.2f} m/s", align="left", font=("Arial", 12, "normal"))

    # Create a planet turtle
    planet = turtle.Turtle()
    planet.shape("circle")
    planet.color("blue")
    planet.penup()

    # Orbital motion parameters
    orbital_circumference = 2 * math.pi * radius  # Actual orbit length (meters)
    time_per_orbit = orbital_circumference / velocity  # Time for one full orbit (seconds)
    angle_step = (360 / time_per_orbit) * (step_time / 1000)  # Angle change per frame

    # Start animation loop
    update_position()

    # Keep window open
    turtle.mainloop()

UserInput = tk.Tk()
UserInput.title("Orbit Calculator")

label = tk.Label(UserInput, text="Enter your data (you can leave one blank and it will be calculated)")
label = tk.Label(UserInput, text="for scientific notation use eX format (1.02*10^21 = 1.02e21):")
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

submit_button = tk.Button(UserInput, text="Submit", command=submit)
submit_button.pack()

UserInput.mainloop()

