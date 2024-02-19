import sys

from pyccapt.calibration.data_tools.dataset_path_qt import gui_fname

if __name__ == "__main__":
	folder_path = sys.argv[1]
	result = gui_fname(folder_path)
	if result:
		print(result)
	else:
		print("No file chosen")
