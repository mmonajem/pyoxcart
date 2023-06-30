import re
import struct
import sys

import matplotlib.colors as cols
import numpy as np
import pandas as pd
from vispy import app, scene


def read_pos(file_path):
    """
    Loads an APT .pos file as a pandas DataFrame.

    Columns:
        x: Reconstructed x position
        y: Reconstructed y position
        z: Reconstructed z position
        Da: Mass/charge ratio of ion
    """
    with open(file_path, 'rb') as file:
        data = file.read()
        n = len(data) // 4
        d = struct.unpack('>' + 'f' * n, data)
    pos = pd.DataFrame({
        'x (nm)': d[0::4],
        'y (nm)': d[1::4],
        'z (nm)': d[2::4],
        'm/n (Da)': d[3::4]
    })
    return pos


def read_epos(file_path):
    """
    Loads an APT .epos file as a pandas DataFrame.

    Columns:
        x: Reconstructed x position
        y: Reconstructed y position
        z: Reconstructed z position
        Da: Mass/charge ratio of ion
        ns: Ion Time Of Flight
        DC_kV: Potential
        pulse_kV: Size of voltage pulse (voltage pulsing mode only)
        det_x: Detector x position
        det_y: Detector y position
        pslep: Pulses since last event pulse (i.e. ionisation rate)
        ipp: Ions per pulse (multihits)
    """
    with open(file_path, 'rb') as file:
        data = file.read()
        n = len(data) // 4
        rs = n // 11
        d = struct.unpack('>' + 'fffffffffII' * rs, data)
    epos = pd.DataFrame({
        'x (nm)': d[0::11],
        'y (nm)': d[1::11],
        'z (nm)': d[2::11],
        'm/n (Da)': d[3::11],
        'TOF (ns)': d[4::11],
        'HV_DC (V)': d[5::11],
        'pulse (V)': d[6::11],
        'det_x (cm)': d[7::11],
        'det_y (cm)': d[8::11],
        'pslep': d[9::11],
        'ipp': d[10::11]
    })
    return epos


def read_rrng(file_path):
    """
    Loads a .rrng file produced by IVAS. Returns two DataFrames of 'ions' and 'ranges'.

    Parameters:
    - file_path (str): The path to the .rrng file.

    Returns:
    - ions (DataFrame): A DataFrame containing ion data with columns 'number' and 'name'.
    - rrngs (DataFrame): A DataFrame containing range data with columns 'number', 'lower', 'upper', 'vol', 'comp', and 'colour'.
    """

    # Read the file and store its contents as a list of lines
    rf = open(file_path, 'r').readlines()

    # Define the regular expression pattern to extract ion and range data
    patterns = re.compile(
        r'Ion([0-9]+)=([A-Za-z0-9]+).*|Range([0-9]+)=(\d+.\d+) +(\d+.\d+) +Vol:(\d+.\d+) +([A-Za-z:0-9 ]+) +Color:([A-Z0-9]{6})')

    # Initialize empty lists to store ion and range data
    ions = []
    rrngs = []

    # Iterate over each line in the file
    for line in rf:
        # Search for matches using the regular expression pattern
        m = patterns.search(line)
        if m:
            # If match groups contain ion data, append to ions list
            if m.groups()[0] is not None:
                ions.append(m.groups()[:2])
            # If match groups contain range data, append to rrngs list
            else:
                rrngs.append(m.groups()[2:])

    # Convert ions list to a DataFrame with columns 'number' and 'name', and set 'number' as the index
    ions = pd.DataFrame(ions, columns=['number', 'name'])
    ions.set_index('number', inplace=True)

    # Convert rrngs list to a DataFrame with columns 'number', 'lower', 'upper', 'vol', 'comp', and 'colour', and set 'number' as the index
    rrngs = pd.DataFrame(rrngs, columns=['number', 'lower', 'upper', 'vol', 'comp', 'colour'])
    rrngs.set_index('number', inplace=True)

    # Convert 'lower', 'upper', and 'vol' columns in rrngs DataFrame to float data type
    rrngs[['lower', 'upper', 'vol']] = rrngs[['lower', 'upper', 'vol']].astype(float)
    rrngs[['comp', 'colour']] = rrngs[['comp', 'colour']].astype(str)

    # Return the ions and rrngs DataFrames
    return ions, rrngs


def label_ions(pos, rrngs):
    """
    Labels ions in a .pos or .epos DataFrame (anything with a 'Da' column) with composition and color,
    based on an imported .rrng file.

    Parameters:
    - pos (DataFrame): A DataFrame containing ion positions, with a 'Da' column.
    - rrngs (DataFrame): A DataFrame containing range data imported from a .rrng file.

    Returns:
    - pos (DataFrame): The modified DataFrame with added 'comp' and 'colour' columns.
    """

    # Initialize 'comp' and 'colour' columns in the DataFrame pos
    pos['comp'] = ''
    pos['colour'] = '#FFFFFF'

    # Iterate over each row in the DataFrame rrngs
    for n, r in rrngs.iterrows():
        # Assign composition and color values to matching ion positions in pos DataFrame
        pos.loc[(pos['Da'] >= r.lower) & (pos['Da'] <= r.upper), ['comp', 'colour']] = [r['comp'], '#' + r['colour']]

    # Return the modified pos DataFrame with labeled ions
    return pos


def deconvolve(lpos):
    """
    Takes a composition-labelled pos file and deconvolves the complex ions.
    Produces a DataFrame of the same input format with the extra columns:
    'element': element name
    'n': stoichiometry
    For complex ions, the location of the different components is not altered - i.e. xyz position will be the same
    for several elements.

    Parameters:
    - lpos (DataFrame): A composition-labelled pos file DataFrame.

    Returns:
    - out (DataFrame): A deconvolved DataFrame with additional 'element' and 'n' columns.
    """

    # Initialize an empty list to store the deconvolved data
    out = []

    # Define the regular expression pattern to extract element and stoichiometry information
    pattern = re.compile(r'([A-Za-z]+):([0-9]+)')

    # Group the input DataFrame 'lpos' based on the 'comp' column
    for g, d in lpos.groupby('comp'):
        if g != '':
            # Iterate over the elements in the 'comp' column
            for i in range(len(g.split(' '))):
                # Create a copy of the grouped DataFrame 'd'
                tmp = d.copy()
                # Extract the element and stoichiometry values using the regular expression pattern
                cn = pattern.search(g.split(' ')[i]).groups()
                # Add 'element' and 'n' columns to the copy of DataFrame 'tmp'
                tmp['element'] = cn[0]
                tmp['n'] = cn[1]
                # Append the modified DataFrame 'tmp' to the output list
                out.append(tmp.copy())

    # Concatenate the DataFrame in the output list to create the final deconvolved DataFrame
    return pd.concat(out)


def volvis(pos, size=2, alpha=1):
    """
    Displays a 3D point cloud in an OpenGL viewer window. If points are not labelled with colors,
    point brightness is determined by Da values (higher = whiter).

    Parameters:
    - pos (DataFrame): A DataFrame containing 3D point cloud data.
    - size (int): The size of the markers representing the points. Default is 2.
    - alpha (float): The transparency of the markers. Default is 1.

    Returns:
    - None
    """

    # Create an OpenGL viewer window
    canvas = scene.SceneCanvas('APT Volume', keys='interactive')
    view = canvas.central_widget.add_view()
    view.camera = scene.TurntableCamera(up='z')

    # Extract the position data from the 'pos' DataFrame
    cpos = pos[['x (nm)', 'y (nm)', 'z (nm)']].values

    # Check if the 'colour' column is present in the 'pos' DataFrame
    if 'colour' in pos.columns:
        # Extract colors from the 'colour' column
        colours = np.asarray(list(pos['colour'].apply(cols.hex2color)))
    else:
        # Calculate brightness based on Da values
        Dapc = pos['m/n (Da)'].values / pos['m/n (Da)'].max()
        colours = np.array(zip(Dapc, Dapc, Dapc))

    # Adjust colors based on transparency (alpha value)
    if alpha != 1:
        colours = np.hstack([colours, np.array([0.5] * len(colours))[..., None]])

    # Create and configure markers for the point cloud
    p1 = scene.visuals.Markers()
    p1.set_data(cpos, face_color=colours, edge_width=0, size=size)

    # Add the markers to the viewer
    view.add(p1)

    # Create arrays to store ion labels and corresponding colors
    ions = []
    cs = []

    # Group the 'pos' DataFrame by color
    for g, d in pos.groupby('colour'):
        # Remove ':' and whitespaces from the 'comp' column values
        ions.append(re.sub(r':1?|\s?', '', d['comp'].iloc[0]))
        cs.append(cols.hex2color(g))

    ions = np.array(ions)
    cs = np.asarray(cs)

    # Create positions and text for the legend
    pts = np.array([[20] * len(ions), np.linspace(20, 20 * len(ions), len(ions))]).T
    tpts = np.array([[30] * len(ions), np.linspace(20, 20 * len(ions), len(ions))]).T

    # Create a legend box
    legb = scene.widgets.ViewBox(parent=view, border_color='red', bgcolor='k')
    legb.pos = 0, 0
    legb.size = 100, 20 * len(ions) + 20

    # Create markers for the legend
    leg = scene.visuals.Markers()
    leg.set_data(pts, face_color=cs)
    legb.add(leg)

    # Add text to the legend
    legt = scene.visuals.Text(text=ions, pos=tpts, color='white', anchor_x='left', anchor_y='center', font_size=10)
    legb.add(legt)

    # Display the canvas
    canvas.show()

    # Run the application event loop if not running interactively
    if sys.flags.interactive == 0:
        app.run()
