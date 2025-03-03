from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QWidget, QGridLayout
from PyQt5.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from params import PARAMS

class ResultWindow(QDialog):
    def __init__(self, best_path, best_distance, cities):
        super().__init__()
        self.best_distance = best_distance
        self.cities = cities

        self.points_x = [cities[e][0] for e in best_path] + [cities[best_path[0]][0]]
        self.points_y = [cities[e][1] for e in best_path] + [cities[best_path[0]][1]]
        self.index = 0
        self.segments = []

        self.setWindowTitle("TSP Result")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    # --- GRAPHICAL METHODS --- #

    def initUI(self):
        layout = QVBoxLayout()

        # Result label
        result_label = QLabel(f"Best Distance: {self.best_distance}", self)
        result_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        result_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(result_label)

        self.make_legend(layout)
        self.make_graph(layout)
        self.make_buttons(layout)

        if PARAMS.animated:
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_plot)
            if PARAMS.auto_start:
                self.play_timer()
        else:
            self.ax.plot(self.points_x, self.points_y, 'b-')

        self.setLayout(layout)

    def make_legend(self, layout):
        legend_layout = QGridLayout()
        legend_layout.setAlignment(Qt.AlignLeft)

        start_legend = QLabel("Start city: ", self)
        start_legend.setStyleSheet("font-size: 14px; font-weight: bold;")
        start_legend.setMinimumHeight(16)
        legend_layout.addWidget(start_legend, 0, 0)

        start_color = QLabel(self)
        start_color.setFixedSize(10, 16)
        start_color.setStyleSheet("background-color: green; border-radius: 5px;")
        legend_layout.addWidget(start_color, 0, 1)


        start_legend = QLabel("City: ", self)
        start_legend.setStyleSheet("font-size: 14px; font-weight: bold;")
        start_legend.setMinimumHeight(16)
        legend_layout.addWidget(start_legend, 1, 0)

        start_color = QLabel(self)
        start_color.setFixedSize(10, 16)
        start_color.setStyleSheet("background-color: red; border-radius: 5px;")
        legend_layout.addWidget(start_color, 1, 1)

        start_legend = QLabel("Path: ", self)
        start_legend.setStyleSheet("font-size: 14px; font-weight: bold;")
        start_legend.setMinimumHeight(16)
        legend_layout.addWidget(start_legend, 2, 0)

        start_color = QLabel(self)
        start_color.setFixedSize(10, 16)
        start_color.setStyleSheet("background-color: blue; border-radius: 5px;")
        legend_layout.addWidget(start_color, 2, 1)

        legend_layout.setSpacing(10)
        layout.addLayout(legend_layout)

    def make_buttons(self, layout):
        if not PARAMS.animated:
            return

        buttons_layout = QHBoxLayout()

        self.previous_button = QPushButton("Previous", self)
        self.previous_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #39ED4B;")
        self.previous_button.clicked.connect(self.previous_segment)
        buttons_layout.addWidget(self.previous_button)

        self.play_button = QPushButton("Play", self)
        play_button_bg_color = "#39ED4B" if PARAMS.auto_start else "#FF0000"
        self.play_button.setStyleSheet(f"font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: {play_button_bg_color};")
        buttons_layout.addWidget(self.play_button)

        self.next_button = QPushButton("Next", self)
        self.next_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #39ED4B;")
        self.next_button.clicked.connect(self.next_segment)
        buttons_layout.addWidget(self.next_button)

        layout.addLayout(buttons_layout)

    def make_graph(self, layout):
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)

        self.vertices = self.ax.plot(self.points_x, self.points_y, 'ro') + \
                        self.ax.plot(self.points_x[:1], self.points_y[:1], 'go')
        self.ax.set_xlim(min(self.points_x) - 0.05, max(self.points_x) + 0.05)
        self.ax.set_ylim(min(self.points_y) - 0.05, max(self.points_y) + 0.05)

        layout.addWidget(self.canvas)

        # Add tooltips
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),
                                      textcoords="offset points",
                                      bbox=dict(boxstyle="round", fc="w"),
                                      arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)

        self.canvas.mpl_connect("motion_notify_event", self.hover)

    # --- UTILITY METHODS --- #

    def update_plot(self):
        if self.index < len(self.points_x) - 1:
            self.next_segment()
        else:
            self.stop_timer()

    def next_segment(self):
        if self.index >= len(self.points_x) - 1:
            return
        segment, = self.ax.plot(
            [self.points_x[self.index], self.points_x[self.index+1]],
            [self.points_y[self.index], self.points_y[self.index+1]],
            'b-'
        )

        for v in self.vertices:
            v.remove()
        self.vertices = self.ax.plot(self.points_x, self.points_y, 'ro') + \
                        self.ax.plot(self.points_x[:1], self.points_y[:1], 'go')

        self.segments.append(segment)
        self.canvas.draw()
        self.index += 1
        self.update_buttons()

    def previous_segment(self):
        if self.index == 0:
            return
        self.segments.pop().remove()
        self.canvas.draw()
        self.index -= 1
        self.update_buttons()

    def play_timer(self):
        if self.index < len(self.points_x) - 1:
            self.timer.start(PARAMS.animation_speed)
            self.play_button.clicked.connect(self.stop_timer)
        self.update_buttons()

    def stop_timer(self):
        self.timer.stop()
        self.play_button.clicked.connect(self.play_timer)
        self.update_buttons()

    def update_buttons(self):
        def set_button_style(button, text, color):
            button.setText(text)
            button.setStyleSheet(f"font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: {color};")

        prev_color = "#A0A0A0" if self.index == 0 else "#39ED4B"
        set_button_style(self.previous_button, "Previous", prev_color)

        if self.index >= len(self.points_x) - 1:
            set_button_style(self.play_button, "Play", "#A0A0A0")
            set_button_style(self.next_button, "Next", "#A0A0A0")
        else:
            play_text = "Pause" if self.timer.isActive() else "Play"
            set_button_style(self.play_button, play_text, "#39ED4B")
            set_button_style(self.next_button, "Next", "#39ED4B")

    def update_annot(self, ind):
        x, y = self.points_x[ind], self.points_y[ind]
        self.annot.xy = (x, y)
        text = f"({x:.2f}, {y:.2f})"
        self.annot.set_text(text)
        # Box transparency
        self.annot.get_bbox_patch().set_alpha(0.4)

    def hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            for i, (x, y) in enumerate(zip(self.points_x, self.points_y)):
                if abs(x - event.xdata) < 0.01 and abs(y - event.ydata) < 0.01:
                    self.update_annot(i)
                    self.annot.set_visible(True)
                    self.canvas.draw_idle()
                    return
            if vis:
                self.annot.set_visible(False)
                self.canvas.draw_idle()