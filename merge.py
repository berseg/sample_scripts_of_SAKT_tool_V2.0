import sys
import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLabel, QWidget, QComboBox, QTableWidget, QTableWidgetItem, QTextEdit, QDateEdit, QFileDialog
)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt, QDate
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class CombinedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagnostic Parameters Application")
        self.setGeometry(100, 100, 1200, 800)

        # Main layout
        main_layout = QGridLayout()

        # Section 1: Column Selector and Plotter
        self.column_selector_widget = self.create_column_selector_widget()
        main_layout.addWidget(self.column_selector_widget, 0, 0)

        # Section 2: Real-time Diagnostic Data Analysis
        self.realtime_diagnostics_widget = self.create_realtime_diagnostics_widget()
        main_layout.addWidget(self.realtime_diagnostics_widget, 0, 1)

        # Section 3: Noise and Amplitude Analysis
        self.noise_analysis_widget = self.create_noise_analysis_widget()
        main_layout.addWidget(self.noise_analysis_widget, 1, 0)

        # Section 4: Empty Space (Reserved for Future Use)
        self.empty_widget = QLabel("Reserved for future use", alignment=Qt.AlignCenter)
        self.empty_widget.setFont(QFont("Arial", 14, QFont.Bold))
        main_layout.addWidget(self.empty_widget, 1, 1)

        # Set main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Load data files
        self.sakt_dfd2 = pd.DataFrame()
        self.sakt_dfp2 = pd.DataFrame()
    def toggle_dark_mode(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

    def create_column_selector_widget(self):
        """Create the column selector and plotter widget."""
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Column Selector and Plotter")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)

        self.load_button = QPushButton("Load Data Files")
        self.load_button.clicked.connect(self.load_data_files)
        layout.addWidget(self.load_button)

        self.column_selector = QComboBox()
        self.column_selector.addItems([
            "Columns 0 to 11",
            "Columns 12 to 22",
            "Columns 22 to 34",
            "Columns 33 to 45",
            "Columns 45 to 55"
        ])
        layout.addWidget(self.column_selector)

        self.plot_button = QPushButton("Plot Selected Columns")
        self.plot_button.clicked.connect(self.plot_selected_columns)
        layout.addWidget(self.plot_button)

        # Button to reset column plots
        self.reset_column_button = QPushButton("Reset Column Plots")
        self.reset_column_button.clicked.connect(self.reset_column_plots)
        layout.addWidget(self.reset_column_button)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        widget.setLayout(layout)
        return widget

    def create_realtime_diagnostics_widget(self):
        """Create the real-time diagnostic data analysis widget."""
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Real-time Diagnostic Data Analysis")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)

        self.date_picker = QDateEdit(calendarPopup=True)
        self.date_picker.setDate(QDate.currentDate())
        layout.addWidget(self.date_picker)

        self.fetch_button = QPushButton("Fetch Data for Selected Date")
        layout.addWidget(self.fetch_button)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels([
            "Channel", "Amplitude Peak", "Background Level", "Time of Noise"
        ])
        layout.addWidget(self.results_table)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        widget.setLayout(layout)
        return widget

    def create_noise_analysis_widget(self):
        """Create the noise and amplitude analysis widget."""
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Noise and Amplitude Analysis")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)

        self.mean_button = QPushButton("Plot Mean of Sensors")
        self.mean_button.clicked.connect(self.plot_mean)
        layout.addWidget(self.mean_button)

        self.median_button = QPushButton("Plot Median of Sensors")
        self.median_button.clicked.connect(self.plot_median)
        layout.addWidget(self.median_button)

        # Button to reset mean/median plots
        self.reset_mean_median_button = QPushButton("Reset Mean/Median Plots")
        self.reset_mean_median_button.clicked.connect(self.reset_mean_median_plots)
        layout.addWidget(self.reset_mean_median_button)

        self.analysis_figure = Figure()
        self.analysis_canvas = FigureCanvas(self.analysis_figure)
        layout.addWidget(self.analysis_canvas)

        widget.setLayout(layout)
        return widget

    def load_data_files(self):
        """Load data files using a file dialog."""
        try:
            file1, _ = QFileDialog.getOpenFileName(self, "Open Data File 1", "", "Text Files (*.txt)")
            file2, _ = QFileDialog.getOpenFileName(self, "Open Data File 2", "", "Text Files (*.txt)")

            if file1 and file2:
                self.sakt_dfd2 = pd.read_table(file1)
                self.sakt_dfp2 = pd.read_table(file2)
                print("Data files loaded successfully.")
            else:
                print("File selection canceled.")
        except Exception as e:
            print(f"Error loading data files: {e}")

    def plot_selected_columns(self):
        """Plot the selected columns from the combined data."""
        try:
            selection = self.column_selector.currentText()
            # Extract start and end indices from the selection
            parts = selection.split(' ')
            start = int(parts[1])  # Convert the start index
            end = int(parts[3])     # Convert the end index

            if self.sakt_dfd2.empty:
                raise ValueError("Data not loaded correctly.")

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.sakt_dfd2.iloc[:, start:end].plot(ax=ax)
            ax.set_title(selection)
            ax.grid()
            self.canvas.draw()
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"Error plotting selected columns: {e}")

    def plot_mean(self):
        """Plot the mean of sensor readings."""
        try:
            if self.sakt_dfd2.empty or self.sakt_dfp2.empty:
                raise ValueError("Data not loaded correctly.")

            m1 = self.sakt_dfd2.loc[:, 'A01 10JEC13CY203':'A64 10JAB10CY210'].mean()
            m2 = self.sakt_dfp2.loc[:, 'A01 10JEC13CY203':'A64 10JAB10CY210'].mean()

            self.analysis_figure.clear()
            ax = self.analysis_figure.add_subplot(111)
            ax.scatter(range(len(m1)), m1, label='Before', color='blue')
            ax.scatter(range(len(m2)), m2, label='After', color='red')
            ax.legend()
            ax.set_title('Mean of Sensor Readings')
            ax.grid()
            self.analysis_canvas.draw()
        except Exception as e:
            print(f"Error plotting mean: {e}")

    def plot_median(self):
        """Plot the median of sensor readings."""
        try:
            if self.sakt_dfd2.empty or self.sakt_dfp2.empty:
                raise ValueError("Data not loaded correctly.")

            m1 = self.sakt_dfd2.loc[:, 'A01 10JEC13CY203':'A64 10JAB10CY210'].median()
            m2 = self.sakt_dfp2.loc[:, 'A01 10JEC13CY203':'A64 10JAB10CY210'].median()

            self.analysis_figure.clear()
            ax = self.analysis_figure.add_subplot(111)
            ax.scatter(range(len(m1)), m1, label='Before', color='blue')
            ax.scatter(range(len(m2)), m2, label='After', color='red')
            ax.legend()
            ax.set_title('Median of Sensor Readings')
            ax.grid()
            self.analysis_canvas.draw()
        except Exception as e:
            print(f"Error plotting median: {e}")

    def reset_column_plots(self):
        """Reset the column plots to start from zero."""
        self.figure.clear()  # Clear the figure
        ax = self.figure.add_subplot(111)
        ax.set_ylim(0, 1)  # Set y-axis limits to start from zero
        ax.set_title("Column Plots Reset", fontsize=16)
        ax.set_xlabel("Index", fontsize=12)
        ax.set_ylabel("Value", fontsize=12)
        ax.grid(True)
        self.canvas.draw()  # Refresh the canvas

    def reset_mean_median_plots(self):
        """Reset the mean/median plots to start from zero."""
        self.analysis_figure.clear()  # Clear the figure
        ax = self.analysis_figure.add_subplot(111)
        ax.set_ylim(0, 1)  # Set y-axis limits to start from zero
        ax.set_title("Mean/Median Plots Reset", fontsize=16)
        ax.set_xlabel("Sensor Number", fontsize=12)
        ax.set_ylabel("U, mkV", fontsize=12)
        ax.grid(True)
        self.analysis_canvas.draw()  # Refresh the canvas

def main():
    app = QApplication(sys.argv)
    window = CombinedApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
