import time
import pyautogui
import pyautogui as hid
from win32api import GetSystemMetrics

from utils import voice


class Interactor:
	# This class is for forward gesture commands to computer.

	def __init__(self):
		self.last_runtime = 0
		self.default_sleep_time = 2 # Sleep time for using bounce miss clicks.
		self.screensize_x = GetSystemMetrics(0) # Get screen width
		self.screensize_y = GetSystemMetrics(1) # Get Screen height
		self.mouse_cursor_last_position = pyautogui.position() # get last position of mouse cursor.

	def left_click(self): # Mouse left click.
		current_time = time.time()
		if current_time - self.last_runtime > self.default_sleep_time: # This condition for bounce blocking. (Multi clicks for a command)
			self.last_runtime = current_time # Time is holding for bounce blocking.
			hid.click(button='left') # PyAutoGUI's click function using for mouse left click.

	def right_click(self): # Mouse right click.
		current_time = time.time()
		if current_time - self.last_runtime > self.default_sleep_time:
			self.last_runtime = current_time
			hid.click(button='right')

	def scroll(self, is_up: bool = True, speed: float = 0.1): # Mouse scroll function. Variables: is_up: for direction, speed: scroll speed.
		if is_up:
			hid.scroll(speed)
		elif  is_up is not True :
			speed = int((-1)*speed)
			hid.scroll(speed)

	def move(self, landmark:list): # Mouse cursor move function, work with landmark coordinates.
		# Landmark is an array, it's structure [index, x_coordinate, y_coordinate]
		hid.moveTo(landmark[1], landmark[2])

	def write_text(self, text):
		hid.write(text)

	def add_new_tab(self): # Shortcut key combination function for open a new tab in browser.
		current_time = time.time()
		if current_time - self.last_runtime > self.default_sleep_time:
			hid.hotkey('ctrl','t')
			self.last_runtime = current_time

	def close_tab(self): # Shortcut key combination function for close current tab in browser.
		current_time = time.time()
		if current_time - self.last_runtime > self.default_sleep_time:
			hid.hotkey('ctrl','w')
			self.last_runtime = current_time

	def change_tab(self): # Shortcut key combination function for change to next tab in browser.
		current_time = time.time()
		if current_time - self.last_runtime > self.default_sleep_time:
			hid.hotkey('ctrl','tab')
			self.last_runtime = current_time

	def voice_listen(self): # This function voice listen function run and get text. After write text to selected input.
		current_time = time.time()
		if current_time - self.last_runtime > 5:
			self.last_runtime = current_time
			text = voice.voice_to_text()
			if text != None:
				print(text)
				self.write_text(text)
			else:
				print("else: ",text)

