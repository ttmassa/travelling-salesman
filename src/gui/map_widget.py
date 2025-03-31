from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from utils import makeButton, setButtonStyle

class MapWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.paths = []
        self.distances = []
        self.path_index = 0
        self.cities_x, self.cities_y = [], []
        self.selected_city = None

        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_xlabel("longitude")
        self.ax.set_ylabel("latitude")
        self.ax.set_title("Path")
        self.edges = self.ax.plot([], [], 'go', label="Start City") + self.ax.plot([], [], 'ro', label="City")
        self.vertices = self.ax.plot([], [], 'b-', label="Path")
        self.ax.legend()
        self.layout().addWidget(self.canvas)

        self.extends_button = self.ax.text(1.1, 1.1, '➔', transform=self.ax.transAxes,
                                    fontsize=12, fontweight='400', color='black',
                                    ha='right', va='bottom', bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))
        self.extends_button.set_picker(True)
        self.canvas.mpl_connect('pick_event', self.parent().showEvolution)

        self.path_control_buttons = QWidget()
        path_buttons_layout = QHBoxLayout()

        self.previous_button = makeButton("Previous", "5060FF", self.previousPath)
        path_buttons_layout.addWidget(self.previous_button)

        self.play_button = makeButton("Play", "5060FF", self.playPath)
        path_buttons_layout.addWidget(self.play_button)

        self.next_button = makeButton("Next", "5060FF", self.nextPath)
        path_buttons_layout.addWidget(self.next_button)

        path_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.path_control_buttons.setLayout(path_buttons_layout)
        self.path_control_buttons.hide()
        self.layout().addWidget(self.path_control_buttons)

        # Add coordinates
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(10,10),
                                    textcoords="offset points",
                                    bbox=dict(boxstyle="round", fc="w", alpha=1),
                                    arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        self.canvas.mpl_connect("motion_notify_event", self.hover)
        self.canvas.mpl_connect("button_press_event", self.onClick)

    def remove(self, obj, count):
        for i in range(count):
            obj.pop().remove()

    def setCities(self, points_x, points_y):
        self.remove(self.edges, len(self.edges))
        if points_x and points_y:
            # Start city
            self.edges = self.ax.plot(points_x[0], points_y[0], 'go', label="Start City")
            self.edges += self.ax.plot(points_x[1:], points_y[1:], 'ro', label="City")
        self.canvas.draw()
        self.cities_x, self.cities_y = points_x, points_y

    def moveCity(self, city, x, y):
        self.cities_x[city], self.cities_y[city] = x, y
        self.setCities(self.cities_x, self.cities_y)

    def setPath(self, path, distance):
        self.remove(self.vertices, len(self.vertices))
        points_x = [self.cities_x[city] for city in path]
        points_y = [self.cities_y[city] for city in path]
        self.vertices = self.ax.plot(list(points_x) + [points_x[0]], list(points_y) + [points_y[0]], 'b-')
        self.ax.set_title(f"Path {self.path_index + 1} Distance : {distance:.5f}")
        self.canvas.draw()

    def previousPath(self):
        if self.path_index <= 0:
            return
        self.path_index -= 1
        self.setPath(self.paths[self.path_index], self.distances[self.path_index])
        self.updateControlPathButtons()

    def nextPath(self):
        if self.path_index >= len(self.paths) - 1:
            self.stopPath()
            return
        self.path_index += 1
        self.setPath(self.paths[self.path_index], self.distances[self.path_index])
        self.updateControlPathButtons()

    def playPath(self):
        if self.path_index >= len(self.paths) - 1:
            self.path_index = -1

        if hasattr(self, 'timer') and self.timer.isActive():
            self.stopPath()
        else:
            self.timer = QTimer()
            self.timer.timeout.connect(self.nextPath)
            self.timer.start(250)
            self.play_button.setText("Stop")

    def stopPath(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
            self.play_button.setText("Play")

    def updatePath(self):
        if self.path_index < len(self.paths) - 1:
            self.path_index += 1
            self.setPath(self.paths[self.path_index])
            self.updateControlPathButtons()
        else:
            self.timer.stop()

    def updatePlot(self, generation, path, distance):
        if self.parent().show_evolution:
            self.paths.append(path)
            self.distances.append(distance)
            self.path_index = generation
            self.updateControlPathButtons()
        self.setPath(path, distance)
        self.canvas.draw()

    def updateControlPathButtons(self):
        setButtonStyle(self.next_button, '505050' if self.path_index >= len(self.paths) - 1 else '5060FF')
        setButtonStyle(self.previous_button, '505050' if self.path_index <= 0 else '5060FF')

    def updateAnnot(self, ind):
        x, y = self.cities_x[ind], self.cities_y[ind]
        self.annot.xy = (x, y)
        text = f"({x:.2f}, {y:.2f})"
        self.annot.set_text(text)

        x_offset, y_offset = 10, 10
        if x > 0.85 * self.ax.get_xlim()[1]:
            x_offset = -30
        self.annot.set_position((x_offset, y_offset))

    def hover(self, event):
        if event.inaxes == self.ax:
            if self.selected_city is not None:
                if event.button != 1:
                    self.selected_city = None
                self.moveCity(self.selected_city, event.xdata, event.ydata)
                return
            for i, (x, y) in enumerate(zip(self.cities_x, self.cities_y)):
                if abs(x - event.xdata) < 0.01 and abs(y - event.ydata) < 0.01:
                    self.updateAnnot(i)
                    self.annot.set_visible(True)
                    self.canvas.draw_idle()
                    return
        if self.annot.get_visible():
            self.annot.set_visible(False)
            self.canvas.draw_idle()

    def onClick(self, event):
        if event.button == 0:
            self.selected_city = None
            for i, (x, y) in enumerate(zip(self.cities_x, self.cities_y)):
                if abs(x - event.xdata) < 0.01 and abs(y - event.ydata) < 0.01:
                    self.selected_city = i
                    return
        elif event.button == 2:
            self.addCity(event.xdata, event.ydata)

    def initTCP(self):
        self.paths.clear()
        self.distances.clear()
        self.path_index = 0
        self.updateControlPathButtons()
        self.path_control_buttons.show()