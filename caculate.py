import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseButton

class DraggablePoint:
    def __init__(self, point, annotation, line, other_point):
        self.point = point
        self.annotation = annotation
        self.line = line
        self.other_point = other_point
        self.press = None
        self.background = None

    def connect(self):
        self.cidpress = self.point.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        if event.button is not MouseButton.LEFT: return
        contains, attr = self.point.contains(event)
        if not contains: return
        self.press = (self.point.get_xdata(), self.point.get_ydata()), event.xdata, event.ydata
        self.point.set_animated(True)
        self.annotation.set_animated(True)
        self.line.set_animated(True)
        self.point.figure.canvas.draw()
        self.background = self.point.figure.canvas.copy_from_bbox(self.point.axes.bbox)

    def on_motion(self, event):
        if self.press is None: return
        if event.inaxes != self.point.axes: return
        (x0, y0), xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.point.set_xdata([x0[0] + dx])
        self.point.set_ydata([y0[0] + dy])
        self.annotation.xy = (x0[0] + dx, y0[0] + dy)
        self.annotation.set_position((x0[0] + dx, y0[0] + dy + 10 if self.annotation.get_text() == 'A' else -15))

        x_data = [self.point.get_xdata()[0], self.other_point.get_xdata()[0]]
        y_data = [self.point.get_ydata()[0], self.other_point.get_ydata()[0]]
        self.line.set_data(x_data, y_data)

        self.point.figure.canvas.restore_region(self.background)
        self.point.axes.draw_artist(self.point)
        self.point.axes.draw_artist(self.annotation)
        self.point.axes.draw_artist(self.line)
        self.point.figure.canvas.blit(self.point.axes.bbox)

    def on_release(self, event):
        if self.press is None: return
        self.press = None
        self.point.set_animated(False)
        self.annotation.set_animated(False)
        self.line.set_animated(False)
        self.background = None
        self.point.figure.canvas.draw()

    def disconnect(self):
        self.point.figure.canvas.mpl_disconnect(self.cidpress)
        self.point.figure.canvas.mpl_disconnect(self.cidrelease)
        self.point.figure.canvas.mpl_disconnect(self.cidmotion)

class DraggableLine:
    def __init__(self, line):
        self.line = line
        self.press = None
        self.background = None

    def connect(self):
        self.cidpress = self.line.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.line.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.line.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.line.axes: return
        if event.button is not MouseButton.LEFT: return
        contains, attr = self.line.contains(event)
        if not contains: return
        self.press = event.ydata
        self.line.set_animated(True)
        self.line.figure.canvas.draw()
        self.background = self.line.figure.canvas.copy_from_bbox(self.line.axes.bbox)

    def on_motion(self, event):
        if self.press is None: return
        if event.inaxes != self.line.axes: return
        dy = event.ydata - self.press
        xdata = self.line.get_xdata()
        ydata = self.line.get_ydata() + dy
        self.line.set_ydata(ydata)
        self.press = event.ydata

        self.line.figure.canvas.restore_region(self.background)
        self.line.axes.draw_artist(self.line)
        self.line.figure.canvas.blit(self.line.axes.bbox)

    def on_release(self, event):
        if self.press is None: return
        self.press = None
        self.line.set_animated(False)
        self.background = None
        self.line.figure.canvas.draw()

    def disconnect(self):
        self.line.figure.canvas.mpl_disconnect(self.cidpress)
        self.line.figure.canvas.mpl_disconnect(self.cidrelease)
        self.line.figure.canvas.mpl_disconnect(self.cidmotion)

# Function to find intersection points
def find_intersections(x, y1, y2):
    x_intersections = []
    y_intersections = []
    for i in range(len(x) - 1):
        if (y1[i] - y2[i]) * (y1[i + 1] - y2[i + 1]) < 0:
            x_intersections.append((x[i] + x[i + 1]) / 2)
            y_intersections.append((y1[i] + y1[i + 1]) / 2)
    return x_intersections, y_intersections

x = np.linspace(-50, 50, 800)
uK = np.tan(np.radians(150))

fig, ax = plt.subplots(figsize=(10, 10))

line_density = 4
num_lines = int((100 - (-50)) / line_density) + 1

# Store diagonal lines for intersection checks
diagonal_lines = []
for i in range(num_lines):
    offset = i * line_density - 50
    y = uK * (x + offset)
    line, = ax.plot(x, y, color='blue', linewidth=0.5)
    diagonal_lines.append(line)

x_coord = np.random.uniform(-50, 50)
y_coords = np.random.uniform(-50, 50, 2)

if y_coords[0] < y_coords[1]:
    y_coords[0], y_coords[1] = y_coords[1], y_coords[0]

pointA, = ax.plot([x_coord], [y_coords[0]], 'ro', markersize=8)
pointB, = ax.plot([x_coord], [y_coords[1]], 'ro', markersize=8)
connecting_line, = ax.plot([x_coord, x_coord], y_coords, 'blue', linewidth=2)

annotationA = ax.annotate('A', (x_coord, y_coords[0]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=12, color='black')
annotationB = ax.annotate('B', (x_coord, y_coords[1]), textcoords="offset points", xytext=(0, -15), ha='center', fontsize=12, color='black')

draggableA = DraggablePoint(pointA, annotationA, connecting_line, pointB)
draggableA.connect()

draggableB = DraggablePoint(pointB, annotationB, connecting_line, pointA)
draggableB.connect()

x_horizon = np.linspace(-50, 50, 800)
y_horizon = np.zeros_like(x_horizon)
initial_offsets = [0, 12]  # Initial offsets for 2 green lines
green_lines = [
    ax.plot(x_horizon, y_horizon + offset, color='green', linewidth=1)[0] for offset in initial_offsets
]

draggable_green_lines = [DraggableLine(line) for line in green_lines]
for draggable_green_line in draggable_green_lines:
    draggable_green_line.connect()

# Function to adjust green lines' distances
def adjust_green_lines(step):
    for i, line in enumerate(green_lines):
        current_ydata = line.get_ydata()
        new_ydata = current_ydata + step * (i + 1)  # (i + 1) to ensure line 2 moves more than line 1
        line.set_ydata(new_ydata)
    fig.canvas.draw_idle()

# Find and plot intersections for each green line with diagonal lines
for green_line in green_lines:
    green_y_data = green_line.get_ydata()
    for diag_line in diagonal_lines:
        diag_y_data = diag_line.get_ydata()
        x_intersections, y_intersections = find_intersections(x, green_y_data, diag_y_data)
        ax.scatter(x_intersections, y_intersections, color='black', s=10, zorder=5)  # s=10 sets the size smaller

ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_ylim(-100, 100)

def on_key(event):
    if event.key == 'up':
        adjust_green_lines(-0.2)  # Decrease distance
    elif event.key == 'down':
        adjust_green_lines(0.2)  # Increase distance

fig.canvas.mpl_connect('key_press_event', on_key)

plt.show()