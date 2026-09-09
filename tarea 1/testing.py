from pregunta_1 import ColorSaturation
from tkinter import filedialog
import cv2
from transformations import bgr_to_rgb


if __name__ == "__main__":
    select = input("pregunta numero: ")
    if select == "1":
        my_path = "tarea 1/test_imgs/istockphoto-2133271106-1024x1024.jpg"
        img = cv2.imread(my_path) #saves in bgr

        gray = ((0,0), (120, 0), (240, 0))
        no_red = ((0, 0), (30, 1), (120, 1), (240, 1), (330, 1))
        no_green = ((0, 1), (90, 0.3), (120, 0), (150, 0.3), (240, 1), (100, 0), (140, 0), (80, 0.5), (160, 0.5))
        no_blue = ((0, 1), (120, 1), (210, 0.3), (240, 0), (270, 0.6), (220, 0), (260, 0))
        selections = [gray, no_red, no_green, no_blue]
        print("1. gray")
        print("2. no_red")
        print("3. no_green")
        print("4. no_blue")
        pts = selections[int(input("prueba :")) - 1]
        print("0. HSI")
        print("1. Lch")
        space = int(input("espacio:"))
        colorsaturation = ColorSaturation(bgr_to_rgb(img), pts, space)
        colorsaturation.modify()
        colorsaturation.show()
    else:
        pass
