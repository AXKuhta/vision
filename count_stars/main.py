from scipy.ndimage import binary_erosion, binary_dilation, binary_opening, binary_closing, label
import matplotlib.pyplot as plt
import numpy as np

star_type_1 = np.array(
	[[0, 0, 1, 0, 0],
	 [0, 0, 1, 0, 0],
	 [1, 1, 1, 1, 1],
	 [0, 0, 1, 0, 0],
	 [0, 0, 1, 0, 0]]
)

star_type_2 = np.array(
	[[1, 0, 0, 0, 1],
	 [0, 1, 0, 1, 0],
	 [0, 0, 1, 0, 0],
	 [0, 1, 0, 1, 0],
	 [1, 0, 0, 0, 1]]
)

arr = np.load("stars.npy").astype("i1")

detections_type_1 = binary_erosion(arr, star_type_1)
stars_type_1 = binary_dilation(detections_type_1, star_type_1)

detections_type_2 = binary_erosion(arr, star_type_2)
stars_type_2 = binary_dilation(detections_type_2, star_type_2)

_, count_type_1 = label(detections_type_1)
_, count_type_2 = label(detections_type_2)

print("Total:", count_type_1 + count_type_2)

def visual_debug():
	plt.figure()
	plt.subplot(121)
	plt.imshow(arr)
	plt.subplot(122)
	plt.imshow(arr ^ stars_type_1 ^ stars_type_2)
	plt.show()
