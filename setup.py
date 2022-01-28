from distutils.core import setup
files = ["devices/*", "drs/*", "tdc_roentec/*", "tdc_surface_consept/*", "tools/*"]

setup(name = "APT Control Software",
    version = "0.0.1",
    author = "Mehrpad Monajem",
    packages = ['APT_Pycontrol'],
    package_data = {'package' : files },
    scripts = [],
)