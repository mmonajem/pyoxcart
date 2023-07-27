import os
from subprocess import check_output
from sys import argv
from sys import executable

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QFileDialog


def gui_fname(directory='./'):
    """
    Open a file dialog and return the chosen filename.

    Args:
        directory: Starting directory for the file dialog

    Returns:
        The chosen filename
    """
    # Run this exact file in a separate process and grab the result
    file = check_output([executable, __file__, directory])
    return file.strip()


if __name__ == "__main__":
    os.chdir('..//..//..//..//tests//data//')
    directory = argv[1]
    app = QApplication([directory])
    fname = QFileDialog.getOpenFileName(None, "Select a file...", directory, filter="All files (*)")
    print(fname[0])