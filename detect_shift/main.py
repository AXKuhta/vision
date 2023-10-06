import matplotlib.pyplot as plt
import numpy as np

def load_img(filename):
	with open(filename) as f:
		for line in f:
			if line.strip() == "#":
				break

		return np.loadtxt(f)

img1 = load_img("img1.txt")
img2 = load_img("img2.txt")

assert img1.shape == img2.shape
w, h = img1.shape

y1, x1 = np.where(img1 > 0)
y2, x2 = np.where(img2 > 0)

center1 = np.array([y1.mean(), x1.mean()])
center2 = np.array([y2.mean(), x2.mean()])

print("Shift Y X:", center2 - center1)
