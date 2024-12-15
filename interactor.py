import time
import pyautogui
import pyautogui as hid
from win32api import GetSystemMetrics

import voice


class Interactor:

	def __init__(self):
		self.last_runtime = 0
		self.default_sleep_time = 2
		self.screensize_x = GetSystemMetrics(0)
		self.screensize_y = GetSystemMetrics(1)
		self.mouse_cursor_last_position = pyautogui.position()
		self.is_first_click = 0

	def left_click(self):
		current_time = time.time()
		if current_time - self.last_runtime > self.default_sleep_time:
			self.last_runtime = current_time
			hid.click(button='left')

	def right_click(self):
		current_time = time.time()
		if current_time - self.last_runtime > self.default_sleep_time:
			self.last_runtime = current_time
			hid.click(button='right')

	def scroll(self, is_up: bool = True, speed: float = 0.1):
		if is_up:
			hid.scroll(speed)
		elif  is_up is not True :
			speed = int((-1)*speed)
			hid.scroll(speed)

	def move(self, landmark:list):
		hid.moveTo(landmark[1], landmark[2])

	def write_text(self, text):
		hid.write(text)

	def add_new_tab(self):
		current_time = time.time()
		if current_time - self.last_runtime > self.default_sleep_time:
			hid.hotkey('ctrl','t')
			self.last_runtime = current_time

	def close_tab(self):
		current_time = time.time()
		if current_time - self.last_runtime > self.default_sleep_time:
			hid.hotkey('ctrl','w')
			self.last_runtime = current_time

	def change_tab(self):
		current_time = time.time()
		if current_time - self.last_runtime > self.default_sleep_time:
			hid.hotkey('ctrl','tab')
			self.last_runtime = current_time

	def voice_listen(self):
		current_time = time.time()
		if current_time - self.last_runtime > self.default_sleep_time:
			self.last_runtime = current_time
			text = voice.voice_to_text()
			self.write_text(text)
