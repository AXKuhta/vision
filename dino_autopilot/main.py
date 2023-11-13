import matplotlib.pyplot as plt
from mss import mss
import numpy as np
import pyautogui
from time import sleep

sct = mss()

def visual_debug(image):
	plt.figure()
	plt.imshow(image)
	plt.show()

# Захватить экран и бинаризировать
def binary_frame():
	shot = sct.grab(sct.monitors[0])
	h, w = shot.height, shot.width

	# rgb = геттер (https://github.com/BoboTiG/python-mss/blob/main/src/mss/screenshot.py)
	# Если нужен один канал, лучше взять shot.raw[::4]
	bin = np.array(shot.raw[::4]).reshape(h, w) == 83

	# visual_debug(bin)

	return bin

while True:
	frame = binary_frame()

	if np.any(frame.sum(0)[1160:1260] > 10):
		pyautogui.press("space")

	sleep(.1)
