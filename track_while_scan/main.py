import matplotlib.pyplot as plt
from scipy.ndimage import label
from math import dist
import numpy as np

# Трек в памяти
class Track:
	def __init__(self, id, point):
		print("New track:", id, point)
		self.id = id
		self.log = [point]

	def plot(self):
		rows = [point[0] for point in self.log]
		cols = [point[1] for point in self.log]

		plt.plot(rows, cols, label=f"Track {self.id}")
		plt.scatter(*self.extrapolate())

	def extrapolate(self):
		if len(self.log) < 2:
			return self.log[-1]

		row_a, col_a = self.log[-2]
		row_b, col_b = self.log[-1]
		row_delta = row_b - row_a
		col_delta = col_b - col_a

		return row_b + row_delta, col_b + col_delta

# Память треков
memory = []

def correlate_point(point):
	min_dist = 100
	best = None

	for track in memory:
		distance = dist(track.extrapolate(), point)
		#distance = dist(track.log[-1], point)

		if distance < min_dist:
			min_dist = distance
			best = track

	if best is not None:
		return best.log.append(point)

	memory.append(Track(len(memory), point))

plt.figure()

for i in range(100):
	filename = f"out/h_{i}.npy"
	image = np.load(filename)

	plt.clf()
	plt.imshow(image.T)

	for track in memory:
		track.plot()

	plt.legend()
	plt.pause(.1)

	field, count = label(image)

	for i in range(1, count + 1):
		row_pts, col_pts = np.where(field == i)
		point = row_pts.mean(), col_pts.mean()

		correlate_point(point)

plt.show()
