import cv2
import numpy as np
import mss
import time
from pynput.mouse import Controller as MouseController, Button
from time import sleep
import pyautogui

ready = 'img.png'
dismiss = 'dismiss.png'
water = 'water.png'
boo = 'boo.png'
bug = 'bug.png'
lastwater = 'lastwater.png'

bug = cv2.imread(bug)
hbug, wbug, _ = bug.shape

ready = cv2.imread(ready)
hrea, wrea, _ = ready.shape

dismiss = cv2.imread(dismiss)
hdis, wdis, _ = dismiss.shape

water = cv2.imread(water)
hwat, wwat, _ = water.shape

boo = cv2.imread(boo)
hboo, wboo, _ = boo.shape

lastwater = cv2.imread(lastwater)
hlas, wlas, _ = lastwater.shape

second_monitor = {
    "top": 540,
    "left": 1920,
    "width": 1080,
    "height": 1920
}


def detect(template, img, w, h, mouse, mode):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray, cv2.cvtColor(template, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
    threshold = 0.8176
    loc = np.where(result >= threshold)
    if loc[0].size > 0:
        pt = (loc[1][0], loc[0][0])
        click_x = pt[0] + w // 2 + 1920
        click_y = pt[1] + h // 2 + 540

        if mode:
            original_position = mouse.position
            mouse.position = (click_x, click_y)
            mouse.click(Button.left)
            print(f"Clicked at: ({click_x}, {click_y})")
            mouse.position = original_position
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            pyautogui.keyUp('alt')
        return True
    else:
        return False


def click():
    mouse = MouseController()
    with mss.mss() as sct:
        print("Detecting...")
        while True:
            img = np.array(sct.grab(second_monitor))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            if detect(ready, img, wrea, hrea, mouse, False):
                if not detect(lastwater, img, wlas, hlas, mouse, False) and not detect(boo, img, wboo, hboo, mouse, False):
                    detect(water, img, wwat, hwat, mouse, True)
            detect(dismiss, img, wdis, hdis, mouse, True)
            detect(bug, img, wbug, hbug, mouse, True)
            sleep(1)


if __name__ == "__main__":
    print("Starting detection...")
    click()
