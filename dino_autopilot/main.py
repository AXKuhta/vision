import matplotlib.pyplot as plt
from mss import mss
import numpy as np
import pyautogui
from time import sleep, perf_counter

# ОСТОРОЖНО
pyautogui.PAUSE = 0

sct = mss()

def visual_debug(image):
	plt.figure()
	plt.imshow(image)
	plt.show()

# Захватить экран и бинаризировать
def binary_frame(roi=None):
	if roi is None:
		roi = sct.monitors[0]

	shot = sct.grab(roi)
	h, w = shot.height, shot.width

	# rgb = геттер (https://github.com/BoboTiG/python-mss/blob/main/src/mss/screenshot.py)
	# Если нужен один канал, лучше взять shot.raw[::4]
	bin = np.array(shot.raw[::4]).reshape(h, w) == 83

	# visual_debug(bin)

	return bin

def roi_detect():
	frame = binary_frame()
	baseline = frame.sum(1).argmax()
	first_col = None
	last_col = None

	for i, v in enumerate(frame[baseline]):
		if v:
			last_col = i
			if first_col is None:
				first_col = i

	print("Game detect:", first_col, last_col)

	# Предположим, что соотношение сторон всегда 7/30
	width = last_col - first_col
	height = round(width * 7/30)

	return {
		"width": width,
		"height": height,
		"left": first_col,
		"top": baseline - height,
		"mon": 0
	}

roi = roi_detect()

# Предположим, что динозавр всегда в первой 1/8 экрана
dino_ends = round(roi["width"] / 8)

# Предположим, что все наземные препятствия можно увидеть по линии, расположенной на 7/8 высоты экрана
obstacle_level = round(roi["height"] * 7/8)

danger_zone = round(dino_ends*1.25)

np.set_printoptions(linewidth=120)

while True:
	start = perf_counter()
	game = binary_frame(roi)

	dino = game[:, :dino_ends]
	r_pts, c_pts = np.where(dino)
	dino_r, dino_c = r_pts.mean(), c_pts.mean()

	dino_airborne = dino_r < roi["height"] * 0.7

	obstacles = game[obstacle_level, dino_ends:dino_ends+danger_zone]

	if not dino_airborne:
		if np.any(obstacles):
			pyautogui.keyDown("space")
			sleep(1/50) # 50 Hz
			pyautogui.keyUp("space")

	elapsed = perf_counter() - start
	#print(f"{elapsed*1000:.1f}ms processing")
	sleep(1/20) # 20 Hz
