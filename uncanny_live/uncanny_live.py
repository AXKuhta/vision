from math import hypot
import numpy as np
import cv2
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.connect("tcp://192.168.0.105:6556")

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("COMPOSITE", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("BINARY", cv2.WINDOW_KEEPRATIO)

# ###########################################################################################
# Определение круглости
# ###########################################################################################

# Mean Radial Distance / Stddev Radial Distance
def roundness_v3(boundary_pts):
	relative_pts = boundary_pts - boundary_pts.mean(0)
	rd = np.linalg.norm(relative_pts, axis=1)

	return rd.mean() / rd.std()

# ###########################################################################################
# Главный цикл
# ###########################################################################################

# Загрузка кадра из файла при отсутствии камеры
with open("dump", "rb") as f:
	buffer = f.read()

while True:
	try:
		#buffer = socket.recv(zmq.NOBLOCK)

		#with open("dump", "wb") as f:
		#	f.write(buffer)
		#	input("DUMP OK")

		arr = np.frombuffer(buffer, np.uint8)
		frame = cv2.imdecode(arr, -1)

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
		hue = hsv[:, :, 0]
		sat = hsv[:, :, 1] / 255
		val = hsv[:, :, 2] / 255

		composite = sat*val
		composite_u8 = (composite * 256).astype("ubyte")

		# Помогает заделать дырки
		composite_u8 = cv2.GaussianBlur(composite_u8, (7, 7), 0)

		cv2.imshow("COMPOSITE", composite_u8)

		# Otsu теряёт зелёный кубик, у которого уровень ~67
		# thresh, binary = cv2.threshold(composite_u8, 0, 255, cv2.THRESH_OTSU)
		binary = ((composite_u8 > 40) * 255).astype("ubyte")

		cv2.imshow("BINARY", binary)

		balls = 0
		rects = 0

		# CHAIN_APPROX_SIMPLE = Упрощать контур
		# CHAIN_APPROX_NONE = Не упрощать контур
		# Мы хотим полный контур
		contours, tree = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

		for c, h in zip(contours, tree[0]):
			next, prev, first_child, parent = h
			pts = c[:, 0, :]

			# Пропускать все вложенные контуры
			if parent != -1:
				continue

			roundness = roundness_v3(pts)

			if roundness > 20:
				color = (0,255,0)
				balls += 1
			else:
				color = (0,0,255)
				rects += 1

			cv2.drawContours(frame, [pts], 0, color, 2)

		cv2.putText(frame, f"{balls} circular, {rects} noncircular", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (40, 40, 0))

		#value = cv2.GaussianBlur(composite_u8, (7, 7), 0)
		#contours = cv2.Canny(threshed, flimit, slimit)

		cv2.imshow("Camera", frame)
	except zmq.error.Again as e:
		pass
	except Exception as e:
		print(type(e), e)

	if cv2.waitKey(1) == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()
