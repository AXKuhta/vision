import matplotlib.pyplot as plt
from mss import mss
import numpy as np
import pyautogui
from time import sleep, perf_counter

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

while True:
	start = perf_counter()
	game = binary_frame(roi)

	# 1134 is the last pixel of the dino
	if np.any(game.sum(0)[100:150] > 10):
		pyautogui.press("space")

	elapsed = perf_counter() - start
	print(f"{elapsed*1000:.1f}ms processing")
	sleep(.05)
