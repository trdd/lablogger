import sys
import random
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets, QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class IntegerTextField(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(IntegerTextField, self).__init__(*args, **kwargs)
        self.setValidator(QtGui.QIntValidator())
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)


        


class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.columns = None
        self.le  = QtWidgets.QLineEdit("")
        self.le_delay  = IntegerTextField("10")
        self.le.setDragEnabled(True)
        self.cbx = QtWidgets.QComboBox()
        self.cby = QtWidgets.QComboBox()
        self.btn_open = QtWidgets.QPushButton('open')
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.le, 0, 0, 1, 6)
        layout.addWidget(self.btn_open, 0, 6, 1, 1)
        layout.addWidget(QtWidgets.QLabel('plot'), 1,0,1,1)
        layout.addWidget(self.cbx, 1, 1, 1, 1)
        layout.addWidget(QtWidgets.QLabel('versus'), 1,2,1,1)
        layout.addWidget(self.cby, 1, 3, 1, 1)
        layout.addWidget(QtWidgets.QLabel('and update every'), 1,4,1,1)
        layout.addWidget(self.le_delay, 1, 5, 1, 1)
        layout.addWidget(QtWidgets.QLabel('seconds'), 1,6,1,1)


        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        outer_layout = QtWidgets.QVBoxLayout()
        outer_layout.addLayout(layout)
        outer_layout.addLayout(layout)
        self.toolbar = NavigationToolbar(self.canvas, self)
        outer_layout.addWidget(self.toolbar)
        outer_layout.addWidget(self.canvas)

        self.setLayout(outer_layout)


        self.show()
        self.create_signals()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.change_delay()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def getFileName(self):
        sender = self.sender()
        fn, other = QtWidgets.QFileDialog.getOpenFileName(self)
        self.le.setText(fn)
    
    def load_file(self):
        fn = self.le.text()
        fh = open(fn, 'r')
        self.columns = fh.readline().strip().split()
        if '#' in self.columns:
            self.columns.remove('#')
        self.cbx.clear()
        self.cby.clear()
        self.cbx.addItems(self.columns)
        self.cby.addItems(self.columns)
        # self.update_plot()

    def create_signals(self):
        self.btn_open.clicked.connect(self.getFileName)
        self.le.returnPressed.connect(self.load_file)
        self.le_delay.returnPressed.connect(self.change_delay)
        self.cbx.currentIndexChanged.connect(self.update_plot)
        self.cby.currentIndexChanged.connect(self.update_plot)

    def change_delay(self):
        self.timer.setInterval(1000*int(self.le_delay.text()))


    def update_plot(self):
        if self.columns:
            # add try to avoid issues when the logfile is not completely written
            try:
                data = np.loadtxt(self.le.text())
                if self.cbx.currentText() in self.columns:
                    x = data[:,self.columns.index(self.cbx.currentText())]
                if self.cby.currentText() in self.columns:
                    y = data[:,self.columns.index(self.cby.currentText())]
                    self.canvas.axes.cla()  # Clear the canvas.
                    self.canvas.axes.plot(x, y, 'ko-', ms=2)
                    self.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
