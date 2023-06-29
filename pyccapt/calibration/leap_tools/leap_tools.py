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
    """
    rf = open(file_path, 'r').readlines()
    patterns = re.compile(
        r'Ion([0-9]+)=([A-Za-z0-9]+).*|Range([0-9]+)=(\d+.\d+) +(\d+.\d+) +Vol:(\d+.\d+) +([A-Za-z:0-9 ]+) +Color:([A-Z0-9]{6})')
    ions = []
    rrngs = []
    for line in rf:
        m = patterns.search(line)
        if m:
            if m.groups()[0] is not None:
                ions.append(m.groups()[:2])
            else:
                rrngs.append(m.groups()[2:])
    ions = pd.DataFrame(ions, columns=['number', 'name'])
    ions.set_index('number', inplace=True)
    rrngs = pd.DataFrame(rrngs, columns=['number', 'lower', 'upper', 'vol', 'comp', 'colour'])
    rrngs.set_index('number', inplace=True)
    rrngs[['lower', 'upper', 'vol']] = rrngs[['lower', 'upper', 'vol']].astype(float)
    rrngs[['comp', 'colour']] = rrngs[['comp', 'colour']].astype(str)
    return ions, rrngs


def label_ions(pos, rrngs):
    """
    Labels ions in a .pos or .epos DataFrame (anything with a 'Da' column) with composition and color,
    based on an imported .rrng file.
    """
    pos['comp'] = ''
    pos['colour'] = '#FFFFFF'
    for n, r in rrngs.iterrows():
        pos.loc[(pos['m/n (Da)'] >= r.lower) & (pos['m/n (Da)'] <= r.upper), ['comp', 'colour']] = [r['comp'],
                                                                                                    '#' + r['colour']]
    return pos


def deconvolve(lpos):
    """
    Takes a composition-labelled pos file and deconvolves the complex ions.
    Produces a DataFrame of the same input format with the extra columns:
    'element': element name
    'n': stoichiometry
    For complex ions, the location of the different components is not altered - i.e. xyz position will be the same
    for several elements.
    """
    out = []
    pattern = re.compile(r'([A-Za-z]+):([0-9]+)')
    for g, d in lpos.groupby('comp'):
        if g != '':
            for i in range(len(g.split(' '))):
                tmp = d.copy()
                cn = pattern.search(g.split(' ')[i]).groups()
                tmp['element'] = cn[0]
                tmp['n'] = cn[1]
                out.append(tmp.copy())
    return pd.concat(out)


def volvis(pos, size=2, alpha=1):
    """
    Displays a 3D point cloud in an OpenGL viewer window. If points are not labelled with colors,
    point brightness is determined by Da values (higher = whiter).
    """
    canvas = scene.SceneCanvas('APT Volume', keys='interactive')
    view = canvas.central_widget.add_view()
    view.camera = scene.TurntableCamera(up='z')
    cpos = pos[['x (nm)', 'y (nm)', 'z (nm)']].values
    if 'colour' in pos.columns:
        colours = np.asarray(list(pos['colour'].apply(cols.hex2color)))
    else:
        Dapc = pos['m/n (Da)'].values / pos['m/n (Da)'].max()
        colours = np.array(zip(Dapc, Dapc, Dapc))
    if alpha != 1:
        colours = np.hstack([colours, np.array([0.5] * len(colours))[..., None]])
    p1 = scene.visuals.Markers()
    p1.set_data(cpos, face_color=colours, edge_width=0, size=size)
    view.add(p1)
    ions = []
    cs = []
    for g, d in pos.groupby('colour'):
        ions.append(re.sub(r':1?|\s?', '', d['comp'].iloc[0]))
        cs.append(cols.hex2color(g))
    ions = np.array(ions)
    cs = np.asarray(cs)
    pts = np.array([[20] * len(ions), np.linspace(20, 20 * len(ions), len(ions))]).T
    tpts = np.array([[30] * len(ions), np.linspace(20, 20 * len(ions), len(ions))]).T
    legb = scene.widgets.ViewBox(parent=view, border_color='red', bgcolor='k')
    legb.pos = 0, 0
    legb.size = 100, 20 * len(ions) + 20
    leg = scene.visuals.Markers()
    leg.set_data(pts, face_color=cs)
    legb.add(leg)
    legt = scene.visuals.Text(text=ions, pos=tpts, color='white', anchor_x='left', anchor_y='center', font_size=10)
    legb.add(legt)
    canvas.show()
    if sys.flags.interactive == 0:
        app.run()