import os


from pyccapt.calibration.leap_tools import leap_tools

p = os.path.abspath(os.path.join("", "../../.."))
path = p + '\\tests\\data\\data_leap_test\\'


pos = leap_tools.read_pos(path + 'voldata.pos')
ions, rrngs = leap_tools.read_rrng(path + 'rangefile.rrng')
lpos = leap_tools.label_ions(pos, rrngs)
dpos = leap_tools.deconvolve(lpos)


leap_tools.volvis(dpos, alpha=0.6)

# leap_tools.volvis(dpos.loc[dpos.element=='Na',:])