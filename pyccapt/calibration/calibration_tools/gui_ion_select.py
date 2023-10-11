import sys

import pandas as pd
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QStyledItemDelegate


class LaTeXDelegate(QStyledItemDelegate):
	def createEditor(self, parent, option, index):
		web_view = QWebEngineView(parent)
		return web_view

	def setEditorData(self, editor, index):
		text = index.data()
		html = f'<!DOCTYPE html><html><head><script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script></head><body>{text}</body></html>'
		editor.setHtml(html)

	def setModelData(self, editor, model, index):
		html = editor.page().toHtml(lambda html: model.setData(index, html))


class DataFrameModel(QAbstractTableModel):
	def __init__(self, data_frame):
		super().__init__()
		self.data_frame = data_frame

	def rowCount(self, parent=QModelIndex()):
		return len(self.data_frame)

	def columnCount(self, parent=QModelIndex()):
		return len(self.data_frame.columns)

	def data(self, index, role=0):
		if role == Qt.ItemDataRole.DisplayRole:
			return str(self.data_frame.iloc[index.row(), index.column()])
		return None

	def headerData(self, section, orientation, role):
		if role == Qt.ItemDataRole.DisplayRole:
			if orientation == Qt.Orientation.Horizontal:
				return str(self.data_frame.columns[section])
			if orientation == Qt.Orientation.Vertical:
				return str(section + 1)


class DataFrameViewer(QMainWindow):
	def __init__(self, data_frame):
		super().__init__()

		self.setWindowTitle("Ions List")

		self.data_frame = data_frame
		self.model = DataFrameModel(self.data_frame)

		self.table_view = QTableView()
		self.table_view.setModel(self.model)
		self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
		self.table_view.selectionModel().selectionChanged.connect(self.handle_selection_changed)
		self.table_view.setItemDelegateForColumn(0, LaTeXDelegate())  # Use the LaTeXDelegate for the first column

		central_widget = QWidget()
		layout = QVBoxLayout(central_widget)
		layout.addWidget(self.table_view)

		self.setCentralWidget(central_widget)

	def handle_selection_changed(self, selected, deselected):
		selected_rows = [index.row() for index in selected.indexes()]
		if selected_rows:
			selected_row = selected_rows[0]
			selected_data = self.data_frame.iloc[selected_row]
			print("Selected Row Data:")


def open_gui(df):
	app = QApplication(sys.argv)
	viewer = DataFrameViewer(df)
	viewer.show()
	sys.exit(app.exec())


# Example usage:
# You can use LaTeX formatting in column names like this
data = {'A': [r'$X^2$', 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)

open_gui(df)
