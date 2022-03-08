# Contributing

Contributions to APT_PyControl are always welcome, and they are greatly appreciated!
A list of open problems can be found [here](https://github.com/mmonajem/apt_pycontrol/issues).
Of course, it is also always appreciated bringing own ideas and problems to the community!


Please submit all contributions to the official [Github repository](https://github.com/mmonajem/apt_pycontrol) in the form of a Merge Request. Please do not submit git diffs or files containing the changes.

`APT_PyControl` is an open-source python package under the license of [GPLv3](https://github.com/mmonajem/apt_pycontrol/blob/main/LICENSE). Thus we consider the act of contributing to the code by submitting a Merge Request as the "Sign off" or agreement to the GPLv3 license.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/mmonajem/apt_pycontrol/issues.

### Fix Issues

Look through the GitHub issues. Different tags are indicating the status of the issues.
The "bug" tag indicates problems with APT_PyControl, while the "enhancement" tag shows ideas that should be added in the future.

### Write Documentation

The documentation of APT_PyControl can be found [here](https://github.com/mmonajem/apt_pycontrol/tree/main/docs).
It is always appreciated if new document notebooks are provided
since this helps others a lot.

## Get Started!

Ready to contribute? Here is how to set up `APT_PyControl` for local development.

1. Fork the `APT_PyControl` repo on GitHub.
2. Clone your fork locally:
```bash
    $ git clone https://github.com/mmonajem/APT_PyControl.git
```
3. Install your local copy into a virtualenv. It is also recommended to use anaconda or miniconda to manage the python environments.
```bash
    $ mkvirtualenv APT_PyControl
    $ cd APT_PyControl/
    $ pip install -e .
```
4. Create a branch for local development:
```bash
    $ git checkout -b name-of-your-bugfix-or-feature
```
   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests
```bash
    $ python setup.py test" .
```

   To get all packages needed for development, a requirements list can be found [here](https://github.com/mmonajem/apt_pycontrol/blob/main/setup.py).

6. Commit your changes and push your branch to GitHub::
```bash
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
```
7. Submit a Merge Request on Github.

## Merge Request Guidelines

Before you submit a Merge Request, check that it meets these guidelines:

1. All functionality that is implemented through this Merge Request should be covered by unit tests. These are implemented in `APT_PyControl_tests`. It would be necessary to add your unit test if the new implementation has some features that are not covered by our unit tests.
2. If the Merge Request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring.
3. If you have a maintainer status for `APT_PyControl`, you can merge Merge Requests to the master branch. However, every Merge Request needs to be reviewed by another developer. Thus, it is not allowed to merge a Merge Request, which is submitted by oneself.

## Tips

To run a subset of tests:
```bash
$ python setup.py test
```
