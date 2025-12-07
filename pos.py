import time
import pyautogui

while True:
    x, y = pyautogui.position()  # récupère la position de la souris
    print(f"x={x}, y={y}")
    time.sleep(0.4)
