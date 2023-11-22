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

# Найти длинные объекты на бинарном изображении
def detect_long_objects(binary):

	# Найти объекты
	field, count = label(binary)

	# Подсчитать площадь каждого объекта, одной операцией
	area = np.bincount(field.flatten())
	largest = area.argsort()

	for i in largest[-4:-1]:
		plt.figure()
		plt.title(f"Area: {area[i]}")
		plt.imshow(field == i)
		plt.show()

for filename in glob("images/*.jpg"):
	img = cv2.imread(filename)

	# Сделать RGB из BGR
	img = img[:, :, ::-1]

	#visual_debug(img)
	binary = binarize(img)
	detect_long_objects(binary)
