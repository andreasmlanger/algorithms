import numpy as np
import matplotlib.pyplot as plt


SPAN = 8  # x1, x2 space


# 2D function
def f(x1, x2):
    return (x1 - 2) ** 2 + x2 ** 2 + x1 * x2


x, y = np.meshgrid(np.linspace(-SPAN, SPAN, 100), np.linspace(-SPAN, SPAN, 100))

fig, ax = plt.subplots(1, 1)
cp = ax.contourf(x, y, f(x, y))
fig.colorbar(cp)
ax.set_xlabel('x1')
ax.set_ylabel('x2')

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(x, y, f(x, y), 50)
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('z')

plt.show()
