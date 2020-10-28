import matplotlib.pyplot as plt
import pyautogui
import time

from recognizer import is_game_over, find_field

class BasicModel:

    def __init__(self, name="test"):
        self.name = name
        self._field = None
        self.game_over = False
        self._start_time = time.time()

    def run(self, field):
        self._field = field
        self.game_over = is_game_over(field)
        if not self.game_over:
            self.act()
        else:
            self._end_time = time.time()

    @property
    def score(self):
        return round(self._end_time - self._start_time, 2)

    def act():
        pass

    @staticmethod
    def none():
        pyautogui.keyUp('down')

    @staticmethod
    def jump():
        pyautogui.keyUp('down')
        pyautogui.press('space')

    @staticmethod
    def duck():   
        pyautogui.keyDown('down')

    @staticmethod
    def start_game():
        pyautogui.keyUp('down')
        pyautogui.press('space', presses=3)

