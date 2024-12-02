import pyautogui

class Interactor:
	def __init__(self):
		pass

	def left_click(self):
		pyautogui.click(button='left')

	def right_click(self):
		pyautogui.click(button='right')

	def scroll(self, is_up: bool = True):
		if is_up:
			pyautogui.scroll(10)
		elif  is_up is not True :
			pyautogui.scroll(-10)
		else:
			print("'is_up' is required value for mouse scroll.")

	def move(self, x_offset,y_offset):
		pyautogui.moveTo(x_offset, y_offset)
		return

	def write_text(self, text):
		pyautogui.write(text)

