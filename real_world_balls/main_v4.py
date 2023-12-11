import matplotlib.pyplot as plt
from random import random
from time import sleep
import numpy as np
import cv2

capture = cv2.VideoCapture(14)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
capture.set(cv2.CAP_PROP_EXPOSURE, -8)  # Чем меньше число, тем меньше экспозиция
capture.set(cv2.CAP_PROP_TEMPERATURE, 200)

cv2.namedWindow("Camera")
# cv2.namedWindow("Background")
# cv2.namedWindow("Debug")
position = (0, 0)


def on_mouse_click(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		global position
		position = (x, y)
		print(position)

# Выбрать пиксели в четырёх диапазонах
def select_rygb(frame):
	red_s = frame >= 0
	red_e = frame <= 16

	yellow_s = frame >= 37
	yellow_e = frame <= 50

	green_s = frame >= 95
	green_e = frame <= 115

	blue_s = frame >= 130
	blue_e = frame <= 150

	red_s *= red_e
	yellow_s *= yellow_e
	green_s *= green_e
	blue_s *= blue_e

	return red_s, yellow_s, green_s, blue_s

def detect_ball(mask):
	width = mask.sum(1).max()
	height = mask.sum(0).max()
	area = mask.sum()
	radius = np.sqrt(area / np.pi)
	rows, cols = np.where(mask)
	row, col = rows.mean(), cols.mean()

	return row, col, radius, (width / radius) * (height / radius)

def ask_colors(n=3):
	avail_colors = ["red", "yellow", "green", "blue"]
	request = []

	for i in range(n):
		idx = int(len(avail_colors) * random())
		request.append(avail_colors[idx])
		avail_colors.pop(idx)

	return request

request = ask_colors(3)

req_text = f"Please show me {request}, horizontal"

cv2.setMouseCallback("Camera", on_mouse_click)
plt.figure()
while capture.isOpened():
	ret, frame = capture.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)

	cv2.circle(frame, position, 5, (255, 127, 255))

	bgr_pt = np.uint8([[frame[position[1], position[0]]]])
	hsv_pt = cv2.cvtColor(bgr_pt, cv2.COLOR_BGR2HSV)[0][0]

	red, yellow, green, blue = select_rygb(hsv[:, :, 0])

	bright = hsv[:, :, 2] > 150
	saturated = hsv[:, :, 1] > 200

	nice_red = bright*saturated*red
	nice_yellow = bright*saturated*yellow
	nice_green = bright*saturated*green
	nice_blue = bright*saturated*blue

	red_row, red_col, red_radius, red_ratio = detect_ball(nice_red)
	yellow_row, yellow_col, yellow_radius, yellow_ratio = detect_ball(nice_yellow)
	green_row, green_col, green_radius, green_ratio = detect_ball(nice_green)
	blue_row, blue_col, blue_radius, blue_ratio = detect_ball(nice_blue)

	balls = []

	if red_row > 0 and red_col > 0:
		cv2.circle(frame, (round(red_col), round(red_row)), 5, (0, 0, 125), 4)
		balls.append({
			"color": "red",
			"row": red_row,
			"col": red_col
		})

	if yellow_row > 0 and yellow_col > 0:
		cv2.circle(frame, (round(yellow_col), round(yellow_row)), 5, (0, 125, 125), 4)
		balls.append({
			"color": "yellow",
			"row": yellow_row,
			"col": yellow_col
		})

	if green_row > 0 and green_col > 0:
		cv2.circle(frame, (round(green_col), round(green_row)), 5, (0, 125, 0), 4)
		balls.append({
			"color": "green",
			"row": green_row,
			"col": green_col
		})

	if blue_row > 0 and blue_col > 0:
		cv2.circle(frame, (round(blue_col), round(blue_row)), 5, (125, 0, 0), 4)
		balls.append({
			"color": "blue",
			"row": blue_row,
			"col": blue_col
		})

	sort_horizontal_fn = lambda x: x["col"]
	sort_grid_fn = lambda x: (x["row"], x["col"])

	shown = [x["color"] for x in sorted(balls, key=sort_grid_fn)]

	if shown == request:
		cv2.putText(frame, f"Good!", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))
		cv2.imshow("Camera", frame)
		cv2.waitKey(5000)
		request = ask_colors(4)
		req_text = f"Please show me {request}, grid"
	else:
		cv2.putText(frame, req_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))

	cv2.imshow("Camera", frame) #nice_red.astype("ubyte") * 255
	key = cv2.waitKey(1)
	if key == ord("q"):
		break

capture.release()
cv2.destroyAllWindows()
