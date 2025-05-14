import time
import json

import pyautogui

from capture_window import capture_window
from utils import contains_similar_color


with open("config.json", "r") as f:
    config = json.load(f)
    cell2color = config["cell2color"]


def process_level_transition(proc_name, snake_final_length):
    time.sleep(0.15 * snake_final_length + 2)
    pyautogui.click(2560 // 2, 1150)  # 点击next level
    time.sleep(1)
    image = capture_window(proc_name)[330:330 + 13 * 75, 343:343 + 21 * 75]
    if contains_similar_color(image[550, 1100], cell2color["yellow_button"]):
        pyautogui.click(2560 // 2 + 200, 850)  # 点击GET
        time.sleep(1)
        pyautogui.click(2560 // 2, 1150)  # 点击OK
        time.sleep(1)
        pyautogui.click(2560 // 2, 1150)  # 用于二次点击next level
        time.sleep(1)
    print("=====================================================================================")
