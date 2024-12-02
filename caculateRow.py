import numpy as np
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
gl_FragCoord_y = np.arange(0, 63)

# Function to calculate and print w1 values
def print_w1_values(uM):
    w1_values = np.mod(np.abs(uK * gl_FragCoord_x[:, np.newaxis] - gl_FragCoord_y + 5000.0 + uM)/result, uD)
    for j in range(len(gl_FragCoord_y)):
        row_values = []
        for i in range(len(gl_FragCoord_x)):
            row_values.append(f"{w1_values[i][j]:.2f}")
        # 打印每一行的数据，不包括坐标
        if j == 0 or j == 20 or j == 40: 
            print(f"Row {j}: " + ", ".join(row_values))

# 计算并打印初始值
print_w1_values(uM)
