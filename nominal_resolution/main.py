import numpy as np
from glob import glob

def load_img(filename):
	with open(filename) as f:
		horizontal_size_mm = 0

		for line in f:
			if line.strip() == "#":
				break
			else:
				horizontal_size_mm = float(line)

		return horizontal_size_mm, np.loadtxt(f)

files = sorted(glob("*.txt"))

for name in files:
	size, image = load_img(name)
	max_pixels_in_row = image.sum(1).max() # Т.к. на картинке только один объект, можно найти его ширину в пикселях, просуммировав столбцы

	if max_pixels_in_row > 0:
		resolution = f"{size / max_pixels_in_row} mm"
	else:
		resolution = f"N/A"

	print(f"{name}: {resolution}")
