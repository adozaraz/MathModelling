from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib

matplotlib.use('QT5Agg')


class MplCanvas(Canvas):
    def __init__(self):
        AU = 1.5e11
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.axis('auto')
        self.axis_size = 10
        self.ax.set_xlim(-self.axis_size * AU, self.axis_size * AU)
        self.ax.set_ylim(-self.axis_size * AU, self.axis_size * AU)
        self.ax.set_zlim(-self.axis_size * AU, self.axis_size * AU)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QVBoxLayout()  # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
