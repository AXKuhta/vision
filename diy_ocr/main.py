from scipy.ndimage import label
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import numpy as np

image = plt.imread("symbols.png")

# Перевести в grayscale, примитивно
image = image.max(2)
image[image > 0] = 1
h, w = image.shape

field, count = label(image)

# Найти объекты
# У одного региона есть поля:
# image		Обрезанное изображение
regions = regionprops(field)

# Процент заполнения единичками
# Будет работать исключительно с бинарными изображениями
def filling_factor(region):
	return region.image.mean()

def recognize(region):
	if filling_factor(region) == 1:
		return "-"
	else:
		euler = region.euler_number
		if euler == -1: # Две дырки
			if np.all(region.image[:, 0] == 1): # НЕТ!!!!! 1 in region.image.mean(0):
				return "B"
			else:
				return "8"
		elif euler == 0: # Одна дырка: A D 0 P
			tmp = region.image.copy()
			tmp[-1] = 1
			tmp_lbl, _ = label(tmp)
			tmp_rgs = regionprops(tmp_lbl)
			if tmp_rgs[0].euler_number == -1:
				return "A"
			elif np.all(region.image[:, 0] == 1):
				vertical_symmetry_k = np.mean(region.image == region.image[::-1])

				# Попробовать отгадать между P и D на основе вертикальной симметричности
				if vertical_symmetry_k >= 0.8:
					return "D"
				else:
					return "P"

			else:
				return "0"
		else: # Нет дырок
			if 1 in region.image.mean(0):
				return "1"

			tmp = region.image.copy()
			tmp[[0, -1], :] = 1
			# tmp[:, [0, -1]] = 1
			tmp_lbl, _ = label(tmp)
			tmp_rgs = regionprops(tmp_lbl)

			# plt.figure()
			# plt.imshow(tmp_rgs[0].image)
			# plt.show()

			euler = tmp_rgs[0].euler_number

			if euler == -1:
				return "X"
			elif euler == -2:
				return "W"

			if region.eccentricity < 0.5:
				return "*"
			else:
				return "/"

	return "UNK"

counts = {}

for region in regions:
	sym = recognize(region)
	if sym not in counts:
		counts[sym] = []
	counts[sym].append(region.centroid[::-1])

print("Stats:")
total = 0

plt.figure()
plt.imshow(image)

for k, v in counts.items():
	arr = np.array(v)
	x = arr[:, 0]
	y = arr[:, 1]
	plt.scatter(x, y, label=k)
	print(f"{len(v)} ({100*len(v)/count}%)\t{k}")
	total += len(v)

print(f"Total: {total}/{count} ({100*total/count}%)")

plt.legend()
plt.show()
