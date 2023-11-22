from skimage.filters import threshold_otsu
from scipy.ndimage import label
import matplotlib.pyplot as plt
from glob import glob
import numpy as np
import cv2 # Используется для загрузки картинок

def visual_debug(img):
	plt.figure()
	plt.imshow(img)
	plt.show()

# Бинаризировать по порогу otsu
def binarize(img):
	gray = img.sum(2).astype("uint16")
	thresh = threshold_otsu(gray)

	binary = gray.copy()
	binary[binary > thresh] = 0
	binary[binary > 0] = 1

	return binary

# Повернуть облако точек против часовой стрелки на angle (в радианах) и найти соотношение ширины к высоте
def tilt_and_calc_ratio(rows, cols, angle):
	rows_tilt = -np.sin(angle)*cols + np.cos(angle)*rows
	cols_tilt = np.cos(angle)*cols + np.sin(angle)*rows

	row_span_tilt = rows_tilt.max() - rows_tilt.min()
	col_span_tilt = cols_tilt.max() - cols_tilt.min()

	return col_span_tilt / row_span_tilt

# Найти длинные объекты на бинарном изображении
def detect_long_objects(binary):
	pencils = []

	# Найти объекты
	field, count = label(binary)

	# Подсчитать площадь каждого объекта, одной операцией
	area = np.bincount(field.flatten())
	largest = area.argsort()

	# Пробежка по объектам
	# - Пропустить фон
	# - Пропустить всякую мелочь
	for i, s in enumerate(area):
		if i == 0:
			continue

		if s < 200000:
			continue

		# Получить точки
		rows, cols = np.where(field == i)

		row_span = rows.max() - rows.min()
		col_span = cols.max() - cols.min()

		# Попробовать отгадать угол
		# Будет ~0 для лежащих горизонтально карандашей и ~pi/2 для лежащих вертикально карандашей
		ratio = row_span / col_span
		angle = np.arctan(ratio)

		# Попробовать довернуть карандаш против часовой стрелки... и по часовой стрелке
		# Из одного ratio нельзя однозначно понять, куда его надо доворачивать
		wide_factor_a = tilt_and_calc_ratio(rows, cols, 0)
		wide_factor_b = tilt_and_calc_ratio(rows, cols, angle)
		wide_factor_c = tilt_and_calc_ratio(rows, cols, -angle)

		# Признать это карандашом, если он более чем в 10 раз длиннее, чем он выше
		if wide_factor_b > 10 or wide_factor_c > 10:
			pencils.append(i)
			pencil = True
		else:
			pencil = False

		"""
		plt.figure()
		plt.title(f"Angle: {angle}\nPencil? {pencil}")
		plt.imshow(field == i)
		plt.show()
		"""

	return len(pencils)

total = 0

for filename in glob("images/*.jpg"):
	img = cv2.imread(filename)

	# Сделать RGB из BGR
	img = img[:, :, ::-1]

	#visual_debug(img)
	binary = binarize(img)
	long_count = detect_long_objects(binary)

	print(f"{filename}\t{long_count} pencils")

	total += long_count

print(total, "pencils total")
