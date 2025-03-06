import time
import pyautogui


def imgSearch(img, conf):
    img = str(img)
    global counter
    try:
        imgTest = pyautogui.locateOnScreen(img, confidence=conf)
        print("Results for searching '",img,": ", imgTest)
        if imgTest[1] > 1:
            return pyautogui.center(imgTest)
        else:
            return [0,0]
    except Exception as errorMsg:
        print(errorMsg)
        return [0,0]


def clickHeader():
    path = 'timer_saver_logic/timer_header.jpg'
    search = imgSearch(img=path,conf=0.95)
    if search != [0,0]:
        pyautogui.click(x=search[0], y=search[1]+4, button='left')
        time.sleep(0.2)
        pyautogui.press("num3")
        time.sleep(0.2)
        pyautogui.click(x=search[0], y=search[1]+5, button='right')
        time.sleep(0.2)
        pyautogui.moveTo(x=search[0]+20, y=search[1]+60, duration=0.5)
        time.sleep(0.2)
        pyautogui.click(x=search[0]+20, y=search[1]+60, button='left')
        time.sleep(0.2)
        pyautogui.moveTo(x=search[0]-120, y=search[1]+5, duration=0.5)
        time.sleep(0.2)
        #pyautogui.press("enter")
        return True
    return False

