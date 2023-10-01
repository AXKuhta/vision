import matplotlib.pyplot as plt
import numpy as np

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

size = 100
image = np.zeros((size, size, 3), dtype="uint8")
assert image.shape[0] == image.shape[1]

color2 = [255, 128, 0]
color1 = [0, 128, 255]

u = np.linspace(0, 0.5, size)
v = u.reshape([size, 1])
w = u + v

image[:, :, 0] = lerp(color1[0], color2[0], w)
image[:, :, 1] = lerp(color1[1], color2[1], w)
image[:, :, 2] = lerp(color1[2], color2[2], w)

plt.figure(1)
plt.imshow(image)
plt.show()
