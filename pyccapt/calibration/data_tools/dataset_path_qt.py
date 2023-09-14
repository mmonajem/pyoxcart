import os
from subprocess import check_output
from sys import argv, executable

from PyQt6.QtWidgets import QApplication, QFileDialog

last_chosen_directory = './'  # Initialize with a default directory


def gui_fname():
    """
    Open a file dialog and return the chosen filename.

    Returns:
        The chosen filename
    """
    global last_chosen_directory  # Use the global variable

    # Run this exact file in a separate process and grab the result
    file = check_output([executable, __file__, last_chosen_directory])
    return file.strip()


if __name__ == "__main__":
    try:
        os.chdir('..//..//..//..//tests//data//')
    except:
        pass
    directory = argv[1]
    app = QApplication([directory])

    # Open the file dialog with the last chosen directory as the initial directory
    fname = QFileDialog.getOpenFileName(None, "Select a file...", last_chosen_directory,
                                        filter="PyCCAPT data (*.h5);;"
                                               "LEAP (*.pos *.epos);;"
                                               "APT (*.ato);;"
                                               "CSV (*.csv);;"
                                               "All Files (*)")

    chosen_file = fname[0]

    if chosen_file:
        # Update the last chosen directory with the directory of the chosen file
        last_chosen_directory = os.path.dirname(chosen_file)
    print(chosen_file)
