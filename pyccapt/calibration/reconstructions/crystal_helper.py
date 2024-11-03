import numpy as np
from pymatgen.core import Structure
from scipy.spatial.transform import Rotation


def filter_structure_with_cone_and_hemisphere(structure, width_factor=0.5, height_hemisphere=0.8):
    # Parameters for the cone
    max_x = structure.lattice.a  # Half of the ellipse's maximum x-dimension
    max_y = structure.lattice.b  # Half of the ellipse's maximum y-dimension
    max_z = structure.lattice.c  # Height of the cone

    # Define the center of the cone
    center_x = max_x / 2
    center_y = max_y / 2

    # Hemisphere parameters
    x_center = center_x
    y_center = center_y
    z_max = max_z
    radius = min(max_x, max_y) / 3
    hemisphere_center = np.array([x_center, y_center, height_hemisphere * z_max])

    # Filtered sites will be collected in this list
    filtered_sites = []

    # Loop through all atomic sites to filter based on both cone and hemisphere criteria
    for site in structure.sites:
        x, y, z = site.coords

        # Check if the site is within the cone
        if z < 0 or z > max_z:
            continue  # Outside the height of the cone

        # Calculate the elliptical cross-section at height z, adjusted by the width factor
        ellipse_radius_x = max_x * width_factor * (1 - z / max_z)
        ellipse_radius_y = max_y * width_factor * (1 - z / max_z)

        # Shift x and y by the center values
        shifted_x = x - center_x
        shifted_y = y - center_y

        # Check if the point is within the ellipse at height z
        if (shifted_x**2 / ellipse_radius_x**2 + shifted_y**2 / ellipse_radius_y**2) <= 1:
            # Now check if this point is also within the hemisphere
            distance_to_center = np.linalg.norm([shifted_x, shifted_y])  # Distance in the x-y plane

            # Check if the atom is below or within the hemisphere in the z-direction
            if (radius**2 - distance_to_center**2) >= 0:
                if z <= hemisphere_center[2] + np.sqrt(radius**2 - distance_to_center**2):
                    filtered_sites.append(site)

    # Create a new structure from the filtered sites
    filtered_structure = Structure.from_sites(filtered_sites)

    return filtered_structure

def rotate_coordinates(coords, theta_deg, phi_deg):
    """
    Rotates a set of atomic coordinates by given angles around the x- and y-axes.

    Parameters:
    - coords (list or np.ndarray): List or array of atomic coordinates, shape (N, 3).
    - theta_deg (float): Rotation angle around the x-axis in degrees.
    - phi_deg (float): Rotation angle around the y-axis in degrees.

    Returns:
    - np.ndarray: The rotated coordinates, shape (N, 3).
    """
    # Convert angles from degrees to radians
    theta = np.radians(theta_deg)
    phi = np.radians(phi_deg)

    # Create rotation matrices for each rotation
    rotation_x = Rotation.from_euler('x', theta).as_matrix()  # Rotate around x-axis by theta
    rotation_y = Rotation.from_euler('y', phi).as_matrix()    # Rotate around y-axis by phi

    # Combine rotations: first apply rotation around x, then around y
    combined_rotation = rotation_y @ rotation_x  # Matrix multiplication

    # Apply the combined rotation to each coordinate
    rotated_coords = np.dot(coords, combined_rotation.T)  # Transpose to apply rotation properly

    return rotated_coords
