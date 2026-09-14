from pregunta_1 import ColorSaturation
import cv2
from transformations import bgr_to_rgb
from pregunta_2 import Constrast

if __name__ == "__main__":
    select = input("pregunta numero: ")
    if select == "1":
        my_path = "tarea 1/test_imgs/P1_IMG_2402.tif"
        img = cv2.imread(my_path)

        gray = ((0,0), (120, 0), (240, 0))
        yes_yellow = ((0, 1), (30, 1), (60, 4), (90, 1), (120, 1), (240, 1))
        no_green = ((0, 1), (90, 1), (120, 0), (150, 0.3), (240, 1), (170, 0.6))
        no_blue = ((120, 4), (150, 2.8),
                   (0, 1), (240, 0), (270, 0), (220, 0), (240, 0), (250, 0))
        only_red = ((30, 0), (120, 0), (240, 0), (330, 0), (350, 0), (355, 0),
                    (0, 4),(10, 4), (15, 4))
        selections = [gray, yes_yellow, no_green, no_blue, only_red]
        print("1. gray")
        print("2. yes_yellow")
        print("3. no_green")
        print("4. yes_yellow / no_blue")
        print("5. only_red_more")
        pts = selections[int(input("prueba :")) - 1]
        print("0. HSI")
        print("1. Lch")
        space = int(input("espacio:"))
        colorsaturation = ColorSaturation(bgr_to_rgb(img), pts, space)
        colorsaturation.modify()
        colorsaturation.show()
    elif select == "2":
        my_path = "tarea 1/test_imgs/P2_IMG_2423.tif"
        img = cv2.imread(my_path, cv2.IMREAD_GRAYSCALE)

        contrast = Constrast(img)
        contrast.show()
    else:
        pass
