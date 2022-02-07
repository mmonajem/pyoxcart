from distutils.core import setup
files = ["devices/*", "drs/*", "tdc_roentdec/*", "tdc_surface_concept/*", "tools/*", "apt_ex/*", "gui/*"]

setup(name = "APT Control Software",
    version = "0.0.1",
    author = "Mehrpad Monajem",
    packages = ["devices", "drs", "tdc_roentdec", "tdc_surface_concept", "tools", "apt_ex", "gui"],
    package_data = {"package" : files },
    scripts = [],
)