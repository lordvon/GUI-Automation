import pyautogui
import time

# Run this script when game is set up, and mouse is positioned inside the game area.

#pyautogui.PAUSE = 0.74

mp = pyautogui.position()
pyautogui.click(mp[0],mp[1])
time.sleep(0.72)
pyautogui.click(mp[0],mp[1])
