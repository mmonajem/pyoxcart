import os


from pyccapt.calibration.leap_tools import apt_importers

p = os.path.abspath(os.path.join("", "../../.."))
path = p + '\\tests\\data\\data_leap_test\\'


pos = apt_importers.read_pos(path + 'voldata.pos')
ions, rrngs = apt_importers.read_rrng(path + 'rangefile.rrng')
lpos = apt_importers.label_ions(pos, rrngs)
dpos = apt_importers.deconvolve(lpos)


apt_importers.volvis(dpos, alpha=0.6)

# apt_importers.volvis(dpos.loc[dpos.element=='Na',:])