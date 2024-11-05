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

def cut_cone_from_structure(structure, cone_radius, cone_height, min_x, max_x, min_y, max_y):
    """
    Cut the structure based on a cone defined by a radius and height.

    Args:
        structure (Structure): The pymatgen Structure object.
        cone_radius (float): The radius of the cone's base.
        cone_height (float): The height of the cone.
        min_x (float): Minimum x-coordinate of the cutting region.
        max_x (float): Maximum x-coordinate of the cutting region.
        min_y (float): Minimum y-coordinate of the cutting region.
        max_y (float): Maximum y-coordinate of the cutting region.

    Returns:
        Structure: A new Structure object containing only the atoms within the cone.
    """
    filtered_sites = []

    for site in structure:
        x, y, z = site.coords

        # Check if the site is within the x-y bounds
        if min_x <= x <= max_x and min_y <= y <= max_y:
            # Calculate the distance from the z-axis (center of the cone)
            r = np.sqrt(x**2 + y**2)

            # Check if the point lies within the cone
            if z <= cone_height and r <= (cone_radius / cone_height) * z:
                filtered_sites.append(site)

    # Create a new structure with the filtered sites
    filtered_structure = Structure(
        lattice=structure.lattice,
        species=[site.species for site in filtered_sites],
        coords=[site.coords for site in filtered_sites],
        coords_are_cartesian=True
    )

    return filtered_structure


def filter_structure_with_cone_and_hemisphere_2(structure, specified_height, height_hemisphere=0.8):
    # Parameters for the cone
    max_x = structure.lattice.a  # Half of the ellipse's maximum x-dimension
    max_y = structure.lattice.b  # Half of the ellipse's maximum y-dimension
    max_z = structure.lattice.c  # Height of the cone
    cone_radius = min(max_x, max_y)  # Radius of the cone at the base

    # Define the center of the cone
    center_x = max_x / 2
    center_y = max_y / 2

    # Hemisphere parameters
    x_center = center_x
    y_center = center_y
    hemisphere_center = np.array([x_center, y_center, max_z * height_hemisphere])
    hemisphere_radius = cone_radius / 3  # Radius of the hemisphere

    # Filtered sites will be collected in this list
    filtered_sites = []

    # Loop through all atomic sites to filter based on both cone and hemisphere criteria
    for site in structure.sites:
        x, y, z = site.coords

        # Check if the site is within the cone
        if z < 0 or z > specified_height:
            continue  # Outside the specified height of the cone

        # Calculate the elliptical cross-section radius at height z based on specified_height
        ellipse_radius_x = cone_radius * (1 - z / specified_height)
        ellipse_radius_y = cone_radius * (1 - z / specified_height)

        # Shift x and y by the center values
        shifted_x = x - center_x
        shifted_y = y - center_y

        # Check if the point is within the ellipse at height z
        if (shifted_x ** 2 / ellipse_radius_x ** 2 + shifted_y ** 2 / ellipse_radius_y ** 2) <= 1:
            # Now check if this point is also within the hemisphere
            distance_to_center = np.linalg.norm([shifted_x, shifted_y])  # Distance in the x-y plane

            # Check if the atom is below or within the hemisphere in the z-direction
            # if (hemisphere_radius ** 2 - distance_to_center ** 2) >= 0:
            #     if z <= hemisphere_center[2] + np.sqrt(hemisphere_radius ** 2 - distance_to_center ** 2):
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
