from skimage.measure import regionprops
import matplotlib.pyplot as plt
from scipy.ndimage import label
import numpy as np
import cv2

image = cv2.imread("balls_and_rects.png")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
hue = hsv[:, :, 0]
val = hsv[:, :, 2]

field, count = label(val)
regions = regionprops(field)

rect = []
circ = []

# Разделить на квадраты и неквадраты
for region in regions:
	if region.area == region.area_bbox:
		rect.append(region.centroid)
	else:
		circ.append(region.centroid)

# Разделить на классы оттенков
def print_hue_hist(hue, pts):
	hues = []

	for r, c in pts:
		r = round(r)
		c = round(c)

		hues.append(hue[r][c])

	bins = np.bincount(hues)

	# При неоднозначности оттенка выбрать тот, в сторону которого перевес сильнее
	for i in range(1, bins.shape[0]):
		if bins[i-1] and bins[i]:
			if bins[i-1] > bins[i]:
				bins[i-1] += bins[i]
				bins[i] = 0
			else:
				bins[i] += bins[i-1]
				bins[i-1] = 0

	# print(bins)

	print("Hue\tCount")

	for i, v in enumerate(bins):
		if v > 0:
			print(f"{i}\t{v}")

print(count, "shapes total.")
print()

print(len(rect), "rects total; hues:")
print_hue_hist(hue, rect)

print()

print(len(circ), "circles total; hues:")
print_hue_hist(hue, circ)

plt.imshow(val.T)
plt.scatter(*np.array(rect).T)
plt.scatter(*np.array(circ).T)
plt.show()
