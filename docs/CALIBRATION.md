# Calibration

The PyCCAPT Calibration Sub-Module provides essential tools and workflows for calibrating and processing atom probe
tomography (APT) data. This module is designed to assist researchers in preparing and enhancing their APT data for
further analysis.


## Jupyter data processing Workflows

The workflows in PyCCAPT Calibration Sub-Module are designed to streamline the following APT key tasks:

### 1. Data Cropping

- *Description*: Allows you to crop atom probe data, whether it's originally collected using PyCCAPT or in various other
  formats such as EPOS, POS, ATO, and CSV.
- *Usage*: Define the region of interest (ROI) to focus on specific areas of the dataset.

### 2. Time of Flight Calibration

- *Description*: Perform time-of-flight (TOF) calibration to correct for flight time distortions in the data.
- *Usage*: Improve the accuracy of spatial information in the APT dataset.

### 3. Converting time-of-flight to mass-to-charge ratio

- *Description*: Calibrate the mass-to-charge ratio (MC) of ions in the dataset.
- *Usage*: Enhance the accuracy of quantitative analysis by ensuring precise MC values.

### 4. 3D Reconstruction

- *Description*: Reconstruct the 3D spatial distribution of from the atom probe data.
- *Usage*: Visualize the spatial distribution of atoms within the material.

### 5. Ranging the Mass-to-Charge Ratio

- *Description*: Define a range for the mass-to-charge ratio to filter ions based on specific MC values.
- *Usage*: Focus on ions within a specific MC range for analysis.

### 6. Visualization

- *Description*: Visualize the atom probe data using various plotting and visualization techniques.
- *Usage*: Gain insights into the data through 2D and 3D visualizations.

### 7. T0 and Flight Path Calculation

- *Description*: Calculate T0 and flight paths length for ions.
- *Usage*: Essential for precise quantitative analysis and data interpretation.

## Data structures

For the data structure you can check the [data structure](Control_DATA_STRUCTURE.md) file. There is also possibility to
convert
the PyCCAPT HDF5 file data to EPOS, POS, ATO, and CSV file. You can find the
example code in the [tutorial](tutorials.rst)  section.

## Additional Features

In addition to the core functionalities mentioned above, the calibration module of PyCCAPT offers various advanced
features and capabilities, such as the following:

- **Data Analysis**: Perform advanced data analysis on atom probe data, such as spatial distribution map (SDM), isosurface
  generation, and radial distribution function (RDF) calculation.
- **Data Export**: Export atom probe data to various file formats, including EPOS, POS, ATO, and CSV.
- **Data Import**: Import atom probe data from various file formats, including EPOS, POS, ATO, and CSV.
- **Data Filtering**: Filter atom probe data based on specific criteria, such as mass-to-charge ratio (MC) or spatial
  coordinates.


For specific usage examples and code snippets, explore the Jupyter notebooks provided in
the [`tutorials`](https://github.com/mmonajem/pyccapt/tree/main/pyccapt/calibration/tutorials/jupyter_files)
or [`colab`](https://github.com/mmonajem/pyccapt/tree/main/pyccapt/calibration/tutorials/colab)
of the PyCCAPT repository. 

