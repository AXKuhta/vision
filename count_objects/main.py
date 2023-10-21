from scipy.ndimage import binary_erosion, binary_dilation, binary_opening, binary_closing, label
import matplotlib.pyplot as plt
import numpy as np

hole_d = np.array(
	[[1,1,1,1,1,1],
	 [1,1,1,1,1,1],
	 [1,1,0,0,1,1],
	 [1,1,0,0,1,1]]
)

hole_u = hole_d[::-1, :]
hole_r = hole_d.T
hole_l = hole_r[:, ::-1]

no_hole = np.ones([4, 6])

arr = np.load("ps.npy.txt")

detections_no_hole = binary_erosion(arr, no_hole)
no_hole_mask = binary_dilation(detections_no_hole, no_hole)

arr_clean = arr ^ no_hole_mask

detections_hole_d = binary_erosion(arr_clean, hole_d)
detections_hole_u = binary_erosion(arr_clean, hole_u)
detections_hole_r = binary_erosion(arr_clean, hole_r)
detections_hole_l = binary_erosion(arr_clean, hole_l)

def visual_debug():
	plt.figure()
	plt.imshow(arr)
	plt.scatter(*np.where(detections_no_hole)[::-1], label="no hole")
	plt.scatter(*np.where(detections_hole_d)[::-1], label="hole down")
	plt.scatter(*np.where(detections_hole_u)[::-1], label="hole up")
	plt.scatter(*np.where(detections_hole_r)[::-1], label="hole right")
	plt.scatter(*np.where(detections_hole_l)[::-1], label="hole left")
	plt.legend()
	plt.show()

#visual_debug()

print("No hole:\t", detections_no_hole.sum())
print("Hole down:\t", detections_hole_d.sum())
print("Hole up:\t", detections_hole_u.sum())
print("Hole right:\t", detections_hole_r.sum())
print("Hole left:\t", detections_hole_l.sum())
