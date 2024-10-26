import numpy as np
from mayavi import mlab

# Function to create a sphere (Black Hole)
def create_sphere(radius, resolution):
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

# Function to create a thin accretion disk with sharp edges
def create_accretion_disk(inner_radius, outer_radius, resolution):
    theta = np.linspace(0, 2 * np.pi, resolution)
    r = np.linspace(inner_radius, outer_radius, resolution)
    R, T = np.meshgrid(r, theta)
    x = R * np.cos(T)
    y = R * np.sin(T)
    z = np.zeros_like(R)  # Keep the disk flat for sharp edges
    return x, y, z

# Function to set up the 3D plot
def setup_plot():
    mlab.figure(size=(800, 800), bgcolor=(0.1, 0.1, 0.1))  # Set background to dark gray
    mlab.view(azimuth=45, elevation=30, distance=5)  # Initial view setup

# Function to plot the black hole and accretion disk
def plot_black_hole_with_disk(black_hole_radius, disk_inner_radius, disk_outer_radius, resolution):
    # Create the black hole
    x_black_hole, y_black_hole, z_black_hole = create_sphere(black_hole_radius, resolution)
    mlab.mesh(x_black_hole, y_black_hole, z_black_hole, color=(0, 0, 0), opacity=1)
    
    # Create the accretion disk (farside and underside with sharp edges)
    x_disk, y_disk, z_disk = create_accretion_disk(disk_inner_radius, disk_outer_radius, resolution)
    disk_farside = mlab.mesh(x_disk, y_disk, z_disk, color=(1, 0.6, 0), opacity=0.6)  # Farside in orange
    disk_underside = mlab.mesh(x_disk, y_disk, -z_disk, color=(0.6, 0.2, 0), opacity=0.5)  # Underside in darker red

    # Animation parameters
    time_offset = 0

    # Update function for animation
    def update():
        nonlocal time_offset
        # Rotate the accretion disk slowly
        x_disk_rotated = x_disk * np.cos(time_offset) - y_disk * np.sin(time_offset)
        y_disk_rotated = x_disk * np.sin(time_offset) + y_disk * np.cos(time_offset)
        
        # Update accretion disk mesh
        disk_farside.mlab_source.set(x=x_disk_rotated, y=y_disk_rotated, z=z_disk)
        disk_underside.mlab_source.set(x=x_disk_rotated, y=y_disk_rotated, z=-z_disk)
        
        # Update time offset for slow rotation
        time_offset += 0.01  # Slow down the disk rotation
        
        # Schedule the next update
        mlab.animate(update)

    # Start the animation
    mlab.animate(update)

# Parameters for the black hole and accretion disk
black_hole_radius = 0.2  # Radius of the black hole
disk_inner_radius = 0.25  # Inner radius of the accretion disk
disk_outer_radius = 0.6  # Outer radius of the accretion disk
resolution = 100  # Increased resolution for better detail

# Set up the plot
setup_plot()

# Plot the black hole and accretion disk
plot_black_hole_with_disk(black_hole_radius, disk_inner_radius, disk_outer_radius, resolution)

# Add a title
mlab.title('Black Hole with Accretion Disk', size=0.5, color=(1, 1, 1))

# Show the plot
mlab.show()
