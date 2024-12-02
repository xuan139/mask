import numpy as np
import matplotlib.pyplot as plt
import math

# Given constants
uD = 2.5859 - 0.044
uM = 0
angle_degrees = 152.585709  # 夹角为60度

# Convert angle to radians
angle_radians = math.radians(angle_degrees)
# Calculate tangent value
uK = math.tan(angle_radians)

# Calculate result of square root
result = np.sqrt(uK ** 2 + 1.0)
halfD = uD * result * 0.50
xStep = halfD / uK

print("uD:", uD, "halfD:", halfD, "uK:", uK, 'xStep', xStep)

# Generate gl_FragCoord.x and gl_FragCoord.y values
gl_FragCoord_x = np.arange(0, 63)
gl_FragCoord_y = np.arange(0, 32)

# Function to calculate and plot w1 values
def plot_w1_values(uM):
    plt.clf()  # Clear the current figure
    w1_values = np.mod(np.abs(uK * gl_FragCoord_x[:, np.newaxis] - gl_FragCoord_y + 5000.0 + uM)/result, uD)
    red_points = {'x': [], 'y': [], 'value': []}
    green_points = {'x': [], 'y': [], 'value': []}
    
    for j in range(len(gl_FragCoord_y)):
        row_values = []
        for i in range(len(gl_FragCoord_x)):
            if w1_values[i][j] < uD * 0.5:
                red_points['x'].append(gl_FragCoord_x[i])
                red_points['y'].append(gl_FragCoord_y[j])
                red_points['value'].append(w1_values[i][j])
                row_values.append(f"{w1_values[i][j]:.2f}")
            else:
                green_points['x'].append(gl_FragCoord_x[i])
                green_points['y'].append(gl_FragCoord_y[j])
                green_points['value'].append(w1_values[i][j])
                row_values.append(f"{w1_values[i][j]:.2f}")
        # 打印每一行的数据，不包括坐标
        if(j==0):
            print(f"Row {j}: " + ", ".join(row_values))
    
    plt.scatter(red_points['x'], red_points['y'], color='red', marker='s', s=40)
    plt.scatter(green_points['x'], green_points['y'], color='green', marker='s', s=40)
    
    plt.gca().set_aspect(1.0)
    plt.ylim(0, len(gl_FragCoord_y))  # Set Y axis limits to start from 0 at the bottom
    plt.title(f'Points with w1 < {uD * 0.5} (uM = {uM})')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.draw()

# Initial plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots(figsize=(10, 5.35))
plot_w1_values(uM)

uK = math.tan(angle_radians)
# Event handler for key press
def on_key(event):
    global uM
    if event.key == 'up':
        uM += (uK)
        print("uD:", uD, "halfD:", halfD, "uK:", uK, 'xStep', xStep)
        plot_w1_values(uM)
    elif event.key == 'down':
        uM -= (uK)
        print("uD:", uD, "halfD:", halfD, "uK:", uK, 'xStep', xStep)
        plot_w1_values(uM)
    elif event.key == 'left':
        uM += 1.0
        print("uD:", uD, "halfD:", halfD, "uK:", uK, 'xStep', xStep)
        plot_w1_values(uM)
    elif event.key == 'right':
        print("uD:", uD, "halfD:", halfD, "uK:", uK, 'xStep', xStep)
        uM -= 1.0
        plot_w1_values(uM)
    elif event.key == ' ':
        uM = 0
        plot_w1_values(uM)

# Connect the event handler to the figure
fig.canvas.mpl_connect('key_press_event', on_key)

plt.show(block=True)
