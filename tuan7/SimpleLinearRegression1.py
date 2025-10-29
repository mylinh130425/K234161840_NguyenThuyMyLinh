import matplotlib.pyplot as plt
import numpy as np

x = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]).T
y = np.array([[2, 4, 3, 6, 9, 12, 13, 15, 18, 20]]).T

# usage
def calculateb1b0(x, y):
    # tính trung bình
    xbar = np.mean(x)
    ybar = np.mean(y)
    x2bar = np.mean(x ** 2)
    xybar = np.mean(x * y)

    # tính b1, b0
    b1 = (xbar * ybar - xybar) / (xbar ** 2 - x2bar)
    b0 = ybar - b1 * xbar
    return b1, b0

# calculate b1, b0
b1, b0 = calculateb1b0(x, y)
print("b1 =", b1)
print("b0 =", b0)

y_predicted = b0 + b1 * x
print(y_predicted)
