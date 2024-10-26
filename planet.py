import numpy as np
from mayavi import mlab

# Function to create a sphere
def create_sphere(radius, resolution):
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

# Function to create a warped space effect around the black hole
def create_warped_space(radius, resolution, warp_factor):
    theta = np.linspace(0, 2 * np.pi, resolution)
    r = np.linspace(radius, radius + warp_factor, resolution)
    R, T = np.meshgrid(r, theta)
    x = R * np.cos(T)
    y = R * np.sin(T)
    z = np.sin(T) * (R - radius)  # Creating a wave effect in z
    return x, y, z

# Function to set up the 3D plot
def setup_plot():
    mlab.figure(size=(800, 800), bgcolor=(0.8, 0.8, 0.8))  # Set background to light gray
    mlab.view(azimuth=45, elevation=45, distance=5)

# Function to plot the black hole and warped space
def plot_black_hole_with_warp(black_hole_radius, warp_radius, warp_factor, resolution):
    # Create the black hole
    x_black_hole, y_black_hole, z_black_hole = create_sphere(black_hole_radius, resolution)
    mlab.mesh(x_black_hole, y_black_hole, z_black_hole, color=(0, 0, 0), opacity=1)

    # Create the warped space (static)
    x_warped, y_warped, z_warped = create_warped_space(warp_radius, resolution, warp_factor)
    mlab.mesh(x_warped, y_warped, z_warped, colormap='gray', opacity=0.3)  # Set opacity to 0.3 for transparency

# Parameters for the black hole
black_hole_radius = 0.2  # Radius of the black hole
warp_radius = 0.5  # Radius where the warping effect starts
warp_factor = 0.3  # How much the space is warped
resolution = 100  # Increased resolution for better detail

# Set up the plot
setup_plot()

# Plot the black hole and warped space
plot_black_hole_with_warp(black_hole_radius, warp_radius, warp_factor, resolution)

# Add a title
mlab.title('Black Hole with Static Space Warping Effect', size=0.5, color=(0, 0, 0))

# Show the plot
mlab.show()