import re
import struct
import sys
from enum import Enum
from typing import Union, Tuple, Any
from warnings import warn

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
        'det_x (mm)': d[7::11],
        'det_y (mm)': d[8::11],
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


def write_rrng(file_path, ions, rrngs):
    """
    Writes two DataFrames of 'ions' and 'ranges' to a .rrng file in IVAS format.

    Parameters:
    - file_path (str): The path to the .rrng file to be created.
    - ions (DataFrame): A DataFrame containing ion data with columns 'number' and 'name'.
    - rrngs (DataFrame): A DataFrame containing range data with columns 'number', 'lower', 'upper', 'vol', 'comp',
      and 'color'.

    Returns:
    None
    """
    with open(file_path, 'w') as f:
        # Write ion data
        f.write('[Ions]\n')
        for index, row in ions.iterrows():
            ion_line = f'Ion{index}={row["name"]}\n'
            f.write(ion_line)

        # Write range data
        f.write('[Ranges]\n')
        for index, row in rrngs.iterrows():
            range_line = f'Range{index}={row["lower"]:.2f} {row["upper"]:.2f} Vol:{row["vol"]:.2f} {row["comp"]} Color:{row["color"]}\n'
            f.write(range_line)


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





class RelType(Enum):
    REL_UNKNOWN = 0
    ONE_TO_ONE = 1
    INDEXED = (2,)
    UNRELATED = 3
    ONE_TO_MANY = 4


class RecordType(Enum):
    RT_UNKNOWN = 0
    FIXED_SIZE = 1
    VARIABLE_SIZE = 2
    VARIABLE_INDEXED = 3


class RecordDataType(Enum):
    DT_UNKNOWN = 0
    INT = 1
    UINT = 2
    FLOAT = 3
    CHARSTRING = 4
    OTHER = 5


class Dtype(Enum):
    int32 = 4
    int64 = 8
    char = 1
    wchar_t = 2
    filetime = 8


class RelType(Enum):
    REL_UNKNOWN = 0
    ONE_TO_ONE = 1
    INDEXED = (2,)
    UNRELATED = 3
    ONE_TO_MANY = 4


class RecordType(Enum):
    RT_UNKNOWN = 0
    FIXED_SIZE = 1
    VARIABLE_SIZE = 2
    VARIABLE_INDEXED = 3


class RecordDataType(Enum):
    DT_UNKNOWN = 0
    INT = 1
    UINT = 2
    FLOAT = 3
    CHARSTRING = 4
    OTHER = 5


class Dtype(Enum):
    int32 = 4
    int64 = 8
    char = 1
    wchar_t = 2
    filetime = 8


def read_apt(filepath: str, verbose: bool = False):
    """
    Read apt file into a pandas DataFrame

    Args:
        filepath (str): Path to apt file
        verbose (bool): Print the structure of the apt file as it is read (for debug purposes)

    Returns:
        pandas.DataFrame: A DataFrame containing the apt file data

    """

    def record_dtype2numpy_dtype(rec_dtype: RecordDataType, size: int):
        """
        Map a section's record data type to its equivalent numpy dtype
        """
        if rec_dtype in (RecordDataType.UINT, RecordDataType.CHARSTRING):
            raise ValueError("Cannot map to UINT or CHARSTRING")

        int_map = {8: np.int8, 16: np.int16, 32: np.int32, 64: np.int64}

        float_map = {32: np.float32, 64: np.float64}

        if rec_dtype == RecordDataType.INT:
            return int_map[size]
        elif rec_dtype == RecordDataType.FLOAT:
            return float_map[size]
        else:
            raise ValueError(f"Unexpected record data type {rec_dtype}")

    # Maps the apt format data type to str format needed for struct.unpack
    dtype2fmt = {Dtype.int32: "i", Dtype.int64: "q", Dtype.char: "c", Dtype.filetime: "Q", Dtype.wchar_t: "c"}

    # Maps the apt format data type to python data type
    dtype2constr = {
        Dtype.int32: int,
        Dtype.int64: int,
        Dtype.char: lambda x: x.decode("utf-8"),
        Dtype.wchar_t: lambda x: x.decode("utf-16"),
        Dtype.filetime: int,
    }

    with open(filepath, "rb") as dat:

        def read_chunk(dtype: Dtype, count: int = 1, start: Union[None, int] = None) -> Union[Tuple[Any], Any]:
            if isinstance(start, int):
                dat.seek(start)

            fmt = dtype2fmt[dtype] * count
            constructor = dtype2constr[dtype]
            dtype_size = dtype.value

            if dtype in (Dtype.wchar_t, Dtype.char):
                return constructor(dat.read(dtype_size * count)).replace("\x00", "")
            else:
                retn = struct.unpack("<" + fmt, dat.read(dtype_size * count))

            if len(retn) == 1:
                return constructor(retn[0])
            else:
                return tuple(constructor(i) for i in retn)

        cSignature = read_chunk(Dtype.char, 4)

        # Read the APT file header --------------------------------------------------------------------------------
        iHeaderSize = read_chunk(Dtype.int32)
        iHeaderVersion = read_chunk(Dtype.int32)
        wcFileName = read_chunk(Dtype.wchar_t, 256)
        ftCreationTime = read_chunk(Dtype.filetime)
        llIonCount = read_chunk(Dtype.int64)

        if verbose:
            print(f"\nReading header of {filepath}")
            print(f"\tcSignature: " + cSignature)
            print(f"\tiHeaderSize: {iHeaderSize}")
            print(f"\tiHeaderVersion: {iHeaderVersion}")
            print(f"\twcFileName: {wcFileName}")
            print(f"\tftCreationTime: {ftCreationTime}")
            print(f"\t11IonCount: {llIonCount}")

        # Read the APT sections ----------------------------------------------------------------------------
        section_start = iHeaderSize
        section_data = {}

        while True:
            sec_sig = read_chunk(Dtype.char, 4, section_start)

            if sec_sig == "":
                # EOF reached
                break

            # Flag used to not include a section in the Roi when a configuration
            # situation is not implemented or handled
            skip_sec = False

            sec_header_size = read_chunk(Dtype.int32)
            sec_header_ver = read_chunk(Dtype.int32)
            sec_type = read_chunk(Dtype.wchar_t, 32)
            sec_ver = read_chunk(Dtype.int32)

            sec_rel_type = RelType(read_chunk(Dtype.int32))
            is_one_to_one = sec_rel_type == RelType.ONE_TO_ONE
            if not is_one_to_one:
                warn(f'APAV does not handle REL_TYPE != ONE_TO_ONE, section "{sec_type}" will be ignored')
                skip_sec = True

            sec_rec_type = RecordType(read_chunk(Dtype.int32))
            is_fixed_size = sec_rec_type == RecordType.FIXED_SIZE
            if not is_fixed_size:
                warn(f'APAV does not handle RECORD_TYPE != FIXED_SIZE, section "{sec_type}" will be ignored')
                skip_sec = True

            sec_rec_dtype = RecordDataType(read_chunk(Dtype.int32))
            if sec_rec_dtype in (RecordDataType.DT_UNKNOWN, RecordDataType.OTHER, RecordDataType.CHARSTRING):
                warn(f'APAV does not handle RECORD_TYPE == {sec_rec_dtype}, section "{sec_type}" will be ignored')
                skip_sec = True

            sec_dtype_size = read_chunk(Dtype.int32)
            sec_rec_size = read_chunk(Dtype.int32)
            sec_data_unit = read_chunk(Dtype.wchar_t, 16)
            sec_rec_count = read_chunk(Dtype.int64)
            sec_byte_count = read_chunk(Dtype.int64)

            if verbose:
                print("\nReading new section")
                print(f"\tSection header sig: {sec_sig}")
                print(f"\tSection header size: {sec_header_size}")
                print(f"\tSection header version: {sec_header_ver}")
                print(f"\tSection type: {sec_type}")
                print(f"\tSection version: {sec_ver}")
                print(f"\tSection relative type: {sec_rel_type}")
                print(f"\tSection record type: {sec_rec_type}")
                print(f"\tSection record data type: {sec_rec_dtype}")
                print(f"\tSection data type size (bits): {sec_dtype_size}")
                print(f"\tSection record size: {sec_rec_size}")
                print(f"\tSection data type unit: {sec_data_unit}")
                print(f"\tSection record count: {sec_rec_count}")
                print(f"\tSection byte count: {sec_byte_count}")

            if not skip_sec:
                columns = int(sec_rec_size / (sec_dtype_size / 8))
                records = int(sec_rec_count)
                count = records * columns
                in_data = np.fromfile(
                    filepath,
                    record_dtype2numpy_dtype(sec_rec_dtype, sec_dtype_size),
                    count,
                    offset=section_start + sec_header_size,
                )
                if columns > 1:
                    section_data[sec_type] = in_data.reshape(records, columns)
                else:
                    section_data[sec_type] = in_data

            section_start = section_start + sec_byte_count + sec_header_size

    has_mass_data = "Mass" in section_data.keys()
    has_pos_data = "Position" in section_data.keys()

    # Map some APT section names to those that APAV expects, otherwise the provided name is retained
    name_map = {
        "Multiplicity": "ipp",
        "Time of Flight": "tof",
        "XDet_mm": "det_x",
        "YDet_mm": "det_y",
        "Voltage": "dc_voltage",
        "Pulse Voltage": "pulse_voltage",
    }

    # Require mass and position data, clean up some sections, and account for possible duplicate sections (i.e.
    # XDet_mm + YDet_mm combined with Detector Coordinates
    if not has_mass_data:
        raise AttributeError("APT file must have include a mass section")
    elif not has_pos_data:
        raise AttributeError("APT file must have include a position section")

    # There are 2 difference ways that detector space coordinates can be included in an apt file, as a single
    # section containing both x/y or the x and y in separate sections. Only when the separate x/y sections are not
    # present we will load the combined x/y data (which we separate into different x and y arrays).
    if "Detector Coordinates" in section_data.keys():
        temp = section_data.pop("Detector Coordinates")
        if "XDet_mm" not in section_data.keys():
            section_data["det_x"] = temp[:, 0]
        if "YDet_mm" not in section_data.keys():
            section_data["det_y"] = temp[:, 1]

    if "Position" in section_data.keys():
        temp = section_data.pop("Position")
        if "x" not in section_data.keys():
            section_data["x"] = temp[:, 0]
        if "y" not in section_data.keys():
            section_data["y"] = temp[:, 1]
        if "z" not in section_data.keys():
            section_data["z"] = temp[:, 2]

    if "Position" in section_data.keys():
        pos = section_data.pop("Position")
    if "Detector Coordinates" in section_data.keys():
        detector_coordinates = section_data.pop("Detector Coordinates")

    df = pd.DataFrame(section_data)

    return df
