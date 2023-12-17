import numpy as np
import cv2

cap = cv2.VideoCapture('output.avi')
detections = 0
i = 0

while cap.isOpened():
	ret, frame = cap.read()
	i += 1

	# if frame is read correctly ret is True
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break

	binary = (frame < np.array([100, 100, 100])).prod(2).astype("ubyte") * 255
	cv2.imshow('frame', binary)

	#gray = 255 - cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	contours, tree = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# 1. Найти уровень иерархии, на котором 40 точек
	# 2. Если этот уровень не является корнем дерева, признать эту фигуру "мухобойкой"
	if tree is not None:
		terminal_contour_count = {}

		for next, prev, first_child, parent in tree[0]:
			if first_child == -1:
				terminal_contour_count[parent] = terminal_contour_count[parent] + 1 if parent in terminal_contour_count else 1

		matches = 0

		for parent, count in terminal_contour_count.items():
			if count == 40 and parent != -1:
				matches += 1

		if matches == 1:
			print("Detected at frame", i)
			detections += 1
			# cv2.waitKey(1000)
		elif matches == 0:
			pass
		else:
			raise Exception("???")

	if cv2.waitKey(1) == ord('q'):
		break

print(detections, "detections total")

cap.release()
cv2.destroyAllWindows()
