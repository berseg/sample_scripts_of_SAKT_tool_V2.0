import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, 
    QPushButton, QComboBox, QLabel, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt

class DiagnosticParameterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagnostic Parameters - Column Selector")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

        # Load the data files at startup
        self.df_combined = self.load_and_concatenate_data()
        self.sakt_dfd2 = pd.read_table('med2_do_vihoda.txt')
        self.sakt_dfp2 = pd.read_table('med2_posle_vihoda.txt')

    def initUI(self):
        # Set font and colors
        title_font = QFont("Arial", 16, QFont.Bold)
        label_font = QFont("Arial", 12)
        button_font = QFont("Arial", 12, QFont.Bold)

        # Background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f0f0f0"))
        self.setPalette(palette)

        # Logo or image (Optional: Add 'logo.png' in the same folder)
        self.logo = QLabel(self)
        pixmap = QPixmap("1.png").scaled(150, 150, Qt.KeepAspectRatio)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)

        # Label for instructions
        self.label = QLabel("Select column range to plot:", self)
        self.label.setFont(title_font)
        self.label.setAlignment(Qt.AlignCenter)

        # Dropdown to select column ranges
        self.column_selector = QComboBox(self)
        self.column_selector.setFont(label_font)
        self.column_selector.addItems([
            "Columns 0 to 11",
            "Columns 12 to 22",
            "Columns 22 to 34",
            "Columns 33 to 45",
            "Columns 45 to 55"
        ])
        self.column_selector.setStyleSheet("""
            QComboBox {
                background-color: #e0f7fa;
                border: 1px solid #00796b;
                padding: 5px;
            }
        """)

        # Button to plot the selected columns
        self.plot_button = QPushButton("Plot Selected Columns", self)
        self.plot_button.setFont(button_font)
        self.plot_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.plot_button.clicked.connect(self.plot_selected_columns)

        # Button for Mean plot
        self.mean_button = QPushButton("Plot Mean of Sensors", self)
        self.mean_button.setFont(button_font)
        self.mean_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.mean_button.clicked.connect(self.plot_mean)

        # Button for Median plot
        self.median_button = QPushButton("Plot Median of Sensors", self)
        self.median_button.setFont(button_font)
        self.median_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #FB8C00;
            }
        """)
        self.median_button.clicked.connect(self.plot_median)

        # Button to reset column plots
        self.reset_column_button = QPushButton("Reset Column Plots", self)
        self.reset_column_button.setFont(button_font)
        self.reset_column_button.setStyleSheet(""" 
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        self.reset_column_button.clicked.connect(self.reset_column_plots)

        # Button to reset mean/median plots
        self.reset_mean_median_button = QPushButton("Reset Mean/Median Plots", self)
        self.reset_mean_median_button.setFont(button_font)
        self.reset_mean_median_button.setStyleSheet(""" 
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        self.reset_mean_median_button.clicked.connect(self.reset_mean_median_plots)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.logo)
        layout.addWidget(self.label)
        layout.addWidget(self.column_selector)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.mean_button)
        layout.addWidget(self.median_button)
        layout.addWidget(self.reset_column_button)  # Add reset button for column plots
        layout.addWidget(self.reset_mean_median_button)  # Add reset button for mean/median plots
        layout = QVBoxLayout()
        layout.addWidget(self.logo)
        layout.addWidget(self.label)
        layout.addWidget(self.column_selector)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.mean_button)
        layout.addWidget(self.median_button)

        # Create a widget for the matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set layout in the main widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_and_concatenate_data(self):
        """Load and concatenate data from the two files."""
        try:
            dfd2 = pd.read_table('med2_do_vihoda.txt')
            dfp2 = pd.read_table('med2_posle_vihoda.txt')
            df_combined = pd.concat([dfd2, dfp2])
            print("Data loaded and concatenated successfully.")
            return df_combined
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
            sys.exit(1)

    def plot_selected_columns(self):
        """Plot the columns based on the user's selection."""
        selection = self.column_selector.currentText()

        # Determine the column range based on the selection
        if selection == "Columns 0 to 11":
            self.plot_columns(0, 11, selection)
        elif selection == "Columns 12 to 22":
            self.plot_columns(12, 22, selection)
        elif selection == "Columns 22 to 34":
            self.plot_columns(22, 34, selection)
        elif selection == "Columns 33 to 45":
            self.plot_columns(33, 45, selection)
        elif selection == "Columns 45 to 55":
            self.plot_columns(45, 55, selection)

    def plot_columns(self, start_col, end_col, title):
        """Plot the selected columns."""
        try:
            self.figure.clear()  # Clear the figure before plotting
            ax = self.figure.add_subplot(111)
            self.df_combined.iloc[:, start_col:end_col].plot(ax=ax)
            ax.set_title(title, fontsize=16, fontweight='bold')
            ax.set_xlabel("Index", fontsize=12)
            ax.set_ylabel("Value", fontsize=12)
            ax.grid(True)
            ax.legend(loc="best")
            self.canvas.draw()  # Refresh the canvas to show the new plot
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to plot: {str(e)}")

    def plot_mean(self):
        """Plot the mean of sensor readings."""
        try:
            m1 = self.sakt_dfd2.loc[:, 'A01 10JEC13CY203':'A64 10JAB10CY210'].mean()
            m2 = self.sakt_dfp2.loc[:, 'A01 10JEC13CY203':'A64 10JAB10CY210'].mean()

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            x1 = [x for x in range(len(m1))]
            x2 = [x for x in range(len(m2))]

            ax.set_title('Mean of Sensor Readings', fontsize=16)
            ax.set_xlabel("Sensor Number", fontsize=12)
            ax.set_ylabel("U, mkV", fontsize=12)
            ax.scatter(x1, m1, label='Before', color='blue')
            ax.scatter(x2, m2, label='After', color='red')
            ax.legend()
            ax.grid()
            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to plot mean: {str(e)}")

    def plot_median(self):
        """Plot the median of sensor readings."""
        try:
            m1 = self.sakt_dfd2.loc[:, 'A01 10JEC13CY203':'A64 10JAB10CY210'].median()
            m2 = self.sakt_dfp2.loc[:, 'A01 10JEC13CY203':'A64 10JAB10CY210'].median()

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            x1 = [x for x in range(len(m1))]
            x2 = [x for x in range(len(m2))]

            ax.set_title('Median of Sensor Readings', fontsize=16)
            ax.set_xlabel("Sensor Number", fontsize=12)
            ax.set_ylabel("U, mkV", fontsize=12)
            ax.scatter(x1, m1, label='Before', color='blue')
            ax.scatter(x2, m2, label='After', color='red')
            ax.legend()
            ax.grid()
            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to plot median: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = DiagnosticParameterApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()