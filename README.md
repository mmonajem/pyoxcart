# PyCCAPT (APT_PyControl)

A modular, FAIR open-source Python atom probe tomography software package for experiment control and data calibration.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10210507.svg)](https://doi.org/10.5281/zenodo.10210507)
[![Documentation Status](https://readthedocs.org/projects/pyccapt/badge/?version=latest)](https://pyccapt.readthedocs.io/en/latest/?badge=latest)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-GPLv3-green.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

<img align="right" src="https://github.com/mmonajem/pyccapt/blob/main/pyccapt/files/logo2.png?raw=True" alt="PyCCAPT Logo" width="300" height="300">

## Overview

PyCCAPT is an open-source software package designed for controlling atom probe systems and calibrating data. The package is:
- Modular and adaptable for a wide range of devices in atom probe instruments
- Currently supports Surface Concept and RoentDek TDC systems
- Developed in Python 3.9+
- Includes a comprehensive calibration module with features for:
  - t₀ and flight path calculation
  - Region of interest (ROI) selection
  - Voltage and bowl calibration
  - 3D reconstruction techniques

## Features

### Control Module
- Modular design for easy integration with different instruments
- Support for various devices including:
  - Pfeifer gauges
  - Fug power supplies
  - Siglent signal generators
- Proven compatibility with Surface Concept and RoentDek TDC systems
- Graphical user interface for experiment control and visualization

### Calibration Module
- Comprehensive data calibration tools
- Advanced visualization capabilities
- Support for various calibration techniques
- 3D reconstruction capabilities

## Installation

### Prerequisites
- Python 3.9 or higher
- Anaconda (recommended)

### Installation Options

PyCCAPT can be installed in three ways:

1. **Calibration Module Only** (default):
   ```bash
   pip install pyccapt
   ```
   Includes:
   - Complete calibration module
   - Data analysis tools
   - Visualization capabilities
   - Jupyter integration
   - Material science tools

2. **Calibration + Control Modules** (full installation):
   ```bash
   pip install "pyccapt[full]"
   ```
   Includes everything from option 1, plus:
   - GUI components
   - Hardware control
   - Control algorithms
   - Image processing

3. **Development Installation** (for contributors):
   ```bash
   pip install "pyccapt[dev]"
   ```
   Adds development tools:
   - Testing (pytest)
   - Code formatting (black, flake8)
   - Type checking (mypy)
   - Pre-commit hooks

### Installation Steps

1. Create a virtual environment:
   ```bash
   conda create -n apt_env python=3.9
   ```

2. Activate the environment:
   ```bash
   conda activate apt_env
   ```

3. Install PyCCAPT with your preferred option (see above)

### Running the Application

If you have installed the control module, you can start the control GUI using either:
```bash
pyccapt
```
or
```bash
python -m pyccapt.control
```

For calibration module usage, start Jupyter Lab:
```bash
jupyter lab
```

### Tutorials

To access the tutorials:
1. Open your terminal
2. Navigate to the project folder
3. Start Jupyter Lab:
   ```bash
   jupyter lab
   ```

## Documentation

- [Latest Documentation](https://pyccapt.readthedocs.io/)
- [Configuration Guide](https://pyccapt.readthedocs.io/en/latest/configuration.html)
- [Calibration Tutorials](https://pyccapt.readthedocs.io/en/latest/tutorials.html)

### Google Colab Tutorials
- [Data Processing](https://colab.research.google.com/github/mmonajem/pyccapt/blob/main/pyccapt/calibration/tutorials/colab/data_processing.ipynb)
- [Data Visualization](https://colab.research.google.com/github/mmonajem/pyccapt/blob/main/pyccapt/calibration/tutorials/colab/visualization.ipynb)
- [t₀ and Flight Path Calculation](https://colab.research.google.com/github/mmonajem/pyccapt/blob/main/pyccapt/calibration/tutorials/colab/L_and_t0_determination.ipynb)

## Project Structure

```
pyccapt/
├── pyccapt/
│   ├── __init__.py
│   ├── config.json   
│   ├── calibration/
│   │   ├── __init__.py
│   │   └── module_folders   
│   ├── control/
│   │   ├── __init__.py
│   │   └── module_folders
│   └── files/
├── docs/
├── setup.py
├── README.md
├── CONTRIBUTING.md
├── MANIFEST.in
├── LICENSE
├── tox.ini
└── tests/
    ├── __init__.py
    ├── data/
    └── tests
```

## Data Structure

- [Control Module Data Structure](pyccapt/control/DATA_STRUCTURE.md)
- [Calibration Module Data Structure](pyccapt/calibration/DATA_STRUCTURE.md)

## Test Data

Test data (pure Aluminium) is available for calibration package evaluation:
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14673955.svg)](https://doi.org/10.5281/zenodo.14673955)

The dataset includes:
- Raw data from OXCART atom probe
- Calibrated data
- Reconstructed data
- Range file (HDF5)

## Support

- Report bugs and issues on [GitHub Issues](https://github.com/mmonajem/pyccapt/issues)
- Contact: Mehrpad Monajem (mehrpad.monajem@fau.de)

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Citation

If you use PyCCAPT in your research, please cite:
```
@software{pyccapt2024,
  author = {Monajem, Mehrpad},
  title = {PyCCAPT: A modular Python package for atom probe tomography},
  year = {2024},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.10210507},
  url = {https://doi.org/10.5281/zenodo.10210507}
}
```
