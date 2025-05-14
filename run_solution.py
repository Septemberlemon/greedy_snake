import time
import json

import pyautogui


pyautogui.FAILSAFE = False

with open("config.json") as f:
    config = json.load(f)
    num2key = {int(k): v for k, v in config["num2key"].items()}


def run_solution(solution):
    for direction in solution:
        pyautogui.keyDown(num2key[direction])
        time.sleep(0.7)
        pyautogui.keyUp(num2key[direction])
