import pandas as pd
import struct
from vispy import app, scene  # mpl_plot
import numpy as np
import sys
import matplotlib.colors as cols
import re


def read_pos(f):
    """
    Loads an APT .pos file as a pandas dataframe.

    Columns:
        x: Reconstructed x position
        y: Reconstructed y position
        z: Reconstructed z position
        Da: mass/charge ratio of ion
        """
    # read in the data
    with open(f, 'rb') as f:
        data = f.read()
        print(len(data))
        n = int(len(data)/4)
        d = struct.unpack('>'+'f'*n, data)
                        # '>' denotes 'big-endian' byte order
    # unpack data
    pos = pd.DataFrame({'x (nm)': d[0::4],
                        'y (nm)': d[1::4],
                        'z (nm)': d[2::4],
                        'm/n (Da)': d[3::4]})
    return pos


def read_epos(f):
    """
    Loads an APT .epos file as a pandas dataframe.

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

     [x,y,z,Da,ns,DC_kV,pulse_kV,det_x,det_y,pslep,ipp].
        pslep = pulses since last event pulse
        ipp = ions per pulse

    When more than one ion is recorded for a given pulse, only the
    first event will have an entry in the "Pulses since last evenT
    pulse" column. Each subsequent event for that pulse will have
    an entry of zero because no additional pulser firings occurred
    before that event was recorded. Likewise, the "Ions Per Pulse"
    column will contain the total number of recorded ion events for
    a given pulse. This is normally one, but for a sequence of records
    a pulse with multiply recorded ions, the first ion record will
    have the total number of ions measured in that pulse, while the
    remaining records for that pulse will have 0 for the Ions Per
    Pulse value.
        ~ Appendix A of 'Atom Probe tomography: A Users Guide',
          notes on ePOS format.
    """
    # read in the data
    with open(f, 'rb') as f:
        data = f.read()
        n = int(len(data)/4)
        rs = int(n / 11)
        d = struct.unpack('>'+'fffffffffII'*rs, data)

    # unpack data
    epos = pd.DataFrame({'x (nm)': d[0::11],
                        'y (nm)': d[1::11],
                        'z (nm)': d[2::11],
                        'm/n (Da)': d[3::11],
                        'TOF (ns)': d[4::11],
                        'HV_DC (kV)': d[5::11],
                        'pulse (kV)': d[6::11],
                        'det_x (cm)': d[7::11],
                        'det_y (cm)': d[8::11],
                        'pslep': d[9::11], # pulses since last event pulse
                        'ipp': d[10::11]}) # ions per pulse
    return epos


def read_rrng(f):
    """Loads a .rrng file produced by IVAS. Returns two dataframes of 'ions'
    and 'ranges'."""


    rf = open(f,'r').readlines()

    patterns = re.compile(r'Ion([0-9]+)=([A-Za-z0-9]+).*|Range([0-9]+)=(\d+.\d+) +(\d+.\d+) +Vol:(\d+.\d+) +([A-Za-z:0-9 ]+) +Color:([A-Z0-9]{6})')

    ions = []
    rrngs = []
    for line in rf:
        m = patterns.search(line)
        if m:
            if m.groups()[0] is not None:
                ions.append(m.groups()[:2])
            else:
                rrngs.append(m.groups()[2:])

    ions = pd.DataFrame(ions, columns=['number','name'])
    ions.set_index('number', inplace=True)
    rrngs = pd.DataFrame(rrngs, columns=['number', 'lower', 'upper', 'vol', 'comp', 'colour'])
    rrngs.set_index('number',inplace=True)

    rrngs[['lower', 'upper', 'vol']] = rrngs[['lower', 'upper', 'vol']].astype(float)
    rrngs[['comp', 'colour']] = rrngs[['comp', 'colour']].astype(str)

    return ions,rrngs


def label_ions(pos, rrngs):
    """labels ions in a .pos or .epos dataframe (anything with a 'Da' column)
    with composition and colour, based on an imported .rrng file."""

    pos['comp'] = ''
    pos['colour'] = '#FFFFFF'

    for n, r in rrngs.iterrows():
        pos.loc[(pos.loc[:, 'm/n (Da)'] >= r.lower) & (pos.loc[:, 'm/n (Da)'] <= r.upper),
                ['comp', 'colour']] = [r['comp'], '#' + r['colour']]

    return pos


def deconvolve(lpos):
    """Takes a composition-labelled pos file, and deconvolves
    the complex ions. Produces a dataframe of the same input format
    with the extra columns:
       'element': element name
       'n': stoichiometry
    For complex ions, the location of the different components is not
    altered - i.e. xyz position will be the same for several elements."""

    out = []
    pattern = re.compile(r'([A-Za-z]+):([0-9]+)')

    for g,d in lpos.groupby('comp'):
        if g != '':
            for i in range(len(g.split(' '))):
                tmp = d.copy()
                cn = pattern.search(g.split(' ')[i]).groups()
                tmp['element'] = cn[0]
                tmp['n'] = cn[1]
                out.append(tmp.copy())
    return pd.concat(out)


def volvis(pos, size=2, alpha=1):
    """Displays a 3D point cloud in an OpenGL viewer window.
    If points are not labelled with colours, point brightness
    is determined by Da values (higher = whiter)"""

    canvas = scene.SceneCanvas('APT Volume', keys='interactive')
    view = canvas.central_widget.add_view()
    view.camera = scene.TurntableCamera(up='z')

    cpos = pos.loc[:, ['x', 'y', 'z']].values
    if 'colour' in pos.columns:
        colours = np.asarray(list(pos.colour.apply(cols.hex2color)))
    else:
        Dapc = pos.Da.values / pos.Da.max()
        colours = np.array(zip(Dapc, Dapc, Dapc))
    if alpha != 1:
        np.hstack([colours, np.array([0.5] * len(colours))[..., None]])

    p1 = scene.visuals.Markers()
    p1.set_data(cpos, face_color=colours, edge_width=0, size=size)

    view.add(p1)

    # make legend
    ions = []
    cs = []
    for g, d in pos.groupby('colour'):
        ions.append(re.sub(r':1?|\s?', '', d.comp.iloc[0]))
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

    # show viewer
    canvas.show()
    if sys.flags.interactive == 0:
        app.run()

